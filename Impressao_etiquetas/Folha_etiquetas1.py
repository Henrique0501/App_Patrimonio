# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:29:57 2022

@author: Samaung
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Frame, Image
import PIL
import barcode
from barcode.writer import ImageWriter
ITF = barcode.get_barcode_class('itf')
import pandas as pd
import os

doc = canvas.Canvas("Folha_etiquetas.pdf", pagesize = A4)

def mm_to_p(mm):
    return mm/0.352777

def etiqueta(tomb, descri, local, ind):
    cod = ITF(tomb, writer=ImageWriter())
    cod.save("Codigo_de_barras")
    
    img = PIL.Image.new('RGB', (360, 200), color = (255, 255, 255))
 

    unb = PIL.Image.open("../Imagens/unb_logo.PNG")
    cod = PIL.Image.open("Codigo_de_barras.png")

    cod = cod.crop((0,60, cod.size[0],120))
    cod = cod.resize((int(cod.size[0]*2.2),int(cod.size[1])))

    img.paste(cod, (int((img.size[0] - cod.size[0])/2),80))
    img.paste(unb, (180, 10))
    
    for dig in local:
        if dig.isalpha():
            loc = local[local.find(dig):]
            break

    draw_title = PIL.ImageDraw.Draw(img)
    draw_descri = PIL.ImageDraw.Draw(img)
    draw_loc = PIL.ImageDraw.Draw(img)
    draw_tomb = PIL.ImageDraw.Draw(img)
    
    title = PIL.ImageFont.truetype(r'C:\Users\Samaung\anaconda3\Lib\site-packages\reportlab\fonts\Vera.ttf', 25)
    font = PIL.ImageFont.truetype(r'C:\Users\Samaung\anaconda3\Lib\site-packages\reportlab\fonts\Vera.ttf', 15)

    draw_title.text((130,10), "FUB", fill=(0,0,0), font = title)
    draw_descri.text(((img.size[0] - draw_descri.textsize(descri, font = font)[0])/2, 40), descri, fill=(0,0,0), font = font)
    draw_loc.text(((img.size[0] - draw_loc.textsize(loc, font = font)[0])/2, 60), loc, fill=(0,0,0), font = font)
    draw_tomb.text(((img.size[0] - draw_tomb.textsize(tomb, font = title)[0])/2, 180-40), tomb, fill=(0,0,0), font = title)
    
    img.save('Etiquetas/Etiqueta'+ ind + '.jpg', quality = 100 , optimize = True)
    return 'Etiquetas/Etiqueta'+ ind + '.jpg'
    
    
class Folha():
    def __init__(self, m_s, m_l, e_v, e_h, h, w, qpl, lpp):
        self.m_s = m_s
        self.m_l = m_l
        self.e_v = e_v
        self.e_h = e_h
        self.h = h
        self.w = w
        self.qpl = qpl
        self.lpp = lpp
        
    def dividir(self):
        # m_s = margem superior
        # m_l = margem lateral
        # e_v = espaço vertical
        # e_h = espaço horizontal
        # h = altura
        # w = largura
        # qpl = quantidade de etiquetas por linha
        # lpp = linhas por página
        
        f = []
        self.inds = []
        for i in range(1, self.lpp + 1):
            f.append([])
            self.inds.append([])
            for j in range(1, self.qpl + 1):
                f[i-1].append("")
                self.inds[i-1].append("")
                

        for i in range(1, self.lpp + 1):
            for j in range(1, self.qpl + 1):
                f[i-1][j-1] = Frame(mm_to_p(self.m_l + (j-1)*(self.w + self.e_h)),
                          mm_to_p(297 - self.m_s - self.h - (i-1)*(self.h + self.e_v)),
                          mm_to_p(self.w),
                          mm_to_p(self.h), showBoundary=0)
                self.inds[i-1][j-1] = f"{i},{j}"
                img = Image("cods/17303.png",
                      width = mm_to_p(self.w - 2),
                      height = mm_to_p(self.h -2))
                f[i-1][j-1].addFromList([img], doc)
        


    
    def carimbar(self, img, etiqueta):
        lista_inds = []
        
        for i in self.inds:
            lista_inds = lista_inds + i
            
        y, x = etiqueta.split(",")
        x= int(x)
        y = int(y)
        
        doc.drawImage(img,
                      mm_to_p(self.m_l + (x-1)*(self.w + self.e_h)) + (mm_to_p(self.w) - 0.9*mm_to_p(self.w))/2,
                      mm_to_p(297 - self.m_s - self.h - (y-1)*(self.h + self.e_v)) + (mm_to_p(self.h) - 0.9*mm_to_p(self.h))/2,
                      0.9*mm_to_p(self.w),
                      0.9*mm_to_p(self.h))
        
        if etiqueta == "13,5":
            doc.showPage()
            
       
        
        
    def carimbar_tudo(self, df, start = "1,1"):
        os.chdir("Etiquetas")
        for file in os.listdir():
            os.remove(file)
        os.chdir("..")
        lista_inds = []
        for linha in self.inds:
            lista_inds = lista_inds + linha
            
        ind_impressao = lista_inds.index(start)
        k = 0
        etq = []
        for line in range(df.shape[0]):
            etq.append(etiqueta(*[str(i) for i in list(df.loc[line, ["Tombamento", "Denominação", "Localidade"]])], str(k)))
            try:
                self.carimbar(etq[k], lista_inds[ind_impressao])
            except:
                ind_impressao = 0
                self.carimbar(etq[k], lista_inds[ind_impressao])
            ind_impressao+=1
            k+=1
            
# A4251 = Folha(10.7, 4.5, 0, 2.5, 21.2, 38.2, 5, 13)
# A4251.dividir()
# # df = pd.read_excel("filtro.xlsx")
# # df1 = pd.read_excel("LEVANTAMENTO_PATRIMONIAL/LAB_FIS_1/ATUALIZAR.xlsx").fillna('')
# # df = df1[df1['Obs.'].str.contains('Imprimir nova etiqueta')]
# A4251.carimbar_tudo(df, "1,1")
# # etiqueta = etiqueta("17303", "Juba", "Lab1")
# # A4251.carimbar(etiqueta, "6,2")
# #doc.rect(10,10, 300, 300, stroke = 0, fill = 0)
# doc.save()
