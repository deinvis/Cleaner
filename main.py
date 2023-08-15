import os
import PIL
import pandas as pd
from PIL import Image, UnidentifiedImageError
from PIL.Image import DecompressionBombWarning

def inicializacao(): #read the settings files
    folders = pastas()
    dados = data(folders)
    return dados, folders


def clean(dados, pastas):
    totalDeletedFilesCount = 0 #total deleted files in pastas
    for pasta in pastas:
        localDeletedFilesCount = 0 #total deleted files in pasta 
        for diretorio, subpastas, arquivos in os.walk(pasta):
            if dados.values[dados.index[dados['pasta'] == pasta].tolist()[0]][1] != len(arquivos): 
                print(f"Pasta: {diretorio}\nTotal de arquivos = {len(arquivos)}")
                for arquivo in arquivos:
                    if not arquivo.__contains__('.encrypted') and not arquivo.__contains__('.part') and imageVerify(
                            arquivo):
                        try:
                            im = Image.open(diretorio + '/' + arquivo)
                            altura = im.height
                            im.close()
                            if altura < 640:
                                os.remove(diretorio + '/' + arquivo)
                                print(f"Apagando {arquivo}...")
                                localDeletedFilesCount = localDeletedFilesCount + 1
                        except UnidentifiedImageError:
                            os.remove(diretorio + '/' + arquivo)
                            print(f"UnidentifiedImageError no {arquivo}...")
                            localDeletedFilesCount = localDeletedFilesCount + 1
                        except PIL.Image.DecompressionBombError:
                            os.remove(diretorio + '/' + arquivo)
                            print(f"DecompressionBombError no {arquivo}...")
                            localDeletedFilesCount = localDeletedFilesCount + 1
                        except DecompressionBombWarning:
                            os.remove(diretorio + '/' + arquivo)
                            print(f"DecompressionBombWarning no {arquivo}...")
                            localDeletedFilesCount = localDeletedFilesCount + 1
                        except UserWarning:
                            os.remove(diretorio + '/' + arquivo)
                            print(f"UserWarning no {arquivo}...")
                            localDeletedFilesCount = localDeletedFilesCount + 1
            dados.loc[dados['pasta'] == pasta, ['total de arquivos']] = len(arquivos) - localDeletedFilesCount
            totalDeletedFilesCount = totalDeletedFilesCount + localDeletedFilesCount
    dados.to_csv("Settings/data.csv", index=False)
    return totalDeletedFilesCount


def data(pastas):
    folder = 'Settings'
    file = 'data.csv'
    path = folder + '/' + file
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        dados = pd.read_csv(path)
    except FileNotFoundError:    
        file = open(path, 'w')
        file.write('pasta,total de arquivos')
        file.close()
        dados = pd.read_csv(path)        
        print('Folder file created, set it up.')
        return []
    
    if len(pastas) != len(dados):
        for pasta in pastas:
            if pasta not in dados.values:
                dados.loc[len(dados)] = [pasta, 0]
        print("Pastas adicionadas")
        dados.to_csv(path, index=False)
    if len(dados) == 0:
        for pasta in pastas:
            dados.loc[len(dados)] = [pasta, 0]
        dados.to_csv(path, index=False)
    return dados


def pastas():
    folder = 'Settings'
    filename = 'folders.txt'
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        file = open(folder + '/' + filename, 'r')

    except FileNotFoundError:    
        file = open(folder + '/' + filename, 'w')
        print('Folder file created, set it up.')
        return []

    file.close
    return file.read().split('\n')


def imageVerify(name):
    return name.__contains__(".png") or name.__contains__(".png") or name.__contains__(".jpg") or name.__contains__(
        ".jpeg") or name.__contains__(".webp") or name.__contains__(".jfif") or name.__contains__(
        ".tiff") or name.__contains__(".bmp")

dados, pastas = inicializacao()
if len(pastas) > 0:
    print(f"Total de arquivos deletados: {clean(dados, pastas)}\n")