#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书API配置验证脚本
专门验证飞书API密钥配置是否正确
"""

import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

def load_config():
    """加载配置文件"""
    # 尝试加载不同路径的配置文件
    config_paths = [
        ".env",
        "C:\\Users\\13312\\Desktop\\ai软件\\git\\obsidian-ai-helper\\.env",
        str(Path(__file__).parent / ".env")
    ]
    
    config_loaded = False
    for config_path in config_paths:
        if os.path.exists(config_path):
            print(f"📁 找到配置文件: {config_path}")
            load_dotenv(config_path)
            config_loaded = True
            break
    
    if not config_loaded:
        print("❌ 未找到配置文件 (.env)")
        return False
    
    return True

def check_environment_variables():
    """检查环境变量配置"""
    print("\n🔍 检查环境变量配置")
    
    required_vars = {
        "FEISHU_APP_ID": "飞书应用ID",
        "FEISHU_APP_SECRET": "飞书应用密钥",
        "FEISHU_TENANT_ACCESS_TOKEN": "飞书访问令牌"
    }
    
    optional_vars = {
        "ZHIPU_API_KEY": "智谱AI API密钥（可选）"
    }
    
    print("\n📋 必需的环境变量:")
    all_required_ok = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # 只显示部分内容，保护隐私
            if var == "FEISHU_APP_SECRET":
                display_value = value[:8] + "..." if len(value) > 8 else value
            elif var == "FEISHU_TENANT_ACCESS_TOKEN":
                display_value = value[:20] + "..." if len(value) > 20 else value
            else:
                display_value = value
            
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 未配置")
            all_required_ok = False
    
    print("\n📋 可选的环境变量:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            display_value = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️ {var}: 未配置（可选）")
    
    return all_required_ok

def test_tenant_access_token():
    """测试访问令牌"""
    print("\n🔍 测试访问令牌")
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    tenant_access_token = os.getenv("FEISHU_TENANT_ACCESS_TOKEN")
    
    if not all([app_id, app_secret, tenant_access_token]):
        print("❌ 缺少必需的环境变量")
        return False
    
    # 方法1：直接测试令牌有效性
    print("\n📋 方法1：测试访问令牌有效性")
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 使用App ID和Secret获取新的访问令牌
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    try:
        print("🔄 正在获取新的访问令牌...")
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("code") == 0:
            new_token = result.get("tenant_access_token")
            print("✅ 成功获取新的访问令牌")
            print(f"📝 令牌长度: {len(new_token)} 字符")
            
            # 测试新令牌
            if test_token_validity(new_token):
                print("✅ 新令牌有效")
                return True
            else:
                print("❌ 新令牌无效")
                return False
        else:
            print(f"❌ 获取访问令牌失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 获取访问令牌异常: {e}")
        return False

def test_token_validity(access_token):
    """测试访问令牌有效性"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/verify"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            return True
        else:
            print(f"❌ 令牌验证失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 令牌验证异常: {e}")
        return False

def test_message_sending():
    """测试消息发送"""
    print("\n🔍 测试消息发送")
    
    tenant_access_token = os.getenv("FEISHU_TENANT_ACCESS_TOKEN")
    
    if not tenant_access_token:
        print("❌ 缺少访问令牌")
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "receive_id": "all",  # 发送给所有人
        "msg_type": "text",
        "content": {
            "text": "🧪 飞书API配置验证测试消息 - Obsidian新闻发送器"
        }
    }
    
    try:
        print("🔄 正在发送测试消息...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            print("✅ 测试消息发送成功")
            return True
        else:
            print(f"❌ 消息发送失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 消息发送异常: {e}")
        return False

def get_app_info():
    """获取应用信息"""
    print("\n🔍 获取应用信息")
    
    app_id = os.getenv("FEISHU_APP_ID")
    tenant_access_token = os.getenv("FEISHU_TENANT_ACCESS_TOKEN")
    
    if not all([app_id, tenant_access_token]):
        print("❌ 缺少应用ID或访问令牌")
        return False
    
    url = "https://open.feishu.cn/open-apis/app/v1/applications"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            apps = result.get("data", {}).get("app_list", [])
            if apps:
                app = apps[0]
                print(f"✅ 应用名称: {app.get('app_name', '未知')}")
                print(f"✅ 应用ID: {app.get('app_id', '未知')}")
                print(f"✅ 应用类型: {app.get('app_type', '未知')}")
                
                # 检查权限
                permissions = app.get("permissions", [])
                print(f"✅ 权限数量: {len(permissions)}")
                
                # 检查是否需要im.message.send_v1权限
                message_send_perm = any("im.message" in str(perm) for perm in permissions)
                if message_send_perm:
                    print("✅ 具备消息发送权限")
                else:
                    print("❌ 缺少消息发送权限")
                    return False
                
                return True
            else:
                print("❌ 未找到应用信息")
                return False
        else:
            print(f"❌ 获取应用信息失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 获取应用信息异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 飞书API配置验证工具")
    print("=" * 60)
    
    # 步骤1：加载配置
    print("\n📋 步骤1：加载配置文件")
    if not load_config():
        print("❌ 无法加载配置文件")
        return False
    
    # 步骤2：检查环境变量
    print("\n📋 步骤2：检查环境变量")
    if not check_environment_variables():
        print("❌ 必需的环境变量未配置")
        return False
    
    # 步骤3：测试访问令牌
    print("\n📋 步骤3：测试访问令牌")
    token_ok = test_tenant_access_token()
    
    # 步骤4：获取应用信息
    print("\n📋 步骤4：获取应用信息")
    app_ok = get_app_info()
    
    # 步骤5：测试消息发送
    print("\n📋 步骤5：测试消息发送")
    message_ok = test_message_sending()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证结果总结:")
    
    all_ok = all([token_ok, app_ok, message_ok])
    
    if token_ok:
        print("✅ 访问令牌: 有效")
    else:
        print("❌ 访问令牌: 无效")
    
    if app_ok:
        print("✅ 应用信息: 正常")
    else:
        print("❌ 应用信息: 异常")
    
    if message_ok:
        print("✅ 消息发送: 成功")
    else:
        print("❌ 消息发送: 失败")
    
    if all_ok:
        print("\n🎉 飞书API配置完全正确！")
        print("\n💡 接下来你可以:")
        print("1. 运行主脚本: python news_feishu_sender.py")
        print("2. 查看Cron任务: cronjob action=list")
        print("3. 系统将在每天早上8点自动执行")
    else:
        print("\n⚠️ 飞书API配置存在问题，请检查:")
        print("1. 确认App ID和App Secret正确")
        print("2. 确认访问令牌未过期")
        print("3. 确认应用具备消息发送权限")
        print("4. 重新生成访问令牌")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)