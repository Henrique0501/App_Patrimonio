# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 12:46:05 2022

@author: Samaung
"""

import pandas as pd

df_enc = pd.read_excel("Concats - NOVOS_NOMES.xlsx")
df_n = pd.read_excel("NAO_ENCONTRADO_GERAL - NOVOS_NOMES.xlsx")

df = pd.concat([df_enc, df_n])

bens = list(df["Denominação"].unique())

df = pd.DataFrame({"Denominação": bens, "Tipo": len(bens)*[""]})

df = df.sort_values("Denominação")

df.to_excel("Planilha_de_tipos_de_bens.xlsx")