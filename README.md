# Obsidian AI Helper — 智能笔记助手

> **AI-powered note review + Feishu news delivery** · AI 笔记点评 + 飞书日报推送
>
> Uses Zhipu GLM to review your Obsidian notes, and deliver daily news summaries to Feishu with a charming persona.
> 用智谱 AI 自动点评你的 Obsidian 笔记、生成高质量反馈，还能以「三月七」的口吻把新闻发送到飞书群。

---

## Why This Tool?

**中文**

记笔记不难，难的是持续地记出高质量的笔记。

这个工具诞生于一个朴素的想法：如果每天 AI 能帮你看看昨天写了什么笔记，告诉你哪里写得好、哪里可以改进，那笔记质量就会像滚雪球一样越滚越好。

**English**

Taking notes is easy. Taking great notes, consistently? That's the hard part.

This tool was born from a simple idea: what if AI reviewed your daily notes, told you what's good and what could be improved, so your note quality snowballs day by day?

Two superpowers:
1. **AI Note Review** — Scan your Obsidian vault for quality insights
2. **Feishu Daily Push** — Deliver curated content to your Feishu groups every morning

---

## Features

### AI Note Review
Search your Obsidian vault by keyword, then let Zhipu GLM analyze note quality and suggest improvements.

### Feishu News Sender
Auto-send daily news summaries to Feishu groups with March 7th persona — lively, warm, and fun.

### One-Click Setup
```bash
python setup_feishu.py
```

---

## Quick Start

```bash
git clone https://github.com/Xiaopeng212321414321413231/obsidian-ai-helper.git
cd obsidian-ai-helper
pip install -r requirements.txt
cp .env.example .env
# Edit .env, set ZHIPUAI_API_KEY
python ai_review.py --keyword "Transformer" --recursive
```

---

## Project Structure

```
obsidian-ai-helper/
├── ai_review.py              # AI note review core
├── news_feishu_sender.py     # Feishu news sender
├── setup_feishu.py           # Feishu setup assistant
├── verify_feishu_config.py   # Config verification
├── test_news_sender.py       # Sender test
├── SETUP.md                  # Setup guide
├── requirements.txt          # Dependencies
└── .env.example              # Config template
```

---

## Tech Stack

| Layer | Tech | Description |
|-------|------|-------------|
| AI | Zhipu GLM-4-Flash | Free LLM, note analysis + news summary |
| Push | Feishu Webhook | Group robot message push |
| Storage | Obsidian Markdown | Local-first, zero cloud dependency |
| Config | python-dotenv | .env config management |

---

## About March 7th Persona

中文：推送消息使用「三月七」风格——不是冷冰冰的机器人通知，而是一个活泼可爱的助手。

English: The Feishu notifications speak in a lively, warm persona — turning cold machine alerts into morning conversations.

---

## License

MIT
