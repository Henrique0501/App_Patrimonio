# -*- coding: utf-8 -*-
"""
Created on Tue May 10 13:47:45 2022

@author: Samaung
"""

import tkinter as tk
import pandas as pd
import os
from Folha_etiquetas1 import Folha, doc
from tkinter import ttk
from tkinter.messagebox import askyesno
import tkinter.filedialog
import numpy as np
import link_se_ne1
import sys

sys.path.insert(0, '../PLANILHAS_GERAIS')
import Concatenar_dfs
Concatenar_dfs.run()

os.chdir('Impressao_etiquetas')
link_se_ne1.run()
#Dados


df_n = pd.read_excel('PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx')
os.chdir('Impressao_etiquetas')
print(os.listdir())
root = tk.Tk()
filename = None
def pegar_dir():
    if var_se.get() == 1 or var_imp.get() == 1:
        global filename
        filename = tk.filedialog.askdirectory()
        locais = list(pd.read_excel(filename + '/SEM_ETIQUETA.xlsx')['Localidade'])
        lista = list(np.unique(locais))
        print(lista)
        list_dfs = [pd.read_excel(filename + '/' + file) for file in ['OK.xlsx', 'ATUALIZAR.xlsx', 'SEM_REGISTRO.xlsx']]
        df_entrada = pd.concat([df.fillna('') for df in list_dfs])
        df_imp = df_entrada.loc[df_entrada["Obs."].str.contains("Imprimir nova etiqueta"), ["Tombamento", "Denominação", "Localidade"]].reset_index(drop = True)
        df_imp["Situação"] = df_imp.shape[0]*['Imprimir nova etiqueta']
        df_link = pd.read_excel("df_link.xlsx")
        lista_df_se = [df_link[df_link["Localidade do bem sem etiqueta"].str.contains(loc)] for loc in lista]
        if var_se.get() == 0:
            df = df_imp
        elif var_imp.get() == 0:
            df_se = pd.concat(lista_df_se).loc[:,
                    ["Tombamento do bem perdido", "Denominação", "Localidade do bem sem etiqueta"]].reset_index(
                drop=True)
            df_se.rename(
                columns={"Tombamento do bem perdido": "Tombamento", "Localidade do bem sem etiqueta": "Localidade"},
                inplace=True)
            df_se["Situação"] = df_se.shape[0] * ['Link']
            df = df_se
        else:
            df_se = pd.concat(lista_df_se).loc[:,
                    ["Tombamento do bem perdido", "Denominação", "Localidade do bem sem etiqueta"]].reset_index(
                drop=True)
            df_se.rename(
                columns={"Tombamento do bem perdido": "Tombamento", "Localidade do bem sem etiqueta": "Localidade"},
                inplace=True)
            df_se["Situação"] = df_se.shape[0] * ['Link']
            df = pd.concat([df_imp, df_se])
        df.to_excel('Filtro.xlsx')
        tk.Label(aba_home, text = filename.rsplit('/')[-1]).grid(row = 7, column=0, columnspan = 2)
    else:
        tk.messagebox.showerror(title = 'Erro: Nada para imprimir', message = 'Selecione uma das opções de impressão.')


def editar():
    tk.messagebox.showinfo(title= 'Um arquivo excel será aberto.', message = 'Um arquivo excel com as informações das etiquetas de impressão será aberto. Você pode editá-lo e salvá-lo para imprimir conforme sua necessidade.')
    os.startfile('Filtro.xlsx')
    
def imprimir():
    df = pd.read_excel('Filtro.xlsx')
    atualizar = askyesno("Atualizar arquivos?", message= "Deseja que os arquivos associados sejam atualizados?\nCaso você opte por 'Sim', os tombamentos impressos que estavam perdidos serão alterados para o status de encontrado.")
    if atualizar==True:
        if 'Link' in list(df['Situação']):
            print('oi')
            lista_tombs_link = list(df[df['Situação']=='Link']['Tombamento'])
            lista_locs_link = list(df[df['Situação']=='Link']['Localidade'])
            lista_denom_link = list(df[df['Situação']=='Link']['Denominação'])
            global df_n
            df_add = df_n[df_n['Tombamento'].isin(lista_tombs_link)== True]
            df_n = df_n[df_n['Tombamento'].isin(lista_tombs_link) == False]
            print(lista_tombs_link)
            print(list(df_add["Tombamento"]))
            for tomb, local in zip(lista_tombs_link, lista_locs_link):
                df_add.loc[df_add['Tombamento']==tomb, 'Localidade'] = local
            df_at = pd.read_excel(f'{filename}/ATUALIZAR.xlsx')
            df_at = pd.concat([df_at, df_add])
            df_at.to_excel(f'{filename}/ATUALIZAR.xlsx')
            df_n.to_excel('../PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx')
            df_se = pd.read_excel(f'{filename}/SEM_ETIQUETA.xlsx')
            for denom, local in zip(lista_denom_link, lista_locs_link):
               ind = df_se[(df_se['Denominação']==denom) & (df_se['Localidade']==local)].index.tolist()
               df_se = df_se.drop(ind[0], axis = 0)
            df_se.to_excel(f'{filename}/SEM_ETIQUETA.xlsx')
        
        if 'Imprimir nova etiqueta' in list(df['Situação']):
            print('olá')
            lista_tombs_imp = list(df[df['Situação']=='Imprimir nova etiqueta']['Tombamento'])
            dfs = [pd.read_excel(filename + '/' + file) for file in ['ATUALIZAR.xlsx', 'OK.xlsx', 'SEM_REGISTRO.xlsx', 'DAR_BAIXA.xlsx']]
            for tomb in lista_tombs_imp:
                for df_ in dfs:
                    # print(df.loc[df['Tombamento']==tomb, 'Obs.'])
                    df_.loc[df_['Tombamento']==tomb, 'Obs.'] = df_.loc[df_['Tombamento']==tomb, 'Obs.'].replace('Imprimir nova etiqueta', 'Nova etiqueta colocada',regex=True)
            dfs[0].to_excel(filename + '/ATUALIZAR.xlsx')
            dfs[1].to_excel(filename + '/OK.xlsx')
            dfs[2].to_excel(filename + '/SEM_REGISTRO.xlsx')
            dfs[3].to_excel(filename + '/DAR_BAIXA.xlsx')

    A4251 = Folha(11.57, 4.5, 0, 2.5, 21.2, 38.2, 5, 13)
    A4251.dividir()
    A4251.carimbar_tudo(df, '{0},{1}'.format(spin_row.get(), spin_col.get()))
    doc.showPage()
    doc.save()
    os.startfile('Folha_etiquetas.pdf')
    root.destroy()
    quit()

#Variáveis    
var_se = tk.IntVar()
var_imp = tk.IntVar()

#Layout
Notebook = ttk.Notebook(root)
Notebook.pack()
aba_home = ttk.Frame(Notebook)
aba_editar = ttk.Frame(Notebook)
aba_imprimir = ttk.Frame(Notebook)
Notebook.add(aba_home, text = "Home")
Notebook.add(aba_editar, text = "Editar")
Notebook.add(aba_imprimir, text = "Imprimir")

tk.Label(aba_home, text = 'O que você quer imprimir?', font = 'Helvetica 16 bold').grid(row = 0, column = 0, columnspan = 2)

check_se = tk.Checkbutton(aba_home, text = 'Arquivo SEM_ETIQUETA.xlsx', variable = var_se)
check_se.grid(row = 1, column = 0, columnspan = 2)

check_imp = tk.Checkbutton(aba_home, text = 'Todos marcados com "Imprimir nova etiqueta"', variable = var_imp)
check_imp.grid(row = 2, column = 0, columnspan = 2)

tk.Label(aba_home, text = 'De onde começar a imprimir?', font = 'Helvetica 12 bold').grid(row = 3, column = 0, columnspan = 2)


tk.Label(aba_home, text = 'Linha').grid(row = 4, column = 0)
spin_row = tk.Spinbox(aba_home, from_ = 1, to = 13, width = 5)
spin_row.grid(row = 4, column = 1)

tk.Label(aba_home, text = 'Coluna').grid(row = 5, column = 0)
spin_col = tk.Spinbox(aba_home, from_ = 1, to = 5, width = 5)
spin_col.grid(row = 5, column = 1)

bt_dir = tk.Button(aba_home, text = 'Escolher pasta', command=pegar_dir)
bt_dir.grid(row = 6, column = 0, columnspan = 2)

bt_editar = tk.Button(aba_editar, text = "Editar impressão", command = editar)
bt_editar.pack(pady = 70)

bt_imprimir = tk.Button(aba_imprimir, text = 'Imprimir', command = imprimir)
bt_imprimir.pack(pady = 70)


root.mainloop()

