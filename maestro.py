#!/usr/bin/env python3
"""
Organizador de Arquivos Automático

Percorre um diretório raiz, classifica arquivos por tipo e ano/extensão,
e organiza em um diretório de destino.

Requisitos:
- Python 3.8+
- Bibliotecas: tqdm, os, pathlib, shutil, argparse, datetime, csv
"""

import os
import shutil
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
import argparse
import csv
import time

# ----------------------------
# CONFIGURAÇÃO DE CATEGORIAS
# ----------------------------
CATEGORIES = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".webp", ".heic", ".ico", ".raw", ".psd", ".ai", ".indd"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".mpeg", ".mpg", ".3gp", ".m4v", ".vob"],
    "Musicas": [".mp3", ".flac", ".wav", ".aac", ".ogg", ".wma", ".m4a", ".alac", ".aiff", ".opus"],
    "Documentos": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".odt", ".ods", ".odp", ".rtf", ".tex", ".csv", ".md", ".log"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".dmg", ".cab"],
    "Executáveis": [".exe", ".msi", ".bat", ".cmd", ".sh", ".jar", ".app", ".apk"],
    "Fontes": [".ttf", ".otf", ".woff", ".woff2", ".fnt"],
    "Scripts e Código": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".rb", ".php", ".html", ".css", ".json", ".xml", ".sql", ".sh", ".pl", ".go", ".rs", ".swift", ".kt"],
    "Imagens de Disco": [".iso", ".img", ".bin", ".cue", ".mdf", ".mds"],
    "Modelos 3D": [".obj", ".fbx", ".stl", ".dae", ".3ds", ".blend", ".ply"],
    "Outros": [".bak", ".tmp", ".log", ".dat", ".cfg", ".ini"]
}

# ----------------------------
# FUNÇÕES AUXILIARES
# ----------------------------

def get_file_category(file_path: Path) -> str:
    """Retorna a categoria principal do arquivo baseado na extensão."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Outros"

def get_subfolder_name(file_path: Path, category: str) -> str:
    """Retorna o subfolder baseado em ano ou extensão."""
    if category in ["Imagens", "Videos"]:
        try:
            timestamp = file_path.stat().st_mtime
            year = datetime.fromtimestamp(timestamp).year
            return f"{year}"
        except Exception:
            return "AnoDesconhecido"
    elif category in ["Documentos","Compactados","Executáveis","Fontes","Scripts e Código","Imagens de Disco","Modelos 3D","Outros"]:
        return file_path.suffix.lower().lstrip(".")
    else:
        return "Desconhecido"

def safe_move_or_copy(src: Path, dst: Path, move: bool = True):
    """Move ou copia arquivo, renomeando se já existir."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    counter = 1
    target = dst
    while target.exists():
        target = dst.with_name(f"{dst.stem}_{counter}{dst.suffix}")
        counter += 1
    try:
        if move:
            shutil.move(str(src), str(target))
        else:
            shutil.copy2(str(src), str(target))
        return target
    except Exception as e:
        print(f"[ERRO] Não foi possível processar {src}: {e}")
        return None

# ----------------------------
# FUNÇÃO PRINCIPAL
# ----------------------------

def organize_files(
    source_dir: Path,
    dest_dir: Path,
    move: bool = True,
    dry_run: bool = False,
    report_file: Path = None
):
    """
    Organiza arquivos do diretório de origem para o destino.
    """
    files_to_process = []

    # 1️⃣ Percorrer recursivamente o diretório de origem
    for root, dirs, files in os.walk(source_dir):
        # Ignorar a própria pasta de destino
        dirs[:] = [d for d in dirs if Path(root, d) != dest_dir]
        for file in files:
            files_to_process.append(Path(root) / file)

    # 2️⃣ Preparar contagem para resumo
    summary = {}
    for file_path in files_to_process:
        category = get_file_category(file_path)
        summary.setdefault(category, 0)
        summary[category] += 1

    # 3️⃣ Mostrar resumo para o usuário
    print("\nResumo de arquivos encontrados por categoria:")
    for cat, count in summary.items():
        print(f"- {cat}: {count}")
    print(f"Total: {len(files_to_process)} arquivos\n")

    # 4️⃣ Confirmar execução
    proceed = input("Deseja continuar? (s/n): ").lower()
    if proceed != "s":
        print("Operação cancelada pelo usuário.")
        return

    # 5️⃣ Processar arquivos com barra de progresso
    processed_files = []
    for file_path in tqdm(files_to_process, desc="Organizando", unit="arquivo"):
        category = get_file_category(file_path)
        subfolder = get_subfolder_name(file_path, category)
        target_dir = dest_dir / category / subfolder
        target_path = target_dir / file_path.name

        if dry_run:
            # Apenas simulação
            processed_files.append({
                "origem": str(file_path),
                "destino": str(target_path),
                "acao": "MOVER" if move else "COPIAR"
            })
            continue

        result = safe_move_or_copy(file_path, target_path, move=move)
        if result:
            processed_files.append({
                "origem": str(file_path),
                "destino": str(result),
                "acao": "MOVER" if move else "COPIAR"
            })

    # 6️⃣ Gerar relatório opcional
    if report_file:
        try:
            with open(report_file, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["origem", "destino", "acao"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in processed_files:
                    writer.writerow(row)
            print(f"Relatório salvo em: {report_file}")
        except Exception as e:
            print(f"[ERRO] Não foi possível gerar relatório: {e}")

    print("\nOrganização concluída!")
    print(f"Tempo total de execução: {time.perf_counter() - start_time:.2f} segundos")

# ----------------------------
# EXECUÇÃO VIA ARGPARSE
# ----------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Organizador de Arquivos Automático"
    )
    parser.add_argument(
        "-o", "--origem", required=True, type=Path,
        help="Diretório raiz de origem"
    )
    parser.add_argument(
        "-d", "--destino", required=True, type=Path,
        help="Diretório de destino"
    )
    parser.add_argument(
        "-c", "--copia", action="store_true",
        help="Copiar arquivos ao invés de mover"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simular operação sem mover/copiar arquivos"
    )
    parser.add_argument(
        "-r", "--report", type=Path,
        help="Gerar relatório em CSV após execução"
    )
    return parser.parse_args()

# ----------------------------
# PONTO DE ENTRADA
# ----------------------------

if __name__ == "__main__":
    args = parse_args()
    start_time = time.perf_counter()
    organize_files(
        source_dir=args.origem.resolve(),
        dest_dir=args.destino.resolve(),
        move=not args.copia,
        dry_run=args.dry_run,
        report_file=args.report.resolve() if args.report else None
    )