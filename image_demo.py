import streamlit as st
import os
from PIL import Image
import base64

def main():
    st.title("📸 Streamlit 图片显示方法演示")
    st.markdown("---")
    
    # 检查图片是否存在
    image_path = "images/image.png"
    if not os.path.exists(image_path):
        st.error(f"❌ 图片文件 {image_path} 不存在")
        return
    
    st.success(f"✅ 找到图片文件: {image_path}")
    
    # 方法1: 基本的 st.image()
    st.subheader("方法1: 基本的 st.image()")
    st.image(image_path, caption="使用 st.image() 显示")
    
    st.code("""
    st.image("images/image.png", caption="使用 st.image() 显示")
    """)
    
    # 方法2: 设置宽度
    st.subheader("方法2: 设置固定宽度")
    st.image(image_path, caption="固定宽度 300px", width=300)
    
    st.code("""
    st.image("images/image.png", caption="固定宽度 300px", width=300)
    """)
    
    # 方法3: 使用列宽
    st.subheader("方法3: 使用列宽")
    st.image(image_path, caption="使用列宽", use_column_width=True)
    
    st.code("""
    st.image("images/image.png", caption="使用列宽", use_column_width=True)
    """)
    
    # 方法4: 在列中居中显示
    st.subheader("方法4: 在列中居中显示")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image_path, caption="居中显示")
    
    st.code("""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/image.png", caption="居中显示")
    """)
    
    # 方法5: 使用 PIL 加载图片
    st.subheader("方法5: 使用 PIL 加载图片")
    try:
        pil_image = Image.open(image_path)
        st.image(pil_image, caption="使用 PIL 加载的图片")
        
        st.code("""
        from PIL import Image
        pil_image = Image.open("images/image.png")
        st.image(pil_image, caption="使用 PIL 加载的图片")
        """)
    except Exception as e:
        st.error(f"PIL 加载失败: {e}")
    
    # 方法6: 在 expander 中显示
    st.subheader("方法6: 在 expander 中显示")
    with st.expander("点击查看图片", expanded=False):
        st.image(image_path, caption="在 expander 中的图片")
    
    st.code("""
    with st.expander("点击查看图片", expanded=False):
        st.image("images/image.png", caption="在 expander 中的图片")
    """)
    
    # 方法7: 使用 HTML 和 base64 编码
    st.subheader("方法7: 使用 HTML 和 base64 编码")
    try:
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        html_img = f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{img_base64}" 
                 style="max-width: 300px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <p style="color: #666; font-style: italic;">使用 HTML 和 base64 编码</p>
        </div>
        """
        st.markdown(html_img, unsafe_allow_html=True)
        
        st.code("""
        import base64
        
        with open("images/image.png", "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        html_img = f'''
        <div style="text-align: center;">
            <img src="data:image/png;base64,{img_base64}" 
                 style="max-width: 300px; border-radius: 10px;">
        </div>
        '''
        st.markdown(html_img, unsafe_allow_html=True)
        """)
    except Exception as e:
        st.error(f"base64 编码失败: {e}")
    
    # 方法8: 多列显示多张图片
    st.subheader("方法8: 多列显示")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(image_path, caption="图片1", use_column_width=True)
    with col2:
        st.image(image_path, caption="图片2", use_column_width=True)
    with col3:
        st.image(image_path, caption="图片3", use_column_width=True)
    
    st.code("""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/image.png", caption="图片1", use_column_width=True)
    with col2:
        st.image("images/image.png", caption="图片2", use_column_width=True)
    with col3:
        st.image("images/image.png", caption="图片3", use_column_width=True)
    """)
    
    # 常见问题解答
    st.markdown("---")
    st.subheader("❓ 常见问题")
    
    with st.expander("为什么图片不显示？"):
        st.markdown("""
        **可能的原因：**
        1. 图片路径不正确
        2. 图片文件不存在
        3. 图片格式不支持
        4. 权限问题
        
        **解决方法：**
        1. 检查文件路径是否正确
        2. 使用 `os.path.exists()` 检查文件是否存在
        3. 支持的格式：PNG, JPG, JPEG, GIF, SVG
        4. 确保文件有读取权限
        """)
    
    with st.expander("如何调整图片大小？"):
        st.markdown("""
        **方法：**
        1. `width` 参数：设置固定宽度（像素）
        2. `use_column_width=True`：使用列宽
        3. 使用 PIL 调整大小后再显示
        4. 使用 HTML 和 CSS 样式
        """)

if __name__ == "__main__":
    main()
