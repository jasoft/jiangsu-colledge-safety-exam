import streamlit as st
import re
import subprocess
import sys
import os
from urllib.parse import urlparse, parse_qs


def extract_userid_from_url(url):
    """
    从URL中提取userid参数

    Args:
        url (str): 输入的URL

    Returns:
        str: 提取的userid，如果未找到则返回None
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # 查找userid参数
        if "userid" in query_params:
            return query_params["userid"][0]
        else:
            return None
    except Exception as e:
        st.error(f"URL解析错误: {e}")
        return None


def run_main_script(userid):
    """
    运行main.py脚本

    Args:
        userid (str): 用户ID

    Returns:
        tuple: (success, output)
    """
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_script_path = os.path.join(current_dir, "main.py")

        # 使用subprocess运行main.py，并传入userid
        process = subprocess.Popen(
            [sys.executable, main_script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=current_dir,
        )

        # 向stdin发送userid
        stdout, stderr = process.communicate(input=userid + "\n")

        if process.returncode == 0:
            return True, stdout
        else:
            return False, stderr

    except Exception as e:
        return False, str(e)


def on_url_change():
    """URL输入变化时的回调函数"""
    if "url_input" in st.session_state:
        url = st.session_state.url_input.strip()
        if url:
            userid = extract_userid_from_url(url)
            st.session_state.current_userid = userid
        else:
            st.session_state.current_userid = None


def main():
    st.set_page_config(
        page_title="江苏省大学新生安全知识教育自动完成工具",
        page_icon="🎓",
        layout="wide",
    )

    # 初始化session state
    if "current_userid" not in st.session_state:
        st.session_state.current_userid = None

    st.title("🎓 江苏省大学新生安全知识教育自动完成工具")
    st.markdown("---")

    # URL输入部分移到最上面
    st.subheader("📝 输入登录后的URL")
    url_input = st.text_input(
        "请粘贴完整的URL：",
        placeholder="http://wap.xiaoyuananquantong.com/guns-vip-main/wap/jshome?userid=12345678901234567890",
        help="URL应该包含userid参数",
        key="url_input",
        on_change=on_url_change,
    )

    # URL验证和userid提取 - 实时更新
    userid = st.session_state.current_userid

    # 实时更新URL状态
    if url_input.strip():
        # 确保实时更新userid
        current_userid = extract_userid_from_url(url_input.strip())
        st.session_state.current_userid = current_userid
        userid = current_userid

        if userid:
            st.success(f"✅ 成功提取到用户ID: `{userid}`")
        else:
            st.error("❌ 无法从URL中提取userid参数，请检查URL是否正确")
            st.info("💡 确保URL包含类似 `?userid=12345678901234567890` 的参数")
    elif url_input:  # 如果有输入但只是空格
        st.warning("⚠️ 请输入有效的URL")
        st.session_state.current_userid = None
        userid = None
    else:
        st.info("💡 请在上方输入框中粘贴登录后的完整URL")
        st.session_state.current_userid = None
        userid = None

    # 自动完成按钮始终显示
    st.markdown("---")
    if st.button(
        "🚀 开始自动完成",
        type="primary",
        use_container_width=True,
        disabled=(userid is None),
    ):
        if userid:
            with st.spinner("正在执行自动完成流程，请稍候..."):
                # 创建进度条
                progress_bar = st.progress(0)
                status_text = st.empty()

                # 更新进度
                status_text.text("正在启动脚本...")
                progress_bar.progress(10)

                # 运行主脚本
                success, output = run_main_script(userid)

                progress_bar.progress(100)

                if success:
                    st.success("🎉 自动完成流程执行成功！")

                    # 显示执行结果
                    with st.expander("📋 执行日志", expanded=False):
                        st.code(output, language="text")

                else:
                    st.error("❌ 执行过程中出现错误")

                    # 显示错误信息
                    with st.expander("🔍 错误详情", expanded=True):
                        st.code(output, language="text")
        else:
            st.warning("⚠️ 请先输入有效的URL")

    # 使用说明放到下面
    st.markdown("---")
    with st.expander("📖 使用说明", expanded=True):
        st.markdown("""
        ### 如何使用：
        1. 登录到江苏省大学新生安全知识教育平台
        2. 登录进去后看到下图点右上角的三个点，选择复制链接：
        """)

        # 显示图片
        if os.path.exists("images/image.png"):
            st.image("images/image.png", caption="操作流程图")
        else:
            st.warning("⚠️ 图片文件 images/image.png 未找到")

        st.markdown("""
        3. 将URL粘贴到上方输入框中
        4. 点击"开始自动完成"按钮

        ### 注意事项：
        - 请确保您已经成功登录到平台
        - URL中必须包含有效的userid参数
        - 程序将自动完成所有课程学习和考试
        - 请耐心等待程序执行完成
        """)

    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🔧 基于原始脚本开发的Streamlit界面</p>
            <p>⚠️ 仅供学习交流使用，请遵守相关规定</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
