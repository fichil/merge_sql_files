from pathlib import Path
from datetime import datetime

# =========================
# 配置区：修改成你的绝对路径
# =========================
print("script loaded")
ROOT_DIR = Path(r"D:\document\sino\chainworkCode\chainwork-common-databean\upgradeSQL_TMS_BMS")

# 输出文件名（会生成在 ROOT_DIR 目录下）
OUTPUT_FILE_NAME = "all_sql_merged.sql"

# 是否在每个文件前面写入分隔注释
WRITE_FILE_HEADER = True


def read_file_with_fallback(file_path: Path) -> str:
    """
    读取文件内容，优先 utf-8，其次 gbk，最后 latin1 兜底。
    """
    encodings = ["utf-8", "utf-8-sig", "gbk", "latin1"]
    last_error = None

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError as e:
            last_error = e

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"无法识别文件编码: {file_path}. 原始错误: {last_error}"
    )


def collect_sql_files(root_dir: Path, output_file: Path):
    """
    递归收集所有 .sql 文件，并排除输出文件本身。
    """
    sql_files = []
    for file_path in root_dir.rglob("*.sql"):
        if file_path.resolve() == output_file.resolve():
            continue
        if file_path.is_file():
            sql_files.append(file_path)

    # 排序，保证每次输出顺序一致
    sql_files.sort(key=lambda p: str(p.relative_to(root_dir)).lower())
    return sql_files


def merge_sql_files(root_dir: Path, output_file_name: str):
    if not root_dir.exists():
        raise FileNotFoundError(f"配置的目录不存在: {root_dir}")

    if not root_dir.is_dir():
        raise NotADirectoryError(f"配置的路径不是目录: {root_dir}")

    output_file = root_dir / output_file_name
    sql_files = collect_sql_files(root_dir, output_file)

    if not sql_files:
        print(f"未找到任何 .sql 文件，扫描目录：{root_dir}")
        return

    merged_parts = []

    # 文件头
    merged_parts.append("-- =====================================")
    merged_parts.append("-- Auto generated SQL merge file")
    merged_parts.append(f"-- Root Directory : {root_dir}")
    merged_parts.append(f"-- Generated Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    merged_parts.append(f"-- File Count     : {len(sql_files)}")
    merged_parts.append("-- =====================================")
    merged_parts.append("")

    for index, sql_file in enumerate(sql_files, start=1):
        relative_path = sql_file.relative_to(root_dir)
        content = read_file_with_fallback(sql_file).strip()

        if WRITE_FILE_HEADER:
            merged_parts.append("")
            merged_parts.append("-- ----------------------------------------------------------------")
            merged_parts.append(f"-- [{index}] BEGIN FILE: {relative_path}")
            merged_parts.append("-- ----------------------------------------------------------------")

        merged_parts.append(content)

        # 保证每个文件结尾至少有一个分号或换行分隔
        if content and not content.endswith(";"):
            merged_parts.append(";")

        if WRITE_FILE_HEADER:
            merged_parts.append(f"-- [{index}] END FILE: {relative_path}")
            merged_parts.append("")

    output_file.write_text("\n".join(merged_parts), encoding="utf-8")

    print("SQL 合并完成")
    print(f"扫描目录: {root_dir}")
    print(f"SQL 文件数量: {len(sql_files)}")
    print(f"输出文件: {output_file}")

if __name__ == "__main__":
    print("脚本开始执行...")
    merge_sql_files(ROOT_DIR, OUTPUT_FILE_NAME)
    print("脚本执行结束...")
    