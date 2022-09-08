
import boto3

def UploadFile_file_ipca_processedS3(NomeBucketS3, nomeArquivo, pathArquivo):
    client = boto3.client(
        service_name='s3',
        aws_access_key_id='xxxxxxxxxxxxxxxxxxxxxxxxx',
        aws_secret_access_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        region_name='eu-west-1' # voce pode usar qualquer regiao
        ) 

    client.upload_file(pathArquivo, NomeBucketS3, nomeArquivo)        