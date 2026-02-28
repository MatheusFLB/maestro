import os
import random
import pathlib

# Pasta raiz do HD simulado
root = pathlib.Path('HD_SIMULADO')

# Categorias e extensões
exts = ['jpg','png','mp4','mp3','pdf','docx','xlsx','txt','zip','']
pastas = ['Downloads','Documentos','Fotos','Videos','Musicas','Backup','Projetos','Coisas_Aleatorias']
nomes = ['relatorio','foto','video','arquivo','backup','nota','print','planilha']

# Criar arquivos aleatórios
for _ in range(50):  # quantidade pequena, ajustável
    p = root / random.choice(pastas) / ('Sub_' + str(random.randint(1,3)))
    p.mkdir(parents=True, exist_ok=True)
    e = random.choice(exts)
    nome = random.choice(nomes) + '_' + str(random.randint(1,50)) + (('.'+e) if e else '')
    (p / nome).write_bytes(os.urandom(random.randint(0,1024)))

print('HD simulado criado com sucesso.')