# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:55:42 2022

@author: Samaung
"""

import pandas as pd
import os

df_locais = pd.read_excel("Locais_geral.xlsx").fillna("")


def cod(ind):
    if df_locais.loc[ind, "Código"] == "":
        return "Código a determinar"
    else:
        return df_locais.loc[ind, "Código"]


def loc_maior(ind):
    if df_locais.loc[ind, "Local maior"] == "":
        return " "
    else:
        return df_locais.loc[ind, "Local maior"]


def denom(ind):
    if df_locais.loc[ind, "Denominação"] == "":
        return ""
    else:
        return " (" + df_locais.loc[ind, "Denominação"] + ")"


def endr(ind):
    if df_locais.loc[ind, "Endereço"] == "":
        return "Endereço não informado"
    else:
        return df_locais.loc[ind, "Endereço"]


def run1():
    global df_locais
    for ind in range(df_locais.shape[0]):
        df_locais["Novo nome completo"][ind] = cod(ind) + " - " + loc_maior(ind) + denom(ind) + " - " + endr(ind)
        df_locais["Novo nome"][ind] = loc_maior(ind) + denom(ind) + " - " + endr(ind)

    df_criados = df_locais[df_locais["Código"]!=""]
    df_antigos = df_locais[df_locais["Código"].str.contains("11010116_")]

    df_criados = df_criados.sort_values(["Local maior", "Denominação"])
    df_antigos = df_antigos.sort_values(["Local maior", "Denominação"])
    df_locais = df_locais.sort_values(["Local maior", "Denominação"]).reset_index(drop = True)

    df_criados.to_excel("Locais_criados.xlsx")
    df_antigos.to_excel("Locais_antigos.xlsx")
    df_locais.to_excel("Locais_geral.xlsx")


def novo_nome(loc): # Trocar nomes locais
    if loc not in list(df_locais["Novo nome"]):
        ind = list(df_locais["Nome Completo"]).index(loc)
        return df_locais.loc[ind, "Novo nome"]
    else:
        return loc


def run2():
    df_enc = pd.read_excel("../PLANILHAS_GERAIS/Concats.xlsx")
    df_n = pd.read_excel("../PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx")
    df_pai = pd.read_excel("../PLANILHAS_GERAIS/novo_relatorio_bens.xlsx")

    df_enc["Localidade"] = [novo_nome(loc) for loc in list(df_enc["Localidade"])]
    df_n["Localidade"] = [novo_nome(loc) for loc in list(df_n["Localidade"])]
    df_pai["Localidade"] = [novo_nome(loc) for loc in list(df_pai["Localidade"])]


    df_enc.to_excel("../PLANILHAS_GERAIS/Concats - NOVOS_NOMES.xlsx")
    df_n.to_excel("../PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL - NOVOS_NOMES.xlsx")
    df_pai.to_excel("../PLANILHAS_GERAIS/novo_relatorio_bens - NOVOS_NOMES.xlsx")


