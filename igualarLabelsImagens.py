import os
import shutil

def process_images(image_dir, label_dir, output_dir):
    """
    Lista as imagens em um diretório, encontra os arquivos de label correspondentes
    e move ambos para um diretório de saída.

    Args:
        image_dir (str): Caminho para o diretório contendo as imagens.
        label_dir (str): Caminho para o diretório contendo os arquivos de label.
        output_dir (str): Caminho para o diretório onde as imagens e labels serão movidos.
    """

    # Cria o diretório de saída se ele não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lista todos os arquivos no diretório de imagens
    for filename in os.listdir(image_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Filtra por extensões de imagem
            image_name, image_ext = os.path.splitext(filename) # Separa nome do arquivo da extensão
            label_filename = image_name + '.txt'  # Assume que os labels são arquivos .txt

            label_path = os.path.join(label_dir, label_filename)
            image_path = os.path.join(image_dir, filename)

            # Verifica se o arquivo de label correspondente existe
            if os.path.exists(label_path):
                # Move a imagem e o label para o diretório de saída
                shutil.move(image_path, os.path.join(output_dir, filename))
                shutil.move(label_path, os.path.join(output_dir, label_filename))
                print(f"Movido: {filename} e {label_filename} para {output_dir}")
            else:
                print(f"Arquivo de label não encontrado para: {filename}")

# Exemplo de uso:

current_directory = os.getcwd()

image_directory = current_directory + "/Fase_V/imagens/valid/images"  # Substitua pelo caminho do seu diretório de imagens
label_directory = current_directory + "/Fase_V/imagens/valid/labels"  # Substitua pelo caminho do seu diretório de labels
output_directory = current_directory + "/Fase_V/imagens/valid/consolidado"  # Substitua pelo caminho do diretório de saída

process_images(image_directory, label_directory, output_directory)
