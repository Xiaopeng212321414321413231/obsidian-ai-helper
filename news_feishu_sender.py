#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian新闻飞书发送器
每天早上8点自动从Obsidian vault中读取昨天的新闻文件，通过飞书以三月七口吻发送
"""

import os
import re
import json
import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ObsidianNewsFeishuSender:
    def __init__(self):
        self.obsidian_vault_path = Path(r"C:\Users\13312\Desktop\ai软件\obsidian\ai新闻")
        self.news_dir = self.obsidian_vault_path / "ai每日新闻"
        
        # 飞书配置
        self.feishu_app_id = os.getenv("FEISHU_APP_ID", "cli_aac6e3fb60649cff")
        self.feishu_app_secret = os.getenv("FEISHU_APP_SECRET")
        self.feishu_tenant_access_token = os.getenv("FEISHU_TENANT_ACCESS_TOKEN")
        
        # 智谱AI配置（用于生成三月七口吻的摘要）
        self.zhipu_api_key = os.getenv("ZHIPU_API_KEY")
        self.zhipu_base_url = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
        self.zhipu_model = os.getenv("ZHIPU_MODEL", "glm-4-flash")
    
    def get_yesterday_date(self):
        """获取昨天的日期"""
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")
    
    def find_yesterday_news_files(self):
        """查找昨天的新闻文件"""
        yesterday_date = self.get_yesterday_date()
        
        # 查找匹配的文件模式
        patterns = [
            f"AI日报_{yesterday_date}.md",
            f"AI工具日报（早）_{yesterday_date}.md", 
            f"AI每日简报_{yesterday_date}.md",
            f"AI每日内容产出_{yesterday_date}.md"
        ]
        
        for pattern in patterns:
            news_file = self.news_dir / pattern
            if news_file.exists():
                return news_file
        
        # 如果没有找到特定文件，查找所有昨天的文件
        all_news_files = list(self.news_dir.glob("*.md"))
        yesterday_files = []
        
        for file_path in all_news_files:
            if yesterday_date in file_path.name:
                yesterday_files.append(file_path)
        
        if yesterday_files:
            # 返回第一个匹配的文件
            return yesterday_files[0]
        
        return None
    
    def extract_news_content(self, file_path):
        """提取新闻内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
    
    def generate_march7_style_summary(self, news_content):
        """使用智谱AI生成三月七风格的新闻摘要"""
        if not self.zhipu_api_key or "请在此处填入" in self.zhipu_api_key:
            print("智谱API密钥未配置，使用基础摘要")
            return self.generate_basic_summary(news_content)
        
        prompt = f"""
请以崩坏星穹铁道「三月七」的口吻风格，将以下新闻内容改写成生动的对话式摘要：

要求：
1. 使用短句口语化节奏，像聊天一样自然
2. 大量使用"你/我/我们"制造在场感
3. 以具体人名/外号制造亲密感
4. 用括号备注制造当下调侃语气
5. 情感混合遗憾与笃定，把荒唐小事直接升华为友谊/成长的注释
6. 善用"贼难绷"等年轻网络语
7. 将当下感受与过去环境对比
8. 结尾用密集遗憾清单式收束情绪
9. 开头可以用轻松吐槽或笑话

新闻内容：
{news_content}

请生成500字以内的三月七风格摘要：
"""
        try:
            url = f"{self.zhipu_base_url}chat/completions"
            headers = {
                "Authorization": f"Bearer {self.zhipu_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.zhipu_model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.8
            }
            
            # 手动编码JSON，避免latin-1编码问题
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            response = requests.post(url, headers=headers, data=body, timeout=30)
            response.encoding = 'utf-8'
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            else:
                return self.generate_basic_summary(news_content)
                
        except Exception as e:
            print(f"智谱AI调用失败: {e}")
            return self.generate_basic_summary(news_content)
    
    def generate_basic_summary(self, news_content):
        """生成基础摘要（备用方案）"""
        # 提取主要新闻标题
        lines = news_content.split('\n')
        headlines = []
        
        for line in lines:
            if '##' in line and '今日头条' not in line and len(line.strip()) > 10:
                headlines.append(line.strip().replace('##', '').strip())
            elif line.startswith('# ') and 'AI日报' in line:
                headlines.append(line.strip().replace('# ', '').strip())
        
        summary = "嘿！今天的AI圈可真是热闹得不得了～\n\n"
        
        if headlines:
            summary += "🔥 重点新闻：\n"
            for i, headline in enumerate(headlines[:3], 1):
                summary += f"{i}. {headline}\n"
        else:
            summary += "今天AI圈的大新闻就是：变化真快啊！\n"
        
        summary += "\n（三月七帮你整理的AI日报，记得关注这些动态哦～）"
        
        return summary
    
    def send_to_feishu(self, message):
        """发送消息到飞书"""
        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            headers = {"Content-Type": "application/json; charset=utf-8"}
            resp = requests.post(url, json={"app_id": os.getenv("FEISHU_APP_ID", "cli_aac6e3fb60649cff"), "app_secret": os.getenv("FEISHU_APP_SECRET")}, timeout=10)
            token = resp.json()["tenant_access_token"]
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8"
            }
            
            user_open_id = "ou_131a15db6d87df44b3626b65bbfb8533"
            data = {
                "receive_id": user_open_id,
                "msg_type": "text",
                "content": json.dumps({"text": message}, ensure_ascii=False)
            }
            
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            resp = requests.post("https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id", headers=headers, data=body, timeout=10)
            resp.encoding = 'utf-8'
            
            result = resp.json()
            if result.get("code") == 0:
                print("✅ 飞书消息发送成功！")
                return True
            else:
                print(f"❌ 飞书发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"发送飞书消息失败: {e}")
            return False
    
    def run(self):
        """执行主流程"""
        print("开始执行新闻发送任务...")
        
        # 查找昨天的新闻文件
        news_file = self.find_yesterday_news_files()
        
        if not news_file:
            print(f"未找到昨天的新闻文件")
            return False
        
        print(f"找到新闻文件: {news_file}")
        
        # 提取新闻内容
        news_content = self.extract_news_content(news_file)
        if not news_content:
            print("新闻内容提取失败")
            return False
        
        print("新闻内容提取成功")
        
        # 生成三月七风格的摘要
        summary = self.generate_march7_style_summary(news_content)
        print("生成三月七风格摘要完成")
        
        # 发送到飞书
        success = self.send_to_feishu(summary)
        
        if success:
            print("任务完成：新闻已发送到飞书")
            return True
        else:
            print("任务失败：发送到飞书失败")
            return False

def main():
    """主函数"""
    sender = ObsidianNewsFeishuSender()
    success = sender.run()
    
    if success:
        print("✅ 任务执行成功")
    else:
        print("❌ 任务执行失败")

if __name__ == "__main__":
    main()