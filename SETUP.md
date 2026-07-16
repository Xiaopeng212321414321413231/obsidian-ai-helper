# Obsidian新闻飞书发送器设置指南

## 🎯 功能说明

每天早上8点自动从Obsidian vault中读取昨天的新闻文件，通过飞书以崩坏星穹铁道「三月七」的口吻发送AI日报摘要。

## 📋 系统要求

- Python 3.8+
- 已安装依赖包：`requests`, `python-dotenv`
- 飞书应用权限
- 智谱AI API（可选，用于生成三月七风格摘要）

## 🔧 配置步骤

### 1. 安装依赖包

```bash
cd "C:\Users\13312\Desktop\ai软件\git\obsidian-ai-helper"
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的配置信息：

```bash
copy .env.example .env
```

然后编辑 `.env` 文件，填入以下信息：

```env
# 飞书配置
FEISHU_APP_ID=your_feishu_app_id_here
FEISHU_APP_SECRET=你的飞书应用密钥
FEISHU_TENANT_ACCESS_TOKEN=你的飞书访问令牌

# 智谱AI配置（可选，用于生成三月七风格的摘要）
ZHIPU_API_KEY=你的智谱AI API密钥
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
ZHIPU_MODEL=glm-4-flash
```

### 3. 获取飞书API密钥和访问令牌

#### 3.1 获取应用密钥
1. 登录[飞书开放平台](https://open.feishu.cn/)
2. 进入"应用管理" → "自建应用"
3. 找到"三月七"应用（或创建新应用）
4. 在"凭证与基础信息"页面复制 `App ID` 和 `App Secret`

#### 3.2 获取访问令牌
使用以下Python脚本获取访问令牌：

```python
import requests
import json

# 替换为你的App ID和Secret
app_id = "your_feishu_app_id_here"
app_secret = "你的应用密钥"

url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
payload = {
    "app_id": app_id,
    "app_secret": app_secret
}

response = requests.post(url, json=payload)
result = response.json()

if result.get("code") == 0:
    tenant_access_token = result.get("tenant_access_token")
    print(f"访问令牌: {tenant_access_token}")
else:
    print(f"获取失败: {result}")
```

### 4. 获取智谱AI API密钥（可选）

1. 访问[智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录账户
3. 在"API管理"页面创建API密钥
4. 将密钥填入 `.env` 文件的 `ZHIPU_API_KEY`

## 🧪 测试功能

运行测试脚本验证配置：

```bash
python test_news_sender.py
```

## ⏰ 设置定时任务

### 1. 使用Hermes Cron任务（已配置）

系统已创建每天早上8点执行的Cron任务：
- 任务名称：Obsidian新闻飞书日报
- 执行时间：每天早上8点
- 执行脚本：`news_feishu_sender.py`

### 2. Windows任务计划（备用方案）

如果需要设置Windows任务计划：

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器：每天 08:00
4. 设置操作：启动程序
   - 程序路径：`C:\Users\13312\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
   - 参数：`"C:\Users\13312\Desktop\ai软件\git\obsidian-ai-helper\news_feishu_sender.py"`
   - 起始位置：`C:\Users\13312\Desktop\ai软件\git\obsidian-ai-helper`

## 📊 功能验证

### 1. 验证文件查找
脚本会自动查找以下模式的昨天的新闻文件：
- `AI日报_YYYY-MM-DD.md`
- `AI工具日报（早）_YYYY-MM-DD.md`
- `AI每日简报_YYYY-MM-DD.md`
- `AI每日内容产出_YYYY-MM-DD.md`

### 2. 验证摘要生成
- 如果配置了智谱AI，会生成三月七风格的对话式摘要
- 如果没有配置智谱AI，会生成基础摘要格式

### 3. 验证飞书发送
- 使用飞书Webhook API发送消息
- 支持文本消息格式

## 🔍 故障排除

### 常见问题

1. **找不到新闻文件**
   - 检查Obsidian vault路径是否正确
   - 确认昨天是否有新闻文件生成

2. **智谱AI调用失败**
   - 检查API密钥是否正确
   - 检查网络连接
   - 脚本会自动回退到基础摘要

3. **飞书发送失败**
   - 检查访问令牌是否有效
   - 检查应用权限是否正确
   - 检查消息格式是否符合要求

### 日志查看

运行脚本时会显示详细的日志信息，包括：
- 文件查找结果
- 内容提取状态
- API调用详情
- 错误信息

## 📝 自定义配置

### 修改发送时间
编辑Cron任务的schedule表达式：
- `0 8 * * *` = 每天8点
- `0 9 * * 1-5` = 工作日上午9点
- `*/30 * * * *` = 每30分钟

### 修改摘要风格
编辑 `news_feishu_sender.py` 中的 `generate_march7_style_summary` 方法来自定义摘要风格。

### 修改发送对象
编辑 `send_to_feishu` 方法中的 `receive_id` 参数来指定发送对象。

## 🎉 完成

完成以上配置后，系统将在每天早上8点自动从你的Obsidian vault中读取昨天的新闻，并通过飞书以三月七的口吻发送AI日报摘要。