# dvIPCAproject
O projeto dvIPCA tem como objetivo baixar mensalmente a tabela de IPCA do site do IBGE do endereço https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/Numeros_Indices/Numind_INPC_IPCA/ipca_NumindGRUPOS.zip, extrair os dados das tabelas anuais de ipca,
transformar em tabelas separadas e gravar cada uma em um arquivos parquet, fazer a ingestão em um bucket s3 na AWS para posterior catalogação desses arquivos parquet através do AWS Glue Data Catalog, sendo os dados posteriormente liberados para os Data Analysts e Data Scientysts que usarão ferramentas de insights para geração de apresentações gráficas para a empresa.
