#coding:utf-8

import os
import shutil
from subprocess import Popen, PIPE
import shlex

path_origin = '/home/massariol/Documentos/HD_EXT/IPTV'
path_destiny = '/home/massariol/Imagens/BACKUP/'

def is_path(path):
    print(os.path.exists(path))
    return os.path.exists(path)

def walks_folders(path):
    for folder_current, subfolder, filename in os.walk(path):
        print("Pasta atual: {}".format(folder_current))
        
        for sb in subfolder:
            print("As subpastas: {}".format(sb))

        for file in filename:
            print("Nomes dos arquivos: {}".format(file))

if is_path(path_origin):
    walks_folders(path_origin)
else:
    print("O path origem não é válido")

if is_path(path_origin):
    walks_folders(path_destiny)
else:
    print("O path destino não é válido")


exec = Popen(["rsync","-avzh","--progress","{}".format(path_origin), "{}".format(path_destiny)])
#exec = s.Popen([cmd])
print("Aguradando.....")
while exec.poll() == None:
    pass
print("Finalizado")
