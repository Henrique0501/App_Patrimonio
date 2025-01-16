# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 08:22:18 2021

@author: Samaung
"""

import cv2
from PIL import Image, ImageTk
import imutils
from pyzbar.pyzbar import decode
import pandas as pd
import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntry
import os
from playsound import playsound
import gtts
import speech_recognition as sr
import winsound


class Aplicativo():
    
    def Ler_codbarras(self, frame):
        codbarras = decode(frame)
        for codbarra in codbarras:
            x, y , largura, altura = codbarra.rect
            self.tombamento = int(codbarra.data.decode('utf-8'))
            Lista_tombamentos.append(self.tombamento)
            cv2.rectangle(frame, (x, y),(x+largura, y+altura), (0, 255, 0), 2)
            
            # Fala tombamento
            if jan_tudoOK == None and jan_sem_tomb == None:
                if "arquivo_som.mp3" in os.listdir():
                    os.remove("arquivo_som.mp3")
                if (str(self.tombamento) not in dic_tree_OK["Tombamento"]) and (str(self.tombamento) not in dic_tree_atualizar["Tombamento"]) and (str(self.tombamento) not in dic_tree_sr["Tombamento"]) and (str(self.tombamento) not in dic_tree_baixa["Tombamento"]):
                    frase = gtts.gTTS(tratar.separar_nums(self.tombamento), lang = "pt-br")
                else:
                    frase = gtts.gTTS("Esse tombamento já está no arquivo", lang = "pt-br")
                if Lista_tombamentos[-1]==Lista_tombamentos[-2]:
                    frase.save("arquivo_som.mp3")
                    if configurar.config_falar_tomb() == True:
                        playsound("arquivo_som.mp3")
                    else:
                        frequency = 2000
                        duration = 200
                        winsound.Beep(frequency, duration)
                            
                # Tirar a coluna de índices que o pandas cria
                if 'Unnamed: 0' in dic_pai:
                    del dic_pai['Unnamed: 0']
    
                if self.tombamento not in dic_pai["Tombamento"] and Lista_tombamentos[-1]==Lista_tombamentos[-2] and frase != gtts.gTTS("Esse tombamento já está no arquivo", lang = "pt-br"):
                    var_tomb_m.set(self.tombamento)
                    self.append_DF_tudoOK(self.tombamento)

        return frame
    
    def escanear(self):
        global camera
        try:
            camera = cv2.VideoCapture(0)
        except:
            camera = cv2.VideoCapture(0)

        self.mostrar()
        
    def mostrar(self):
        global camera
        ret, frame = camera.read()
        if ret == True:
            frame = self.Ler_codbarras(frame)
            frame = imutils.resize(frame, width = 600)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image = img)
            webcam.configure(image=image)
            webcam.image = image
                
            webcam.after(10, self.mostrar)
        
    def abrir_jan_sem_tomb(self):
        global jan_sem_tomb
        if jan_sem_tomb == None:
            self.LOCK = True
            jan_sem_tomb = tk.Toplevel()
            jan_sem_tomb.title("Bem sem etiqueta")
            jan_sem_tomb.protocol('WM_DELETE_WINDOW', self.jan_sem_tomb_none)
            jan_sem_tomb.geometry('+450+200')
            
            #Título
            label_titulo_st = tk.Label(jan_sem_tomb, text = "Digite os dados desse bem.")
            label_titulo_st.grid(row = 0, column = 0, columnspan = 2)
            
            #Descri
            label_descri_st = tk.Label(jan_sem_tomb, text = "Descrição")
            label_descri_st. grid(row = 1, column =0)
            
            descri_st = AutocompleteEntry(jan_sem_tomb, textvar = var_descri_st, width = 50, completevalues = lista_bens)
            descri_st.grid(row = 1, column = 1, padx = 5, pady = 5)
            
            #Local
            label_local_st = tk.Label(jan_sem_tomb, text = "Local")
            label_local_st. grid(row = 2, column =0)
            
            local_st = AutocompleteEntry(jan_sem_tomb, textvar = var_local_st, width = 50, completevalues = lista_descris)
            local_st.grid(row = 2, column = 1, padx = 5, pady = 5)
            
            #Detentor
            label_detentor_st = tk.Label(jan_sem_tomb, text = "Detentor")
            label_detentor_st. grid(row = 3, column = 0)
            
            detentor_st = AutocompleteEntry(jan_sem_tomb, textvar = var_detentor_st, width = 50, completevalues = lista_detentores)
            detentor_st.grid(row = 3, column = 1, padx = 5, pady = 5)
            
            #Condição
            label_condi_st = tk.Label(jan_sem_tomb, text = "Estado")
            label_condi_st. grid(row = 4, column =0)
            
            condi_st = AutocompleteEntry(jan_sem_tomb, textvar = var_condi_st, width = 50, completevalues = ["Em uso", 'Irrecuperável'])
            condi_st.grid(row = 4, column = 1, padx = 5, pady = 5)
            
            #Observação
            label_obs_st = tk.Label(jan_sem_tomb, text = "Observação")
            label_obs_st. grid(row = 5, column =0, stick = "n")
            
            self.obs_st = tk.Text(jan_sem_tomb, width = 37, height = 3)
            self.obs_st.grid(row = 5, column = 1, padx = 5, pady = 5)
            
            #Dar baixa
            baixa_st = tk.Checkbutton(jan_sem_tomb, text = "Dar baixa", variable = var_baixa_st)
            baixa_st.grid(row = 6, column = 0, pady = 5)
            
            #Motivo
            self.motivo_st = tk.Text(jan_sem_tomb, width = 37, height = 3)
            self.motivo_st.grid(row = 6, column = 1, padx = 5, pady = 5)
            
            #Quantidade
            self.quant = tk.Spinbox(jan_sem_tomb, from_ =1, to = 100, width = 5)
            self.quant.grid(row = 7, column = 0)
            
            #Botão_pronto
            pronto_st = tk.Button(jan_sem_tomb, text = "Pronto",  command = self.func_pronto_st)
            pronto_st.grid(row = 7, column = 1, stick = "ew")
            
    
    def func_pronto_st(self):
        
        if var_local_st.get() in nv_descris:
            if nv_cods[nv_descris.index(var_local_st.get())] != "":
                self.localidade_st = "11010116_" + nv_cods[nv_descris.index(var_local_st.get())] + " - " + var_local_st.get()
            else:
                self.localidade_st = var_local_st.get()
        elif var_local_st.get() in nv_cods:
            self.localidade_st = "11010116_" + var_local_st.get() + " - " + nv_descris[nv_cods.index(var_local_st.get())]
        else:
            if self.LOCK == True:
                global jan_local_errado_st
                jan_local_errado_st = tk.Toplevel()
                jan_local_errado_st.title("Local não reconhecido")
                jan_local_errado_st.geometry("+420+100")
                
                
                tk.Label(jan_local_errado_st, text = f"O local {var_local_st.get()} não foi reconhecido.\nSelecione o local:").pack()
                
                Frame_tree_st = tk.Frame(jan_local_errado_st)
                Frame_tree_st.pack()
                
                scrolly_outro_st = ttk.Scrollbar(Frame_tree_st, orient="vertical")
                scrolly_outro_st.pack(side = tk.RIGHT, fill = "y")
                
                tree_locais_st = ttk.Treeview(Frame_tree_st, columns=["Local", "Código"], show='headings', height =20, yscrollcommand = scrolly_outro_st.set)
                tree_locais_st.pack()
                
                tree_locais_st.column("Local", anchor="w", stretch=True, width = 400, minwidth =100)
                tree_locais_st.heading("Local", text="Local")
                
                tree_locais_st.column("Código", anchor="w", stretch=True, width = 120, minwidth =100)
                tree_locais_st.heading("Código", text="Código")
                
                scrolly_outro_st.config(command = tree_locais_st.yview)
                
                for i in range(len(nv_descris)):
                    tree_locais_st.insert("", "end", values = (nv_descris[i], nv_cods[i]))
                
                tk.Label(jan_local_errado_st, text = "Outro:").pack()
                
                outro_local_st = tk.Entry(jan_local_errado_st, textvar = var_outro_local_st)
                outro_local_st.pack()
                
                tk.Button(jan_local_errado_st, text = "Ok", command = lambda: self.setar_local(tree_locais_st, var_local_st, jan_local_errado_st) if var_outro_local_st.get() == "" else self.setar_outro_local(var_local_st, var_outro_local_st, jan_local_errado_st) ).pack(pady = 10)
                
                if var_local_st.get() in nv_descris:
                    self.localidade_st = "11010116_" + nv_cods[nv_descris.index(var_local_st.get())] + " - " + var_local_st.get()
                elif var_local_st.get() in nv_cods:
                    self.localidade_st = "11010116_" + var_local_st.get() + " - " + nv_descris[nv_cods.index(var_local_st.get())]
            
        if var_local_st.get() in nv_descris or  var_local_st.get() in nv_cods or self.LOCK == False:
            if self.LOCK == False:
                self.LOCK == True
                self.localidade_st = var_outro_local_st.get()
            if var_baixa_st.get() == 0:
                self.dado_se = [var_descri_st.get(), self.localidade_st, var_detentor_st.get(), var_condi_st.get(), self.obs_st.get(1.0, "end-1c")]
                for i in range(int(self.quant.get())):
                    tratar.inserir_tree_dic(tree_se, dic_tree_se, self.dado_se)
                
                self.jan_sem_tomb_none()
                var_descri_st.set("")
                # var_local_st.set("")
                self.localidade_st = ""
                var_detentor_st.set("")
                var_condi_st.set("")
                var_baixa_st.set(0)
            else:
                self.dado_se = len(colunas_baixa)*[""]
                self.dado_se[colunas_baixa.index("Tombamento")] = "Sem etiqueta"
                self.dado_se[colunas_baixa.index("Denominação")] = var_descri_st.get()
                self.dado_se[colunas_baixa.index("Localidade")] =  self.localidade_st
                self.dado_se[colunas_baixa.index("Detentor")] = var_detentor_st.get()
                self.dado_se[colunas_baixa.index("Estado")] = var_condi_st.get()
                self.dado_se[colunas_baixa.index("Obs.")] = self.obs_st.get(1.0, "end-1c")
                self.dado_se[colunas_baixa.index("Motivo para baixa")] = self.motivo_st.get(1.0, "end-1c")
                for i in range(int(self.quant.get())):
                    tratar.inserir_tree_dic(tree_baixa, dic_tree_baixa, self.dado_se)
                
                self.jan_sem_tomb_none()
                var_descri_st.set("")
                # var_local_st.set("")
                self.localidade_st = ""
                var_detentor_st.set("")
                var_condi_st.set("")
                var_baixa_st.set(0)
                
            var_outro_local_st.set("")
        
    def jan_sem_tomb_none(self):
        global jan_sem_tomb
        jan_sem_tomb.destroy()
        jan_sem_tomb = None
        
    def imprimir_etiqueta(self):
        if var_etiqueta.get() == 1:
            self.obs_OK.insert(1.0, "Imprimir nova etiqueta\n")
        else:
            if "Imprimir nova etiqueta\n" in self.obs_OK.get(1.0, "end-1c"):
                text = self.obs_OK.get(1.0, "end-1c")
                text = text.replace("Imprimir nova etiqueta\n", "")
                self.obs_OK.delete(1.0, tk.END)
                self.obs_OK.insert(1.0, text)
                
    def append_DF_tudoOK(self, tombamento):
        if (str(tombamento) not in dic_tree_OK["Tombamento"]) and (str(tombamento) not in dic_tree_atualizar["Tombamento"]) and (str(tombamento) not in dic_tree_sr["Tombamento"]) and (str(tombamento) not in dic_tree_baixa["Tombamento"]) and (int(tombamento) not in dic_tree_OK["Tombamento"]) and (int(tombamento) not in dic_tree_atualizar["Tombamento"]) and (int(tombamento) not in dic_tree_sr["Tombamento"]) and (int(tombamento) not in dic_tree_baixa["Tombamento"]):
            global jan_tudoOK
            if jan_tudoOK == None:
                self.LOCK = True
                jan_tudoOK = tk.Toplevel()
                jan_tudoOK.title("Tudo Ok?")
                global df_tudo_encontrado
                if str(tombamento) in [str(i) for i in list(df_tudo_encontrado["Tombamento"])]:
                    jan_tudoOK["bg"] = "red"
                #jan_tudoOK.grab_set()
                jan_tudoOK.protocol('WM_DELETE_WINDOW', self.jan_tudoOK_none)
                jan_tudoOK.geometry('+380+150')
                label_tomb_OK = tk.Label(jan_tudoOK, text = f"Tombamento {tombamento}", font = 'Helvetica 18 bold')
                label_tomb_OK.grid(row = 0, column  = 2)
                #Título
                label_titulo_OK = tk.Label(jan_tudoOK)
                label_titulo_OK.grid(row = 0, column = 0, columnspan = 2)
                
                self.linha = tratar.checar_no_pai(str(tombamento), "Tombamento", nv_DF_pai)
                if self.linha != None:
                    var_descri_OK.set(DF_pai["Denominação"][self.linha])
                    try:
                        cod, loc = DF_pai["Localidade"][self.linha].split(" - ", maxsplit = 1)
                    except:
                        cod = ""
                        loc = ""
                    var_local_OK.set(loc.strip())
                    var_detentor_OK.set(DF_pai["Detentor"][self.linha])
                    var_condi_OK.set(DF_pai["Estado"][self.linha])
                    var_opt_descri_OK.set("Registro na base de dados")
                    var_opt_local_OK.set("Registro na base de dados")
                    var_opt_detentor_OK.set("Registro na base de dados")
                    var_opt_condi_OK.set("Registro na base de dados")
                    label_titulo_OK["text"] = "Esse tombamento foi encontrado na base de dados.\nSe você não alterá-lo, ele será registrado em 'Tudo OK'. \nSe você alterá-lo, ele será registrado em 'Atualizar'.\nSe você marcar a opção 'Dar Baixa', ele será registrado em 'Dar baixa'."
                    
                else:
                    var_descri_OK.set("")
                    var_local_OK.set("")
                    var_detentor_OK.set("")
                    var_condi_OK.set("")
                    label_titulo_OK["text"] = "Esse tombamento não foi encontrado na base de dados"
                #Descri
                label_descri_OK = tk.Label(jan_tudoOK, text = "Descrição")
                label_descri_OK. grid(row = 1, column =0)
                
                descri_OK = AutocompleteEntry(jan_tudoOK, textvar = var_descri_OK, width = 50, completevalues = lista_bens)
                descri_OK.grid(row = 1, column = 1, padx = 5, pady = 5)
                
                opt_descri_OK = tk.OptionMenu(jan_tudoOK, var_opt_descri_OK, *["Registro na base de dados", "Última registro"], command = lambda g: self.setar(var_opt_descri_OK, var_descri_OK, "Denominação"))
                opt_descri_OK.grid(row = 1, column = 2, padx = 5, pady = 5)
                                              
                #Local
                label_local_OK = tk.Label(jan_tudoOK, text = "Local")
                label_local_OK. grid(row = 2, column =0)
                
                local_OK = AutocompleteEntry(jan_tudoOK, textvar = var_local_OK, width = 50, completevalues = nv_descris)
                local_OK.grid(row = 2, column = 1, padx = 5, pady = 5)
                
                opt_local_OK = tk.OptionMenu(jan_tudoOK, var_opt_local_OK, *["Registro na base de dados", "Última registro"], command = lambda g: self.setar(var_opt_local_OK, var_local_OK, "Localidade"))
                opt_local_OK.grid(row = 2, column = 2, padx = 5, pady = 5)
                
                #Detentor
                label_detentor_OK = tk.Label(jan_tudoOK, text = "Detentor")
                label_detentor_OK. grid(row = 3, column =0)
                
                detentor_OK = AutocompleteEntry(jan_tudoOK, textvar = var_detentor_OK, width = 50, completevalues = lista_detentores)
                detentor_OK.grid(row = 3, column = 1, padx = 5, pady = 5)
                
                opt_detentor_OK = tk.OptionMenu(jan_tudoOK, var_opt_detentor_OK, *["Registro na base de dados", "Última registro"], command = lambda g: self.setar(var_opt_detentor_OK, var_detentor_OK, "Detentor"))
                opt_detentor_OK.grid(row = 3, column = 2, padx = 5, pady = 5)
                
                #Condição
                label_condi_OK = tk.Label(jan_tudoOK, text = "Estado")
                label_condi_OK. grid(row = 4, column =0)
                
                self.condi_OK = AutocompleteEntry(jan_tudoOK, textvar = var_condi_OK, width = 50, completevalues = ["Em uso", 'Irrecuperável'])
                self.condi_OK.grid(row = 4, column = 1, padx = 5, pady = 5)
                
                opt_condi_OK = tk.OptionMenu(jan_tudoOK, var_opt_condi_OK, *["Registro na base de dados", "Última registro"], command = lambda g: self.setar(var_opt_condi_OK, var_condi_OK, "Estado"))
                opt_condi_OK.grid(row = 4, column = 2, padx = 5, pady = 5)
                
                #Observação
                label_obs_OK = tk.Label(jan_tudoOK, text = "Observação")
                label_obs_OK. grid(row = 5, column =0, stick = "n")
                
                self.obs_OK = tk.Text(jan_tudoOK, width = 37, height = 3)
                self.obs_OK.grid(row = 5, column = 1, padx = 5, pady = 5)
                
                #Etiqueta
                check_etiqueta = tk.Checkbutton(jan_tudoOK, text = "Imprimir nova etiqueta", variable = var_etiqueta, command = self.imprimir_etiqueta)
                check_etiqueta.grid(row = 5, column = 2, padx = 5, pady = 5)
                
                #Dar baixa
                baixa_OK = tk.Checkbutton(jan_tudoOK, text = "Dar baixa", variable = var_baixa_OK)
                baixa_OK.grid(row = 6, column = 0, pady = 5)
                
                #Motivo
                self.motivo_OK = tk.Text(jan_tudoOK, width = 37, height = 3)
                self.motivo_OK.grid(row = 6, column = 1, padx = 5, pady = 5)
                
                #Botão_pronto
                pronto_OK = tk.Button(jan_tudoOK, text = "Pronto",  command = self.func_pronto_OK)
                pronto_OK.grid(row = 7, column = 0, columnspan = 2, stick = "ew")
        else:
            tk.messagebox.showinfo(title = "Tombamento já registrado", message = "Esse tombamento já foi registrado.")
            
    def setar(self, var_menu, var_entry, key):
        if var_menu.get() == "Registro na base de dados":
            if var_entry != var_local_OK.get():
                var_entry.set(DF_pai[key][self.linha])
            else:
                codigo, loc = DF_pai[key][self.linha].split(" - ", maxsplit = 1)
                var_entry.set(loc.strip())
                
        else:
            if key == "Denominação":
                var_entry.set(descri_anterior)
            if key == "Localidade":
                var_entry.set(local_anterior)
            if key == "Detentor":
                var_entry.set(detentor_anterior)
            if key == "Estado":
                var_entry.set(condi_anterior)
    
    def setar_local(self, tree, var, jan):
        var.set(nv_descris[tree.index(tree.selection())])
        jan.destroy()
        self.LOCK = True
        
    def setar_outro_local(self, var_entry_local, var_entry_outro, jan):
        var_entry_local.set(var_entry_outro.get())
        nv_descris.append(var_entry_outro.get())
        nv_cods.append("")
        self.LOCK = False
        jan.destroy()
    
    def func_pronto_OK(self):
        if var_local_OK.get() in nv_descris:
            if nv_cods[nv_descris.index(var_local_OK.get())] != "":
                self.localidade = "11010116_" + nv_cods[nv_descris.index(var_local_OK.get())] + " - " + var_local_OK.get()
            else:
                self.localidade = var_local_OK.get()
        elif var_local_OK.get() in nv_cods:
            self.localidade = "11010116_" + var_local_OK.get() + " - " + nv_descris[nv_cods.index(var_local_OK.get())]
        else:
            if self.LOCK == True:
                global jan_local_errado
                jan_local_errado = tk.Toplevel()
                jan_local_errado.title("Local não reconhecido")
                jan_local_errado.geometry("+420+100")
                
                tk.Label(jan_local_errado, text = f"O local {var_local_OK.get()} não foi reconhecido.\nSelecione o local:").pack()
                
                Frame_tree_OK = tk.Frame(jan_local_errado)
                Frame_tree_OK.pack()
                
                scrolly_outro_OK = ttk.Scrollbar(Frame_tree_OK, orient="vertical")
                scrolly_outro_OK.pack(side = tk.RIGHT, fill = "y")
                
                tree_locais = ttk.Treeview(Frame_tree_OK, columns=["Local", "Código"], show='headings', height =20, yscrollcommand = scrolly_outro_OK.set)
                tree_locais.pack()
                
                tree_locais.column("Local", anchor="w", stretch=True, width = 400, minwidth =100)
                tree_locais.heading("Local", text="Local")
                
                tree_locais.column("Código", anchor="w", stretch=True, width = 120, minwidth =100)
                tree_locais.heading("Código", text="Código")
                
                scrolly_outro_OK.config(command = tree_locais.yview)
                
                for i in range(len(nv_descris)):
                    tree_locais.insert("", "end", values = (nv_descris[i], nv_cods[i]))
                    
                tk.Label(jan_local_errado, text = "Outro:").pack()
                    
                outro_local = tk.Entry(jan_local_errado, textvar = var_outro_local, width = 50)
                outro_local.pack()
                    
                tk.Button(jan_local_errado, text = "Ok", command = lambda: self.setar_local(tree_locais, var_local_OK, jan_local_errado) if var_outro_local.get() == "" else self.setar_outro_local(var_local_OK, var_outro_local, jan_local_errado)).pack(pady = 10)
        
        if var_local_OK.get() in nv_descris or  var_local_OK.get() in nv_cods or self.LOCK == False:
            if self.LOCK == False:
                self.LOCK == True
                self.localidade = var_outro_local.get()
            if self.linha != None:
                self.dado_OK = [DF_pai[i][self.linha] for i in colunas_pai]
                self.dado_OK[colunas_pai.index("Detentor")] = var_detentor_OK.get()
                self.dado_OK[colunas_pai.index("Denominação")] = var_descri_OK.get()
                self.dado_OK[colunas_pai.index("Localidade")] = self.localidade
                self.dado_OK[colunas_pai.index("Estado")] = var_condi_OK.get()
                self.dado_OK.append(self.obs_OK.get(1.0, "end-1c"))
            else:
                self.dado_OK = len(colunas_sr)*[""]
                self.dado_OK[colunas_sr.index("Tombamento")] = var_tomb_m.get()
                self.dado_OK[colunas_sr.index("Detentor")] = var_detentor_OK.get()
                self.dado_OK[colunas_sr.index("Denominação")] = var_descri_OK.get()
                self.dado_OK[colunas_sr.index("Localidade")] = self.localidade
                self.dado_OK[colunas_sr.index("Estado")] = self.condi_OK.get()
                self.dado_OK[colunas_sr.index("Obs.")] = self.obs_OK.get(1.0, "end-1c")
                
            if var_baixa_OK.get() == 0:
                self.inserir_dado_OK()
            else:
                self.dado_OK.insert(colunas_baixa.index("Motivo para baixa"),self.motivo_OK.get(1.0,"end-1c"))
                self.dar_baixa_OK()
            var_baixa_OK.set(0)
            var_outro_local.set("")
            
    def dar_baixa_OK(self):
        if self.linha != None:
            self.dado_OK.append("Sim")
            if var_descri_OK.get() == DF_pai["Denominação"][self.linha] and self.localidade == DF_pai["Localidade"][self.linha] and var_detentor_OK.get() == DF_pai["Detentor"][self.linha] and var_condi_OK.get() == DF_pai["Estado"][self.linha]:
                self.dado_OK.append("")
            else:
                atributos_alterados = ""
                if var_descri_OK.get() != DF_pai["Denominação"][self.linha]:
                    atributos_alterados = atributos_alterados +"Denominação "
                if self.localidade != DF_pai["Localidade"][self.linha]:
                    atributos_alterados = atributos_alterados +"Localidade "
                if var_detentor_OK.get() != DF_pai["Detentor"][self.linha]:
                    atributos_alterados = atributos_alterados +"Detentor"
                if var_condi_OK.get() != DF_pai["Estado"][self.linha]:
                    atributos_alterados = atributos_alterados +"Estado"
                self.dado_OK.append(atributos_alterados)
        else:
            self.dado_OK = len(colunas_baixa)*[""]
            self.dado_OK[colunas_baixa.index("Tombamento")] = var_tomb_m.get()
            self.dado_OK[colunas_baixa.index("Detentor")] = var_detentor_OK.get()
            self.dado_OK[colunas_baixa.index("Denominação")] = var_descri_OK.get()
            self.dado_OK[colunas_baixa.index("Localidade")] = self.localidade
            self.dado_OK[colunas_baixa.index("Estado")] = self.condi_OK.get()
            self.dado_OK[colunas_baixa.index("Obs.")] = self.obs_OK.get(1.0, "end-1c")
            self.dado_OK[colunas_baixa.index("Consta no DF_pai")] = "Não"
        tratar.inserir_tree_dic(tree_baixa, dic_tree_baixa, self.dado_OK)
        self.jan_tudoOK_none()
    
    def inserir_dado_OK(self):
        if self.linha != None:
            if var_descri_OK.get() == DF_pai["Denominação"][self.linha] and self.localidade == DF_pai["Localidade"][self.linha] and var_detentor_OK.get() == DF_pai["Detentor"][self.linha] and var_condi_OK.get() == DF_pai["Estado"][self.linha]:
                tratar.inserir_tree_dic(tree_OK, dic_tree_OK, self.dado_OK)
            else:
                self.dado_OK.append("")
                atributos_alterados = ""
                if var_descri_OK.get() != DF_pai["Denominação"][self.linha]:
                    atributos_alterados = atributos_alterados +"Denominação "
                if self.localidade != DF_pai["Localidade"][self.linha]:
                    atributos_alterados = atributos_alterados +"Localidade "
                if var_detentor_OK.get() != DF_pai["Detentor"][self.linha]:
                    atributos_alterados = atributos_alterados +"Detentor"
                if var_condi_OK.get() != DF_pai["Estado"][self.linha]:
                    atributos_alterados = atributos_alterados +"Estado"
                    
                self.dado_OK[colunas_atualizar.index("Atributos alterados")] = atributos_alterados
                tratar.inserir_tree_dic(tree_atualizar, dic_tree_atualizar, self.dado_OK)
        else:
            tratar.inserir_tree_dic(tree_sr, dic_tree_sr, self.dado_OK)
        self.jan_tudoOK_none()
            
            
    def jan_tudoOK_none(self):
        global jan_tudoOK
        jan_tudoOK.destroy()
        jan_tudoOK = None
        
    def msg_inserir_tomb(self):
        tk.messagebox.showinfo(title = "Tombamento não informado", message = "Informe um tombamento na caixa de texto 'Inserir manualmente' ou escaneie o código de barras.")
        
    def adicionar_label(self, master, text):
        ttk.Label(master, text = text).pack(anchor = "w")
        mycanva.yview_moveto('1.5')
        
    def abrir_jan_save(self, nome_arquivo, mydic):
        global jan_save
        if jan_save == None:
            jan_save = tk.Toplevel()
            jan_save.title("Salvar planilha")
            jan_save.protocol('WM_DELETE_WINDOW', self.jan_save_none)
            jan_save.geometry('+540+300')
            
            label_arquivo = tk.Label(jan_save, text = "Nome do arquivo")
            label_arquivo.grid(row =1 , column = 0)
            
            var_entry_arquivo.set(nome_arquivo) 
            entry_arquivo = tk.Entry(jan_save, textvar = var_entry_arquivo)
            entry_arquivo.grid(row = 1, column =1)

            lista_extens = [".xlsx"]
            exten = tk.OptionMenu(jan_save, var_exten, *lista_extens)
            exten.grid(row = 1, column = 2)
            
            bt_save = tk.Button(jan_save, text = "Salvar", command = lambda: tratar.salvar_df(mydic, var_entry_arquivo.get()))
            bt_save.grid(row = 2, column =0, columnspan =2 , padx = 5, pady = 5)
            
        
    def jan_save_none(self):
        global jan_save
        jan_save.destroy()
        jan_save = None
        
        
        
    def abrir_salvar_pasta (self):
        global jan_salvar_pasta
        if jan_salvar_pasta == None:
            jan_salvar_pasta = tk.Toplevel()
            jan_salvar_pasta.title("Salvar em uma nova pasta")
            jan_salvar_pasta.protocol('WM_DELETE_WINDOW', self.jan_salvar_pasta_none)
            jan_salvar_pasta.geometry("+570+250")
            
            tk.Label(jan_salvar_pasta, text = "Nome da pasta").grid(row = 0, column = 0, pady = 10)
            
            entry_salvar_pasta = tk.Entry(jan_salvar_pasta, textvar = var_entry_salvar_pasta)
            entry_salvar_pasta.grid(row = 0, column = 1, pady =10)
            
            
            label_salvar_OK = tk.Label(jan_salvar_pasta, text = "Tudo OK")
            label_salvar_OK.grid(row = 1 , column = 0)
            
            entry_salvar_OK = tk.Entry(jan_salvar_pasta, textvar = var_entry_salvar_OK)
            entry_salvar_OK.grid(row = 1 , column = 1)
            
            
            
            label_salvar_atualizar = tk.Label(jan_salvar_pasta, text = "Atualizar")
            label_salvar_atualizar.grid(row = 2 , column = 0)
            
            entry_salvar_atualizar = tk.Entry(jan_salvar_pasta, textvar = var_entry_salvar_atualizar)
            entry_salvar_atualizar.grid(row = 2 , column = 1)
            
            
            
            label_salvar_sr = tk.Label(jan_salvar_pasta, text = "Sem registro")
            label_salvar_sr.grid(row = 3 , column = 0)
            
            entry_salvar_sr = tk.Entry(jan_salvar_pasta, textvar = var_entry_salvar_sr)
            entry_salvar_sr.grid(row = 3 , column = 1)
            
            
            
            label_salvar_se = tk.Label(jan_salvar_pasta, text = "Sem etiqueta")
            label_salvar_se.grid(row = 4 , column = 0)
            
            entry_salvar_se = tk.Entry(jan_salvar_pasta, textvar = var_entry_salvar_se)
            entry_salvar_se.grid(row = 4 , column = 1)
            
            
            
            label_salvar_baixa = tk.Label(jan_salvar_pasta, text = "Dar baixa")
            label_salvar_baixa.grid(row = 5 , column = 0)
            
            entry_salvar_baixa = tk.Entry(jan_salvar_pasta, textvar = var_entry_salvar_baixa)
            entry_salvar_baixa.grid(row = 5 , column = 1)
            
            
            
            label_salvar_oq_falta = tk.Label(jan_salvar_pasta, text = "Não encontrado")
            label_salvar_oq_falta.grid(row = 6 , column = 0)
            
            entry_salvar_oq_falta = tk.Entry(jan_salvar_pasta, textvar =var_entry_salvar_oq_falta)
            entry_salvar_oq_falta.grid(row = 6 , column = 1)
            
            
            
            bt_salvar_pasta = tk.Button(jan_salvar_pasta, text = "Salvar pasta", command = app.salvar_pasta)
            bt_salvar_pasta.grid(row = 7 , column = 0, columnspan = 2, padx = 5, pady = 5)
        
    def jan_salvar_pasta_none(self):
        global jan_salvar_pasta
        jan_salvar_pasta.destroy()
        jan_salvar_pasta = None
        
    def salvar_pasta(self):
        os.chdir("LEVANTAMENTO_PATRIMONIAL")
        self.df_OK = pd.DataFrame(dic_tree_OK)
        self.df_atualizar = pd.DataFrame(dic_tree_atualizar)
        self.df_sr = pd.DataFrame(dic_tree_sr)
        self.df_se = pd.DataFrame(dic_tree_se)
        self.df_baixa = pd.DataFrame(dic_tree_baixa)
        self.df_oq_falta = pd.DataFrame(dic_oq_falta)
      
        
        if var_entry_salvar_pasta.get() == "":
            tk.messagebox.showerror(title="Erro", message="Dê um nome para a pasta.")
            

        elif var_entry_salvar_OK.get() == "" or var_entry_salvar_atualizar.get() == "" or var_entry_salvar_se.get() == "" or var_entry_salvar_baixa.get() == "":
            tk.messagebox.showerror(title="Erro", message="Todos os arquivos devem ter nome.")
            
        else:
            os.makedirs(var_entry_salvar_pasta.get())
            self.df_OK.to_excel(var_entry_salvar_pasta.get()+ "/" + var_entry_salvar_OK.get()+".xlsx")
            self.df_atualizar.to_excel(var_entry_salvar_pasta.get()+ "/" + var_entry_salvar_atualizar.get()+".xlsx")
            self.df_sr.to_excel(var_entry_salvar_pasta.get()+ "/" + var_entry_salvar_sr.get()+".xlsx")
            self.df_se.to_excel(var_entry_salvar_pasta.get()+ "/" + var_entry_salvar_se.get()+".xlsx")
            self.df_baixa.to_excel(var_entry_salvar_pasta.get()+ "/" + var_entry_salvar_baixa.get()+".xlsx")
            self.df_oq_falta.to_excel(var_entry_salvar_pasta.get()+ "/" + var_entry_salvar_oq_falta.get()+".xlsx")
            self.jan_salvar_pasta_none()
            
        os.chdir("..")
        os.chdir("LEVANTAMENTO_PATRIMONIAL")
        arqs = os.listdir()
        print(arqs)
        for arq in arqs:
            if arq != var_entry_salvar_pasta.get():
                with open(arq + "/" + "LOCAIS_SELECIONADOS.txt", "r", encoding = "ISO-8859-1") as locs_sel:
                    locs = locs_sel.read()
                    if "\n" in locs:
                        list_locs = locs.split("\n")
                    else:
                        list_locs = [locs]
                    print(arq)
                    print(list_locs)
                oq_falta = pd.concat([DF_n_encontrado[DF_n_encontrado["Localidade"].str.contains(loc)]  for loc in list_locs])
                oq_falta.to_excel(arq + "/" "NAO_ENCONTRADO.xlsx")
            
        
        self.locais = open(var_entry_salvar_pasta.get()+ "/" + "LOCAIS_SELECIONADOS.txt", "w")
        for loc in locais_selecionados:
            self.locais.write(loc + '\n')
        self.locais.close()
        
        os.chdir("..")
        
        DF_n_encontrado.to_excel("PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx")
        
        

        
    def abrir_pasta(self):
        self.pasta = tk.filedialog.askdirectory()
        self.files = os.listdir(self.pasta)
        print(self.files)

        self.funcs = {"Tudo OK":[], "Atualizar": [], "Sem registro": [], "Sem etiqueta": [], "Dar baixa": []}
    
        for  file in self.files:
            if file != "LOCAIS_SELECIONADOS.txt" and file != "NAO_ENCONTRADO.xlsx":
                df = pd.read_excel(self.pasta + "/" + file).drop(columns = ["Unnamed: 0"])
                if "Tombamento" not in list(df.columns):
                    self.funcs["Sem etiqueta"].append(df)
                    self.funcs["Sem etiqueta"].append(file)
                elif "Motivo para baixa" in list(df.columns):
                    self.funcs["Dar baixa"].append(df)
                    self.funcs["Dar baixa"].append(file)
                elif ("Atributos alterados" in list(df.columns)) and ("Motivo para baixa" not in list(df.columns)):
                    self.funcs["Atualizar"].append(df)
                    self.funcs["Atualizar"].append(file)
                elif list(df.columns) == ["Tombamento", "Denominação", "Detentor", "Localidade", "Estado", "Obs."]:
                    self.funcs["Sem registro"].append(df)
                    self.funcs["Sem registro"].append(file)
                else:
                    self.funcs["Tudo OK"].append(df)
                    self.funcs["Tudo OK"].append(file)
        global locais_selecionados
        try:   
            with open(self.pasta + "/LOCAIS_SELECIONADOS.txt", "r", encoding = "utf-8") as locs_sel:
                locs = locs_sel.read()
                if "\n" in locs:
                    locais_selecionados = locs.split("\n")[:-1]
                else:
                    locais_selecionados = [locs]
                print("loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooocs = ", locais_selecionados)
        except:
            with open(self.pasta + "/LOCAIS_SELECIONADOS.txt", "r", encoding = "ISO-8859-1") as locs_sel:
                locs = locs_sel.read()
                if "\n" in locs:
                    locais_selecionados = locs.split("\n")[:-1]
                else:
                    locais_selecionados = [locs]
                print("loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooocs = ", locais_selecionados)
        for loc in locais_selecionados:
            app.lista_oq_falta(loc)
                
        dic_OK = self.funcs["Tudo OK"][0].to_dict("list")
        dic_atualizar = self.funcs["Atualizar"][0].to_dict("list")
        dic_sr = self.funcs["Sem registro"][0].to_dict("list")
        dic_se = self.funcs["Sem etiqueta"][0].to_dict("list")
        dic_baixa = self.funcs["Dar baixa"][0].to_dict("list")
        #dic_n_encontrado = self.funcs["Não encontrado"][0].to_dict("list")
        
        self.dist1(dic_OK, dic_tree_OK, tree_OK)
        self.dist1(dic_atualizar, dic_tree_atualizar, tree_atualizar)
        self.dist1(dic_sr, dic_tree_sr, tree_sr)
        self.dist1(dic_se, dic_tree_se, tree_se)
        self.dist1(dic_baixa, dic_tree_baixa, tree_baixa)
       
    def dist1(self, dic_i, dic_f, tree):
        for i in range(len(dic_i[list(dic_i.keys())[0]])):
            dado = []
            for key in dic_i:
                dado.append(dic_i[key][i])
            tratar.inserir_tree_dic(tree, dic_f, dado)
    
    def atualizar_tudo(self):
        global tudo
        tudo = True
        res = tk.messagebox.askyesno(title = "Atualizar tudo", message = f"Você realmente deseja que os arquivos da pasta {self.pasta} sejam atualizados?")

        if res == True:
            self.abrir_atua_file(tree_OK)
            self.abrir_atua_file(tree_se)
            self.abrir_atua_file(tree_sr)
            self.abrir_atua_file(tree_baixa)
            self.abrir_atua_file(tree_atualizar)
        tudo = False
        
        print("dirrrrrrrr ",os.listdir())
        
        os.chdir("LEVANTAMENTO_PATRIMONIAL")
        arqs = os.listdir()
        print(arqs)
        for arq in arqs:
            if arq != self.pasta:
                with open(arq + "/" + "LOCAIS_SELECIONADOS.txt", "r", encoding = "ISO-8859-1") as locs_sel:
                    locs = locs_sel.read()
                    if "\n" in locs:
                        list_locs = locs.split("\n")[:-1]
                    else:
                        list_locs = [locs]
                    print(arq)
                    print(list_locs)
                oq_falta = pd.concat([DF_n_encontrado[DF_n_encontrado["Localidade"].str.contains(loc)]  for loc in list_locs])
                oq_falta.loc[:, ["Denominação", "Detentor", "Tombamento", "Localidade"]].to_excel(arq + "/" "NAO_ENCONTRADO.xlsx")

        self.locais = open(self.pasta + "/" + "LOCAIS_SELECIONADOS.txt", "w")
        for loc in locais_selecionados:
            self.locais.write(loc + '\n')
        self.locais.close()
        
        os.chdir("..")
        
        DF_n_encontrado.to_excel("PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx")
        
    def abrir_atua_file(self, tree):
        print(tree)
        arq = self.funcs[tratar.nome_tree(tree)][1]
        if tratar.nome_tree(tree) == "Tudo OK":
            mydic = dic_tree_OK
        elif tratar.nome_tree(tree) == "Atualizar":
            mydic = dic_tree_atualizar
        elif tratar.nome_tree(tree) == "Sem etiqueta":
            mydic = dic_tree_se
        elif tratar.nome_tree(tree) == "Dar baixa":
            mydic = dic_tree_baixa
        elif tratar.nome_tree(tree) == "Sem registro":
            mydic = dic_tree_sr
        elif tratar.nome_tree(tree) == "Não encontrado":
            mydic = dic_oq_falta
        global tudo
        if tudo == False:
            res = tk.messagebox.askyesno(title = "Atualizar arquivo", message = f"Você realmente deseja que os dados desta Treeview sejam escritos no arquivo {arq}?")
            if res == True:
                tratar.atualizar_arquivo(mydic, self.pasta + "/" + arq)
        else:
            tratar.atualizar_arquivo(mydic, self.pasta + "/" + arq)
            
    def lista_oq_falta(self, local):
        print("local = ", local)
        if local != '':
            print('lista_SIPAC', lista_SIPAC)
            local_SIPAC = lista_SIPAC[lista_descris.index(local)]

            if local not in locais_selecionados:
                locais_selecionados.append(local)
                locais_selecionados_completo.append(local_SIPAC)

            global df_oq_falta
            df_oq_falta = pd.concat([df_oq_falta, DF_n_encontrado[DF_n_encontrado["Localidade"]==local_SIPAC]])
            df_local = df_oq_falta[df_oq_falta["Localidade"]==local_SIPAC]
            print(df_local)
            print(df_local["Tombamento"])
            for i in list(df_local.index):
                dado = list(df_local.loc[i, ["Denominação", "Detentor", "Tombamento", "Localidade"]])
                print(dado)
                tratar.inserir_tree_dic(tree_oq_falta, dic_oq_falta, dado)
            app.adicionar_label(myframe, f"Local {local} selecionado")

            lb_locais["text"] = lb_locais["text"] + "\n" + str(local_SIPAC)
            global quant_n
            global df_locs_sel
            df_locs_sel = pd.concat([df_locs_sel, DF_pai[DF_pai["Localidade"] == local_SIPAC]])
            quant_n = df_locs_sel.shape[0]
            lb_quant["text"] = f"Quantidade total de bens: {quant_n}"
        
        
    def pesquisar(self, tree, coluna_tomb, coluna_descri, valor):
        try:
            coluna_str = [str(i) for i in coluna_tomb]
            
            for dig in valor:
                if dig.isnumeric() == False:
                    coluna_str = coluna_descri
                    break
            ind = [i for i, x in enumerate(coluna_str) if x ==valor]
            itens = []
            for item in tree.get_children():
                if tree.index(item) in ind:
                    itens.append(item)
            tree.selection_set(*itens)
            print(itens)
            if itens == []:
                tk.messagebox.showinfo(title= "Pesquisa não encontrada", message = "Não consguimos encontrar o que você pesquisou.")
            else:
                tree.see(itens[0])
        except:
            tk.messagebox.showinfo(title= "Pesquisa não encontrada", message = "Não consguimos encontrar o que você pesquisou.")
                
                
class Tratar_dados():
    
    def apenas_numeros(self,x):
        if x.isnumeric()==True:
            return True
        else:
            return False
        
    def filtrar_numeros(self, x):
        return "".join(filter(self.apenas_numeros, x)).strip()
    
    def checar_no_pai(self, x, coluna, pai): #retorna a lista com os índices de onde ocorre a igualdade
        if x in list(pai[coluna]):
            return pai[pai[coluna]==x].index.tolist()[0]
        else:
            return None
        
    def separar_nums(self, num):
        v = []
        for i in range(len(str(num))):
            v.append(str(num)[i])
        return " ".join(v)
     
    def inserir_tree_dic(self, tree, dicionario, dado):
        tree.insert("", "end", values = tuple(dado))
        indice = 0
        for atributo in list(dicionario.keys()):
            dicionario[atributo].append(dado[indice])
            indice+=1
        
        if tree != tree_oq_falta:
            if tree != tree_se:
                app.adicionar_label(myframe, f"Tombamento {Entry_tomb_m.get()} adicionado à Treeview {tratar.nome_tree(tree)}")
            else:
                app.adicionar_label(myframe, f"Item {dicionario['Denominação'][-1]} adicionado à Treeview {tratar.nome_tree(tree)}")
            
            global DF_n_encontrado  
            if tree != tree_se:
                try:
                    if str(dicionario["Tombamento"][-1]) in dic_oq_falta["Tombamento"] or int(dicionario["Tombamento"][-1]) in dic_oq_falta["Tombamento"]:
                        if str(dicionario["Tombamento"][-1]) in dic_oq_falta["Tombamento"]:
                            i = dic_oq_falta["Tombamento"].index(str(dicionario["Tombamento"][-1]))
                        else:
                            i = dic_oq_falta["Tombamento"].index(int(dicionario["Tombamento"][-1]))
                        for key in list(dic_oq_falta.keys()):
                            del(dic_oq_falta[key][i])
                        tree_oq_falta.delete(*tree_oq_falta.get_children())
                        linha = DF_n_encontrado.index[DF_n_encontrado["Tombamento"] == str(dicionario["Tombamento"][-1])].tolist()
                        print("linha = ", linha)
                        DF_n_encontrado = DF_n_encontrado.drop(linha[0], axis = 0)
                        for i in range(len(dic_oq_falta[list(dic_oq_falta.keys())[0]])):
                            tree_oq_falta.insert("", "end", values = tuple([dic_oq_falta[key][i] for key in list(dic_oq_falta.keys())]))
                    if dicionario["Tombamento"][-1] != "Sem etiqueta":
                        if str(dicionario["Tombamento"][-1]) in list(DF_n_encontrado["Tombamento"]) or int(dicionario["Tombamento"][-1]) in list(DF_n_encontrado["Tombamento"]):
                            linha = DF_n_encontrado.index[DF_n_encontrado["Tombamento"] == str(dicionario["Tombamento"][-1])].tolist()
                            print("linha = ", linha)
                            DF_n_encontrado = DF_n_encontrado.drop(linha[0], axis = 0)
                except:
                    if str(dicionario["Tombamento"][-1]) in dic_oq_falta["Tombamento"]:
                        i = dic_oq_falta["Tombamento"].index(str(dicionario["Tombamento"][-1]))
                        for key in list(dic_oq_falta.keys()):
                            del(dic_oq_falta[key][i])
                        tree_oq_falta.delete(*tree_oq_falta.get_children())
                        #global DF_n_encontrado
                        linha = DF_n_encontrado.index[DF_n_encontrado["Tombamento"] == str(dicionario["Tombamento"][-1])].tolist()
                        print("linha = ", linha)
                        DF_n_encontrado = DF_n_encontrado.drop(linha[0], axis = 0)
                        for i in range(len(dic_oq_falta[list(dic_oq_falta.keys())[0]])):
                            tree_oq_falta.insert("", "end", values = tuple([dic_oq_falta[key][i] for key in list(dic_oq_falta.keys())]))
                    if dicionario["Tombamento"][-1] != "Sem etiqueta":
                        if str(dicionario["Tombamento"][-1]) in list(DF_n_encontrado["Tombamento"]) or int(dicionario["Tombamento"][-1]) in list(DF_n_encontrado["Tombamento"]):
                            linha = DF_n_encontrado.index[DF_n_encontrado["Tombamento"] == str(dicionario["Tombamento"][-1])].tolist()
                            print("linha = ", linha)
                            DF_n_encontrado = DF_n_encontrado.drop(linha[0], axis = 0)
                        
        global descri_anterior
        global local_anterior
        global detentor_anterior
        global condi_anterior
        
        if tree != tree_oq_falta:
            descri_anterior = dicionario["Denominação"][-1]
            if " - " in dicionario["Localidade"][-1]:
                cod_local, local_anterior = dicionario["Localidade"][-1].split(" - ", maxsplit = 1)
            else:
                local_anterior = dicionario["Localidade"][-1]
            detentor_anterior = dicionario["Detentor"][-1]
            condi_anterior = dicionario["Estado"][-1]
        
        var_tomb_m.set("")
        
        var_etiqueta.set(0)
        
        self.quant_bens()
            
    def deletar_tree_dic(self, tree, dicionario, dados):
        global DF_n_encontrado
        dados = list(dados)
        dados.reverse()
        for dado in dados:
            ind = tree.index(dado)
            tree.delete(dado)
            if tree != tree_se:
                tomb = dicionario["Tombamento"][ind]
                if  dicionario["Localidade"][ind].startswith("11010116_"):
                    codigo, descri = dicionario["Localidade"][ind].split(" - ", maxsplit = 1)
                else:
                    descri = dicionario["Localidade"][ind]
                if descri in locais_selecionados:
                    self.inserir_tree_dic(tree_oq_falta, dic_oq_falta, (dicionario["Denominação"][ind], dicionario["Detentor"][ind], dicionario["Tombamento"][ind], dicionario["Localidade"][ind]))
                    index = nv_DF_pai.index[nv_DF_pai["Tombamento"] == str(tomb)].tolist()
                    print('index', index)
                    try:
                        DF_n_encontrado.loc[index[0]] = nv_DF_pai.loc[index[0]]
                        DF_n_encontrado = DF_n_encontrado.sort_index()
                    except:
                        pass
            for key in dicionario:
                del(dicionario[key][ind])
            if tree != tree_se:    
                app.adicionar_label(myframe, f"Tombamento {tomb} deletado da Treeview {tratar.nome_tree(tree)}")
    
        self.quant_bens()
        
    def quant_bens(self):
        quant_bens_encontrados = len(dic_tree_OK["Tombamento"]) + len(dic_tree_atualizar["Tombamento"]) + len(dic_tree_baixa["Tombamento"]) + len(dic_tree_sr["Tombamento"]) + len(dic_tree_se["Denominação"])
        lb_quant_en["text"] = f"Quantidade de bens encontrados: {quant_bens_encontrados}"
        
        
        lb_quant_n["text"] = f"Quantidade de bens não encontrados: {len(dic_oq_falta['Tombamento'])}"
        
    
    def limpar_tree_dic(self, tree, dic):
        res = tk.messagebox.askyesno(title = "Limpar treeview", message = "Tem certeza que quer limpar a treeview dos bens que faltam ser encontrados nesse local?")
        if res == True:
            for key in list(dic.keys()):
                dic[key]=[]
            tree.delete(*tree.get_children())
            lb_locais["text"] = "Locais selecionados:"
            app.adicionar_label(myframe, "A treeview 'O que falta nesse local?' foi limpa")
            global df_oq_falta
            df_oq_falta = None
    
    def salvar_df(self, mydic, arquivo):
        self.df = pd.DataFrame(mydic)
        if var_exten.get() == ".xlsx":
            self.df.to_excel(arquivo+".xlsx")
        else:
            self.df.to_csv(arquivo+".csv", sep=';', encoding='utf-8')
        var_entry_arquivo.set("")
        app.jan_save_none()
        
        
    def nome_tree(self, tree):
        nome_tree = ""
        if tree == tree_OK:
            nome_tree = "Tudo OK"
        elif tree == tree_atualizar:
            nome_tree = "Atualizar"
        elif tree == tree_baixa:
            nome_tree = "Dar baixa"
        elif tree == tree_se:
            nome_tree = "Sem etiqueta"
        elif tree == tree_sr:
            nome_tree = "Sem registro"
        elif tree == tree_oq_falta:
            nome_tree = "Não encontrado"
        return nome_tree
    
    def atualizar_arquivo(self, mydic, arq):
        df = pd.DataFrame(mydic)
        df.to_excel(arq)
        
            
    def tirar_nulos(self, v):
        inds = []
        for i in range(len(v)):
            if pd.isnull(v[i]) == True:
                inds.append(i)
        inds.reverse()
        for ind in inds:
            del(v[ind])
        return v
        
    
    
        
        
        
class Elisa():
    def ouvir(self, func):
        with sr.Microphone() as source:
            print("Diga")
            func()
            self.ouvido = sr.Recognizer()
            self.audio = self.ouvido.listen(source)
            #try:
            self.frase = self.ouvido.recognize_google(self.audio, language = "pt-br")
            #except:
            print(self.frase)
            #    self.frase = ""
        self.reconhecer()
        
    def reconhecer(self):
        if self.frase != "":
            try:
                print(self.frase)
            except:
                print("Não consegui entender")
        else:
            print('Não ouvi nada')
                
    def ouvir_tombamento(self):
        self.ouvir(self.top)
        var_tomb_m.set(self.frase)
        app.append_DF_tudoOK(Entry_tomb_m.get()) if Entry_tomb_m.get() !="" else app.msg_inserir_tomb()
        global top_ouvir_tomb
        top_ouvir_tomb.destroy()
    
    def top(self):
        global top_ouvir_tomb
        top_ouvir_tomb = tk.Toplevel()
        top_ouvir_tomb.title("Ouvindo...")
        top_ouvir_tomb.geometry('+570+300')
        top_ouvir_tomb.focus_force()
        tk.Label(top_ouvir_tomb, text = "Diga o tombamento em voz alta...", font = 'bold').pack(padx = 15, pady = 15)
        top_ouvir_tomb.update()
        janela.update()
        
class Configurar():
    def config_msg(self):
        res = tk.messagebox.askyesno(title = "Configurar mensagem inicial", message = "Quer que apareça a mensagem de ações recomendadas ao iniciar o programa?")
        if res == True:
            config["Mensagem Inicial"][0] = "Sim"
        else:
            config["Mensagem Inicial"][0] = "Não"
        config.to_excel("config.xlsx")
        
    def config_voz_som(self):
        jan_som = tk.Toplevel()
        jan_som.title("Configurar voz e som")
        
        tk.Checkbutton(jan_som, text = "Falar tombamento", variable = var_som_tomb, command = self.config_falar_tomb).pack()
        
    def config_falar_tomb(self):
        if var_som_tomb.get() == 1:
            return True
        else:
            return False
            
#Classes
app = Aplicativo()
assist = Elisa()
tratar = Tratar_dados()
configurar = Configurar()

#Variáveis
Lista_tombamentos = [1, 2]

#Configurações
config = pd.read_excel("config.xlsx")

#DF_pai
DF_pai = pd.read_csv("PLANILHAS_GERAIS/relatorio_bens.csv", encoding = "utf-8", sep = ";")
DF_pai = DF_pai.drop(columns = ["Unnamed: 25"])

colunas_pai = list(DF_pai.columns)

dic_pai = DF_pai.to_dict("list")
nv_DF_pai = DF_pai
for i in range(len(nv_DF_pai["Tombamento"])):
    nv_DF_pai["Tombamento"][i] = tratar.filtrar_numeros(nv_DF_pai["Tombamento"][i])
nv_DF_pai = nv_DF_pai.fillna("")

def n_info(loc):
    if loc == "":
        return "Não informado"
    else:
        return loc
    
nv_DF_pai["Localidade"] = [n_info(loc) for loc in nv_DF_pai["Localidade"]]
    
nv_DF_pai.to_excel("PLANILHAS_GERAIS/novo_relatorio_bens.xlsx")
DF_n_encontrado = pd.read_excel("PLANILHAS_GERAIS/NAO_ENCONTRADO_GERAL.xlsx")
DF_n_encontrado["Tombamento"] = [str(list(DF_n_encontrado["Tombamento"])[i]) for i in range(len(list(DF_n_encontrado["Tombamento"])))]
DF_n_encontrado.index = list(DF_n_encontrado["Unnamed: 0"])
if "Unnamed: 0" in list(DF_n_encontrado.columns):
    DF_n_encontrado = DF_n_encontrado.drop(columns = ["Unnamed: 0"])
if "Unnamed: 25" in list(DF_n_encontrado.columns):
    DF_n_encontrado = DF_n_encontrado.drop(columns = ["Unnamed: 25"])

df_oq_falta = DF_pai[DF_pai["Tombamento"] == "Oi"]

df_locs_sel = DF_pai[DF_pai["Tombamento"] == "Oi"]
camera = None

df_tudo_encontrado = pd.read_excel("PLANILHAS_GERAIS/Concats.xlsx")

#TopLevels
jan_sem_tomb = None
jan_tudoOK = None
jan_save = None
jan_salvar_pasta = None
jan_abrir_pasta = None
top_ouvir_tomb = None
jan_local_errado = None
tudo = False

#Aplicativo
janela = tk.Tk()
janela.title("Levantamento Patrimonial")
janela.state("zoomed")
janela.rowconfigure(0, minsize = 3000)

#Ícones
img_save = Image.open("Imagens/save_icon.png")
img_save = img_save.resize((30,30))
save_icon = ImageTk.PhotoImage(img_save)

img_atualizar = Image.open("Imagens/atualizar_icon.png")
img_atualizar = img_atualizar.resize((30,30))
atualizar_icon = ImageTk.PhotoImage(img_atualizar)

img_mic = Image.open("Imagens/mic_icon.png")
img_mic = img_mic.resize((20,20))
mic_icon = ImageTk.PhotoImage(img_mic)

#Variáveis
var_check = tk.IntVar()
var_check.set(0)

var_etiqueta = tk.IntVar()
var_etiqueta.set(0)
 
var_tomb_m = tk.StringVar()

var_descri_m = tk.StringVar()

var_local_st = tk.StringVar()
var_descri_st = tk.StringVar()
var_detentor_st = tk.StringVar()
var_condi_st = tk.StringVar()
var_baixa_st = tk.IntVar()

var_local_OK = tk.StringVar()
var_descri_OK = tk.StringVar()
var_detentor_OK = tk.StringVar()
var_condi_OK = tk.StringVar()
var_baixa_OK = tk.IntVar()
var_baixa_OK.set(0)
var_entry_arquivo = tk.StringVar()
var_exten = tk.StringVar()
var_exten.set(".xlsx")

var_opt_descri_OK = tk.StringVar()
var_opt_descri_OK.set("Registro na base de dados")
var_opt_local_OK = tk.StringVar()
var_opt_local_OK.set("Registro na base de dados")
var_opt_detentor_OK = tk.StringVar()
var_opt_detentor_OK.set("Registro na base de dados")
var_opt_condi_OK = tk.StringVar()
var_opt_condi_OK.set("Registro na base de dados")

var_entry_salvar_OK= tk.StringVar()
var_entry_salvar_atualizar= tk.StringVar()
var_entry_salvar_sr = tk.StringVar()
var_entry_salvar_se= tk.StringVar()
var_entry_salvar_baixa= tk.StringVar()
var_entry_salvar_oq_falta = tk.StringVar()
var_entry_salvar_pasta= tk.StringVar()

var_entry_salvar_OK.set("OK")
var_entry_salvar_atualizar.set("ATUALIZAR")
var_entry_salvar_sr.set("SEM_REGISTRO")
var_entry_salvar_se.set("SEM_ETIQUETA")
var_entry_salvar_baixa.set("DAR_BAIXA")
var_entry_salvar_oq_falta.set("NAO_ENCONTRADO")

pesq_OK = tk.StringVar()
pesq_AT = tk.StringVar()
pesq_SR = tk.StringVar()
pesq_SE = tk.StringVar()
pesq_BA = tk.StringVar()

var_outro_local = tk.StringVar()
var_outro_local_st = tk.StringVar()

var_local_antigo = tk.StringVar()

var_som_tomb = tk.IntVar()
var_som_tomb.set(1)

configurar.config_falar_tomb()

descri_anterior = ""
local_anterior = ""
detentor_anterior = ""
condi_anterior = ""


#Abas
Notebook = ttk.Notebook(janela)
Notebook.pack()
aba_menu = ttk.Frame(Notebook)
aba_OK = ttk.Frame(Notebook)
aba_sem_etiqueta = ttk.Frame(Notebook)
aba_baixa = ttk.Frame(Notebook)
aba_atualizar = ttk.Frame(Notebook, width =20)
aba_sr = ttk.Frame(Notebook)

Notebook.add(aba_menu, text = "Menu")
Notebook.add(aba_OK, text = "Tudo OK")
Notebook.add(aba_atualizar, text = "Atualizar")
Notebook.add(aba_sr, text = "Sem registro")
Notebook.add(aba_sem_etiqueta, text = "Sem etiqueta")
Notebook.add(aba_baixa, text = "Dar baixa")

#Barra de menu
barra_menu=tk.Menu(janela)
menu_Arquivo=tk.Menu(barra_menu, tearoff=0)
menu_Arquivo.add_command(label="Abrir pasta", command = app.abrir_pasta)
menu_Arquivo.add_command(label="Abrir arquivo")
menu_Arquivo.add_command(label="Salvar tudo em uma nova pasta", command = app.abrir_salvar_pasta)
menu_Arquivo.add_command(label="Atualizar todas os arquivos associados", command = app.atualizar_tudo)
barra_menu.add_cascade(label="Arquivo", menu=menu_Arquivo)


menu_config=tk.Menu(barra_menu, tearoff=0)
menu_config.add_command(label="Voz e som", command = configurar.config_voz_som)
menu_config.add_command(label="Mensagem ao iniciar", command = configurar.config_msg)
barra_menu.add_cascade(label="Configurações", menu=menu_config)
janela.config(menu=barra_menu)


#Denominação
lista_bens = []
for bem in list(DF_pai["Denominação"]):
    if bem not in lista_bens:
        lista_bens.append(bem)


#Detentor
lista_detentores = []
for detentor in list(DF_pai["Detentor"]):
    if detentor not in lista_detentores:
        lista_detentores.append(detentor)
lista_detentores = tratar.tirar_nulos(lista_detentores)


#Frame local
Frame_local = ttk.LabelFrame(aba_menu, text = "O que falta nesse local?", height =80)
Frame_local.pack(side = tk.LEFT, fill ="y", expand ="yes", padx=5)

Frame_tree = tk.Frame(Frame_local)
Frame_tree.pack(fill = "both", expand = "yes", side = tk.BOTTOM)

colunas_oq_falta = ["Denominação", "Detentor", "Tombamento", "Localidade"]

scrollx_local = ttk.Scrollbar(Frame_tree, orient="horizontal")
scrollx_local.pack(side = tk.BOTTOM, fill = "x")
scrolly_local = ttk.Scrollbar(Frame_tree, orient="vertical")
scrolly_local.pack(side = tk.RIGHT, fill = "y")
        
tree_oq_falta =  ttk.Treeview(Frame_tree, columns= colunas_oq_falta, show='headings', xscrollcommand = scrollx_local.set, yscrollcommand = scrolly_local.set)
tree_oq_falta.pack(fill = "both", expand = "yes")

bt_exc_loc = tk.Button(Frame_local, text = "Limpar treeview", command = lambda: tratar.limpar_tree_dic(tree_oq_falta, dic_oq_falta))
bt_exc_loc.pack(side = "right")

Frame_control_local = tk.Frame(Frame_local)
Frame_control_local.pack(side = "left")


scrollx_local.config(command = tree_oq_falta.xview)
scrolly_local.config(command = tree_oq_falta.yview)

for i in colunas_oq_falta:
    tree_oq_falta.column(i, anchor="w", stretch=True, width = 50, minwidth =150)
    tree_oq_falta.heading(i, text=i)
dic_oq_falta = {"Denominação":[], "Detentor": [], "Tombamento": [], "Localidade": []}

planilha_locais_antigos = pd.read_excel("PLANILHAS_LOCALIDADES/Lista_locais_IF.xlsx")
lista_SIPAC = list(planilha_locais_antigos["Registros no SIPAC"])
lista_descris = list(planilha_locais_antigos["Descrição"])
df_tdd = DF_n_encontrado[["Denominação", "Detentor", "Tombamento", "Localidade"]]


tk.Label(Frame_control_local, text = "Selecionar Local").grid(row = 0, column =0)
option_locais = tk.OptionMenu(Frame_control_local, var_local_antigo, *lista_descris)
option_locais.grid(row = 0, column = 1)
bt_local = tk.Button(Frame_control_local, text = "Adicionar local selecionado", width = 20 ,  command =lambda: app.lista_oq_falta(var_local_antigo.get()) )
bt_local.grid(row = 0, column = 2, pady = 10)
lb_locais = tk.Label(Frame_control_local, text = "Locais selecionados:", anchor = "w", justify =tk.LEFT)
lb_locais.grid(row = 1, column = 0, columnspan = 3, stick = "w")

Frame_bt_local = tk.Frame(Frame_control_local)
Frame_bt_local.grid(row = 2, column =0, columnspan =3, stick = "w")

bt_salvar_oq_falta= ttk.Button(Frame_bt_local, image = save_icon, width = 90, command = lambda: app.abrir_jan_save("", dic_oq_falta))
bt_salvar_oq_falta.grid(row =0 , column =0, rowspan = 3)

bt_atualizar_oq_falta= ttk.Button(Frame_bt_local, image = atualizar_icon, width = 90, command =lambda: app.abrir_atua_file(tree_oq_falta))
bt_atualizar_oq_falta.grid(row =0 , column =1, rowspan = 3)

lb_quant = tk.Label(Frame_bt_local)
lb_quant.grid(row = 0, column = 2, stick = "w")

lb_quant_en = tk.Label(Frame_bt_local)
lb_quant_en.grid(row = 1, column = 2, stick = "w")

lb_quant_n = tk.Label(Frame_bt_local)
lb_quant_n.grid(row = 2, column = 2, stick = "w")

quant_n = 0

locais_selecionados = []
locais_selecionados_completo = []


#Novos locais
nv_locais = pd.read_excel("PLANILHAS_LOCALIDADES/Novos_locais.xlsx")
nv_descris = list(nv_locais["Novos locais"])
nv_codes = list(nv_locais["Código"])
nv_cods = []
for code in nv_codes:
    IF, cod = code.split("_")
    nv_cods.append(cod)
    

#Frame tombamento
Frame_tomb = ttk.LabelFrame(aba_menu, text = "Tombamento")
Frame_tomb.pack(side = tk.TOP)
Frame_local.pack(side = tk.LEFT, fill ="both", expand ="yes", padx=5)

Label_tomb_m = ttk.Label(Frame_tomb, text = "Inserir manualmente")
Label_tomb_m.grid(row = 0 , column = 0, stick = "w")

Entry_tomb_m = ttk.Entry(Frame_tomb, textvar = var_tomb_m, width =40)
Entry_tomb_m.grid(row = 0 ,column = 1 , stick = "ew", padx = 5)

bt_mic_tomb = ttk.Button(Frame_tomb, image = mic_icon, command = assist.ouvir_tombamento)
bt_mic_tomb.grid(row = 0, column = 2, stick = "e")

bot_tomb_m = ttk.Button(Frame_tomb, text = "Registrar tombamento", command = lambda: app.append_DF_tudoOK(Entry_tomb_m.get()) if Entry_tomb_m.get() !="" else app.msg_inserir_tomb())
bot_tomb_m.grid(row = 1, column = 0, columnspan = 3, stick = "ew")
Entry_tomb_m.bind("<Return>", bot_tomb_m["command"])

webcam = ttk.Label(Frame_tomb)
webcam.grid(row = 2, column =0, columnspan = 4)

bot_sem_etiq = ttk.Button(Frame_tomb, text = "Bem sem etiqueta de tombamento", command = app.abrir_jan_sem_tomb)
bot_sem_etiq.grid(row = 0 , column = 3 , rowspan =2, stick = "nsew")




#Frame_saida
Frame_saida = ttk.LabelFrame(aba_menu, text = "Saída", width =800)
Frame_saida.pack(side = tk.BOTTOM, fill = "x", padx = 5)
frame_s = ttk.Frame(Frame_saida)

mycanva = tk.Canvas(frame_s)
mycanva.pack(side = tk.LEFT, fill = "x", expand = "yes")

scroll_canva = ttk.Scrollbar(frame_s, orient = "vertical", command = mycanva.yview)
scroll_canva.pack(side = tk.RIGHT, fill = "y")

mycanva.config(yscrollcommand = scroll_canva.set)

myframe = ttk.Frame(mycanva)
mycanva.create_window((0,0), window = myframe, anchor = "nw")

myframe.bind("<Configure>", lambda e: mycanva.configure(scrollregion=mycanva.bbox("all")))

frame_s.pack(fill = "x")

ttk.Label(myframe, text = "").pack(side = tk.BOTTOM)


#aba_tudoOK
frame_botoes_OK = ttk.Frame(aba_OK)
frame_botoes_OK.pack(fill = "x")

bt_salvar_OK= ttk.Button(frame_botoes_OK, image = save_icon, width = 50, command = lambda: app.abrir_jan_save("", dic_tree_OK))
bt_salvar_OK.grid(row =0 , column =0)

bt_atualizar_OK= ttk.Button(frame_botoes_OK, image = atualizar_icon, width = 50, command =lambda: app.abrir_atua_file(tree_OK))
bt_atualizar_OK.grid(row =0 , column =1)

lb_pesq_OK = tk.Label(frame_botoes_OK, text = "Pesquisar")
lb_pesq_OK.grid(row = 0, column = 2)

entry_pesq_OK = tk.Entry(frame_botoes_OK, textvariable = pesq_OK)
entry_pesq_OK.grid(row = 0 , column = 3)


frame_tree_OK = ttk.Frame(aba_OK)
frame_tree_OK.pack()

scrollx_OK = ttk.Scrollbar(frame_tree_OK, orient="horizontal")
scrollx_OK.pack()

scrolly_OK = ttk.Scrollbar(frame_tree_OK, orient="vertical")
scrolly_OK.pack()

colunas_OK = [atributo for atributo in colunas_pai]
colunas_OK.append("Obs.")

tree_OK = ttk.Treeview(frame_tree_OK, columns=colunas_OK, show='headings', height =25)
dic_tree_OK = {}
for coluna in colunas_OK:
    dic_tree_OK[coluna] = []
    
for i in colunas_OK:
    tree_OK.column(i, anchor="w", stretch=True, width = 80, minwidth =300)
    tree_OK.heading(i, text=i)

tree_OK.pack(side = tk.LEFT)
scrollx_OK.pack(fill = "x", side = tk.BOTTOM)
scrollx_OK.config(command = tree_OK.xview)
scrolly_OK.pack(fill = "y", side = tk.RIGHT)
scrolly_OK.config(command = tree_OK.yview)
tree_OK.config(xscrollcommand = scrollx_OK.set)
tree_OK.config(yscrollcommand = scrolly_OK.set)

bot_del_OK = tk.Button(aba_OK, text = "Deletar item", command  = lambda: tratar.deletar_tree_dic(tree_OK, dic_tree_OK, tree_OK.selection()))
bot_del_OK.pack( pady = 10)
tree_OK.bind("<Delete>", bot_del_OK["command"])

bt_pesq_OK = tk.Button(frame_botoes_OK, text = "Pesquisar", command = lambda: app.pesquisar(tree_OK, dic_tree_OK["Tombamento"], dic_tree_OK["Denominação"], entry_pesq_OK.get()))
bt_pesq_OK.grid(row =0, column = 4)


#aba_atualizar
frame_botoes_atualizar = ttk.Frame(aba_atualizar)
frame_botoes_atualizar.pack(fill = "x")

bt_salvar_atualizar= ttk.Button(frame_botoes_atualizar, image = save_icon, width = 50, command = lambda: app.abrir_jan_save("", dic_tree_atualizar))
bt_salvar_atualizar.grid(row =0 , column =0)

bt_atualizar_atualizar= ttk.Button(frame_botoes_atualizar, image = atualizar_icon, width = 50, command =lambda: app.abrir_atua_file(tree_atualizar))
bt_atualizar_atualizar.grid(row =0 , column =1)

lb_pesq_AT = tk.Label(frame_botoes_atualizar, text = "Pesquisar")
lb_pesq_AT.grid(row = 0, column = 2)

entry_pesq_AT = tk.Entry(frame_botoes_atualizar, textvariable = pesq_AT)
entry_pesq_AT.grid(row = 0 , column = 3)

frame_tree_atualizar = ttk.Frame(aba_atualizar)
frame_tree_atualizar.pack()
scrollx_atualizar = ttk.Scrollbar(frame_tree_atualizar, orient="horizontal")
scrollx_atualizar.pack()
scrolly_atualizar = ttk.Scrollbar(frame_tree_atualizar, orient="vertical")
scrolly_atualizar.pack()

colunas_atualizar = [atributo for atributo in colunas_pai]

colunas_atualizar.append("Obs.")
colunas_atualizar.append("Atributos alterados")

tree_atualizar = ttk.Treeview(frame_tree_atualizar, columns=colunas_atualizar, show='headings', height =25)
dic_tree_atualizar = {}
for coluna in colunas_atualizar:
    dic_tree_atualizar[coluna] = []
    
for i in colunas_atualizar:
    tree_atualizar.column(i, anchor="w", stretch=True, width = 80, minwidth =300)
    tree_atualizar.heading(i, text=i)

tree_atualizar.pack(side = tk.LEFT)
scrollx_atualizar.pack(fill = "x", side = tk.BOTTOM)
scrollx_atualizar.config(command = tree_atualizar.xview)
tree_atualizar.config(xscrollcommand = scrollx_atualizar.set)
scrolly_atualizar.pack(fill = "y", side = tk.RIGHT)
scrolly_atualizar.config(command = tree_atualizar.yview)
tree_atualizar.config(yscrollcommand = scrolly_atualizar.set)

bot_del_atualizar = tk.Button(aba_atualizar, text = "Deletar item", command  = lambda: tratar.deletar_tree_dic(tree_atualizar, dic_tree_atualizar, tree_atualizar.selection()))
bot_del_atualizar.pack( pady = 10)
tree_atualizar.bind("<Delete>", bot_del_atualizar["command"])

bt_pesq_AT = tk.Button(frame_botoes_atualizar, text = "Pesquisar", command = lambda: app.pesquisar(tree_atualizar, dic_tree_atualizar["Tombamento"], dic_tree_atualizar["Denominação"], entry_pesq_AT.get()))
bt_pesq_AT.grid(row =0, column = 4)

#aba_sr
frame_botoes_sr = ttk.Frame(aba_sr)
frame_botoes_sr.pack(fill = "x")

bt_salvar_sr= ttk.Button(frame_botoes_sr, image = save_icon, width = 50, command = lambda: app.abrir_jan_save("", dic_tree_sr))
bt_salvar_sr.grid(row =0 , column =0)

bt_atualizar_sr= ttk.Button(frame_botoes_sr, image = atualizar_icon, width = 50, command =lambda: app.abrir_atua_file(tree_sr))
bt_atualizar_sr.grid(row =0 , column =1)

lb_pesq_SR = tk.Label(frame_botoes_sr, text = "Pesquisar")
lb_pesq_SR.grid(row = 0, column = 2)

entry_pesq_SR = tk.Entry(frame_botoes_sr, textvariable = pesq_SR)
entry_pesq_SR.grid(row = 0 , column = 3)

frame_tree_sr = ttk.Frame(aba_sr)
frame_tree_sr.pack()
scrollx_sr = ttk.Scrollbar(frame_tree_sr, orient="horizontal")
scrollx_sr.pack()
scrolly_sr = ttk.Scrollbar(frame_tree_sr, orient="vertical")
scrolly_sr.pack()

colunas_sr = ["Tombamento", "Denominação", "Detentor", "Localidade", "Estado", "Obs."]

tree_sr = ttk.Treeview(frame_tree_sr, columns=colunas_sr, show='headings', height =25)
dic_tree_sr = {}
for coluna in colunas_sr:
    dic_tree_sr[coluna] = []
    
for i in colunas_sr:
    tree_sr.column(i, anchor="w", stretch=True, width = 280, minwidth =300)
    tree_sr.heading(i, text=i)

tree_sr.pack(side = tk.LEFT)
scrollx_sr.pack(fill = "x", side = tk.BOTTOM)
scrollx_sr.config(command = tree_sr.xview)
tree_sr.config(xscrollcommand = scrollx_sr.set)
scrolly_sr.pack(fill = "y", side = tk.RIGHT)
scrolly_sr.config(command = tree_sr.yview)
tree_sr.config(yscrollcommand = scrolly_sr.set)

bot_del_sr = tk.Button(aba_sr, text = "Deletar item", command  = lambda: tratar.deletar_tree_dic(tree_sr, dic_tree_sr, tree_sr.selection()))
bot_del_sr.pack( pady = 10)
tree_sr.bind("<Delete>", bot_del_sr["command"])

bt_pesq_SR = tk.Button(frame_botoes_sr, text = "Pesquisar", command = lambda: app.pesquisar(tree_sr, dic_tree_sr["Tombamento"], dic_tree_sr["Denominação"], entry_pesq_SR.get()))
bt_pesq_SR.grid(row =0, column = 4)



#aba_baixa
frame_botoes_baixa = ttk.Frame(aba_baixa)
frame_botoes_baixa.pack(fill = "x")

bt_salvar_baixa= ttk.Button(frame_botoes_baixa, image = save_icon, width = 50, command = lambda: app.abrir_jan_save("", dic_tree_baixa))
bt_salvar_baixa.grid(row =0 , column =0)

bt_atualizar_baixa= ttk.Button(frame_botoes_baixa, image = atualizar_icon, width = 50, command =lambda: app.abrir_atua_file(tree_baixa))
bt_atualizar_baixa.grid(row =0 , column =1)

lb_pesq_BA = tk.Label(frame_botoes_baixa, text = "Pesquisar")
lb_pesq_BA.grid(row = 0, column = 2)

entry_pesq_BA = tk.Entry(frame_botoes_baixa, textvariable = pesq_BA)
entry_pesq_BA.grid(row = 0 , column = 3)

frame_tree_baixa = ttk.Frame(aba_baixa)
frame_tree_baixa.pack()
scrollx_baixa = ttk.Scrollbar(frame_tree_baixa, orient="horizontal")
scrollx_baixa.pack()
scrolly_baixa = ttk.Scrollbar(frame_tree_baixa, orient="vertical")
scrolly_baixa.pack()

colunas_baixa = [atributo for atributo in colunas_pai]

colunas_baixa.append("Obs.")
colunas_baixa.append("Motivo para baixa")
colunas_baixa.append("Consta no DF_pai")
colunas_baixa.append("Atributos alterados")

tree_baixa = ttk.Treeview(frame_tree_baixa, columns=colunas_baixa, show='headings', height =25)
dic_tree_baixa = {}
for coluna in colunas_baixa:
    dic_tree_baixa[coluna] = []
    
for i in colunas_baixa:
    tree_baixa.column(i, anchor="w", stretch=True, width = 80, minwidth =300)
    tree_baixa.heading(i, text=i)

tree_baixa.pack(side = tk.LEFT)
scrollx_baixa.pack(fill = "x", side = tk.BOTTOM)
scrollx_baixa.config(command = tree_baixa.xview)
tree_baixa.config(xscrollcommand = scrollx_baixa.set)
scrolly_baixa.pack(fill = "y", side = tk.RIGHT)
scrolly_baixa.config(command = tree_baixa.yview)
tree_baixa.config(yscrollcommand = scrolly_baixa.set)

bot_del_baixa = tk.Button(aba_baixa, text = "Deletar item", command  = lambda: tratar.deletar_tree_dic(tree_baixa, dic_tree_baixa, tree_baixa.selection()))
bot_del_baixa.pack(pady = 10)
tree_baixa.bind("<Delete>", bot_del_baixa["command"])

bt_pesq_BA = tk.Button(frame_botoes_baixa, text = "Pesquisar", command = lambda: app.pesquisar(tree_baixa, dic_tree_baixa["Tombamento"], dic_tree_baixa["Denominação"], entry_pesq_BA.get()))
bt_pesq_BA.grid(row =0, column = 4)


#DF_sem_etiqueta
frame_botoes_se = ttk.Frame(aba_sem_etiqueta)
frame_botoes_se.pack(fill = "x")

bt_salvar_se= ttk.Button(frame_botoes_se, image = save_icon, width = 50, command = lambda: app.abrir_jan_save("", dic_tree_se))
bt_salvar_se.grid(row =0 , column =0)

bt_atualizar_se= ttk.Button(frame_botoes_se, image = atualizar_icon, width = 50, command =lambda: app.abrir_atua_file(tree_se))
bt_atualizar_se.grid(row =0 , column =1)

lb_pesq_SE = tk.Label(frame_botoes_se, text = "Pesquisar")
lb_pesq_SE.grid(row = 0, column = 2)

entry_pesq_SE = tk.Entry(frame_botoes_se, textvariable = pesq_SE)
entry_pesq_SE.grid(row = 0 , column = 3)

frame_tree_se = ttk.Frame(aba_sem_etiqueta)
frame_tree_se.pack(fill = "x")
scrollx_se = ttk.Scrollbar(frame_tree_se, orient="horizontal")
scrollx_se.pack()
scrolly_se = ttk.Scrollbar(frame_tree_se, orient="vertical")
scrolly_se.pack()

colunas_se = ("Denominação", "Localidade", "Detentor", "Estado", "Obs.")
tree_se = ttk.Treeview(frame_tree_se, columns=colunas_se, show='headings', height = 25)
dic_tree_se = {}
for coluna in colunas_se:
    dic_tree_se[coluna] = []
    
for i in colunas_se:
    tree_se.column(i, anchor="w", stretch=True, width = 280, minwidth =300)
    tree_se.heading(i, text=i)

tree_se.pack(side = tk.LEFT, fill = "x")
scrollx_se.pack(fill = "x", side = tk.BOTTOM)
scrollx_se.config(command = tree_se.xview)
tree_se.config(xscrollcommand = scrollx_se.set)
scrolly_se.pack(fill = "y", side = tk.RIGHT)
scrolly_se.config(command = tree_se.yview)
tree_se.config(yscrollcommand = scrolly_se.set)

bot_del_se = tk.Button(aba_sem_etiqueta, text = "Deletar item", command  = lambda: tratar.deletar_tree_dic(tree_se, dic_tree_se, tree_se.selection()))
bot_del_se.pack(pady = 10)
tree_se.bind("<Delete>", bot_del_se["command"])

bt_pesq_SE = tk.Button(frame_botoes_se, text = "Pesquisar", command = lambda: app.pesquisar(tree_se, dic_tree_se["Denominação"], dic_tree_se["Denominação"], entry_pesq_SE.get()))
bt_pesq_SE.grid(row =0, column = 4)


#Mensagem inicial
if list(config["Mensagem Inicial"])[0] == "Sim":
    tk.messagebox.showinfo(title = 'Ações sugeridas', message = "Recomenda-se que a primeira ação ao iniciar o software seja selecionar um local ou abrir uma pasta.")

app.escanear()

janela.mainloop()