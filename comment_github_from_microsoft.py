"""
将 GitHub.txt 中的非注释条目在 Microsoft.txt 中找到并注释掉。
"""

GITHUB_FILE = "mihomo/domain/GitHub.txt"
MICROSOFT_FILE = "mihomo/domain/Microsoft.txt"


def load_active_entries(filepath):
    """返回文件中所有非注释行的集合（去掉换行符）。"""
    entries = set()
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\r\n")
            if stripped and not stripped.startswith("#"):
                entries.add(stripped)
    return entries


def comment_out_matches(microsoft_path, targets):
    """
    读取 Microsoft.txt，将与 targets 中任意条目完全匹配的非注释行注释掉。
    返回 (新内容行列表, 已注释条目列表, 未找到条目列表)。
    """
    with open(microsoft_path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    commented = []
    matched_targets = set()

    for line in lines:
        stripped = line.rstrip("\r\n")
        # 已经是注释行，直接保留
        if stripped.startswith("#"):
            new_lines.append(stripped + "\n")
            continue
        # 非注释行，检查是否在目标集合中
        if stripped in targets:
            new_lines.append("# " + stripped + "\n")
            commented.append(stripped)
            matched_targets.add(stripped)
        else:
            new_lines.append(stripped + "\n")

    not_found = sorted(targets - matched_targets)
    return new_lines, sorted(commented), not_found


def main():
    print("=== 开始处理 ===\n")

    print(f"[1/3] 读取 GitHub.txt 中的非注释条目 ...")
    github_entries = load_active_entries(GITHUB_FILE)
    print(f"      共找到 {len(github_entries)} 个有效条目\n")

    print(f"[2/3] 在 Microsoft.txt 中查找并注释匹配行 ...")
    new_lines, commented, not_found = comment_out_matches(MICROSOFT_FILE, github_entries)

    print(f"[3/3] 写回 Microsoft.txt ...\n")
    with open(MICROSOFT_FILE, "w", encoding="utf-8", newline="") as f:
        f.writelines(new_lines)

    # 汇报
    print("=" * 50)
    print("任务完成汇报")
    print("=" * 50)
    print(f"GitHub.txt 有效条目数   : {len(github_entries)}")
    print(f"Microsoft.txt 成功注释数: {len(commented)}")
    print(f"未在 Microsoft.txt 中找到: {len(not_found)}")

    if commented:
        print("\n【已注释的条目】")
        for entry in commented:
            print(f"  {entry}")

    if not_found:
        print("\n【未找到的条目】")
        for entry in not_found:
            print(f"  {entry}")

    print("\n=== 处理完毕 ===")


if __name__ == "__main__":
    main()
