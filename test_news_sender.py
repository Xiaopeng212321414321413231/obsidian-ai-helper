#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证新闻发送器功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from news_feishu_sender import ObsidianNewsFeishuSender

def test_news_sender():
    """测试新闻发送器"""
    print("🧪 开始测试新闻发送器...")
    
    # 创建发送器实例
    sender = ObsidianNewsFeishuSender()
    
    # 测试1：查找昨天的新闻文件
    print("\n📂 测试1：查找昨天的新闻文件")
    news_file = sender.find_yesterday_news_files()
    if news_file:
        print(f"✅ 找到新闻文件: {news_file}")
    else:
        print("❌ 未找到昨天的新闻文件")
        return False
    
    # 测试2：提取新闻内容
    print("\n📄 测试2：提取新闻内容")
    news_content = sender.extract_news_content(news_file)
    if news_content:
        print(f"✅ 新闻内容提取成功，长度: {len(news_content)} 字符")
        print(f"📝 内容预览: {news_content[:200]}...")
    else:
        print("❌ 新闻内容提取失败")
        return False
    
    # 测试3：生成基础摘要（不依赖智谱API）
    print("\n🤖 测试3：生成基础摘要")
    basic_summary = sender.generate_basic_summary(news_content)
    if basic_summary:
        print(f"✅ 基础摘要生成成功")
        print(f"📝 摘要预览: {basic_summary[:200]}...")
    else:
        print("❌ 基础摘要生成失败")
        return False
    
    # 测试4：测试飞书发送（如果没有配置，会跳过）
    print("\n📤 测试4：测试飞书发送")
    success = sender.send_to_feishu(basic_summary)
    if success:
        print("✅ 飞书发送成功")
    else:
        print("⚠️ 飞书发送失败（可能是配置问题）")
    
    print("\n🎉 测试完成！")
    return True

if __name__ == "__main__":
    test_news_sender()