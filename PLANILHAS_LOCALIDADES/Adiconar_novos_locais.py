# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:52:31 2022

@author: Samaung
"""

#esse arquivo alteral o arquivo Locais_geral-agora para você colocar os novos novos locais na nova nomenclatura

import pandas as pd

df_locs = pd.read_excel("Locais_geral.xlsx")
df_enc = pd.read_excel("../PLANILHAS_GERAIS/Concats.xlsx")

locais_enc = list(df_enc["Localidade"].unique())
locs = list(df_locs["Nome Completo"])
novos_locs = []

for loc in locais_enc:
    if loc not in locs and loc != "":
        print(loc)
        novos_locs.append(loc)
        
df = pd.concat([df_locs, pd.DataFrame({"Nome Completo": novos_locs})])        
df.to_excel("Locais_geral.xlsx")