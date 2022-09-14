''' Camada ETL:
    Abre o site https://www.idinheiro.com.br/tabelas/tabela-ipca/ de tabelas de ipca, procura a tabela
    completa de ipca de todos os anos disponíveis, converte os valores em colunas de ano, mes e perc,
    grava em arquivo parquet e faz a ingestão no bucket s3 arq-ipca-processeds3, deixando os dados 
    disponíveis para a catalogação no aws glue.
'''
import requests
import pandas as pd
from bs4 import BeautifulSoup

import fc_monta_arq_ipca as Mipca
import fc_Upload_File_geral as upds3 

def lambda_handler(event, context):
    
    # ******************** INÍCIO

    nomeBucketS3 = 'arq-ipca-processeds3'
    nomeArquivo = 'ipca'
    pathArquivo = 'arqIPCAprocessed/' #'/tmp/'

    url = 'https://www.idinheiro.com.br/tabelas/tabela-ipca/'
    req = requests.get(url)
    if req.status_code == 200:
        content = req.content
        soup = BeautifulSoup(content, 'html.parser')
        tabela = soup.find("table",{"class":"table-all__value"})
        table_str = str(tabela)
        table_str = table_str.replace(',', '.')
        df = pd.read_html(table_str)[0]

        print(df)
        print(type(req))

    else:
        print('site não encontrado == ' + url)
        exit()

    Mipca.Monta_arq_ipca(df, pathArquivo + nomeArquivo)
    upds3.UploadFile_file_ipca_processedS3(nomeBucketS3, 
                                            nomeArquivo + '.pq', 
                                            pathArquivo + nomeArquivo +  '.pq')                                           

nomeBucketS3 = 'arq-ipca-processeds3'
nomeArquivo = 'ipca'
pathArquivo = 'arqIPCAprocessed/' #'/tmp/'
  
lambda_handler(1, 1)    