# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:07:49 2022

@author: Samaung
"""

import pandas as pd
import os



os.chdir("../LEVANTAMENTO_PATRIMONIAL")
pastas = os.listdir()

def concat_pasta(pasta):
    lista_dfs= []
    os.chdir(pasta)
    arqs = os.listdir()
    for file in arqs:
        if file.endswith("xlsx") and file != "NAO_ENCONTRADO.xlsx":
            print(file)
            df = pd.read_excel(file)
            df["Pasta"] = df.shape[0]*[pasta]
            df["Status"] = df.shape[0]*[file.replace(".xlsx","").replace("_"," ")]
            lista_dfs.append(df)
    os.chdir("..")
    return pd.concat(lista_dfs)

def concat_tudo():
    lista_concats = []
    for pasta in pastas:
        print(pasta)
        df_pasta = concat_pasta(pasta)
        lista_concats.append(df_pasta)
    os.chdir("..")
    return pd.concat(lista_concats)

def run():
    df_concats = concat_tudo()
    df_concats = df_concats.reset_index(drop=True)
    
    df_marca = pd.read_excel("PLANILHAS_GERAIS/df_marcas_datas.xlsx")
    df_n = pd.read_excel("PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx")
    
    df_concats["Ano de Incorporação"] = df_concats.shape[0]*[""]
    df_n["Ano de Incorporação"] = df_n.shape[0]*[""]
    
    for ind in range(df_concats.shape[0]):
        if df_concats["Tombamento"][ind] in list(df_marca["Tombamento"]):
            ind_marca = list(df_marca["Tombamento"]).index(df_concats["Tombamento"][ind])
            df_concats.loc[ind, "Ano de Incorporação"] = df_marca.loc[ind_marca, "Ano Incorp"]
            
    for ind in range(df_n.shape[0]):
        if df_n["Tombamento"][ind] in list(df_marca["Tombamento"]):
            print("nao_enc")
            ind_marca = list(df_marca["Tombamento"]).index(df_n["Tombamento"][ind])
            df_n.loc[ind, "Ano de Incorporação"] = df_marca.loc[ind_marca, "Ano Incorp"]
            print(df_marca.loc[ind_marca, "Ano Incorp"])
        
    df_concats.to_excel("PLANILHAS_GERAIS/Concats.xlsx")
    df_n.to_excel("PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx")
