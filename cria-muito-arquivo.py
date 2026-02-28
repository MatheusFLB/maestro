import os
import random
import pathlib
import string
import time
from datetime import datetime, timedelta

# Pasta raiz do HD simulado
root = pathlib.Path("HD_SIMULADO_GRANDE")
root.mkdir(exist_ok=True)

# Categorias e extensões fornecidas
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

# Lista de algumas extensões extras não incluídas para testar "Outros"
extra_exts = [".xyz", ".abc", ".unknown", ".mystery", ".weird"]

# Todas as extensões combinadas
all_exts = [e for sublist in CATEGORIES.values() for e in sublist] + extra_exts

# Nomes base de arquivos
nomes_base = ["relatorio","foto","video","arquivo","backup","nota","print","planilha","teste","documento","projeto","imagem","musica","dados"]

# Subpastas comuns
pastas = ["Downloads", "Documentos", "Fotos", "Videos", "Musicas", "Backup", "Projetos", "Coisas_Aleatorias"]

# Função para gerar datas aleatórias nos últimos 5 anos
def random_date():
    start = datetime.now() - timedelta(days=5*365)
    end = datetime.now()
    return start + (end - start) * random.random()

# Criar 1000 arquivos
num_arquivos = 1000
for _ in range(num_arquivos):
    # Escolhe pasta aleatória
    p = root / random.choice(pastas) / ('Sub_' + str(random.randint(1, 5)))
    p.mkdir(parents=True, exist_ok=True)
    
    # Escolhe extensão aleatória
    e = random.choice(all_exts)
    
    # Gera nome aleatório
    nome = random.choice(nomes_base) + '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)) + e
    
    # Cria arquivo com tamanho aleatório (0 a 10KB)
    file_path = p / nome
    file_path.write_bytes(os.urandom(random.randint(0, 10240)))
    
    # Define datas de modificação e criação aleatórias
    ts = time.mktime(random_date().timetuple())
    os.utime(file_path, (ts, ts))  # (access_time, modified_time)

print(f"{num_arquivos} arquivos criados com sucesso na pasta {root.resolve()}")