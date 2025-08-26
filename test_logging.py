#!/usr/bin/env python3
"""
测试日志功能
"""

import os
import sys
import logging
from datetime import datetime

# 模拟streamlit_app.py中的日志配置
def setup_logging():
    """配置日志系统"""
    log_filename = f"app_log_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def test_logging():
    print("=== 测试日志功能 ===")
    
    # 设置日志
    logger = setup_logging()
    
    # 测试各种日志级别
    logger.info("测试信息日志：应用启动")
    logger.warning("测试警告日志：使用码验证失败")
    logger.error("测试错误日志：任务执行失败")
    
    # 模拟用户操作日志
    test_userid = "1234567890123456"
    test_code = "TEST12345678"
    
    logger.info(f"用户开始验证使用码: {test_code}")
    logger.info(f"使用码验证成功，开始执行任务: {test_code}")
    logger.info(f"任务执行成功，用户ID: {test_userid}")
    logger.info(f"使用码已标记为已使用: {test_code}")
    
    # 检查日志文件
    log_filename = f"app_log_{datetime.now().strftime('%Y%m%d')}.log"
    
    if os.path.exists(log_filename):
        print(f"✅ 日志文件创建成功: {log_filename}")
        
        # 读取并显示日志内容
        with open(log_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"✅ 日志文件包含 {len(lines)} 行记录")
            
            print("\n📋 最近的日志记录：")
            for line in lines[-5:]:  # 显示最后5行
                print(f"  {line.strip()}")
    else:
        print("❌ 日志文件未创建")
    
    print(f"\n📁 日志文件位置: {os.path.abspath(log_filename)}")
    print("✅ 日志功能测试完成")

if __name__ == "__main__":
    test_logging()
