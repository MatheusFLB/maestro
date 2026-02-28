import os
import shutil
from pathlib import Path
from datetime import datetime

# Função para solicitar o diretório ao usuário
def get_directory_from_user():
    root_dir = input("Digite o diretório onde os arquivos estão localizados: ").strip()
    # Verificar se o diretório existe
    if not os.path.isdir(root_dir):
        print("O diretório informado não existe. Verifique e tente novamente.")
        exit(1)
    return root_dir
root_dir = get_directory_from_user()

# Extensões de imagem que queremos organizar
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']

# Mapeamento de extensões para pastas específicas
EXTENSION_TO_FOLDER = {
    '.txt': 'Textos',
    '.pdf': 'PDFs',
    '.doc': 'Documentos',
    '.docx': 'Documentos',
    '.xlsx': 'Planilhas',
    '.csv': 'Planilhas',
    '.zip': 'Arquivos Compactados',
    '.rar': 'Arquivos Compactados',
    # Adicione mais extensões conforme necessário
}

# Função para criar a pasta, se não existir
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Função para renomear arquivos em sequência
def get_new_image_name(index):
    return f"imagem_{index:04d}.png"  # 4 dígitos com padding, exemplo: imagem_0001.png

# Função principal para organizar os arquivos
def organize_files(root_directory):
    # Diretório onde todos os arquivos organizados serão colocados
    organized_root = os.path.join(root_directory, "☼☼☼")
    create_folder_if_not_exists(organized_root)

    # Diretório onde as imagens serão armazenadas
    images_folder = os.path.join(organized_root, 'Imagens')
    create_folder_if_not_exists(images_folder)

    # Dicionário para contar arquivos organizados por tipo
    file_counters = {ext: 0 for ext in EXTENSION_TO_FOLDER.keys()}
    images_info = []

    # Varredura de todos os arquivos a partir do diretório raiz
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Ignorar a pasta "☼☼☼" para evitar loop infinito
        if "☼☼☼" in dirpath:
            continue

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_extension = Path(filename).suffix.lower()

            # Verificar se é uma imagem
            if file_extension in IMAGE_EXTENSIONS:
                # Obter a data de modificação da imagem e armazenar para ordenação posterior
                mod_time = os.path.getmtime(file_path)
                images_info.append((file_path, mod_time))

            # Verificar se a extensão do arquivo está no mapeamento
            elif file_extension in EXTENSION_TO_FOLDER:
                folder_name = EXTENSION_TO_FOLDER[file_extension]
                destination_folder = os.path.join(organized_root, folder_name)
                create_folder_if_not_exists(destination_folder)

                # Copiar o arquivo para a pasta correta
                destination_path = os.path.join(destination_folder, filename)
                shutil.copy2(file_path, destination_path)
                file_counters[file_extension] += 1

    # Ordenar as imagens por data de modificação (do mais recente para o mais antigo)
    images_info.sort(key=lambda x: x[1], reverse=True)

    # Renomear as imagens de acordo com a ordem de modificação
    image_counter = 1
    for image_path, _ in images_info:
        new_file_name = get_new_image_name(image_counter)
        new_file_path = os.path.join(images_folder, new_file_name)
        shutil.copy2(image_path, new_file_path)
        image_counter += 1

    # Imprimir um resumo da organização
    print(f"Organização concluída. {image_counter-1} imagens organizadas.")
    for ext, count in file_counters.items():
        if count > 0:
            print(f"{count} arquivos de {ext} organizados.")

# Executar a organização
organize_files(root_dir)
