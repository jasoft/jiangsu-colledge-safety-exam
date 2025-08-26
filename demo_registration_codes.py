#!/usr/bin/env python3
"""
注册码功能演示脚本
"""

import os
import sys
from utils import validate_registration_code, mark_registration_code_used, get_registration_code_stats
import sqlite3

def demo_registration_codes():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 注册码功能演示 ===")
    
    # 获取当前统计
    stats = get_registration_code_stats()
    print(f"当前统计：总数 {stats['total']}, 未使用 {stats['unused']}, 已使用 {stats['used']}")
    
    # 显示所有注册码
    print("\n所有注册码列表：")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code, status, created_at, used_at, used_by FROM registration_codes ORDER BY created_at')
    codes = cursor.fetchall()
    conn.close()
    
    for i, (code, status, created_at, used_at, used_by) in enumerate(codes, 1):
        status_emoji = "✅" if status == "unused" else "❌"
        print(f"{i:2d}. {code} {status_emoji} ({status})")
        if status == "used":
            print(f"    使用时间: {used_at}")
            print(f"    使用者: {used_by}")
    
    # 获取一个未使用的注册码
    unused_codes = [code for code, status, _, _, _ in codes if status == "unused"]
    
    if unused_codes:
        print(f"\n可用于测试的注册码：")
        for i, code in enumerate(unused_codes[:3], 1):  # 显示前3个
            print(f"{i}. {code}")
        
        print(f"\n您可以在Streamlit应用中使用这些注册码进行测试。")
        print(f"应用地址: http://localhost:8501")
    else:
        print("\n⚠️ 没有可用的注册码，请先生成一些注册码：")
        print("python3 generate_codes.py 5")

if __name__ == "__main__":
    demo_registration_codes()
