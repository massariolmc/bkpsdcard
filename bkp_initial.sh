#!/bin/bash

#Verificar se existe o caminho do HD_EXT e do cartão de memória

origem="/media/$USER/SDCARD_64G/HD_EXT/"
destino="/media/$USER/HD_MASSA/BACKUP/Documentos/"
inicio=`date +%d%m%Y%H%M`
log="/media/$USER/HD_MASSA/BACKUP/Documentos/LOG_BACKUP_SDCARD64/"

function delete_logs() {
valor=$(ls -tr $log | wc -l)
if [ $valor -gt 7 ];then        
    arq=($(ls -t $log))
    for (( i=7; i<$valor; i++ )); do rm $log${arq[$i]}; done    
    valor2=$(ls $log | wc -l)
    total=$(($valor - $valor2))
    echo "Foram deletados os seguintes logs:"    
    echo "Total: $total"
else
    echo "Não existem arquivos a serem excluídos."
fi

sleep 3
}

function make_bkp(){

#retorna o total de pastas
total_pastas=$( ls $origem | wc -l)
#Inicia o backup
if [ $1 -eq 1 ];then
    s=$(rsync $origem -avzh --progress $destino)

elif [ $1 -eq 2 ];then
    #Não habilitar essa opção. Pode apagar dados erroneamente.
    #s=$(rsync $origem2222 -avzh --delete --progress $destino1111)
    s=0
fi

if [ $? -eq 0 ]
then
	
    final=`date +%d%m%Y%H%M`

    echo "Backup finalizado com sucesso: 
        Origem: $origem
        Destino: $destino
        Inicio: $inicio
        Final: $final
        Total de pastas: $total_pastas
        Saídas: $s
    " >> $log/$inicio.txt
    delete_logs
else
	echo "Comando não executado."
fi

echo "----------------------------------------------------"
echo "Script Finalizado."
sleep 3
}



while [ op != 0 ]; do
    

    echo "Escolha a opção desejada:"
    echo "1 - Backup padrão"
    echo "2 - Backup espelhamento"
    echo "3 - Sair"
    read op

    case "$op" in
    1)
        make_bkp 1        
        ;;

    2)
        make_bkp 2
        sleep 3
        ;;

    3)
        exit 0
        ;;

    *)
        echo "Opção Invalida. Escolha outra." 
        sleep 3   
        ;;

    esac

done



