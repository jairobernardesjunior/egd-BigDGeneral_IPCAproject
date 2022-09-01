
import boto3

def UploadFile_arquivosPMCprocessedS3(NomeBucketS3, nomeArquivo, pathArquivo):
    client = boto3.client(
        service_name='s3',
        aws_access_key_id='xxxxxxxxxxxxxxxxxxxxxxxxxxx',
        aws_secret_access_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        region_name='eu-west-1' # voce pode usar qualquer regiao
        ) 

    client.upload_file(pathArquivo, NomeBucketS3, nomeArquivo)        