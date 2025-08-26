#!/usr/bin/env python3
"""
测试6位数字使用码功能
"""

import os
import sys
from utils import validate_registration_code, mark_registration_code_used, get_registration_code_stats

def test_6digit_codes():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== 测试6位数字使用码功能 ===")
    print()
    
    # 测试特殊测试码
    test_code = "888888"
    print(f"🔑 测试特殊使用码：{test_code}")
    
    if validate_registration_code(test_code):
        print("✅ 特殊使用码验证成功")
    else:
        print("❌ 特殊使用码验证失败")
    
    # 测试标记（应该成功但不实际标记）
    if mark_registration_code_used(test_code, "test_user"):
        print("✅ 特殊使用码标记成功（实际未标记）")
    else:
        print("❌ 特殊使用码标记失败")
    
    # 再次验证（应该仍然有效）
    if validate_registration_code(test_code):
        print("✅ 特殊使用码仍然有效（永久可用）")
    else:
        print("❌ 特殊使用码已失效")
    
    print()
    
    # 获取一个普通的6位数字使用码
    import sqlite3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code FROM registration_codes WHERE status = "unused" AND LENGTH(code) = 6 LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        normal_code = result[0]
        print(f"🔢 测试普通6位使用码：{normal_code}")
        
        # 验证普通使用码
        if validate_registration_code(normal_code):
            print("✅ 普通使用码验证成功")
            
            # 标记为已使用
            if mark_registration_code_used(normal_code, "test_user"):
                print("✅ 普通使用码标记为已使用成功")
                
                # 再次验证（应该失败）
                if validate_registration_code(normal_code):
                    print("❌ 已使用的使用码验证成功（错误）")
                else:
                    print("✅ 已使用的使用码验证失败（正确）")
            else:
                print("❌ 普通使用码标记失败")
        else:
            print("❌ 普通使用码验证失败")
    else:
        print("⚠️ 没有找到6位数字的普通使用码")
    
    print()
    
    # 显示统计信息
    stats = get_registration_code_stats()
    print(f"📊 使用码统计：")
    print(f"- 总数：{stats['total']}")
    print(f"- 已使用：{stats['used']}")
    print(f"- 未使用：{stats['unused']}")
    
    print()
    print("✨ 6位数字使用码优势：")
    print("- 📱 方便在手机上输入")
    print("- 🧠 容易记忆")
    print("- ⚡ 输入速度快")
    print("- 🔢 纯数字，避免字母混淆")
    print("- 📞 可以通过语音传达")
    
    print()
    print("🎯 特殊测试码：888888（永久有效）")
    print("📱 微信操作更便捷，无需切换应用")

if __name__ == "__main__":
    test_6digit_codes()
