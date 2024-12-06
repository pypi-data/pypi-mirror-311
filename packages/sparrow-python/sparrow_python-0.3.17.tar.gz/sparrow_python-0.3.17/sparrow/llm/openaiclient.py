import asyncio
from typing import TYPE_CHECKING, Union

from loguru import logger

from sparrow import ConcurrentRequester
from sparrow.vllm.client.image_processor import batch_process_messages, messages_preprocess

if TYPE_CHECKING:
    from sparrow.async_api.interface import RequestResult


class OpenAIClient:
    def __init__(self,
                 base_url: str,
                 api_key="EMPTY",
                 concurrency_limit=10,
                 timeout=100,
                 **kwargs):
        self._client = ConcurrentRequester(
            concurrency_limit=concurrency_limit,
            timeout=timeout,
        )
        self._headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    async def wrap_to_request_params(self, messages: list, model: str, max_tokens=None, meta=None, preprocess_msg=False, **kwargs):
        if preprocess_msg:
            messages = await messages_preprocess(messages, preprocess_msg=preprocess_msg)
        request_params = {
            "json": {
                "messages": messages,
                "model": model,
                "stream": False,
                "max_tokens": max_tokens,
                **kwargs,
            },
            "headers": self._headers,
            "meta": meta,
        }
        return request_params

    async def chat_completions(self, messages: list, model: str, return_raw=False, preprocess_msg=False, **kwargs) -> Union[str, "RequestResult"]:
        result, _ =  await self._client.process_requests(
            request_params=[await self.wrap_to_request_params(messages, model, preprocess_msg=preprocess_msg, **kwargs)],
            url=f"{self._base_url}/chat/completions",
            method="POST",
            show_progress=False,
        )
        if return_raw:
            return result[0]
        return result[0].data["choices"][0]["message"]["content"]

    def chat_completions_sync(self, messages: list, model: str, return_raw=False, **kwargs):
        return asyncio.run(self.chat_completions(messages, model, return_raw, **kwargs))



    async def chat_completions_batch(self,
                                     messages_list: list[list],
                                     model: str,
                                     return_raw=False,
                                     show_progress=True,
                                     preprocess_msg=False,
                                     **kwargs):
        if preprocess_msg:
            messages_list = await batch_process_messages(messages_list,
                                                         preprocess_msg=preprocess_msg,
                                                         max_concurrent=self._client._concurrency_limit)

        results, _ =  await self._client.process_requests(
            request_params=[await self.wrap_to_request_params(messages, model, preprocess_msg=False, **kwargs)
                            for messages in messages_list],
            url=f"{self._base_url}/chat/completions",
            method="POST",
            show_progress=show_progress,
        )
        if return_raw:
            return results
        content_list = []
        for result in results:
            try:
                content = result.data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.warning(f"Error in chat_completions_batch: {e}\n {result=}\n set content to None")
                content = None
            content_list.append(content)
        return content_list
