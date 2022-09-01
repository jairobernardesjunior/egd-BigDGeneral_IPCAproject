''' CAMADA SILVER:
    LE OS ARQUIVOS de IPCA .xls baixados DO IBGE, COM ETL transforma e grava as tabelas anuais de IPCA
    em arquivos parquet e salva os mesmos no bucket s3 arq-ipca-processeds3 disponibilizando os dados
    para as ferramentas de insight.
'''
from io import BytesIO
import os
import datetime
from pickle import TRUE
import zipfile

import pandas as pd
import fc_montaCatComercioJson2 as MCatC

import requests

import fc_UploadFile_arquivosPMCprocessedS3 as uplf
import fc_Le_arquivosBucketS3 as leS3
import fc_SalvaUltimaURL as sURL   

def lambda_handler(event, context):
    # ******************** INÍCIO
    # Baixa arquivo ultimoProcessado.txt do Buckets3
    nomeBucketS3 = 'arq-ipca-processeds3'
    nomeBucketS3ultimo = 'arq-ipca-ultimos3'
    arquivoUltimoProcessado = 'ultimoProcessado.txt'
    patharquivoUltimoProcessado = 'arqIPCAultimo/ultimoProcessado.txt' #'arquivosPMCprocessed/ultimoProcessado.txt' '/tmp/ultimoProcessado.txt'
    tmpAux = 'arqIPCAultimo/' #arqIPCAultimo/' '/tmp/'  
 
    '''retornoLe = leS3.Le_arquivosBucketS3(nomeBucketS3, arquivoUltimoProcessado, patharquivoUltimoProcessado)

    if retornoLe == False:
        print('arquivo não encontrado: ' + arquivoUltimoProcessado + 
              ' no bucket ' + nomeBucketS3)
        exit()'''

    url = 'https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/Numeros_Indices/Numind_INPC_IPCA/ipca_NumindGRUPOS.zip'
    filebytes = BytesIO(requests.get(url).content)
    myzip = zipfile.ZipFile(filebytes)
    myzip.extractall(tmpAux)

    #ipcaXls = pd.read_excel(tmpAux + )


    exit()        

    # verifica se o arquivo ultimoProcessado.txt existe e, se não, cria o mesmo
    if os.path.exists(patharquivoUltimoProcessado) == False:
        arquivo = open(patharquivoUltimoProcessado,'w')
        arquivo.write("vazio")
        arquivo.close

    # lê o arquivo ultimoProcessado.txt para pegar o último arquivo .csv transformado em Json
    linha='vazio'
    arquivo = open(patharquivoUltimoProcessado,'r')
    for linha in arquivo:
        linha = linha.rstrip()
    arquivo.close()

    # verifica se o arquivo ultimoProcessado.txt tem a informação do último arquivo.csv transformado em Json
    if linha == 'vazio':
        url = 'pmc_201800_00.csv'   
    else:
        url = linha

    ultimoArquivoProcessado = ''
    seq = url[11:13]
    seq = int(seq) + 1
    seq = '%02d' % seq

    ano= url[4:8]
    anomes= url[4:10]
    mes= anomes[5:7]

    anomes = int(anomes) + 1
    mes= int(mes) + 1
    mes = '%02d' % mes

    nomeArq= 'pmc_{}_{}.csv'
    nomeArqJson= 'pmc_{}_{}.json'
    anocorrente = datetime.date.today().year
    mescorrente = datetime.date.today().month
    mescorrente = '%02d' % mescorrente
    anoMesCorrente = str(anocorrente) + str(mescorrente)

    while int(anomes) <= int(anoMesCorrente):

        print(str(anomes) + ' - ' + str(anoMesCorrente))

        while int(mes) <= 1: #12:

            print('mes ' + str(mes))

            while int(seq) <= 13: #13:

                print('seq ' + str(seq))

                # verifica se o arquivo arquivoPMCprocessed .csv existe e processa o mesmo
                retornoLe = leS3.Le_arquivosBucketS3(NomeBucketS3raw, 
                                       nomeArq.format(anomes, seq), 
                                       tmpAuxRaw + nomeArq.format(anomes, seq))  

                arquivo= tmpAuxRaw + nomeArq.format(anomes, seq)

                if retornoLe == True:
                    tabela= pd.read_csv(arquivo)

                    if (tabela.iloc[5, 0] == 'Brasil ') or (tabela.iloc[5, 0] == 'Brasil'):
                        nomeArquivoJson= 'PercUF_' + nomeArqJson.format(anomes, seq)[:13]
                        PathArquivoJson= ('arquivosPMCprocessed/PercUF_' + 
                                            nomeArq.format(anomes, seq)[:13])
                        retorno= MUF.Monta_UF_Json(tabela, ano, mes, PathArquivoJson)

                        if retorno == True:
                            uplf.UploadFile_arquivosPMCprocessedS3(
                                            NomeBucketS3processedUF, 
                                            nomeArquivoJson + '.pq', 
                                            PathArquivoJson + '.pq')
                            ultimoArquivoProcessado = nomeArq.format(anomes, seq)                        
                    else:
                        nomeArquivoJson= 'PercCAT_COMERCIO_' + nomeArqJson.format(anomes, seq)[:13]
                        PathArquivoJson= ('arquivosPMCprocessed/PercCAT_COMERCIO_' + 
                                            nomeArq.format(anomes, seq)[:13])                    
                        retorno= MCatC.Monta_CatComercio_Json(tabela, ano, mes, PathArquivoJson)

                        if retorno == True:
                            uplf.UploadFile_arquivosPMCprocessedS3(
                                            NomeBucketS3processedCatCom, 
                                            nomeArquivoJson + '.pq', 
                                            PathArquivoJson + '.pq')
                            ultimoArquivoProcessado = nomeArq.format(anomes, seq)
         
                seq = int(seq) + 1
                seq = '%02d' % seq

            seq= '01'
            mes= int(mes) + 1
            mes = '%02d' % mes
            anomes = int(anomes) + 1

        mes= '01'
        ano= int(ano) + 1
        anomes= str(ano) + str(mes)
        
    if len(ultimoArquivoProcessado) > 0: # grava a posição do último arquivo pmc.csv Processado
        sURL.SalvaUltimaURL(patharquivoUltimoProcessado, ultimoArquivoProcessado)
        uplf.UploadFile_arquivosPMCprocessedS3(NomeBucketS3raw, arquivoUltimoProcessado, patharquivoUltimoProcessado) 

    nomeBucketS3 = 'arq-ipca-processeds3'
    nomeBucketS3ultimo = 'arq-ipca-ultimos3'
    arquivoUltimoProcessado = 'ultimoProcessado.txt'
    patharquivoUltimoProcessado = 'arqIPCAultimo/ultimoProcessado.txt' #'arquivosPMCprocessed/ultimoProcessado.txt' '/tmp/ultimoProcessado.txt'
    tmpAux = 'arqIPCAultimo/' #arqIPCAultimo/' '/tmp/'  
  
lambda_handler(1, 1)    