
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass(frozen=True)
class Catalog:
    id: int
    name: str

@dataclass(frozen=True)
class File:
    id: int
    name: str
    size_kb: int
    catalog_id: int

@dataclass(frozen=True)
class FileCatalog:
    file_id: int
    catalog_id: int


catalogs: List[Catalog] = [
    Catalog(1, "Документы"),
    Catalog(2, "Фото"),
    Catalog(3, "Архив"),
    Catalog(4, "Проекты"),
]

files: List[File] = [
    File(1, "отчёт_Иванов",   120, 1),
    File(2, "доклад_Петров",  250, 1),
    File(3, "скан_паспорт",    90, 1),
    File(4, "фото_Сидоров",  2048, 2),
    File(5, "скрин_рабстол",  512, 2),
    File(6, "черновик_Орлов",  80, 4),
]

file_catalog_links: List[FileCatalog] = [
    FileCatalog(1, 3),
    FileCatalog(2, 3),
    FileCatalog(4, 3),
    FileCatalog(5, 4),
    FileCatalog(6, 3),
    FileCatalog(1, 4),
]

cat_by_id: Dict[int, Catalog] = {c.id: c for c in catalogs}
files_by_id: Dict[int, File] = {f.id: f for f in files}


def query1_file_catalog_pairs(
    files: List[File],
    cat_by_id: Dict[int, Catalog],
) -> List[Tuple[str, int, str]]:

    pairs = [(f.name, f.size_kb, cat_by_id[f.catalog_id].name) for f in files]
    return sorted(pairs, key=lambda x: x[0].lower())


def query2_catalog_file_counts_with_list(
    files: List[File],
    catalogs: List[Catalog],
) -> List[Tuple[str, int, List[Tuple[str, int]]]]:

    grouped: Dict[int, List[Tuple[str, int]]] = {c.id: [] for c in catalogs}
    for f in files:
        grouped[f.catalog_id].append((f.name, f.size_kb))

    result: List[Tuple[str, int, List[Tuple[str, int]]]] = []
    for c in catalogs:
        file_list = sorted(grouped[c.id], key=lambda t: t[0].lower())
        result.append((c.name, len(file_list), file_list))

    return sorted(result, key=lambda t: (-t[1], t[0].lower()))


def query3_files_ending_ov_with_all_catalogs(
    files: List[File],
    catalogs: List[Catalog],
    links: List[FileCatalog],
) -> List[Tuple[str, int, List[str]]]:
    mm: Dict[int, set] = {}
    for link in links:
        mm.setdefault(link.file_id, set()).add(link.catalog_id)

    result: List[Tuple[str, int, List[str]]] = []
    for f in files:
        if f.name.endswith("ов"):
            all_cat_ids = {f.catalog_id} | mm.get(f.id, set())
            cat_names = [cat_by_id[cid].name for cid in sorted(all_cat_ids)]
            result.append((f.name, f.size_kb, cat_names))

    return sorted(result, key=lambda x: x[0].lower())


if __name__ == "__main__":
    print("Рубежный контроль №1 — Вариант Б | Файл–Каталог")
    print()

    pairs = query1_file_catalog_pairs(files, cat_by_id)
    print("1) Файл—Каталог (1→М), отсортировано по файлам:")
    for fname, size, cname in pairs:
        print(f"   - {fname} ({size} KB)  ->  {cname}")
    print()

    catalogs_info = query2_catalog_file_counts_with_list(files, catalogs)
    print("2) Каталоги: количество файлов и их список:")
    for cname, cnt, flist in catalogs_info:
        print(f"   - {cname}: {cnt}")
        for fn, sz in flist:
            print(f"       • {fn} ({sz} KB)")
    print()

    files_ov = query3_files_ending_ov_with_all_catalogs(files, catalogs, file_catalog_links)
    print("3) Файлы, оканчивающиеся на «ов» и все каталоги (М→М):")
    if not files_ov:
        print("   - Нет файлов, удовлетворяющих условию.")
    else:
        for fname, size, cat_list in files_ov:
            print(f"   - {fname} ({size} KB): {', '.join(cat_list)}")
