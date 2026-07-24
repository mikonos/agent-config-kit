import os
import re
import sys
from datetime import datetime, timedelta

WORKSPACE_ROOT = "/path/to/Nutstore Files/Zettelkasten/AI-Zettelkasten"
NOTES_BASE_DIR = os.path.join(WORKSPACE_ROOT, "05_每日记录")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "memory/入网")

def get_date_dirs(days_back=7):
    """获取过去 N 天的日期目录路径集合"""
    dirs = []
    today = datetime.now()
    for i in range(days_back):
        target_date = today - timedelta(days=i)
        # 匹配 2026/03/20260309 这样的层级格式
        dir_path = os.path.join(
            NOTES_BASE_DIR, 
            target_date.strftime("%Y"),
            target_date.strftime("%m"),
            target_date.strftime("%Y%m%d")
        )
        if os.path.exists(dir_path):
            dirs.append(dir_path)
    return dirs

def find_unindexed_notes(directories):
    """扫描指定目录集合下尚未归网（无归网：✅标记）的所有 markdown 文件"""
    unindexed = []
    for d in directories:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "归网：✅" not in content:
                            unindexed.append(file_path)
    return unindexed

def generate_manifest(unindexed_files, output_filename=None):
    """将扫描结果基于其子目录名称进行聚类预判断，生成人类友好的 markdown 待确认清单"""
    if not output_filename:
        today_str = datetime.now().strftime("%Y%m%d")
        output_filename = f"{today_str}_清单待确认.md"
    
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    category_groups = {}
    
    for file_path in unindexed_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        file_name = os.path.basename(file_path)
        node_name = os.path.splitext(file_name)[0]
        
        # 整理干净展示用的节点名（去掉前缀的日期）
        clean_node = re.sub(r'^(20\d{6}_|20\d{6}_[0-9]{2}_)', '', node_name)
        
        # 使用直属目录作为初筛聚类锚点（假设目录多表现为主题）
        # 如果外层目录就是单纯的日期目录（比如 `20260309`），则归入默认「未分类」
        if re.match(r'^\d{8}$', dir_name):
            category = "❓ 散落日记 (无特定子目录，需手动指定索引)"
        else:
            category = f"📁 子主题：{dir_name} (请手动将此标题替换为目标: [[索引_XXX.md]])"
            
        if category not in category_groups:
            category_groups[category] = []
        category_groups[category].append(f"- [[{node_name}]] (节点：[{clean_node}])")
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {datetime.now().strftime('%Y-%m-%d')} 批量归网确认清单\n\n")
        f.write(f"共扫描到 **{len(unindexed_files)}** 篇未带有 `归网：✅` 标签的笔记。\n\n")
        
        count = 1
        for category, items in category_groups.items():
            f.write(f"### {count}. {category}\n")
            f.write("\n".join(items) + "\n\n")
            count += 1
            
        f.write("---\n**操作说明**：\n")
        f.write("以上为根据笔记存放目录自动聚类的归网提案初步模板。\n")
        f.write("1. 请将 `###` 后面的名称手动改为你的目标卡片（例如 `### 1. [[索引_营销.md]]`）。\n")
        f.write("2. 修改完毕且确认笔记归属无误后，保存此文件。\n")
        f.write("3. 运行批量归网脚本 `python3 .agents/skills/index-note/scripts/batch_network_integration.py` 即可一键完成全自动双向反链与打标！\n")

    return output_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description="自动提取指定天数内尚未入网的笔记并生成归网确认清单")
    parser.add_argument("--days", type=int, default=7, help="搜索过去多少天的日记（默认：7天）")
    parser.add_argument("--output", type=str, default=None, help="自定义输出清单文件名 (默认: YYYYMMDD_清单待确认.md)")
    
    args = parser.parse_args()
    
    print(f"======================================")
    print(f"开始搜集未归网笔记... (范围: 过去 {args.days} 天)")
    
    target_dirs = get_date_dirs(args.days)
    if not target_dirs:
        print("未找到对应的日期目录。")
        return
        
    unindexed = find_unindexed_notes(target_dirs)
    print(f"找到了 {len(unindexed)} 篇缺少 `归网：✅` 标记的笔记。")
    
    if unindexed:
        manifest_path = generate_manifest(unindexed, args.output)
        print(f"======================================")
        print(f"✅ 清单已生成：{manifest_path}")
        print(f"👉 请打开该文件，将其中的目录名替换为你实际要挂载的 [[索引_XXX.md]]，")
        print(f"   然后再搭配 batch_network_integration.py 进行自动化写入！")

if __name__ == "__main__":
    main()
