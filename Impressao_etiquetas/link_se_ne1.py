# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:22:47 2022

@author: Samaung
"""

import pandas as pd
import os


def run():
    os.chdir("../LEVANTAMENTO_PATRIMONIAL")
    lista_pastas = os.listdir()
    
    lev_pat1 = {}
    link_se_ne = {"Denominação": [],
                  "Tombamento do bem perdido": [],
                  "ID do bem sem etiqueta": [],
                  "Localidade do bem sem etiqueta": [],
                  "Localidade do bem perdido": []}
    
    #Dicinoario contendo todos dfs
    c = 0
    for pasta in lista_pastas:
        print(pasta)
        df_se = pd.read_excel(pasta + "/SEM_ETIQUETA.xlsx")
        df_se["ID"] = df_se.shape[0]*[""]
        for line in range(df_se.shape[0]):
            df_se["ID"][line] = c
            c = c + 1
        df_ne = pd.read_excel(pasta + "/NAO_ENCONTRADO.xlsx")
        lev_pat1[pasta] = [df_se, df_ne]
    
    #Comparação pasta por pasta
    for pasta in lev_pat1:
        print(pasta)
        for bem_se, loc_se, id_ in zip(list(lev_pat1[pasta][0]['Denominação']),
                                       list(lev_pat1[pasta][0]['Localidade']),
                                       list(lev_pat1[pasta][0]['ID'])):
            if (bem_se in list(lev_pat1[pasta][0]['Denominação'])) & (loc_se in list(lev_pat1[pasta][0]['Localidade'])) & (id_ in list(lev_pat1[pasta][0]['ID'])): 
                if bem_se in list(lev_pat1[pasta][1]['Denominação']):
                    tomb = lev_pat1[pasta][1][lev_pat1[pasta][1]['Denominação'] == bem_se].iloc[0]['Tombamento']
                    loc_perd = lev_pat1[pasta][1][lev_pat1[pasta][1]['Denominação'] == bem_se].iloc[0]['Localidade']
                    remove_ne = lev_pat1[pasta][1].loc[lev_pat1[pasta][1]["Denominação"] == bem_se]
                    lev_pat1[pasta][1] = lev_pat1[pasta][1].drop(remove_ne.index.tolist()[0])
        
                    link_se_ne['Denominação'].append(bem_se)
                    link_se_ne['Tombamento do bem perdido'].append(tomb)
                    link_se_ne['ID do bem sem etiqueta'].append(id_)
                    link_se_ne['Localidade do bem sem etiqueta'].append(loc_se)
                    link_se_ne['Localidade do bem perdido'].append(loc_perd)
        
                    remove_se = lev_pat1[pasta][0].loc[lev_pat1[pasta][0]["Denominação"] == bem_se]
                    lev_pat1[pasta][0] = lev_pat1[pasta][0].drop(remove_se.index.tolist()[0])
    
    
    #Comparação com o que restou
    df_se_total = pd.concat([lev_pat1[pasta][0] for pasta in lev_pat1])
    df_ne_total = pd.concat([lev_pat1[pasta][1] for pasta in lev_pat1])
    
    for bem_se, loc_se, id_ in zip(list(df_se_total['Denominação']),
                                   list(df_se_total['Localidade']),
                                   list(df_se_total['ID'])):
        if (bem_se in list(df_se_total['Denominação'])) & (loc_se in list(df_se_total['Localidade'])) & (id_ in list(df_se_total['ID'])):
            if bem_se in list(df_ne_total['Denominação']):
                tomb = df_ne_total[df_ne_total['Denominação'] == bem_se].iloc[0]['Tombamento']
                loc_perd = df_ne_total[df_ne_total['Denominação'] == bem_se].iloc[0]['Localidade']
                remove_ne = df_ne_total.loc[df_ne_total["Denominação"] == bem_se]
                df_ne_total = df_ne_total.drop(remove_ne.index.tolist()[0])
        
                link_se_ne['Denominação'].append(bem_se)
                link_se_ne['Tombamento do bem perdido'].append(tomb)
                link_se_ne['ID do bem sem etiqueta'].append(id_)
                link_se_ne['Localidade do bem sem etiqueta'].append(loc_se)
                link_se_ne['Localidade do bem perdido'].append(loc_perd)
        
                remove_se = df_se_total.loc[df_se_total["Denominação"] == bem_se]
                #print(remove_se['Localidade'].iloc[0])
                df_se_total = df_se_total.drop(remove_se.index.tolist()[0])
    
    
    
    os.chdir('..')
    df_link = pd.DataFrame(link_se_ne)
    df_link.to_excel('Impressao_etiquetas/df_link.xlsx')