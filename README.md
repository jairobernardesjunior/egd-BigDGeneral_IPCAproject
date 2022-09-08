# bigDGeneralIPCAproject
    Abre o site https://www.idinheiro.com.br/tabelas/tabela-ipca/ de tabelas de ipca, procura a tabela
    completa de ipca de todos os anos disponíveis, converte os valores em colunas de ano, mes e perc,
    grava em arquivo parquet e faz a ingestão no bucket s3 arq-ipca-processeds3, deixando os dados 
    disponíveis serem catalogados posteriormente pelo Glue e disponibilizados para serem acessados pelo quicksight através do athena, dentro da aws cloud.