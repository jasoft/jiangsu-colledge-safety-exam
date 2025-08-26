import streamlit as st
import re
import subprocess
import sys
import os
import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from utils import validate_registration_code, mark_registration_code_used


# 配置日志
def setup_logging():
    """配置日志系统"""
    log_filename = f"app_log_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


logger = setup_logging()


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


def run_main_script(userid, registration_code):
    """
    运行main.py脚本，并在成功完成后标记注册码为已使用

    Args:
        userid (str): 用户ID
        registration_code (str): 注册码

    Returns:
        tuple: (success, output, code_used)
    """
    try:
        logger.info(f"开始执行主脚本，用户ID: {userid}, 使用码: {registration_code}")

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

        logger.info(f"脚本执行完成，返回码: {process.returncode}")

        if process.returncode == 0:
            # 任务成功完成，标记注册码为已使用
            logger.info("任务执行成功，开始标记使用码")
            code_used = mark_registration_code_used(registration_code, f"user_{userid}")
            logger.info(f"使用码标记结果: {code_used}")
            return True, stdout, code_used
        else:
            # 任务失败，不标记注册码为已使用
            logger.warning(f"任务执行失败，错误信息: {stderr}")
            return False, stderr, False

    except Exception as e:
        logger.error(f"执行主脚本时发生异常: {str(e)}")
        return False, str(e), False


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
        page_title="安全教育自动完成",
        page_icon="🎓",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # 初始化session state
    if "current_userid" not in st.session_state:
        st.session_state.current_userid = None

    # 移动端优化样式
    st.markdown(
        """
    <style>
    .main > div {
        padding-top: 1rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px !important;
    }
    .stButton > button {
        font-size: 18px !important;
        height: 3rem !important;
        border-radius: 10px !important;
    }
    .stMarkdown h3 {
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stMarkdown p {
        font-size: 0.9rem !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # 移动端友好的标题
    st.markdown(
        """
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='font-size: 1.5rem; margin-bottom: 0;'>🎓 安全教育助手</h1>
        <p style='color: #666; font-size: 0.9rem; margin-top: 5px;'>江苏省大学新生安全知识教育</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 简化的输入说明
    st.markdown("### 📱 使用步骤")

    with st.container():
        st.markdown("**第一步：粘贴网址**")
        url_input = st.text_input(
            "登录后复制的完整网址",
            placeholder="粘贴从微信复制的完整网址...",
            help="从微信内置浏览器地址栏复制完整网址",
            key="url_input",
            on_change=on_url_change,
            label_visibility="collapsed",
        )

        st.markdown("**第二步：输入使用码**")
        registration_code = st.text_input(
            "使用码",
            placeholder="输入6位数字使用码",
            help="请输入6位数字使用码",
            label_visibility="collapsed",
            max_chars=6,
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
            st.success("✅ 网址验证成功")
            logger.info(f"URL验证成功，用户ID: {userid}")
        else:
            st.error("❌ 网址格式不正确，请重新复制")
            st.info("💡 请确保复制完整的网址")
    elif url_input:  # 如果有输入但只是空格
        st.warning("⚠️ 请输入有效的网址")
        st.session_state.current_userid = None
        userid = None
    else:
        st.info("💡 请先粘贴登录后的完整网址")
        st.session_state.current_userid = None
        userid = None

    # 开始按钮
    st.markdown("**第三步：开始自动完成**")

    # 检查输入完整性
    can_proceed = userid is not None and registration_code.strip()

    if st.button(
        "🚀 开始自动完成学习",
        type="primary",
        use_container_width=True,
        disabled=not can_proceed,
    ):
        if not userid:
            st.warning("⚠️ 请先输入正确的网址")
        elif not registration_code.strip():
            st.warning("⚠️ 请输入使用码")
        else:
            # 验证注册码
            registration_code = registration_code.strip()
            logger.info(f"开始验证使用码: {registration_code}")

            if not validate_registration_code(registration_code):
                st.error("❌ 使用码无效或已被使用")
                logger.warning(f"使用码验证失败: {registration_code}")
            else:
                logger.info(f"使用码验证成功，开始执行任务: {registration_code}")
                with st.spinner("正在自动完成学习，请耐心等待..."):
                    # 创建进度条
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # 更新进度
                    status_text.text("正在连接系统...")
                    progress_bar.progress(20)

                    # 运行主脚本
                    success, output, code_used = run_main_script(
                        userid, registration_code
                    )

                    progress_bar.progress(100)
                    status_text.empty()

                    if success:
                        st.success("🎉 学习任务完成！")
                        logger.info(f"任务执行成功，用户ID: {userid}")

                        if code_used:
                            st.info("✅ 使用码已消耗")
                            logger.info(f"使用码已标记为已使用: {registration_code}")
                        else:
                            st.warning("⚠️ 系统提示：使用码状态更新异常")
                            logger.warning(f"使用码标记失败: {registration_code}")

                    else:
                        st.error("❌ 执行过程中出现问题，请稍后重试")
                        logger.error(f"任务执行失败，用户ID: {userid}, 错误: {output}")

                        # 简化的错误提示
                        if "网络" in output or "连接" in output:
                            st.info("💡 可能是网络问题，请检查网络连接后重试")
                        else:
                            st.info("💡 请检查网址是否正确，或联系管理员")

    # 使用说明
    st.markdown("---")
    with st.expander("📖 详细使用说明", expanded=True):
        st.markdown("""
        ### 📱 微信操作步骤：

        **1. 登录学习平台**
        - 在微信中打开江苏省大学新生安全知识教育平台
        - 输入账号密码完成登录

        **2. 复制网址**
        - 登录成功后，点击微信右上角"..."菜单
        - 选择"复制链接"
        - 或长按地址栏复制完整网址
        """)

        # 显示图片
        if os.path.exists("images/image.png"):
            st.image("images/image.png", caption="微信复制链接示例", width=300)

        st.markdown("""
        **3. 粘贴网址**
        - 回到本页面，在第一个输入框粘贴网址
        - 看到"✅ 网址验证成功"提示即可

        **4. 输入使用码**
        - 在第二个输入框输入6位数字使用码
        - 使用码由管理员提供，纯数字便于记忆

        **5. 开始学习**
        - 点击"开始自动完成学习"按钮
        - 等待系统自动完成所有课程和考试
        - 完成后会显示"🎉 学习任务完成！"

        ### ⚠️ 重要提醒：
        - 每个使用码只能用一次
        - 请保持网络连接稳定
        - 不要关闭微信页面直到完成
        - 如有问题请联系管理员
        """)

    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8rem; padding: 20px 0;'>
            <p>📚 江苏省大学新生安全知识教育助手</p>
            <p>⚠️ 请遵守学校相关规定，仅限本人使用</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
