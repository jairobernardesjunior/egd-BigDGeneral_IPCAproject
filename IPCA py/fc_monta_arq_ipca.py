''' Monta arquivo de IPCA:
'''

from dataclasses import replace
import pandas as pd

def Monta_arq_ipca(tabela, PathArquivo):
    qtd_linhas = tabela.shape[0] - 1
    linha_cur= 0
    i=0
    
    registro= []
    ano= []
    mes= []
    perc= []             

    while linha_cur <= qtd_linhas:

        coluna= 1
        nroMes= 1
        while coluna <= 13:
            valor= tabela.iloc[linha_cur, coluna]

            if str(valor) == '-':
                valor = 0

            valor= str(valor)
            valor= valor.replace(' ', ',')

            try:
                valor= float(valor)
            except ValueError:
                print('valor inválido = ' + str(valor))
                break

            i= i+1
            registro.append(i)
            ano.append(str(tabela.iloc[linha_cur, 0]))
            mes.append(str(nroMes))
            perc.append(str(valor)) 

            nroMes= nroMes+1
            coluna= coluna+1  

        linha_cur= linha_cur+1

    if i>0:
        df=pd.DataFrame({
                "registro":registro,
                "ano":ano,
                "mes":mes,
                "perc":perc,
                })

        print(df)

        df.to_parquet(PathArquivo + '.pq')
        df.to_string(PathArquivo + '.txt')
        return True 
        
    else:
        return False