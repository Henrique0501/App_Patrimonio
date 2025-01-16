# -*- coding: utf-8 -*-

import plotly.express as px
import jupyter_dash as jd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import callback, dash_table, callback_context, MATCH, State, no_update, Dash
import plotly.express as px
import pandas as pd
import dash
import winsound
from dash.exceptions import PreventUpdate
import gtts
#from playsound import playsound
import os
import numpy as np
import plotly.graph_objects as go
import sys

sys.path.insert(0, '../PLANILHAS_GERAIS')
import Concatenar_dfs
Concatenar_dfs.run()

os.chdir('PLANILHAS_LOCALIDADES')

sys.path.insert(0, '../PLANILHAS_LOCALIDADES')
import atualizar_nomes_locais as at
print('atualizando nomes dos locais...')
at.run1()
at.run2()
print('os nomes dos locais foram atualizados')

os.chdir('..')
os.chdir('Dashboard')

#Funções Auxiliares
def interval(ano):
    if ano != "":
        if 1970 <= ano <= 1979:
            return "1970 - 1979"
        elif 1980 <= ano <= 1989:
            return "1980 - 1989"
        elif 1990 <= ano <= 1999:
            return "1990 - 1999"
        elif 2000 <= ano <= 2009:
            return "2000 - 2009"
        elif 2010 <= ano <= 2019:
            return "2010 - 2019"
        elif 2020 <= ano <= 2022:
            return "2020 - 2022"
    else:
        return "NAO INFORMADO"
    
def tipo_loc(loc):
    ind = list(df_locais["Novo nome"]).index(loc)
    return df_locais.loc[ind, "Tipo"]

def tipo_bem(bem):
    ind = list(df_bens["Denominação"]).index(bem)
    return df_bens.loc[ind, "Tipo"]

def encontrado_ou_n(status):
    if status == "NAO ENCONTRADO":
        return "NAO ENCONTRADO"
    elif status == "OK" or status == "ATUALIZAR":
        return "ENCONTRADO"
    elif status == "OK" or status == "DAR BAIXA":
        return "BAIXA"        
    else:
        return "ADICIONADO"
    
    
#Dados
df_locais = pd.read_excel("../PLANILHAS_LOCALIDADES/Locais_geral.xlsx")
df_bens = pd.read_excel("../PLANILHAS_GERAIS/Bens_IF.xlsx")

df_pai = pd.read_excel("../PLANILHAS_GERAIS/novo_relatorio_bens - NOVOS_NOMES.xlsx")
df_pai["Tipo do local"] = [tipo_loc(loc) for loc in list(df_pai["Localidade"])]
df_pai["Tipo do bem"] = [tipo_bem(bem) for bem in list(df_pai["Denominação"])]


df_enc = pd.read_excel("../PLANILHAS_GERAIS/Concats - NOVOS_NOMES.xlsx").fillna("")
df_enc["Tipo do local"] = [tipo_loc(loc) for loc in list(df_enc["Localidade"])]
df_enc["Tipo do bem"] = [tipo_bem(bem) for bem in list(df_enc["Denominação"])]
#df_enc["Intervalo"] = [interval(data) for data in list(df_enc["Ano de Incorporação"])]

df_n = pd.read_excel("../PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL - NOVOS_NOMES.xlsx")
df_n["Status"] = df_n.shape[0]*["NAO ENCONTRADO"]
df_n["Tipo do local"] = [tipo_loc(loc) for loc in list(df_n["Localidade"])]
df_n["Tipo do bem"] = [tipo_bem(bem) for bem in list(df_n["Denominação"])]
#df_n = df_n.fillna("")
#df_n["Intervalo"] = [interval(data) for data in list(df_n["Ano de Incorporação"])]

df_tudo = pd.concat([df_enc,df_n])
df_tudo = df_tudo.fillna("")
df_tudo["Encontrado"] = [encontrado_ou_n(status) for status in list(df_tudo["Status"])]
df_tudo["Intervalo"] = [interval(data) for data in list(df_tudo["Ano de Incorporação"])]
df_tudo = df_tudo.fillna("")
# df_n_enc= df_tudo[df_tudo["Encontrado"]=="NAO ENCONTRADO"]
# interessse = df_n_enc[df_n_enc["Intervalo"]!="NAO INFORMADO"]

anos = list(df_n.sort_values("Ano de Incorporação")['Ano de Incorporação'].unique())
anos = [x for x in anos if np.isnan(x) == False]

#Informações sobre detentores
#Status
df_atualizar = df_tudo[df_tudo["Status"]=="ATUALIZAR"]
df_ok = df_tudo[df_tudo["Status"]=="OK"]
df_se = df_tudo[df_tudo["Status"]=="SEM ETIQUETA"]
df_sr = df_tudo[df_tudo["Status"]=="SEM REGISTRO"]
df_ba = df_tudo[df_tudo["Status"]=="DAR BAIXA"]
df_ne = df_tudo[df_tudo["Status"]=="NAO ENCONTRADO"]

quant_dets = len(list(df_tudo["Detentor"].unique()))
dic_dets_status = {"Detentor": list(df_tudo["Detentor"].unique()),
                  "Ok": quant_dets*[""],
                  "Atualizar": quant_dets*[""],
                  "Sem etiqueta": quant_dets*[""],
                  "Sem registro": quant_dets*[""],
                  "Dar baixa": quant_dets*[""],
                  "Não encontrado": quant_dets*[""],                  
                  "Total": quant_dets*[""]}

for ind in range(len(dic_dets_status["Detentor"])):
    dic_dets_status["Ok"][ind] = df_ok[df_ok["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    dic_dets_status["Atualizar"][ind] = df_atualizar[df_atualizar["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    dic_dets_status["Sem etiqueta"][ind] = df_se[df_se["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    dic_dets_status["Sem registro"][ind] = df_sr[df_sr["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    dic_dets_status["Dar baixa"][ind] = df_ba[df_ba["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    dic_dets_status["Não encontrado"][ind] = df_ne[df_ne["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    dic_dets_status["Total"][ind] = df_tudo[df_tudo["Detentor"]==dic_dets_status["Detentor"][ind]].shape[0]
    
dic_dets_status["Detentor"][dic_dets_status["Detentor"].index("")] = "0"
df_dets_status = pd.DataFrame(dic_dets_status).sort_values("Detentor")
df_dets_status.loc[1, "Detentor"] = "BENS SEM DETENTOR"
df_dets_status = df_dets_status.reset_index(drop = True)
df_dets_status["id"] = df_dets_status["Detentor"]

#Tipo
df_mob = df_tudo[df_tudo["Tipo do bem"]=="MOBILIA"]
df_lab = df_tudo[df_tudo["Tipo do bem"]=="LABORATORIO"]
df_elet = df_tudo[df_tudo["Tipo do bem"]=="ELETRONICO"]
df_comp = df_tudo[df_tudo["Tipo do bem"]=="COMPUTADOR"]
df_monit = df_tudo[df_tudo["Tipo do bem"]=="MONITOR"]
df_out = df_tudo[df_tudo["Tipo do bem"]=="OUTROS"]
df_ar = df_tudo[df_tudo["Tipo do bem"]=="AR CONDICIONADO"]
df_qua = df_tudo[df_tudo["Tipo do bem"]=="QUADROS"]
df_not = df_tudo[df_tudo["Tipo do bem"]=="NOTEBOOK"]
df_livr = df_tudo[df_tudo["Tipo do bem"]=="MATERIAL BIBLIOGRAFICO"]
df_tabs = df_tudo[df_tudo["Tipo do bem"]=="TABLETS"]

dic_dets_tipo = {"Detentor": list(df_tudo["Detentor"].unique()),
                  "MOBILIA": quant_dets*[""],
                  "LABORATORIO": quant_dets*[""],
                  "ELETRONICO": quant_dets*[""],
                  "COMPUTADOR": quant_dets*[""],
                  "MONITOR": quant_dets*[""],
                  "OUTROS": quant_dets*[""],
                  "AR CONDICIONADO": quant_dets*[""],
                  "QUADROS": quant_dets*[""],
                  "NOTEBOOK": quant_dets*[""],
                  "MATERIAL BIBLIOGRAFICO": quant_dets*[""],
                  "TABLETS": quant_dets*[""]}

for ind in range(len(dic_dets_tipo["Detentor"])):
    dic_dets_tipo["MOBILIA"][ind] = df_mob[df_mob["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["LABORATORIO"][ind] = df_lab[df_lab["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["ELETRONICO"][ind] = df_elet[df_elet["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["COMPUTADOR"][ind] = df_comp[df_comp["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["MONITOR"][ind] = df_monit[df_monit["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["OUTROS"][ind] = df_out[df_out["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["AR CONDICIONADO"][ind] = df_ar[df_ar["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["QUADROS"][ind] = df_qua[df_qua["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["NOTEBOOK"][ind] = df_not[df_not["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["MATERIAL BIBLIOGRAFICO"][ind] = df_livr[df_livr["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]
    dic_dets_tipo["TABLETS"][ind] = df_tabs[df_tabs["Detentor"]==dic_dets_tipo["Detentor"][ind]].shape[0]

df_dets_tipo = pd.DataFrame(dic_dets_tipo).sort_values("Detentor")
df_dets_tipo.loc[1, "Detentor"] = "BENS SEM DETENTOR"
df_dets_tipo = df_dets_tipo.reset_index(drop = True)
df_dets_tipo["id"] = df_dets_tipo["Detentor"]

#Data
df_1970 = df_tudo[df_tudo["Intervalo"]=="1970 - 1979"]
df_1980 = df_tudo[df_tudo["Intervalo"]=="1980 - 1989"]
df_1990 = df_tudo[df_tudo["Intervalo"]=="1990 - 1999"]
df_2000 = df_tudo[df_tudo["Intervalo"]=="2000 - 2009"]
df_2010 = df_tudo[df_tudo["Intervalo"]=="2010 - 2019"]
df_2020 = df_tudo[df_tudo["Intervalo"]=="2020 - 2022"]
df_n_informado = df_tudo[df_tudo["Intervalo"]=="NAO INFORMADO"]

dic_dets_data = {"Detentor": list(df_tudo["Detentor"].unique()),
                  "1970 - 1979": quant_dets*[""],
                  "1980 - 1989": quant_dets*[""],
                  "1990 - 1999": quant_dets*[""],
                  "2000 - 2009": quant_dets*[""],
                  "2010 - 2019": quant_dets*[""],
                  "2020 - 2022": quant_dets*[""],
                  "NAO INFORMADO": quant_dets*[""]}

for ind in range(len(dic_dets_data["Detentor"])):
    dic_dets_data["1970 - 1979"][ind] = df_1970[df_1970["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]
    dic_dets_data["1980 - 1989"][ind] = df_1980[df_1980["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]
    dic_dets_data["1990 - 1999"][ind] = df_1990[df_1990["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]
    dic_dets_data["2000 - 2009"][ind] = df_2000[df_2000["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]
    dic_dets_data["2010 - 2019"][ind] = df_2010[df_2010["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]
    dic_dets_data["2020 - 2022"][ind] = df_2020[df_2020["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]
    dic_dets_data["NAO INFORMADO"][ind] = df_n_informado[df_n_informado["Detentor"]==dic_dets_data["Detentor"][ind]].shape[0]

df_dets_data = pd.DataFrame(dic_dets_data).sort_values("Detentor")
df_dets_data.loc[1, "Detentor"] = "BENS SEM DETENTOR"
df_dets_data = df_dets_data.reset_index(drop = True)
df_dets_data["id"] = df_dets_data["Detentor"]

#Informações sobre os locais
#Status
quants_locs = len(list(df_tudo["Localidade"].unique()))
dic_locs_status = {"Localidade": list(df_tudo["Localidade"].unique()),
                  "Ok": quants_locs*[""],
                  "Atualizar": quants_locs*[""],
                  "Sem etiqueta": quants_locs*[""],
                  "Sem registro": quants_locs*[""],
                  "Dar baixa": quants_locs*[""],
                  "Não encontrado": quants_locs*[""],
                  "Total": quants_locs*[""]}

for ind in range(len(dic_locs_status["Localidade"])):
    dic_locs_status["Ok"][ind] = df_ok[df_ok["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    dic_locs_status["Atualizar"][ind] = df_atualizar[df_atualizar["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    dic_locs_status["Sem etiqueta"][ind] = df_se[df_se["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    dic_locs_status["Sem registro"][ind] = df_sr[df_sr["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    dic_locs_status["Dar baixa"][ind] = df_ba[df_ba["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    dic_locs_status["Não encontrado"][ind] = df_ne[df_ne["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    dic_locs_status["Total"][ind] = df_tudo[df_tudo["Localidade"]==dic_locs_status["Localidade"][ind]].shape[0]
    

df_locs_status = pd.DataFrame(dic_locs_status).sort_values("Localidade")
df_locs_status = df_locs_status.reset_index(drop = True)
df_locs_status["id"] = df_locs_status["Localidade"]

#Tipo de bem
dic_locs_tipo = {"Localidade": list(df_tudo["Localidade"].unique()),
                  "MOBILIA": quants_locs*[""],
                  "LABORATORIO": quants_locs*[""],
                  "ELETRONICO": quants_locs*[""],
                  "COMPUTADOR": quants_locs*[""],
                  "MONITOR": quants_locs*[""],
                  "OUTROS": quants_locs*[""],
                  "AR CONDICIONADO": quants_locs*[""],
                  "QUADROS": quants_locs*[""],
                  "NOTEBOOK": quants_locs*[""],
                  "MATERIAL BIBLIOGRAFICO": quants_locs*[""],
                  "TABLETS": quants_locs*[""]}

for ind in range(len(dic_locs_tipo["Localidade"])):
    dic_locs_tipo["MOBILIA"][ind] = df_mob[df_mob["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["LABORATORIO"][ind] = df_lab[df_lab["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["ELETRONICO"][ind] = df_elet[df_elet["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["COMPUTADOR"][ind] = df_comp[df_comp["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["MONITOR"][ind] = df_monit[df_monit["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["OUTROS"][ind] = df_out[df_out["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["AR CONDICIONADO"][ind] = df_ar[df_ar["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["QUADROS"][ind] = df_qua[df_qua["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["NOTEBOOK"][ind] = df_not[df_not["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["MATERIAL BIBLIOGRAFICO"][ind] = df_livr[df_livr["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]
    dic_locs_tipo["TABLETS"][ind] = df_tabs[df_tabs["Localidade"]==dic_locs_tipo["Localidade"][ind]].shape[0]

df_locs_tipo = pd.DataFrame(dic_locs_tipo).sort_values("Localidade")
df_locs_tipo = df_locs_tipo.reset_index(drop = True)
df_locs_tipo["id"] = df_locs_tipo["Localidade"]

#Data
dic_locs_data = {"Localidade": list(df_tudo["Localidade"].unique()),
                  "1970 - 1979": quants_locs*[""],
                  "1980 - 1989": quants_locs*[""],
                  "1990 - 1999": quants_locs*[""],
                  "2000 - 2009": quants_locs*[""],
                  "2010 - 2019": quants_locs*[""],
                  "2020 - 2022": quants_locs*[""],
                  "NAO INFORMADO": quants_locs*[""]}

for ind in range(len(dic_locs_data["Localidade"])):
    dic_locs_data["1970 - 1979"][ind] = df_1970[df_1970["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]
    dic_locs_data["1980 - 1989"][ind] = df_1980[df_1980["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]
    dic_locs_data["1990 - 1999"][ind] = df_1990[df_1990["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]
    dic_locs_data["2000 - 2009"][ind] = df_2000[df_2000["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]
    dic_locs_data["2010 - 2019"][ind] = df_2010[df_2010["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]
    dic_locs_data["2020 - 2022"][ind] = df_2020[df_2020["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]
    dic_locs_data["NAO INFORMADO"][ind] = df_n_informado[df_n_informado["Localidade"]==dic_locs_data["Localidade"][ind]].shape[0]

df_locs_data = pd.DataFrame(dic_locs_data).sort_values("Localidade")
df_locs_data = df_locs_data.reset_index(drop = True)
df_locs_data["id"] = df_locs_data["Localidade"]

#app

# app = Dash(__name__)
app = jd.JupyterDash(external_stylesheets=[dbc.themes.SLATE])
app.config.suppress_callback_exceptions=True

app.head = [html.Link(rel='stylesheet', href='/static/styledash.css')]

def drawFigure(df, coluna, id_bot, text_bot,link):
    return html.Div([
        dbc.Card([
            #dbc.CardHeader(title),
            dbc.CardBody([
                html.Div([
                dcc.Graph(
                    figure=px.pie(df, names=coluna, hole=.5, height = 395, width = 500
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ).update_traces(hoverinfo='label+percent', textinfo='value'),
                        # style={'width': '50vh', 'height': '50vh'}

                ),],
                    style = {"align-itens":"center",
                           "justify-content": "center",
                           "display":"flex"
                           }),
                html.Div([
                dbc.Button(text_bot, id = id_bot, n_clicks=0, className = "btn btn-dark", href=link)
                ],style = {"align-itens":"center",
                           "justify-content": "center",
                           "display":"flex"
                           })
            ])
        ]),
    ])


#Layout_pai
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://iconape.com/wp-content/png_logo_vector/unb-universidade-de-brasilia-logo.png", height="50px")),
                        dbc.Col(dbc.NavbarBrand("Relatório Patrimonial - IF", className="ms-2", style = {"font-size": "35px", "font-family": "Serif"})),
                    ],
                    align="left",
                    #className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            
        dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            )], fluid = True
    ),
    color="dark",
    dark=True,
    className = "navbar navbar-expand-lg navbar-light bg-light"
),

    html.Div([html.H1("")],id="content")]
    )



#Layout_Home
layout_home = html.Div(children=[
dbc.Card(
    dbc.CardBody([

        dbc.Row([
            dbc.Col([
                
                dbc.Row([
                    html.Div([
                    dbc.Tabs([dbc.Tab(label = "Status", tab_id = "Status"),
                             dbc.Tab(label = "Tipo", tab_id = "Tipo"),
                             dbc.Tab(label = "Local", tab_id = "Local"),
                             dbc.Tab(label = "Data", tab_id = "Data")],
                             id = "radio_info",
                             active_tab = "Status",)
                    ], 
                        # style = {"align-itens":"center",
                        #         "justify-content": "center",
                        #         "display":"flex"},
                        )
                    ],
                    ),
                
                dbc.Row([
                    html.Div(id = "div_info")
                
                ]),       
                
                
            ], width=6),
            
            dbc.Col([
                
                html.Div([
                    dbc.Tabs([dbc.Tab(label='Detentores', tab_id='tab_det'),
                              dbc.Tab(label='Localidades', tab_id='tab_loc')],
                             id='tabs_planilhas', active_tab='tab_det', )
                    ],
                    # style = {"align-itens":"center",
                    #             "justify-content": "center",
                    #             "display":"flex"}
                               ),
                
                dbc.Card(
                    dbc.CardBody([
                        
                        dbc.Row([
                            dbc.Col([
                                    dcc.Dropdown(id = "id_drop_planilhas", options = ["Status", "Tipo dos bens", "Data de incorporação"]),
                                ]),
                            dbc.Col([
                                html.Button("Download CSV", id="btn_geral",
                                            style = {
                                                'background-color': 'rgb(50, 56, 62)',
                                                'border': '3px solid rgba(17,205,45,1)',
                                                'color': 'rgba(17,205,45,1)',
                                                'border-radius': '5px'
                                                }),
                                dcc.Download(id="download_geral")
                                ])
                                ]),
                        html.Br(),
                
                        html.Div(dash_table.DataTable(page_action='none',
                                                      style_table={'height': '400px', 'overflowY': 'auto'},
                                                      fixed_rows={'headers': True},
                                                      style_header={
                                                          'backgroundColor': 'rgb(24, 34, 45)',
                                                          'color': 'white',
                                                          'writing-mode': 'tb-rl'
                                                          },
                                                      style_data={
                                                          'backgroundColor': 'rgb(50, 56, 62)',
                                                          'color': 'white'
                                                          },
                                                      style_cell={'textAlign': 'center',
                                                                  #'minWidth': '120px',
                                                                  'height': 'auto',
                                                                  #'width': '180px',
                                                                  'maxWidth': '180px',
                                                                  'whiteSpace': 'normal'
                                                                  },
                                                      sort_action="native",
                                                      sort_mode="multi",
                                                      id = "planilha_det_loc",
                                                      style_data_conditional=[
                                                                            {
                                                                                'if': {'row_index': 'odd'},
                                                                                'backgroundColor': 'rgba(39,43,48,1)',
                                                                            }
                                                                        ]
                                                      )),
                        ])
                    )
                ], width=6),
            
            
        ], align='center'),


    ],
        style = {"background-image": "radial-gradient(circle, rgba(15,8,232,0) 78%, rgba(17,205,45,1) 100%)",
                 'height': '92vh'}
        )
    , color = 'dark',
)
])


def detalhar(title, fig, id_drop, options, id_sunb, div_table_filtro,
             btn_detalhar_filtro, download_detalhar_filtro, table, radio_filtro, content_div = []):
    layout = html.Div(children=[
        dbc.Card(
            dbc.CardBody([

            dbc.Row([
                dbc.Col([
                    
                    dbc.Card(
                        dbc.CardBody([
                            
                            dbc.Row([
                                dbc.Col([html.P("Informação para detalhar: ")], width = 5),
                                dbc.Col([
                                    dcc.Dropdown(id = id_drop, options = options, value = "Nenhum")
                                ])
                            ]),
                        html.Div([
                        dcc.Graph(
                            
                            figure = fig.update_layout(
                                                     template='plotly_dark',
                                                     plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                     paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                     ),
                                                     id = id_sunb

                                                     )
                        ], id = "div_graph")
                                    ])
                                                     )
                
                                                     ], width=5),
            
            dbc.Col([
                dbc.Row([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(children = content_div),
                                    ])
                            ])
                            ])
                        )
                    ]),
                dbc.Row([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checklist(options = [{"label": 'Mostrar conteúdo do Gráfico', "value": "y"}],
                                                              inputCheckedClassName="border border-secondary bg-secondary",
                                                              input_style = {"background-color": "rgba(0,0,0,0)", "line-height": "35px"},
                                                              switch= True,
                                                              id = radio_filtro
                                                              )
                                ]),
                                
                                dbc.Col([
                                    html.Div(id = div_table_filtro),
                                ]),
                                
                                dbc.Col([
                                    html.Button("Download CSV", id=btn_detalhar_filtro,
                                                style = {
                                                    'background-color': 'rgb(50, 56, 62)',
                                                    'border': '3px solid rgba(17,205,45,1)',
                                                    'color': 'rgba(17,205,45,1)',
                                                    'border-radius': '5px'
                                                    }),
                                    dcc.Download(id=download_detalhar_filtro)
                                    ])
                            
                            ]),
                            dash_table.DataTable(page_action='none',
                                                         style_table={'height': '190px', 'overflowY': 'auto'},
                                                         fixed_rows={'headers': True},
                                                          style_header={
                                                            'backgroundColor': 'rgb(24, 34, 45)',
                                                            'color': 'white'
                                                        },
                                                          style_data={
                                                            'backgroundColor': 'rgb(50, 56, 62)',
                                                            'color': 'white'
                                                        },
                                                        style_cell={'textAlign': 'center',
                                                                    #'minWidth': '120px',
                                                                    'height': 'auto',
                                                                    #'width': '180px',
                                                                    'maxWidth': '120px',
                                                                    'whiteSpace': 'normal'
                                                                    },
                                                        sort_action="native",
                                                        sort_mode="multi",
                                                        style_data_conditional=[{'if': {'row_index': 'odd'},
                                                                                 'backgroundColor': 'rgba(39,43,48,1)'}],
                                                        id=table
                                                        )
                            ])
                        )
                    ])
                ], width=7),
            
            
        ], align='center'),
    
    ],
                style = {"background-image": "radial-gradient(circle, rgba(15,8,232,0) 78%, rgba(17,205,45,1) 100%)",
                         'height': '92vh'}
                ), color = 'dark'
    )
    ])
    return layout


#Callbacks

def content_table(df,coluna_tipo, coluna_nome):
    tipos = list(df[coluna_tipo].unique())
    
    dic_ext = {}

    for tipo in tipos:
        df_tipo = df[df[coluna_tipo] == tipo]
        nomes_do_tipo = list(df[df[coluna_tipo]==tipo][coluna_nome].unique())
        dic_int = {coluna_nome: nomes_do_tipo, "Encontrados":[], "Adicionados": [], "Não encontrados": [], "Baixa": []}
        for nome in nomes_do_tipo:
            df_nome = df_tipo[df_tipo[coluna_nome] == nome]
            dic_int["Encontrados"].append(df_nome[df_nome["Encontrado"] == "ENCONTRADO"].shape[0])
            dic_int["Adicionados"].append(df_nome[df_nome["Encontrado"] == "ADICIONADO"].shape[0])
            dic_int["Baixa"].append(df_nome[df_nome["Encontrado"] == "BAIXA"].shape[0])
            dic_int["Não encontrados"].append(df_nome[df_nome["Encontrado"] == "NAO ENCONTRADO"].shape[0])
        
        dic_ext[tipo]=pd.DataFrame(dic_int).sort_values(coluna_nome)

    return dic_ext
        
def layout_planilhas(df, coluna_tipo, drop_detalhes, id_table, btn_detalhar, download_detalhar):
    tipos = list(df[coluna_tipo].unique())
    layout = [
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id = drop_detalhes, options = tipos, value = tipos[0]),
                        ]),
                    dbc.Col([
                        html.Button("Download CSV", id=btn_detalhar,
                                    style = {
                                        'background-color': 'rgb(50, 56, 62)',
                                        'border': '3px solid rgba(17,205,45,1)',
                                        'color': 'rgba(17,205,45,1)',
                                        'border-radius': '5px'
                                        }),
                        dcc.Download(id=download_detalhar)
                        ])
                ]),
                html.Div([dash_table.DataTable(page_action='none',
                                     style_table={'height': '190px', 'overflowY': 'auto'},
                                     fixed_rows={'headers': True},
                                      style_header={
                                        'backgroundColor': 'rgb(24, 34, 45)',
                                        'color': 'white'
                                    },
                                      style_data={
                                        'backgroundColor': 'rgb(50, 56, 62)',
                                        'color': 'white'
                                    },
                                    style_cell={'textAlign': 'center',
                                                #'minWidth': '120px',
                                                'height': 'auto',
                                                #'width': '180px',
                                                'maxWidth': '90px',
                                                'whiteSpace': 'normal'
                                                },
                                    sort_action="native",
                                    sort_mode="multi",
                                    style_data_conditional=[{'if': {'row_index': 'odd'},
                                                             'backgroundColor': 'rgba(39,43,48,1)'}],
                                    id = id_table)])]
    return layout

@callback(Output('content', 'children'),Output("navbar-collapse", "children"),[Input('url', 'pathname')])
def display_page(pathname):     
    if pathname=="/":
        frequency = 1000
        duration = 200
        winsound.Beep(frequency, duration)
        return layout_home, html.H2("Análise Geral", style = {"margin":"auto"})
    elif pathname=="/detalhar/status":
        frequency = 1000
        duration = 200
        winsound.Beep(frequency, duration)
        return detalhar("Detalhes dos status dos bens",
                        fig = px.sunburst(df_tudo, path = ["Encontrado", "Status"],maxdepth =-1,color_discrete_sequence=px.colors.qualitative.Alphabet),
                        id_drop = {"type": "id_drop", "index": 1},
                        id_sunb = {"type": "id_sunb", "index": 1},
                        table = {"type": "table", "index": 1},
                        btn_detalhar_filtro = {"type": "btn_detalhar_filtro", "index": 1},
                        download_detalhar_filtro = {"type": "download_detalhar_filtro", "index": 1},
                        radio_filtro = {"type": "radio_filtro", "index": 1},
                        div_table_filtro = {"type": "div_table_filtro", "index": 1},
                        options = [{"label": "Nenhum", "value": "Nenhum"},
                                   {"label": "Tipo dos bens", "value": "Tipo do bem"},
                                   {"label": "Localização dos bens", "value": "Tipo do local"},
                                   {"label": "Data de incorporação dos bens", "value": "Intervalo"}]),html.H2("Detalhes dos status dos bens", style = {"margin":"auto"})
    elif pathname=="/detalhar/bens":
        return detalhar("Detalhes dos tipos dos bens",
                        fig = px.sunburst(df_tudo, path = ["Encontrado", "Tipo do bem"],maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet),
                       id_drop = {"type": "id_drop", "index": 2},
                       id_sunb = {"type": "id_sunb", "index": 2},
                       table = {"type": "table", "index": 2},
                       btn_detalhar_filtro = {"type": "btn_detalhar_filtro", "index": 2},
                       download_detalhar_filtro = {"type": "download_detalhar_filtro", "index": 2},
                       radio_filtro = {"type": "radio_filtro", "index": 2},
                       div_table_filtro = {"type": "div_table_filtro", "index": 2},
                        options = [{"label": "Nenhum", "value": "Nenhum"},
                                   {"label": "Status dos bens", "value": "Status"},
                                   {"label": "Localização dos bens", "value": "Tipo do local"},
                                   {"label": "Data de incorporação dos bens", "value": "Intervalo"}],
                        content_div = layout_planilhas(df_tudo, "Tipo do bem", "id_drop_bens", "id_table_bens",
                                                       btn_detalhar = 'btn_detalhar_bens',
                                                       download_detalhar = 'download_detalhar_bens')), html.H2("Detalhes dos tipos dos bens", style = {"margin":"auto"})
    elif pathname=="/detalhar/locais":
        return detalhar("Detalhes dos tipos dos locais",
                        fig = px.sunburst(df_tudo, path = ["Encontrado", "Tipo do local"],maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet),
                        id_drop = {"type": "id_drop", "index": 3},
                        id_sunb = {"type": "id_sunb", "index": 3},
                        table = {"type": "table", "index": 3},
                        btn_detalhar_filtro = {"type": "btn_detalhar_filtro", "index": 3},
                        download_detalhar_filtro = {"type": "download_detalhar_filtro", "index": 3},
                        radio_filtro = {"type": "radio_filtro", "index": 3},
                        div_table_filtro = {"type": "div_table_filtro", "index": 3},
                        options = [{"label": "Nenhum", "value": "Nenhum"},
                                   {"label": "Tipo dos bens", "value": "Tipo do bem"},
                                   {"label": "Status dos bens", "value": "Status"},
                                   {"label": "Data de incorporação dos bens", "value": "Intervalo"},],
                        content_div = layout_planilhas(df_tudo, "Tipo do local", "id_drop_locs", "id_table_locs",
                                                       btn_detalhar = 'btn_detalhar_locs',
                                                       download_detalhar = 'download_detalhar_locs')), html.H2("Detalhes das localidades dos bens", style = {"margin":"auto"})
    elif pathname=="/detalhar/datas":
        return detalhar("Detalhes dss datas de incorporação dos bens",
                        fig = px.sunburst(df_tudo, path = ["Encontrado", "Intervalo"],maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet),
                       id_drop = {"type": "id_drop", "index": 4},
                       id_sunb = {"type": "id_sunb", "index": 4},
                       table = {"type": "table", "index": 4},
                       btn_detalhar_filtro = {"type": "btn_detalhar_filtro", "index": 4},
                       download_detalhar_filtro = {"type": "download_detalhar_filtro", "index": 4},
                       radio_filtro = {"type": "radio_filtro", "index": 4},
                       div_table_filtro = {"type": "div_table_filtro", "index": 4},
                        options = [{"label": "Nenhum", "value": "Nenhum"},
                                   {"label": "Tipo dos bens", "value": "Tipo do bem"},
                                   {"label": "Localização dos bens", "value": "Tipo do local"},
                                   {"label": "Status dos bens", "value": "Status"}],
                        content_div = html.Div([
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        dict(
                                            x=anos,
                                            y=[df_n[df_n["Ano de Incorporação"]==ano].shape[0] for ano in anos],
                                            # name='Rest of world',
                                            marker=dict(
                                                color='rgb(26, 118, 255)'
                                                )
                                            ),
                                        ],
                                    layout=dict(
                                        title='Relação de bens não encontrados para cada ano',
                                        # showlegend=True,
                                        # legend=dict(
                                        #     x=0,
                                        #     y=1.0
                                        # ),
                                        margin=dict(l=40, r=0, t=40, b=30)
                                        )
                                        ).update_layout(
                                        template='plotly_dark',
                                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                        )
                                            ,
                                            style={'height': 300},
                                            id='my-graph-example'
                                            )
                                            ])), html.H2("Detalhes das datas de incorporação dos bens", style = {"margin":"auto"})
                                            
    elif pathname.startswith("/detalhar/detentor/"):
        det = pathname.strip("/detalhar/detentor/").replace("%20", " ")
        df_sipac = df_pai[df_pai["Detentor"] == det]
        df_det_alt = df_tudo[df_tudo["Atributos alterados"].str.contains("Detentor")]
        df_este_det_alt = df_det_alt[df_det_alt["Tombamento"].isin(list(df_sipac["Tombamento"]))]
        df_movidos = df_este_det_alt[df_este_det_alt["Detentor"] != ""]
        df_desauc = df_este_det_alt[df_este_det_alt["Detentor"] == ""]
        df_n_enc = df_n[df_n["Detentor"] == det]
        df_agora = df_enc[df_enc["Detentor"] == det]
        if det == "BENS SEM DETENTOR":
            df_agora = df_enc[df_enc["Detentor"] == ""]
        layout = [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.RadioItems(options = [{"label": "Nº de itens que tinha segundo o SIPAC:_____ " + str(df_sipac.shape[0]), "value": "sipac"},
                                                              {"label": "Nº de itens movidos para outro detentor:___ " + str(df_movidos.shape[0]), "value": "movidos"},
                                                              {"label": "Nº de itens  que foram desacautelados:_____ " + str(df_desauc.shape[0]), "value": "desauc"},
                                                              {"label": "Nº de itens não encontrados:_______________ " + str(df_n_enc.shape[0]), "value": "n_enc"},
                                                              {"label": "Nº de itens que esse detentor tem agora:___ " + str(df_agora.shape[0]), "value": "agora"}],
                                                   value = "sipac",
                                                   inputCheckedClassName="border border-secondary bg-secondary",
                                                   input_style = {"background-color": "rgba(0,0,0,0)", "line-height": "35px"},
                                                   #switch= True,
                                                   id = "radio_det"
                                                   )
                                    ]),
                                ])
                            ])
                        ]),
                    html.Br(),
                    dbc.Card([
                        dbc.CardBody([
                            html.Button("Download CSV", id="btn_det",
                                        style = {
                                            'background-color': 'rgb(50, 56, 62)',
                                            'border': '3px solid rgba(17,205,45,1)',
                                            'color': 'rgba(17,205,45,1)',
                                            'border-radius': '5px'
                                            }),
                            dcc.Download(id="download_det"),
                            dash_table.DataTable(page_action='none',
                                     style_table={'height': '315px', 'overflowY': 'auto'},
                                     fixed_rows={'headers': True},
                                      style_header={
                                        'backgroundColor': 'rgb(24, 34, 45)',
                                        'color': 'white'
                                    },
                                      style_data={
                                        'backgroundColor': 'rgb(50, 56, 62)',
                                        'color': 'white'
                                    },
                                      sort_action="native",
                                      sort_mode="multi",
                                    style_cell={'textAlign': 'left',
                                                'minWidth': '120px'},
                                    id = "table_bens_det")
                            ])
                        ])
                    ], width = 6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Tabs([dbc.Tab(label='Bens', tab_id='tab_bens'),
                                     dbc.Tab(label='Localidades', tab_id='tab_locais')],
                                     id='tabs_graph', active_tab='tab_bens'),
                            dbc.Checklist(options = [{"label": "Analisar Status", "value": "yes"}],
                                          value = ["yes"],
                                          inputCheckedClassName="border border-secondary bg-secondary",
                                          input_style = {"background-color": "rgba(0,0,0,0)", "line-height": "35px"},
                                          switch= True,
                                          id = "check_status_det"),
                            dcc.Graph(
                                id= "graph_detentor")
                            ])
                        ])
                    ])
                ], style = {"margin": "10px"})
            ]
        return layout, html.H2(det, style = {"margin":"auto"})
    
    elif pathname.startswith("/detalhar/local/"):
        loc = pathname.strip("/detalhar/local/").replace("%20", " ")
        df_sipac = df_pai[df_pai["Localidade"] == loc]
        df_loc_alt = df_tudo[df_tudo["Atributos alterados"].str.contains("Localidade")]
        df_este_loc_alt = df_loc_alt[df_loc_alt["Tombamento"].isin(list(df_sipac["Tombamento"]))]
        df_movidos = df_este_loc_alt[df_este_loc_alt["Localidade"] != ""]
        df_desauc = df_este_loc_alt[df_este_loc_alt["Localidade"] == ""]
        df_n_enc = df_n[df_n["Localidade"] == loc]
        df_agora = df_enc[df_enc["Localidade"] == loc]
        layout = [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.RadioItems(options = [{"label": "Nº de itens que tinha segundo o SIPAC:_____ " + str(df_sipac.shape[0]), "value": "sipac"},
                                                              {"label": "Nº de itens movidos para outro local:___ " + str(df_movidos.shape[0]), "value": "movidos"},
                                                              {"label": "Nº de itens  que foram desacautelados:_____ " + str(df_desauc.shape[0]), "value": "desauc"},
                                                              {"label": "Nº de itens não encontrados:_______________ " + str(df_n_enc.shape[0]), "value": "n_enc"},
                                                              {"label": "Nº de itens que esse local tem agora:___ " + str(df_agora.shape[0]), "value": "agora"}],
                                                   value = "sipac",
                                                   inputCheckedClassName="border border-secondary bg-secondary",
                                                   input_style = {"background-color": "rgba(0,0,0,0)", "line-height": "35px"},
                                                   switch= True,
                                                   id = "radio_loc"
                                                   )
                                    ]),
                                ])
                            ])
                        ]),
                    html.Br(),
                    dbc.Card([
                        dbc.CardBody([
                            html.Button("Download CSV", id="btn_loc",
                                        style = {
                                            'background-color': 'rgb(50, 56, 62)',
                                            'border': '3px solid rgba(17,205,45,1)',
                                            'color': 'rgba(17,205,45,1)',
                                            'border-radius': '5px'
                                            }),
                            dcc.Download(id="download_loc"),
                            dash_table.DataTable(page_action='none',
                                     style_table={'height': '315px', 'overflowY': 'auto'},
                                     fixed_rows={'headers': True},
                                      style_header={
                                        'backgroundColor': 'rgb(24, 34, 45)',
                                        'color': 'white'
                                    },
                                      style_data={
                                        'backgroundColor': 'rgb(50, 56, 62)',
                                        'color': 'white'
                                    },
                                      sort_action="native",
                                      sort_mode="multi",
                                    style_cell={'textAlign': 'left',
                                                'minWidth': '120px'},
                                    id = "table_bens_loc")
                            ])
                        ])
                    ], width = 6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Tabs([dbc.Tab(label='Bens', tab_id='tab_bens_loc'),
                                     dbc.Tab(label='Localidades', tab_id='tab_locais_loc')],
                                     id='tabs_graph', active_tab='tab_bens_loc'),
                            dbc.Checklist(options = [{"label": "Analisar Status", "value": "yes"}],
                                          value = ["yes"],
                                          inputCheckedClassName="border border-secondary bg-secondary",
                                          input_style = {"background-color": "rgba(0,0,0,0)", "line-height": "35px"},
                                          switch= True,
                                          id = "check_status_loc"),
                            dcc.Graph(
                                id= "graph_local")
                            ])
                        ])
                    ])
                ], style = {"margin": "10px"})
            ]
        return layout, html.H2(loc, style = {"margin":"auto"})
    
def original_path(sunb):
    if sunb == {"type": "id_sunb", "index": 1}:
        return ["Encontrado", "Status"]
    elif sunb =={"type": "id_sunb", "index": 2}:
        return ["Encontrado", "Tipo do bem"]
    elif sunb =={"type": "id_sunb", "index": 3}:
        return ["Encontrado", "Tipo do local"]
    elif sunb =={"type": "id_sunb", "index": 4}:
        return ["Encontrado", "Intervalo"]

@callback(Output("div_info", 'children'),
          [Input("radio_info", 'active_tab')])
def sel_info(value):
    if value == "Status":
        content = drawFigure(id_bot = "id_bot_status",
                               text_bot = "Detalhar status",
                               df = df_tudo,
                               coluna = "Status",
                               #title = "Status",
                               link = "/detalhar/status")
    elif value == "Tipo":
        content = drawFigure(df = df_tudo,
                           coluna = "Tipo do bem",
                           #title = "Tipo",
                           id_bot = "id_bot_tipo",
                           text_bot = "Detalhar bens",
                           link = "/detalhar/bens")
    elif value == "Local":
        content = drawFigure(df = df_tudo,
                           coluna = "Tipo do local",
                           #title = "Local",
                           id_bot = "id_bot_loc",
                           text_bot = "Detalhar locais",
                           link = "/detalhar/locais")
    elif value == "Data":
        content = drawFigure(df=df_tudo,
                           coluna = "Intervalo",
                           #title = "Data de Incorporação",
                           id_bot = "id_bot_data",
                           text_bot = "Detalhar datas de incorporação",
                           link = "/detalhar/datas")
    return content

@callback(Output({"type": 'id_sunb', "index": MATCH}, 'figure'),
          [Input({"type": 'id_drop', "index": MATCH}, 'value')],
          State({'type': 'id_sunb', 'index': MATCH}, 'id'))
def sel_detalhe(value, id):
    path_sel = original_path(id)
    if len(path_sel) == 2 and value != "Nenhum":
        frequency = 2000
        duration = 200
        winsound.Beep(frequency, duration)
        path_sel.append(value)
    elif len(path_sel) == 3 and value != "Nenhum":
        frequency = 1000
        duration = 200
        winsound.Beep(frequency, duration)
        del path_sel[-1]
        path_sel.append(value)
    elif value == "Nenhum":
        frequency = 1000
        duration = 200
        winsound.Beep(frequency, duration)
        path_sel = path_sel[:2]
        
    return px.sunburst(df_tudo, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )

@callback(Output({'type': 'div_table_filtro', 'index': MATCH}, "children"),
          Input( {"type": "id_sunb", "index": MATCH}, 'clickData'))
def hover(clickData):
    if clickData:
        return html.Div([html.P([html.Strong('Filtro Selecionado: '), clickData["points"][0]["id"]])])
    else: return html.Div(html.P(html.Strong('Filtro Selecionado: ')))
    
@callback(Output({'type': 'table', 'index': MATCH}, "data"),
          Input( {"type": "id_sunb", "index": MATCH}, 'clickData'),
          Input({"type": 'id_drop', "index": MATCH}, 'value'),
          Input({"type": 'radio_filtro', "index": MATCH}, 'value'),
          State({'type': 'id_sunb', 'index': MATCH}, 'id'))
def table(clickData, value, radio, id):
    if radio == ['y']:
        path_sel = original_path(id)
        if len(path_sel) == 2 and value != "Nenhum":
            path_sel.append(value)
        elif len(path_sel) == 3 and value != "Nenhum":
            del path_sel[-1]
            path_sel.append(value)
        elif value == "Nenhum":
            path_sel = path_sel[:2]
        print(path_sel)
            
        if clickData:
            filtro = clickData["points"][0]["id"].split('/')
            print('filtro', filtro)
            
            
            if len(filtro) == 1:
                df = df_tudo[df_tudo[path_sel[0]]==filtro[0]]
            elif len(filtro) == 2:
                df = df_tudo[(df_tudo[path_sel[0]]==filtro[0]) & (df_tudo[path_sel[1]]==filtro[1])]
            elif len(filtro) == 3:
                df = df_tudo[(df_tudo[path_sel[0]]==filtro[0]) & (df_tudo[path_sel[1]]==filtro[1]) & (df_tudo[path_sel[2]]==filtro[2])]
            
            df_tudo_necessario = df.loc[:, ['Denominação', 'Tombamento', 'Detentor', 'Localidade']]
            return df_tudo_necessario.to_dict('records')
        # else:
        #     return df_tudo.loc[:, ['Denominação', 'Tombamento', 'Detentor', 'Localidade']].to_dict('records')
    
@callback(Output('download_geral', 'data'),
          State("planilha_det_loc", 'data'),
          Input("btn_geral", 'n_clicks'),
          prevent_initial_call=True,)
def download_geral(data, click):
    if click is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "planilha_patrimnonio.csv")
    
@callback(Output({"type": "download_detalhar_filtro", "index": MATCH}, 'data'),
          State({"type": "table", "index": MATCH}, 'data'),
          Input({"type": "btn_detalhar_filtro", "index": MATCH}, 'n_clicks'),
          prevent_initial_call=True,)
def download_detalhar_filtro(data, click):
    if click is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "planilha_patrimnonio.csv")
    
@callback(Output('download_detalhar_bens', 'data'),
          State('id_table_bens', 'data'),
          Input('btn_detalhar_bens', 'n_clicks'),
          prevent_initial_call=True,)
def download_detalhar_bens(data, click):
    if click is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "planilha_patrimnonio.csv")
    
    
@callback(Output('download_detalhar_locs', 'data'),
          State('id_table_locs', 'data'),
          Input('btn_detalhar_locs', 'n_clicks'),
          prevent_initial_call=True,)
def download_detalhar_locs(data, click):
    if click is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "planilha_patrimnonio.csv")
    
@callback(Output('download_det', 'data'),
          State('table_bens_det', 'data'),
          Input('btn_det', 'n_clicks'),
          prevent_initial_call=True,)
def download_det(data, click):
    if click is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "planilha_patrimnonio.csv")
    

@callback(Output('download_loc', 'data'),
          State('table_bens_loc', 'data'),
          Input('btn_loc', 'n_clicks'),
          prevent_initial_call=True,)
def download_loc(data, click):
    if click is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, "planilha_patrimnonio.csv")


@callback(Output('id_table_bens', 'data'),
          [Input("id_drop_bens", 'value')])
def sel_tab_bens(tab):
    return content_table(df_tudo, "Tipo do bem", "Denominação")[tab].to_dict('records')

@callback(Output('id_table_locs', 'data'),
          [Input("id_drop_locs", 'value')])
def sel_tab_locs(tab):
    return content_table(df_tudo, "Tipo do local", "Localidade")[tab].to_dict('records')
    
@app.callback(Output('planilha_det_loc', 'data'),
              Output('planilha_det_loc', 'columns'),
              Input('id_drop_planilhas', 'value'),
              Input("tabs_planilhas", "active_tab"))
def content_planilha_det_loc(value, tab):
    if value=="Status":
        if tab == "tab_det":
            df = df_dets_status
        else:
            df = df_locs_status
    
    elif value == "Tipo dos bens":
        if tab == "tab_det":
            df = df_dets_tipo
        else:
            df = df_locs_tipo
        
    else:
        if tab == "tab_det":
            df = df_dets_data
        else:
            df = df_locs_data
            
    return df.to_dict('records'), [{"name": c, "id": c} for c in list(df.columns) if c != "id"]
    print(list(df.columns))
    


@app.callback(Output('url', 'pathname'),
              Input('planilha_det_loc', 'active_cell'),
              Input("tabs_planilhas", "active_tab"))
def detalhar_det(cell,tab):
    if cell is None:
        return no_update
    else:
        if tab == "tab_det":
            return "/detalhar/detentor/" + cell["row_id"]
        else:
            return "/detalhar/local/" + cell["row_id"]
    
@app.callback(Output('graph_detentor', 'figure'),
              Output("table_bens_det", "data"),
              Input('radio_det', "value"),
              Input("url", "pathname"),
              Input("tabs_graph", "active_tab"),
              Input("check_status_det", "value"))
def graph_det(radio, pathname, tab, check):
    det = pathname.strip("/detalhar/detentor/").replace("%20", " ")
    if det == "BENS SEM DETENTOR":
        det = ""
    df_sipac = df_pai[df_pai["Detentor"] == det]
    df_det_alt = df_tudo[df_tudo["Atributos alterados"].str.contains("Detentor")]
    df_este_det_alt = df_det_alt[df_det_alt["Tombamento"].isin(list(df_sipac["Tombamento"]))]
    df_movidos = df_este_det_alt[df_este_det_alt["Detentor"] != ""]
    df_desauc = df_este_det_alt[df_este_det_alt["Detentor"] == ""]
    df_n_enc = df_n[df_n["Detentor"] == det]
    df_agora = df_enc[df_enc["Detentor"] == det]
    
    if tab == "tab_bens":
        path_sel = ["Tipo do bem", "Denominação"]
    else:
        path_sel = ["Tipo do local", "Localidade"]
        
    if check == ["yes"] and len(path_sel)==2:
        path_sel.insert(0, "Status")
    elif check == [] and len(path_sel)==3:
        del path_sel[0]
    
    if radio == "sipac":
        sunb = px.sunburst(df_sipac, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_sipac[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "movidos":
        sunb = px.sunburst(df_movidos, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_movidos[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "desauc":
        sunb = px.sunburst(df_desauc, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_desauc[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "n_enc":
        sunb = px.sunburst(df_n_enc, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_n_enc[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "agora":
        sunb = px.sunburst(df_agora, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_agora[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    return sunb, data

@app.callback(Output('graph_local', 'figure'),
              Output("table_bens_loc", "data"),
              Input('radio_loc', "value"),
              Input("url", "pathname"),
              Input("tabs_graph", "active_tab"),
              Input("check_status_loc", "value"))
def graph_loc(radio, pathname, tab, check):
    loc = pathname.strip("/detalhar/local/").replace("%20", " ")
    df_sipac = df_pai[df_pai["Localidade"] == loc]
    df_loc_alt = df_tudo[df_tudo["Atributos alterados"].str.contains("Localidade")]
    df_este_loc_alt = df_loc_alt[df_loc_alt["Tombamento"].isin(list(df_sipac["Tombamento"]))]
    df_movidos = df_este_loc_alt[df_este_loc_alt["Localidade"] != ""]
    df_desauc = df_este_loc_alt[df_este_loc_alt["Localidade"] == ""]
    df_n_enc = df_n[df_n["Localidade"] == loc]
    df_agora = df_enc[df_enc["Localidade"] == loc]
    
    if tab == "tab_bens_loc":
        path_sel = ["Tipo do bem", "Denominação"]
    else:
        path_sel = ["Tipo do local", "Localidade"]
        
    
    if check == ["yes"] and len(path_sel)==2:
        path_sel.insert(0, "Status")
    elif check == [] and len(path_sel)==3:
        del path_sel[0]
    
    if radio == "sipac":
        sunb = px.sunburst(df_sipac, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_sipac[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "movidos":
        sunb = px.sunburst(df_movidos, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_movidos[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "desauc":
        sunb = px.sunburst(df_desauc, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_desauc[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "n_enc":
        sunb = px.sunburst(df_n_enc, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_n_enc[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    elif radio == "agora":
        sunb = px.sunburst(df_agora, path = path_sel, maxdepth =-1, color_discrete_sequence=px.colors.qualitative.Alphabet).update_layout(template='plotly_dark',
                                                                             plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                                             paper_bgcolor= 'rgba(0, 0, 0, 0)'
                                                                             )
        data = df_agora[
            ["Denominação", "Tombamento", "Localidade", "Detentor", "Status"]
            ].to_dict('records')
    return sunb, data
   
if __name__ == "__main__":
    app.run_server()