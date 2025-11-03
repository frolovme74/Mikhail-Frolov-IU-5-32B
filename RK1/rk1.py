
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

def query1_file_catalog_pairs(files: List[File], cat_by_id: Dict[int, Catalog]) -> List[Tuple[str, str]]:
    pairs = [(f.name, cat_by_id[f.catalog_id].name) for f in files]
    return sorted(pairs, key=lambda x: x[0].lower())

def query2_catalog_file_counts(files: List[File], catalogs: List[Catalog]) -> List[Tuple[str, int]]:
    counts: Dict[int, int] = {c.id: 0 for c in catalogs}
    for f in files:
        counts[f.catalog_id] = counts.get(f.catalog_id, 0) + 1
    result = [(cat_by_id[cid].name, cnt) for cid, cnt in counts.items()]
    return sorted(result, key=lambda t: (-t[1], t[0].lower()))


def query3_files_ending_ov_with_all_catalogs(
    files: List[File],
    catalogs: List[Catalog],
    links: List[FileCatalog],
) -> List[Tuple[str, List[str]]]:
    mm: Dict[int, set] = {}
    for link in links:
        mm.setdefault(link.file_id, set()).add(link.catalog_id)

    result: List[Tuple[str, List[str]]] = []
    for f in files:
        if f.name.endswith("ов"):
            all_cat_ids = {f.catalog_id} | mm.get(f.id, set())
            cat_names = [cat_by_id[cid].name for cid in sorted(all_cat_ids)]
            result.append((f.name, cat_names))
    return sorted(result, key=lambda x: x[0].lower())


if __name__ == "__main__":
    print("Рубежный контроль №1 — Вариант Б | Файл–Каталог")
    print()

    pairs = query1_file_catalog_pairs(files, cat_by_id)
    print("1) Файл—Каталог (1→М), отсортировано по файлам:")
    for fname, cname in pairs:
        print(f"   - {fname}  ->  {cname}")
    print()

    counts = query2_catalog_file_counts(files, catalogs)
    print("2) Каталоги с количеством файлов (1→М), по убыванию количества:")
    for cname, cnt in counts:
        print(f"   - {cname}: {cnt}")
    print()

    files_ov = query3_files_ending_ov_with_all_catalogs(files, catalogs, file_catalog_links)
    print("3) Файлы, оканчивающиеся на «ов», и все их каталоги (М→М):")
    if not files_ov:
        print("   - Нет файлов, удовлетворяющих условию.")
    else:
        for fname, cat_list in files_ov:
            print(f"   - {fname}: {', '.join(cat_list)}")
