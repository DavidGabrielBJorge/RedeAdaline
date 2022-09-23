from tkinter import *
import tkinter as tk    
import os
import numpy as np
import random as rd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

v=[]
v0=[]

class Application:
    
    def __init__(self, master=None):
        self.frameprincipal = Frame(master)
        self.frameprincipal.pack()
        
        self.fontePadrao = ("Arial", "10")
        
        self.primeiroContainer = Frame(self.frameprincipal)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.frameprincipal)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.frameprincipal)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.frameprincipal)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

#===================================TITULO===================================
        self.titulo = Label(self.primeiroContainer, text="Dados do programa")
        self.titulo["font"] = ("Arial", "15", "bold")
        self.titulo.pack()

#===================================ALFA===================================
        self.alfaLabel = Label(self.segundoContainer,text="Digite o valor de alfa:", font=self.fontePadrao)
        self.alfaLabel.pack(side=LEFT)

        self.valorAlfa = Entry(self.segundoContainer)
        self.valorAlfa["width"] = 10
        self.valorAlfa["font"] = self.fontePadrao
        self.valorAlfa.pack(side=LEFT)

#===================================ERRO TOLERADO===================================
        self.erroToleradoLabel = Label(self.terceiroContainer, text="Digite o erro tolerado:", font=self.fontePadrao)
        self.erroToleradoLabel.pack(side=LEFT)
        
        self.valorErrotolerado = Entry(self.terceiroContainer)
        self.valorErrotolerado["width"] = 10
        self.valorErrotolerado["font"] = self.fontePadrao
        self.valorErrotolerado.pack(side=LEFT)

#===================================BOTAO===================================
        self.enviar = Button(self.quartoContainer)
        self.enviar["text"] = "Enviar"
        self.enviar["font"] = ("Calibri", "8")
        self.enviar["width"] = 12
        self.enviar["command"] = self.adalyne
        self.enviar.pack()
        
        self.canvas = None 

        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
            

    #Funcao cara enviar para o adalyne
    def adalyne(self):
        a.clear()
        alfa = float(self.valorAlfa.get())
        print(alfa)
        errotolerado = float(self.valorErrotolerado.get())
        print(errotolerado)
        
        os.chdir(r'C:\Users\david\Documents\iftm\ADS\6 semestre\Inteligencia_Computacional\Trabalho_2-4')
        #Direciona o diretorio para ler os arquivos
        
        x=np.loadtxt('x.txt')
        #Funcao para ler e converter o arquivo em txt pra
        #matriz 

        (amostras, entradas) = np.shape(x)
        #Comando para criar uma matriz, associando a quatidade
        #de linhas de x com a de amostras e a quantidade de 
        #colunas sera a mesma de entrada 

        t=np.loadtxt('target7.csv',delimiter=';',skiprows=0)
        #Funcao para ler e converter o arquivo em csv pra matriz

        (numclasses, targets)=np.shape(t)
        #Comando para criar uma matriz, associando a quatidade de linhas
        #de t com a de amostras e a quantidade de colunas sera 
        #a mesma de entrada 
        #Por ter 7 letras deve ter 7 classes

        limiar=0.0
        #Ao fazer o calculo da combinacao somado com o biers, 
        #deve ser associado a 1 ou a -1
        
        v=np.zeros((entradas,numclasses))
        #geracao dos pesos sinapticos reais tanto v quanto v0
        #quantidade de linhas equivale a quantidade de entradas
        for i in range(entradas):
            #quantidade de colunas equivalentes a quantidade de classes
            for j in range(numclasses):
                v[i][j]=rd.uniform(-0.1, 0.1)
                
        #====================================
        v0=np.zeros((numclasses))
        #====================================

        #Declarando o bias, um byars para cada saída da rede
        for j in range(numclasses):
            v0[j]=rd.uniform(-0.1,0.1)
            
        #vetor que recebera os valores das epocas/ciclos, auxiliando na geracao de grafico
        vetor1=[]
        vetor2=[]

        yin=np.zeros((numclasses,1))
        y=np.zeros((numclasses,1))

        erro=10
        ciclo=0

        #Treinamento da rede
        while erro>errotolerado:
            ciclo=ciclo+1
            erro=0
            #percorrer todos os valores da matriz, sendo 21 linhas
            for i in range(amostras):
                xaux=x[i,:]
                #o xaux vai pegar todos que estao na linha i
                for m in range(numclasses):
                    soma=0
                    for n in range(entradas):
                        soma=soma+xaux[n]*v[n][m]
                    yin[m]=soma+v0[m]
                    
                for j in range(numclasses):
                    if yin[j]>=limiar:
                        y[j]=1.0
                    else:
                        y[j]=-1.0
                for j in range(numclasses):
                    erro=erro+0.5*((t[j][i]-y[j])**2)
                
                vanterior=v
                
                #Atualizar os pesos
                for m in range(entradas):
                    for n in range(numclasses):
                        v[m][n]=vanterior[m][n]+alfa*(t[n][i]-y[n])*xaux[m]
                
                v0anterior=v0
                
                for j in range(numclasses):
                    v0[j]=v0anterior[j]+alfa*(t[j][i]-y[j])
                    
            vetor1.append(ciclo)
            vetor2.append(erro)
            
            a.scatter(vetor1,vetor2, marker='*', color="blue")
            
            if self.canvas: self.canvas.get_tk_widget().pack_forget()
            
            self.canvas = FigureCanvasTkAgg(f, root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
            


root = Tk()
Application(root)
root.mainloop()

