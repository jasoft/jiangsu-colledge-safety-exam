#!/usr/bin/env python3
"""
演示特殊测试注册码的使用
"""

import os
import sys
from utils import validate_registration_code, mark_registration_code_used, get_registration_code_stats

def demo_test_code():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 特殊测试注册码演示 ===")
    print()
    
    # 显示当前统计
    stats = get_registration_code_stats()
    print(f"数据库中的注册码统计：")
    print(f"- 总数：{stats['total']}")
    print(f"- 已使用：{stats['used']}")
    print(f"- 未使用：{stats['unused']}")
    print()
    
    # 演示特殊测试注册码
    test_code = "GODBLESSYOU"
    print(f"🔑 特殊测试注册码：{test_code}")
    print()
    
    print("✨ 特殊功能演示：")
    
    # 1. 验证功能
    print("1. 验证注册码...")
    if validate_registration_code(test_code):
        print("   ✅ 验证成功")
    else:
        print("   ❌ 验证失败")
    
    # 2. 大小写测试
    print("2. 大小写不敏感测试...")
    test_variations = ["godblessyou", "GodBlessYou", "GODBLESSYOU"]
    for variation in test_variations:
        if validate_registration_code(variation):
            print(f"   ✅ '{variation}' 验证成功")
        else:
            print(f"   ❌ '{variation}' 验证失败")
    
    # 3. 使用测试
    print("3. 使用注册码（模拟任务完成）...")
    if mark_registration_code_used(test_code, "demo_user"):
        print("   ✅ 标记成功（但实际未标记）")
    else:
        print("   ❌ 标记失败")
    
    # 4. 重复使用测试
    print("4. 重复使用测试...")
    if validate_registration_code(test_code):
        print("   ✅ 仍然有效，可以重复使用")
    else:
        print("   ❌ 已失效")
    
    print()
    print("🎯 使用场景：")
    print("- 开发和调试时的快速测试")
    print("- 演示系统功能")
    print("- 不需要管理注册码的场景")
    print("- 教学和培训")
    print()
    
    print("📝 在Streamlit应用中使用：")
    print("1. 打开应用：http://localhost:8501")
    print("2. 输入任意有效的URL")
    print("3. 在注册码输入框中输入：GODBLESSYOU")
    print("4. 点击'开始自动完成'按钮")
    print("5. 可以无限次重复使用")
    print()
    
    print("⚠️  注意：")
    print("- 这是专门为测试设计的特殊注册码")
    print("- 在生产环境中请使用正常的注册码")
    print("- 此注册码不会出现在数据库统计中")

if __name__ == "__main__":
    demo_test_code()
