#coding:utf-8

import os
import sys
import shutil
import json
from subprocess import Popen, PIPE
from time import perf_counter as timer
from datetime import datetime

class AutoBkpSd():
    def __init__(self, origin, destiny):
        self.path_origin = origin
        self.path_destiny = destiny    
        self.is_path(self.path_origin)
        self.is_path(self.path_destiny)  

    def is_path(self, path):
        if not os.path.exists(path):
            print("{} - Este caminho não existe. Verifique.".format(path))        
            sys.exit()
    
    def read_config_bkp(self):
        path = os.path.join(self.path_origin,'APPS/bkpsdcard/config_bkp.json')
        self.is_path(path)
        arq = dict()
        try:
            with open(path, 'r') as json_file:    
                arq = json.load(json_file)        
        except Exception as e:
            print("Erro no carregamento do arquivo JSON.")                
            print("Saída do erro",e.args)
        return arq
    
    def send_bkp(self,folders,rel,opt=False):        
        rel['bkp'].append(f"------INICIO DO BACKUP: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ------\n")                            
        start = timer()
        for i in folders:            
            if os.path.exists(os.path.join(self.path_origin,i)):
                folder_or_file = os.path.join(self.path_origin,i)
                print(f"Iniciando {folder_or_file}---")
                print(f"Em andamento backup: {folder_or_file}", end=" ")
                rel['bkp'].append(f"{'Pasta:' if os.path.isdir(folder_or_file) else 'Arquivo:'} {i} - Inicio {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {self.execute(folder_or_file, mirror=opt)}" )                
                print(f"---Finalizado")
            else:
                rel['not_exists'].append(os.path.join(self.path_origin,i))        
        end = timer()
        rel['bkp'].append(f"------TERMINO DO BACKUP: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ------ \n\n")                            
        rel['bkp'].append(f"------TEMPO TOTAL DO BACKUP EM SEGUNDOS: {end - start} ------")
        return rel
    
    def relatory(self, rel):
        file_name = f"log_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.txt"
        folder_log = "BKP_LOGS"
        path = os.path.join(self.path_origin,folder_log,file_name)
        aux = ""       
        for k,v in rel.items():
            if k == "not_exists":
                aux += f"Pastas que não existem: \n"
                for name in v:
                    aux += f"{name}"

            elif k == "bkp":
                aux += f"\n\nO backup foi realizado nos seguintes arquivos e pastas: \n"
                for name in v:
                    aux += f"{name}\n"                            
        with open(path,'w') as file:
            file.write(aux)
        self.verify_folder_log()# Mantem apenas os ultimos 7 backups mais atuais
    
    def verify_folder_log(self):
        #quantidade de arquivos de logs na pasta
        num_logs = 7

        folder_log = "BKP_LOGS"
        path = os.path.join(self.path_origin,folder_log)
        qtde = len(os.listdir(path))        
        sorted_date_files = []
        if qtde > num_logs:
            for old in os.listdir(path):
                if os.path.isfile(os.path.join(path,old)):
                    sorted_date_files.append((old,os.stat(os.path.join(path,old)).st_mtime))                    
            sorted_date_files = sorted(sorted_date_files, key=lambda order: order[1])      
            for i in range(0,int(qtde - num_logs)):                
                os.remove(os.path.join(path,sorted_date_files[i][0]))

    def verify_options(self):
        rel = {
            'not_exists': [],
            'bkp': []
        }
        #Lê os arquivo de configuração
        arq = self.read_config_bkp()  
        # Laço que envia as pastas para o backup       
        for key,value in arq.items():   
            if key == 'mirror_folders_or_files':#Estas pastas fazem o incremento e espelhamento
                rel = self.send_bkp(value,rel,opt=True)
            elif key == 'not_mirror_folders_or_files':#Estas pastas fazem o incremento
                rel = self.send_bkp(value,rel,opt=False)        
        #print(rel)
        self.relatory(rel)
   
    def execute(self,path,mirror=False):
        with open('/tmp/teste.txt','w') as f:
            if mirror:            
                exec = Popen(["rsync","-avzh","--progress","--delete","{}".format(path), "{}".format(self.path_destiny)],stdout=f)
            else:
                exec = Popen(["rsync","-avzh","--progress","{}".format(path), "{}".format(self.path_destiny)],stdout=f)        
            while exec.poll() == None:
                pass               
            #return exec.communicate(timeout=15)[0].decode('UTF-8')
            #return exec.communicate(timeout=15)[0]
        
        with open('/tmp/teste.txt','r') as f_aux:
            return f_aux.read()

origin = '/home/massariol/Documentos/HD_EXT/'
destiny = '/media/massariol/HD_MASSA/BACKUP/Documentos/'
exe = AutoBkpSd(origin, destiny)
exe.verify_options()
