import os
import sys
import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 加载配置
load_dotenv()

# ==================== 配置区域 ==================
API_KEY = os.getenv("AI_API_KEY")
BASE_URL = os.getenv("AI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
MODEL = os.getenv("AI_MODEL", "glm-4-flash")
VAULT_PATH = Path(r"C:\Users\13312\Desktop\ai软件\obsidian\ai新闻")
# ==================================================

def find_md_files(keyword: str, recursive: bool = False) -> list[Path]:
    """在 Vault 里搜索包含关键词的 .md 文件列表"""
    matched_files = []
    pattern = "**/*.md" if recursive else "*.md"

    for p in VAULT_PATH.glob(pattern):
        if keyword.lower() in p.name.lower() or keyword.lower() in str(p).lower():
            matched_files.append(p)

    return matched_files

def call_ai(prompt: str, temperature: float = 0.7) -> str:
    """调用大模型"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()

def ai_summary(content: str) -> str:
    """生成摘要"""
    prompt = (
        "你是一个专业的笔记助手。请阅读以下 Obsidian 笔记内容，"
        "用中文生成一段简洁的摘要（100字以内），指出核心知识点。\n\n"
        f"笔记内容：\n{content[:3000]}"
    )
    return call_ai(prompt, 0.7)

def ai_translate(content: str) -> str:
    """翻译成英文"""
    prompt = (
        "你是一个专业的翻译助手。请将以下中文内容翻译成英文，"
        "保持原意，语言自然流畅。\n\n"
        f"中文内容：\n{content[:3000]}"
    )
    return call_ai(prompt, 0.3)

def ai_keywords(content: str) -> str:
    """提取关键词"""
    prompt = (
        "你是一个关键词提取助手。请从以下内容中提取 5-10 个关键词，"
        "用逗号分隔，关键词要准确反映内容核心。\n\n"
        f"内容：\n{content[:3000]}"
    )
    return call_ai(prompt, 0.2)

def ai_improve(content: str) -> str:
    """优化建议"""
    prompt = (
        "你是一个写作优化助手。请分析以下笔记内容，"
        "给出 3-5 条具体的改进建议，包括结构、内容、表达等方面。\n\n"
        f"内容：\n{content[:3000]}"
    )
    return call_ai(prompt, 0.7)

def process_with_ai(content: str, mode: str) -> str:
    """根据模式调用相应的 AI 处理函数"""
    mode_functions = {
        'summary': ai_summary,
        'translate': ai_translate,
        'keywords': ai_keywords,
        'improve': ai_improve
    }

    if mode not in mode_functions:
        raise ValueError(f"不支持的模式: {mode}")

    return mode_functions[mode](content)

def main():
    parser = argparse.ArgumentParser(description='Obsidian AI 笔记助手')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理所有文件')
    parser.add_argument('--skip-existing', action='store_true', help='跳过已处理的文件')
    parser.add_argument('--mode',
                       choices=['summary', 'translate', 'keywords', 'improve'],
                       default='summary',
                       help='处理模式: summary(摘要), translate(翻译), keywords(关键词), improve(优化建议)')

    args = parser.parse_args()

    matched_files = find_md_files(args.keyword, args.recursive)

    if not matched_files:
        print(f"❌ 在 Vault 中没找到包含「{args.keyword}」的 Markdown 文件")
        sys.exit(1)

    # 不同模式对应的中文名字和标题
    mode_info = {
        'summary': {'name': '摘要', 'title': 'AI 摘要'},
        'translate': {'name': '翻译', 'title': 'AI 英文翻译'},
        'keywords': {'name': '关键词', 'title': 'AI 关键词提取'},
        'improve': {'name': '优化建议', 'title': 'AI 优化建议'}
    }

    info = mode_info[args.mode]
    print(f"📄 找到 {len(matched_files)} 个文件，模式: {info['name']}")

    for md_file in matched_files:
        output_file = md_file.parent / f"{md_file.stem}_AI{info['name']}.md"

        if args.skip_existing and output_file.exists():
            print(f"⏭️  跳过已处理的: {md_file.name}")
            continue

        print(f"\n📄 处理: {md_file.relative_to(VAULT_PATH)}")

        content = md_file.read_text(encoding="utf-8")
        result = process_with_ai(content, args.mode)

        print(result[:100] + "..." if len(result) > 100 else result)

        output_file.write_text(f"# {info['title']}\n\n{result}\n\n---\n\n", encoding="utf-8")
        print(f"✅ 已保存: {output_file.name}")

    print(f"\n🎉 完成！共处理 {len(matched_files)} 个文件")

if __name__ == "__main__":
    main()