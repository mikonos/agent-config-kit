import os
import re
import sys
from datetime import datetime

# 基础路径配置
WORKSPACE_ROOT = "/path/to/Nutstore Files/Zettelkasten/AI-Zettelkasten"
DEFAULT_MANIFEST_DIR = os.path.join(WORKSPACE_ROOT, "memory/入网")

def get_latest_manifest():
    """获取 memory/入网 目录下最新的 _清单待确认.md 文件"""
    candidates = []
    if not os.path.exists(DEFAULT_MANIFEST_DIR):
        return None
    for f in os.listdir(DEFAULT_MANIFEST_DIR):
        if f.endswith("_清单待确认.md"):
            full_path = os.path.join(DEFAULT_MANIFEST_DIR, f)
            candidates.append((full_path, os.path.getmtime(full_path)))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]

def parse_manifest(path):
    """解析清单文件，提取索引路径与笔记节点的映射关系"""
    mapping = {}
    current_index = None
    current_index_full_path = None
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 匹配一级索引卡片：### 1. [[索引_xxx]] 或 ### 1. [[索引_xxx.md]]
            match_index = re.search(r'### \d+\. \[\[(.*?)\]\]', line)
            if match_index:
                current_index = match_index.group(1)
                # 兼容是否带 .md 后缀
                if not current_index.endswith(".md"):
                    current_index += ".md"
                
                # 在 03_索引 目录下寻找准确的索引文件路径
                found = False
                for root, dirs, files in os.walk(os.path.join(WORKSPACE_ROOT, "03_索引")):
                    if current_index in files:
                        current_index_full_path = os.path.join(root, current_index)
                        if current_index_full_path not in mapping:
                            mapping[current_index_full_path] = []
                        found = True
                        break
                if not found:
                    print(f"警告：找不到索引文件 {current_index}，系统将忽略此分类下的笔记归网。")
                    current_index_full_path = None
                continue
            
            # 匹配笔记条目：- [[20261201_xxx]] (节点：[xxx])
            if current_index_full_path and line.startswith("- [["):
                match_note = re.search(r'- \[\[(.*?)\]\]', line)
                if match_note:
                    note_name = match_note.group(1)
                    if note_name not in mapping[current_index_full_path]:
                        mapping[current_index_full_path].append(note_name)
                        
    return mapping

def update_note_file(note_name, index_name):
    """给笔记打标归网标签并建立反向双链"""
    file_found = None
    # 搜索笔记具体位置（全库扫描以防遗漏，通常集中在 05_每日记录）
    search_dirs = [os.path.join(WORKSPACE_ROOT, "05_每日记录")]
    
    for search_dir in search_dirs:
        if file_found: break
        for root, dirs, files in os.walk(search_dir):
            if f"{note_name}.md" in files:
                file_found = os.path.join(root, f"{note_name}.md")
                break
    
    if not file_found:
        print(f"  -> 找不到笔记原文：{note_name}.md")
        return False

    with open(file_found, 'r', encoding='utf-8') as f:
        content = f.read()

    # 如果已经有 ✅ 标记，由于防重机制安全跳过
    if "归网：✅" in content:
        return True

    # 准备追加内容。移除 .md 后缀以保持纯正的双链语法
    target_link = index_name.replace('.md', '')
    backlink = f"\n\n---\n归网：✅ {datetime.now().strftime('%Y-%m-%d')}\n关联索引：[[{target_link}]]\n"
    
    with open(file_found, 'a', encoding='utf-8') as f:
        f.write(backlink)
    return True

def update_index_file(index_path, notes):
    """在索引文件的末尾插入新增条目"""
    if not notes:
        return 0
        
    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    existing_content = "".join(lines)
    new_entries = []
    
    for note in notes:
        if f"[[{note}]]" not in existing_content:
            new_entries.append(f"- [[{note}]]\n")
    
    if not new_entries:
        return 0

    today_str = datetime.now().strftime('%Y-%m-%d')
    with open(index_path, 'a', encoding='utf-8') as f:
        if not existing_content.endswith("\n"):
            f.write("\n")
        f.write(f"\n## {today_str} 批量归网补录\n")
        f.writelines(new_entries)
        
    return len(new_entries)

def main():
    # 允许命令行传参指定清单文件
    if len(sys.argv) > 1:
        manifest_path = sys.argv[1]
    else:
        manifest_path = get_latest_manifest()
        
    if not manifest_path or not os.path.exists(manifest_path):
        print("错误：未找见任何有效的 _清单待确认.md 文件。请指定清单路径。")
        sys.exit(1)

    print(f"======================================")
    print(f"开始批量集成网络...")
    print(f"读取清单文件: {manifest_path}")
    print(f"======================================")

    mapping = parse_manifest(manifest_path)
    if not mapping:
        print("清单中未发现有效的归属条目。")
        sys.exit(0)

    total_updated_notes = 0
    total_updated_indexes = 0

    for index_path, notes in mapping.items():
        if not notes: continue
        index_name = os.path.basename(index_path)
        print(f"\n[处理索引] {index_name} ...")
        
        updated_notes = []
        for note in notes:
            if update_note_file(note, index_name):
                updated_notes.append(note)
                total_updated_notes += 1
        
        added_entries = update_index_file(index_path, updated_notes)
        if added_entries > 0:
            total_updated_indexes += 1
            print(f"  -> {index_name} 已追加 {added_entries} 条新链接")

    print(f"\n======================================")
    print(f"集成完毕！！共更新 {total_updated_notes} 篇实体笔记，更新 {total_updated_indexes} 个知识索引。")
    print(f"======================================")

if __name__ == "__main__":
    main()
