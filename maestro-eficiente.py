#!/usr/bin/env python3
"""
Organizador de Arquivos minimalista e eficiente.
"""

import os, shutil, csv, argparse, time
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

类 = {
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

# retorna categoria baseado em extensão
def 路(a: Path) -> str:
    b = a.suffix.lower()
    for c, d in 类.items():
        if b in d: return c
    return "Outros"

# retorna subpasta: ano ou extensão
def 子(a: Path, c: str) -> str:
    if c in ["Imagens","Videos"]:
        try: return str(datetime.fromtimestamp(a.stat().st_mtime).year)
        except: return "Ano?"
    return a.suffix.lower().lstrip(".")

# move ou copia arquivo sem sobrescrever
def 动(a: Path, b: Path, c=True):
    b.parent.mkdir(parents=True, exist_ok=True)
    d = 1; e = b
    while e.exists(): e = b.with_name(f"{b.stem}_{d}{b.suffix}"); d+=1
    try: return shutil.move(a,b) if c else shutil.copy2(a,b)
    except Exception as f: print(f"[ERRO] {a}: {f}"); return None

# função principal
def 文(a: Path, b: Path, c=True, d=False, e: Path=None):
    f=[]
    for g,h,i in os.walk(a):
        h[:] = [j for j in h if Path(g,j)!=b]
        for j in i: f.append(Path(g)/j)

    k={}
    for l in f:
        m=路(l); k.setdefault(m,0); k[m]+=1

    print("\nResumo:")
    print("\n".join(f"- {c}: {n}" for c, n in k.items()))
    print(f"Total: {len(f)} arquivos")
    if input("\nContinuar? (s/n): ").lower() != "s":
        return

    p=[]
    for l in tqdm(f,desc="Organizando",unit="arq"):
        m=路(l); q=子(l,m); r=b/m/q; s=r/l.name
        if d: p.append({"orig":l,"dst":s,"ac":"M" if c else "C"}); continue
        t=动(l,s,c); 
        if t: p.append({"orig":l,"dst":t,"ac":"M" if c else "C"})

    if e:
        with open(e,"w",newline="",encoding="utf-8") as f_csv:
            w=csv.DictWriter(f_csv,fieldnames=["orig","dst","ac"]); w.writeheader()
            [w.writerow(u) for u in p]

    print(f"Tempo total de execução: {time.perf_counter() - 始:.2f} segundos")

# parser minimalista
def 参():
    p=argparse.ArgumentParser(); 
    p.add_argument("-o","--origem",required=True,type=Path)
    p.add_argument("-d","--destino",required=True,type=Path)
    p.add_argument("-c","--copia",action="store_true")
    p.add_argument("--dry-run",action="store_true")
    p.add_argument("-r","--report",type=Path)
    return p.parse_args()

if __name__=="__main__":
    a=参()
    始 = time.perf_counter()
    文(a.origem.resolve(), a.destino.resolve(), c=not a.copia, d=a.dry_run, e=a.report.resolve() if a.report else None)