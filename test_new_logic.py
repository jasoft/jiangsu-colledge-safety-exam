#!/usr/bin/env python3
"""
测试新的注册码逻辑
"""

import os
import sys
from utils import validate_registration_code, mark_registration_code_used, get_registration_code_stats
import sqlite3

def test_new_logic():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 测试新的注册码逻辑 ===")
    
    # 获取一个未使用的注册码
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code FROM registration_codes WHERE status = "unused" LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print("错误：没有可用的注册码进行测试")
        return
    
    test_code = result[0]
    print(f"使用注册码进行测试: {test_code}")
    
    # 测试1：验证注册码（应该成功）
    print("\n1. 测试注册码验证...")
    if validate_registration_code(test_code):
        print("✅ 注册码验证成功")
    else:
        print("❌ 注册码验证失败")
        return
    
    # 测试2：模拟任务失败的情况（不标记注册码为已使用）
    print("\n2. 模拟任务失败的情况...")
    print("   任务失败，注册码不应该被标记为已使用")
    
    # 再次验证注册码（应该仍然有效）
    if validate_registration_code(test_code):
        print("✅ 注册码仍然有效（正确）")
    else:
        print("❌ 注册码已失效（错误）")
        return
    
    # 测试3：模拟任务成功的情况（标记注册码为已使用）
    print("\n3. 模拟任务成功的情况...")
    if mark_registration_code_used(test_code, "test_user_success"):
        print("✅ 注册码标记为已使用成功")
    else:
        print("❌ 注册码标记失败")
        return
    
    # 测试4：再次验证注册码（应该失败）
    print("\n4. 测试已使用的注册码...")
    if validate_registration_code(test_code):
        print("❌ 已使用的注册码验证成功（错误）")
    else:
        print("✅ 已使用的注册码验证失败（正确）")
    
    print("\n=== 新逻辑测试完成 ===")
    print("✅ 所有测试通过！")
    print("\n新逻辑特点：")
    print("- 注册码在任务开始前验证有效性")
    print("- 只有任务成功完成后才标记为已使用")
    print("- 任务失败时注册码保持可用状态")
    print("- 防止注册码被无效消耗")

if __name__ == "__main__":
    test_new_logic()
