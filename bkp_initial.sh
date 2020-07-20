#!/bin/bash

origem="/media/massariol/sdcard64/HD_EXT/"
destino="/media/massariol/HD_MASSA/BACKUP/Documentos/"
inicio=`date +%d%m%y%H%M`
log="/var/log/backups/sdcard/%d%m%y%H%M"

#retorna o total de pastas
total_pastas=$( ls $origem | wc -l)
#Inicia o backup
rsync $path_sdcard -avzh --progress $path_hdext

if [ $? == 0 ]
then
	
final=`date +%d%m%y%H%M`

echo "Backup finalizado com sucesso: 
    Origem: $origem
    Destino: $destino
    Inicio: $inicio
    Final: $final
" >> $log

else
	echo "Comando não executado."
fi

