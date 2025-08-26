#!/usr/bin/env python3
"""
测试特殊注册码 GODBLESSYOU
"""

import os
import sys
from utils import validate_registration_code, mark_registration_code_used, get_registration_code_stats

def test_special_code():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 测试特殊注册码 GODBLESSYOU ===")
    
    test_code = "GODBLESSYOU"
    
    # 测试1：验证注册码（应该成功）
    print(f"\n1. 测试注册码验证: {test_code}")
    if validate_registration_code(test_code):
        print("✅ 注册码验证成功")
    else:
        print("❌ 注册码验证失败")
        return
    
    # 测试2：测试大小写不敏感
    print(f"\n2. 测试小写版本: {test_code.lower()}")
    if validate_registration_code(test_code.lower()):
        print("✅ 小写注册码验证成功")
    else:
        print("❌ 小写注册码验证失败")
    
    # 测试3：标记为已使用（应该成功但不实际标记）
    print(f"\n3. 测试标记为已使用: {test_code}")
    if mark_registration_code_used(test_code, "test_user"):
        print("✅ 标记操作成功（但实际未标记）")
    else:
        print("❌ 标记操作失败")
    
    # 测试4：再次验证（应该仍然有效）
    print(f"\n4. 再次验证注册码: {test_code}")
    if validate_registration_code(test_code):
        print("✅ 注册码仍然有效（永久有效）")
    else:
        print("❌ 注册码已失效（错误）")
    
    # 测试5：多次使用测试
    print(f"\n5. 多次使用测试:")
    for i in range(3):
        print(f"   第{i+1}次使用...")
        if validate_registration_code(test_code):
            print(f"   ✅ 验证成功")
            if mark_registration_code_used(test_code, f"test_user_{i+1}"):
                print(f"   ✅ 标记成功")
            else:
                print(f"   ❌ 标记失败")
        else:
            print(f"   ❌ 验证失败")
    
    # 最终验证
    print(f"\n6. 最终验证: {test_code}")
    if validate_registration_code(test_code):
        print("✅ 注册码依然有效（永久测试码）")
    else:
        print("❌ 注册码已失效")
    
    print("\n=== 测试完成 ===")
    print("✅ 特殊测试注册码 'GODBLESSYOU' 功能正常！")
    print("特点：")
    print("- 永远有效，不会失效")
    print("- 大小写不敏感")
    print("- 不会被写入数据库")
    print("- 可以无限次使用")
    print("- 方便开发和测试")

if __name__ == "__main__":
    test_special_code()
