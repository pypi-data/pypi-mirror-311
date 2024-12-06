import datetime
import json
from difflib import HtmlDiff
from pathlib import Path

import diff_match_patch as dmp_module
import streamlit as st


class PromptManager:
    def __init__(self):
        self.save_path = Path("prompts")
        self.save_path.mkdir(exist_ok=True)
        self.dmp = dmp_module.diff_match_patch()

    def save_prompt(self, name, content, tags=None, comment=""):
        file_path = self.save_path / f"{name}.json"

        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                prompt_data = json.load(f)
            if prompt_data["versions"][-1]["content"] == content:
                return False
            new_version = len(prompt_data["versions"])
        else:
            prompt_data = {
                "name": name,
                "tags": tags or [],
                "created_at": datetime.datetime.now().isoformat(),
                "versions": [],
            }
            new_version = 0

        version_data = {
            "version": new_version,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat(),
            "comment": comment,
            "deleted": False,
        }

        if new_version > 0:
            prev_content = prompt_data["versions"][-1]["content"]
            patches = self.dmp.patch_make(prev_content, content)
            version_data["diff"] = self.dmp.patch_toText(patches)

        prompt_data["versions"].append(version_data)
        prompt_data["updated_at"] = datetime.datetime.now().isoformat()
        prompt_data["current_version"] = new_version

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, ensure_ascii=False, indent=2)
        return True

    def delete_version(self, name, version):
        file_path = self.save_path / f"{name}.json"
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            if 0 <= version < len(data["versions"]):
                # 标记版本为已删除
                data["versions"][version]["deleted"] = True
                # 如果删除的是当前版本，将当前版本设置为最新的未删除版本
                if data["current_version"] == version:
                    for i in range(len(data["versions"]) - 1, -1, -1):
                        if not data["versions"][i]["deleted"]:
                            data["current_version"] = i
                            break

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        return False

    def restore_version(self, name, version):
        data, _ = self.load_prompt(name)
        if data and 0 <= version < len(data["versions"]):
            data["current_version"] = version
            file_path = self.save_path / f"{name}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        return False

    def compare_versions(self, name, version1, version2):
        data, _ = self.load_prompt(name)
        if data and version1 < len(data["versions"]) and version2 < len(data["versions"]):
            content1 = data["versions"][version1]["content"]
            content2 = data["versions"][version2]["content"]

            # 使用 HtmlDiff 生成差异对比HTML
            diff = HtmlDiff()
            diff_html = diff.make_file(
                content1.splitlines(),
                content2.splitlines(),
                f"版本 {version1}",
                f"版本 {version2}",
                True,
            )
            return diff_html
        return None

    def load_prompt(self, name, version=None):
        file_path = self.save_path / f"{name}.json"
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                if version is None:
                    version = data["current_version"]
                return data, version
        return None, None

    def list_prompts(self):
        return [f.stem for f in self.save_path.glob("*.json")]


# def confirm_delete():
#     # 创建一个占位容器用于显示确认对话框
#     placeholder = st.empty()
#
#     # 在容器中创建确认对话框
#     with placeholder.container():
#         st.warning("确定要删除这个版本吗？此操作无法撤销！")
#         col1, col2 = st.columns([1, 1])
#         with col1:
#             if st.button("确认删除", key="confirm_delete"):
#                 placeholder.empty()  # 清空确认对话框
#                 return True
#         with col2:
#             if st.button("取消", key="cancel_delete"):
#                 placeholder.empty()  # 清空确认对话框
#                 return False
#     return None

def main():
    st.title("Prompt 工程开发工具")

    # 初始化会话状态
    if 'show_delete_confirm' not in st.session_state:
        st.session_state.show_delete_confirm = False
        st.session_state.version_to_delete = None

    pm = PromptManager()

    st.sidebar.header("功能区")
    mode = st.sidebar.radio("选择模式", ["新建 Prompt", "加载已有 Prompt"])

    if mode == "新建 Prompt":
        st.header("创建新的 Prompt")

        prompt_name = st.text_input("Prompt 名称")
        prompt_content = st.text_area("Prompt 内容", height=300)
        prompt_tags = st.text_input("标签 (用逗号分隔)")
        commit_comment = st.text_input("版本说明")

        if st.button("保存"):
            if prompt_name and prompt_content:
                tags = [tag.strip() for tag in prompt_tags.split(",")] if prompt_tags else []
                if pm.save_prompt(prompt_name, prompt_content, tags, commit_comment):
                    st.success(f"Prompt '{prompt_name}' 已保存!")
                else:
                    st.info("内容未发生变化，无需保存新版本")
            else:
                st.error("请填写名称和内容!")

    else:
        st.header("加载已有 Prompt")

        prompts = pm.list_prompts()
        if not prompts:
            st.info("还没有保存的 Prompt")
        else:
            col1, col2 = st.columns([3, 1])

            with col1:
                selected_prompt = st.selectbox("选择 Prompt", prompts)

            if selected_prompt:
                prompt_data, current_version = pm.load_prompt(selected_prompt)
                if prompt_data:
                    # 版本历史
                    versions = [v for v in prompt_data["versions"] if not v.get("deleted", False)]
                    version_list = [f"版本 {v['version']}: {v['timestamp'][:16]} - {v['comment']}"
                                    for v in versions]

                    with col2:
                        selected_version_idx = st.selectbox(
                            "选择版本",
                            range(len(version_list)),
                            format_func=lambda x: version_list[x],
                            index=len(version_list) - 1
                        )

                    # 显示选中版本的内容
                    selected_version = versions[selected_version_idx]
                    st.text_area("Prompt 内容", selected_version["content"], height=300)

                    # 版本信息
                    st.text(f"版本: {selected_version['version']}")
                    st.text(f"创建时间: {prompt_data['created_at']}")
                    st.text(f"最后更新: {prompt_data['updated_at']}")
                    st.text("标签: " + ", ".join(prompt_data['tags']))

                    # 版本控制按钮
                    col3, col4, col5 = st.columns([1, 1, 2])
                    with col3:
                        if st.button("设为当前版本"):
                            if pm.restore_version(selected_prompt, selected_version_idx):
                                st.success(f"已将版本 {selected_version_idx} 设置为当前版本")

                    with col4:
                        if st.button("删除此版本"):
                            if len(versions) > 1:  # 确保至少保留一个版本
                                st.session_state.show_delete_confirm = True
                                st.session_state.version_to_delete = selected_version["version"]
                            else:
                                st.error("无法删除最后一个版本")

                    # 显示删除确认对话框
                    if st.session_state.show_delete_confirm:
                        st.warning(f"确定要删除版本 {st.session_state.version_to_delete} 吗？此操作不可撤销。")
                        col8, col9 = st.columns([1, 1])
                        with col8:
                            if st.button("确认删除"):
                                if pm.delete_version(selected_prompt, st.session_state.version_to_delete):
                                    st.success(f"已删除版本 {st.session_state.version_to_delete}")
                                    st.session_state.show_delete_confirm = False
                                    st.session_state.version_to_delete = None
                                    st.rerun()
                        with col9:
                            if st.button("取消"):
                                st.session_state.show_delete_confirm = False
                                st.session_state.version_to_delete = None
                                st.rerun()


                    # 版本比较功能
                    st.subheader("版本比较")
                    col6, col7 = st.columns([1, 1])
                    with col6:
                        compare_version1 = st.selectbox(
                            "选择比较版本 1",
                            range(len(versions)),
                            format_func=lambda x: f"版本 {versions[x]['version']}",
                        )
                    with col7:
                        compare_version2 = st.selectbox(
                            "选择比较版本 2",
                            range(len(versions)),
                            format_func=lambda x: f"版本 {versions[x]['version']}",
                        )

                    if st.button("比较版本"):
                        v1 = versions[compare_version1]["version"]
                        v2 = versions[compare_version2]["version"]
                        diff_html = pm.compare_versions(selected_prompt, v1, v2)
                        if diff_html:
                            # 自定义CSS来改善差异显示
                            st.markdown("""
                                <style>
                                    .diff_header {background-color: #e6e6e6;}
                                    .diff_next {background-color: #f8f9fa;}
                                    .diff_add {background-color: #e6ffe6;}
                                    .diff_sub {background-color: #ffe6e6;}
                                    .diff_chg {background-color: #e6e6ff;}
                                </style>
                            """, unsafe_allow_html=True)
                            st.components.v1.html(diff_html, height=500, scrolling=True)

    # 调试区域
    st.header("Prompt 调试区")
    if st.checkbox("显示调试区"):
        test_input = st.text_area("测试输入")
        if st.button("运行测试"):
            st.write("测试结果将显示在这里")

if __name__ == "__main__":
    main()
