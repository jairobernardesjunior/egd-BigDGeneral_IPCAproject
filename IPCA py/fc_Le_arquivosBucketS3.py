import boto3
import botocore

def Le_arquivosBucketS3(NomeBucketS3, arquivoUltimoProcessado, patharquivoUltimoProcessado):
    client = boto3.client(
        service_name='s3',
        aws_access_key_id='xxxxxxxxxxxxxxxxxxxxx',
        aws_secret_access_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        region_name='eu-west-1' # voce pode usar qualquer regiao
        )    

    retorno = False

    try:
        client.download_file(NomeBucketS3, arquivoUltimoProcessado, patharquivoUltimoProcessado)
        retorno = True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            retorno = False

    return retorno