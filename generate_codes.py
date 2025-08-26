#!/usr/bin/env python3
"""
注册码生成管理脚本

用于批量生成注册码并保存到数据库中。
每个注册码只能使用一次，使用后会被标记为已使用状态。
"""

import os
import sys
import argparse
from utils import create_registration_codes, get_registration_code_stats

def main():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    parser = argparse.ArgumentParser(description='注册码生成管理工具')
    parser.add_argument('count', type=int, nargs='?', help='要生成的注册码数量')
    parser.add_argument('--stats', action='store_true', help='显示注册码统计信息')
    parser.add_argument('--export', type=str, help='导出注册码到文件')
    
    args = parser.parse_args()
    
    # 显示统计信息
    if args.stats:
        stats = get_registration_code_stats()
        print("=== 注册码统计信息 ===")
        print(f"总数量: {stats['total']}")
        print(f"已使用: {stats['used']}")
        print(f"未使用: {stats['unused']}")
        return
    
    # 生成注册码
    if args.count:
        if args.count <= 0:
            print("错误：注册码数量必须大于0")
            sys.exit(1)
        
        print(f"正在生成 {args.count} 个注册码...")
        
        try:
            codes = create_registration_codes(args.count)
            print(f"成功生成 {len(codes)} 个注册码：")
            
            for i, code in enumerate(codes, 1):
                print(f"{i:3d}. {code}")
            
            # 导出到文件
            if args.export:
                with open(args.export, 'w', encoding='utf-8') as f:
                    for code in codes:
                        f.write(f"{code}\n")
                print(f"\n注册码已导出到文件: {args.export}")
            
            # 显示更新后的统计信息
            stats = get_registration_code_stats()
            print(f"\n当前统计：总数 {stats['total']}, 未使用 {stats['unused']}, 已使用 {stats['used']}")
            
        except Exception as e:
            print(f"生成注册码时出错: {e}")
            sys.exit(1)
    
    else:
        # 交互式模式
        print("=== 注册码生成工具 ===")
        
        # 显示当前统计
        stats = get_registration_code_stats()
        print(f"当前统计：总数 {stats['total']}, 未使用 {stats['unused']}, 已使用 {stats['used']}")
        
        try:
            count = int(input("\n请输入要生成的注册码数量: "))
            if count <= 0:
                print("错误：注册码数量必须大于0")
                return
            
            print(f"\n正在生成 {count} 个注册码...")
            codes = create_registration_codes(count)
            
            print(f"\n成功生成 {len(codes)} 个注册码：")
            for i, code in enumerate(codes, 1):
                print(f"{i:3d}. {code}")
            
            # 询问是否导出
            export_choice = input("\n是否导出到文件？(y/N): ").strip().lower()
            if export_choice in ['y', 'yes']:
                filename = input("请输入文件名 (默认: registration_codes.txt): ").strip()
                if not filename:
                    filename = "registration_codes.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    for code in codes:
                        f.write(f"{code}\n")
                print(f"注册码已导出到文件: {filename}")
            
            # 显示更新后的统计信息
            stats = get_registration_code_stats()
            print(f"\n当前统计：总数 {stats['total']}, 未使用 {stats['unused']}, 已使用 {stats['used']}")
            
        except ValueError:
            print("错误：请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            print(f"生成注册码时出错: {e}")

if __name__ == "__main__":
    main()
