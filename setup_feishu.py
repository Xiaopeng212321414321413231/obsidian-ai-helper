#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书API配置助手
帮助你快速获取飞书访问令牌
"""

import requests
import json
import os
from dotenv import load_dotenv

def get_feishu_access_token():
    """获取飞书访问令牌"""
    # 加载现有的环境变量
    load_dotenv()
    
    # 获取App ID和Secret
    app_id = os.getenv("FEISHU_APP_ID", "cli_aac6e3fb60649cff")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_secret:
        print("❌ 请先在 .env 文件中设置 FEISHU_APP_SECRET")
        return None
    
    print(f"📱 App ID: {app_id}")
    print(f"🔑 App Secret: {app_secret[:8]}...")  # 只显示前8个字符
    
    # 获取访问令牌
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    try:
        print("🔄 正在获取访问令牌...")
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("code") == 0:
            tenant_access_token = result.get("tenant_access_token")
            print("✅ 获取访问令牌成功！")
            
            # 更新.env文件
            with open(".env", "r", encoding="utf-8") as f:
                content = f.read()
            
            # 更新或添加访问令牌
            if "FEISHU_TENANT_ACCESS_TOKEN=" in content:
                content = content.replace(
                    "FEISHU_TENANT_ACCESS_TOKEN=.*",
                    f"FEISHU_TENANT_ACCESS_TOKEN={tenant_access_token}"
                )
            else:
                content += f"\nFEISHU_TENANT_ACCESS_TOKEN={tenant_access_token}\n"
            
            with open(".env", "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"📝 已更新 .env 文件中的访问令牌")
            print(f"🔑 访问令牌: {tenant_access_token[:20]}...")
            
            return tenant_access_token
        else:
            print(f"❌ 获取访问令牌失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def test_feishu_connection():
    """测试飞书连接"""
    load_dotenv()
    
    access_token = os.getenv("FEISHU_TENANT_ACCESS_TOKEN")
    if not access_token:
        print("❌ 请先获取访问令牌")
        return False
    
    # 测试发送消息
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "receive_id": "all",  # 发送给所有人
        "msg_type": "text",
        "content": {
            "text": "🧪 飞书连接测试消息 - Obsidian新闻发送器"
        }
    }
    
    try:
        print("🔄 正在测试飞书连接...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            print("✅ 飞书连接测试成功！")
            return True
        else:
            print(f"❌ 飞书连接测试失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 飞书API配置助手")
    print("=" * 50)
    
    # 步骤1：获取访问令牌
    print("\n📋 步骤1：获取访问令牌")
    access_token = get_feishu_access_token()
    
    if not access_token:
        print("\n❌ 无法获取访问令牌，请检查App Secret是否正确")
        return
    
    # 步骤2：测试连接
    print("\n📋 步骤2：测试飞书连接")
    success = test_feishu_connection()
    
    if success:
        print("\n🎉 飞书配置完成！")
        print("\n💡 接下来你可以：")
        print("1. 运行测试脚本: python test_news_sender.py")
        print("2. 查看Cron任务状态: cronjob action=list")
        print("3. 手动运行脚本: python news_feishu_sender.py")
    else:
        print("\n⚠️ 飞书连接测试失败，请检查配置")

if __name__ == "__main__":
    main()