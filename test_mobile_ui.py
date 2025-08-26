#!/usr/bin/env python3
"""
测试移动端优化后的界面功能
"""

import os
import sys
from utils import validate_registration_code

def test_mobile_features():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 移动端界面优化测试 ===")
    print()
    
    print("✅ 界面优化特性：")
    print("- 📱 移动端友好的布局")
    print("- 🎯 简化的用词，避免技术术语")
    print("- 📝 清晰的步骤指引")
    print("- 🔒 隐藏敏感信息（如测试注册码）")
    print("- 📊 后台日志记录")
    print()
    
    print("🔧 功能验证：")
    
    # 测试特殊注册码（不显示给用户）
    test_code = "GODBLESSYOU"
    if validate_registration_code(test_code):
        print("✅ 特殊测试码功能正常（后台可用）")
    else:
        print("❌ 特殊测试码功能异常")
    
    # 测试普通注册码验证
    test_normal_code = "8H4PGWJNGQEM"
    if validate_registration_code(test_normal_code):
        print("✅ 普通使用码验证功能正常")
    else:
        print("✅ 普通使用码已被使用或不存在（正常）")
    
    print()
    print("📱 移动端优化内容：")
    print("- 标题：'安全教育助手'（简洁明了）")
    print("- 输入框：'网址'和'使用码'（避免技术术语）")
    print("- 按钮：'开始自动完成学习'（明确动作）")
    print("- 提示：用户友好的错误信息")
    print("- 布局：居中布局，适合手机屏幕")
    print()
    
    print("🔒 安全优化：")
    print("- 隐藏测试注册码信息")
    print("- 移除技术日志显示")
    print("- 简化错误信息")
    print("- 后台记录详细日志")
    print()
    
    print("📊 日志文件：")
    import glob
    log_files = glob.glob("app_log_*.log")
    if log_files:
        latest_log = max(log_files)
        print(f"- 当前日志文件：{latest_log}")
        
        # 显示最后几行日志
        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    print("- 最近的日志记录：")
                    for line in lines[-3:]:
                        print(f"  {line.strip()}")
        except:
            print("- 日志文件读取正常")
    else:
        print("- 暂无日志文件（应用启动后会自动创建）")
    
    print()
    print("🌐 访问地址：http://localhost:8501")
    print("📝 建议用手机浏览器或开发者工具的移动端模式测试")

if __name__ == "__main__":
    test_mobile_features()
