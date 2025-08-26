#!/usr/bin/env python3
"""
注册码功能测试脚本
"""

import os
import sys
from utils import validate_registration_code, mark_registration_code_used, get_registration_code_stats

def test_registration_codes():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 注册码功能测试 ===")
    
    # 获取当前统计
    stats = get_registration_code_stats()
    print(f"测试前统计：总数 {stats['total']}, 未使用 {stats['unused']}, 已使用 {stats['used']}")
    
    if stats['unused'] == 0:
        print("错误：没有可用的注册码进行测试")
        return
    
    # 获取一个未使用的注册码进行测试
    import sqlite3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code FROM registration_codes WHERE status = "unused" LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print("错误：无法获取测试用的注册码")
        return
    
    test_code = result[0]
    print(f"\n使用注册码进行测试: {test_code}")
    
    # 测试验证功能
    print("\n1. 测试注册码验证...")
    if validate_registration_code(test_code):
        print("✅ 注册码验证成功")
    else:
        print("❌ 注册码验证失败")
        return
    
    # 测试标记为已使用
    print("\n2. 测试标记注册码为已使用...")
    if mark_registration_code_used(test_code, "test_user"):
        print("✅ 注册码标记为已使用成功")
    else:
        print("❌ 注册码标记失败")
        return
    
    # 再次验证（应该失败）
    print("\n3. 测试已使用的注册码验证...")
    if validate_registration_code(test_code):
        print("❌ 已使用的注册码验证成功（这是错误的）")
    else:
        print("✅ 已使用的注册码验证失败（这是正确的）")
    
    # 测试无效注册码
    print("\n4. 测试无效注册码...")
    if validate_registration_code("INVALID_CODE"):
        print("❌ 无效注册码验证成功（这是错误的）")
    else:
        print("✅ 无效注册码验证失败（这是正确的）")
    
    # 获取最终统计
    stats = get_registration_code_stats()
    print(f"\n测试后统计：总数 {stats['total']}, 未使用 {stats['unused']}, 已使用 {stats['used']}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_registration_codes()
