def SalvaUltimaURL(patharquivoUltimoProcessado, ultimaURL):
    arquivo = open(patharquivoUltimoProcessado,'w')
    arquivo.write(ultimaURL)
    arquivo.close  