# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:23:13 2022

@author: Samaung
"""

import pandas as pd

def apenas_numeros(x):
        if x.isnumeric()==True:
            return True
        else:
            return False

def filtrar_numeros(x):
    return "".join(filter(apenas_numeros, x)).strip()

def subs(lista, v1, v2):
    for i in lista:
        if i==v1:
            lista[lista.index(i)]=v2
    return lista


DF_n_encontrado = pd.read_csv("relatorio_bens.csv", encoding = "utf-8", sep = ";")
#DF_n_encontrado = DF_n_encontrado.drop(columns = ["Unnamed: 25"])

DF_n_encontrado["Tombamento"] = [str(list(DF_n_encontrado["Tombamento"])[i]) for i in range(len(list(DF_n_encontrado["Tombamento"])))]

for i in range(len(DF_n_encontrado["Tombamento"])):
    DF_n_encontrado["Tombamento"][i] = filtrar_numeros(DF_n_encontrado["Tombamento"][i])
    
df_enc = pd.read_excel("Concats.xlsx")

for tomb in list(df_enc["Tombamento"]):
    tomb = str(tomb)
    if tomb in list(DF_n_encontrado["Tombamento"]):
        ind = list(DF_n_encontrado["Tombamento"]).index(tomb)
        DF_n_encontrado = DF_n_encontrado.drop(ind, axis = 0)
        DF_n_encontrado = DF_n_encontrado.reset_index(drop = True)
        
DF_n_encontrado = DF_n_encontrado.fillna("")
DF_n_encontrado["Localidade"] = subs(list(DF_n_encontrado["Localidade"]), "", "Não informado")

DF_n_encontrado.to_excel("NAO_ENCONTRADO_GERAL.xlsx")