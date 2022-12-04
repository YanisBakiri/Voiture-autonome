#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 01:57:26 2022

@author: yanis
"""

########################################################################################################################
## code principal

#Importation des modules
import random
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from pymata4 import pymata4 
import time #importer la librairie temps
import sys
import math

board =pymata4.Pymata4() #detection de la carte Arduino

G={'Rouge':{'Bleu Cyan':3,'Vert':4},'Jaune':{'Bleu Cyan':14,'Rose':7},'Rose':{'Bleu Marine':8,'Orange':10,'Jaune':7},'Orange':{'Rose':10,'Gris':1},'Gris':{'Bleu Marine':5,'Orange':1,'Noir':9},'Bleu Marine':{'Rose':8,'Gris':5,'Vert':6,'Bleu Cyan':12},'Bleu Cyan':{'Bleu Marine':12,'Jaune':14,'Rouge':3},'Vert':{'Bleu Marine':6,'Noir':2,'Rouge':4},'Noir':{'Vert':2,'Gris':9}}

#Variables-Capteur de distance#
trig=9 #pin capteur ultrason (digital)
echo=8 #pin capteur ultrason (digital)
distance=[]

#Variables-Capteurs infrarouges#
RIGHT=5 #pin capteur infrarouge droit (analog)
valeurIRd=[0]
LEFT=0 #pin capteur infrarouge gauche (analog)
valeurIRg=[0]

#Variables-Moteurs#
GA=10 #pin moteur gauche poleA (digital)
GB=5 #pin moteur gauche poleB   (digital)
DA=11 #pin moteur droit poleA  (digital)
DB=6 #pin moteur droit poleB  (digital)
HIGH=255 #Vitesse Max
LOW=0 #Vitesse nulle

#Variables-Servomoteur#
Servo_pin = 4 #pin Servomoteur
anglec=90 #angle nulle
angled=0 #angle droite
angleg=180 #angle gauche

#Variables-Boussole#
declinationmagnetique=1 #Calibrage
Xmin =2597 #Calibrage
Xmax =3360 #Calibrage
Ymin =2332 #Calibrage
Ymax =1266 #Calibrage
Xsf=(Ymax-Ymin)/(Xmax-Xmin) #Calibrage
Ysf=(Xmax-Xmin)/(Ymax-Ymin) #Calibrage
Xoff=(((Xmax-Xmin)/2)-Xmax)*Xsf #Calibrage
Yoff=(((Ymax-Ymin)/2)-Ymax)*Ysf #Calibrage
ang=[] #Liste des angles

#Variables-Dijkstra#
chemin=[]

#Orientation-véhicule
vect=[0,0,0,0]
LVoisin=[]
Direction=[]
Lmatgraph=[]
Lmatgraph2=[]
Lpoids=[]
mvm=[]
########################################-Fonction qui affiche le graph-############################################
def depart():
    entre=input("\nQuelle est votre couleur de départ ? ")
    while (entre not in G):
        entre=input("\nQuelle est votre couleur de départ ? ")
    return entre

def arrivée():
    arrivé=input("\nQuelle est votre couleur d'arrivée ? ")
    while (arrivé not in G):
        arrivé=input("\nQuelle est votre couleur d'arrivée ? ")
    return arrivé

def matrice(G):
    matgraph=[0,0,0,0,0,0,0,0,0]
    nbrvois=[]
    couleur=["Rouge","Jaune","Rose","Orange","Gris","Bleu Marine","Bleu Cyan","Vert","Noir"]
    for cle,valeur in G.items():
        nbrvois.append(len(valeur))
    sommet1=couleur[nbrvois.index(4)]
    matgraph[4]=sommet1
    sommet2=couleur[nbrvois.index(2)]
    matgraph[0]=sommet2
    for cle,valeur in G.items():
        if len(valeur)==3:
            if (sommet2 in valeur):
                sommet3=cle
                break
    matgraph[1]=sommet3
    for cle,valeur in G.items():
        if cle==sommet3:
            for k,j in valeur.items():
                if (k!=sommet2) and (k!=sommet1):
                    sommet4=k
                    break
    matgraph[2]=sommet4
    for cle,valeur in G.items():
        if cle==sommet4:
            for k,j in valeur.items():
                if (k!=sommet3):
                    sommet5=k
                    break
    matgraph[5]=sommet5
    for cle,valeur in G.items():
        if cle==sommet5:
            for k,j in valeur.items():
                if (k!=sommet1) and (k!=sommet4) :
                    sommet6=k
                    break
    matgraph[8]=sommet6
    for cle,valeur in G.items():
        if cle==sommet6:
            for k,j in valeur.items():
                if (k!=sommet5):
                    sommet7=k
                    break
    matgraph[7]=sommet7
    for cle,valeur in G.items():
        if cle==sommet7:
            for k,j in valeur.items():
                if (k!=sommet6) and (k!=sommet1):
                    sommet8=k
                    break
    matgraph[6]=sommet8
    for cle,valeur in G.items():
        if cle==sommet8:
            for k,j in valeur.items():
                if (k!=sommet7):
                    sommet9=k
                    break
    matgraph[3]=sommet9
    matgraph2=matgraph.copy()
    for cle,valeur in G.items():
        if cle==sommet1:
            for k,j in valeur.items():
                if k==sommet3:
                    poids1=j
                elif k==sommet5:
                    poids2=j
                elif k==sommet9:
                    poids3=j
                elif k==sommet7:
                    poids4=j
        elif cle==sommet3:
            for k,j in valeur.items():
                if k==sommet2:
                    poids5=j
                elif k==sommet4:
                    poids6=j
        elif cle==sommet5:
            for k,j in valeur.items():
                if k==sommet4:
                    poids7=j
                elif k==sommet6:
                    poids8=j
        elif cle==sommet7:
            for k,j in valeur.items():
                if k==sommet6:
                    poids9=j
                elif k==sommet8:
                    poids10=j
        elif cle==sommet9:
            for k,j in valeur.items():
                if k==sommet8:
                    poids11=j
                elif k==sommet2:
                    poids12=j
    poids=[poids5,poids6,poids12,poids1,poids7,poids3,poids2,poids11,poids4,poids8,poids10,poids9] 
    for k in range(9):
        if matgraph[k]=="Rouge":
            matgraph[k]="red"
        elif matgraph[k]=="Jaune":
            matgraph[k]="yellow"
        elif matgraph[k]=="Rose":
            matgraph[k]="hotpink"
        elif matgraph[k]=="Orange":
            matgraph[k]="orange"
        elif matgraph[k]=="Gris":
            matgraph[k]="gray"
        elif matgraph[k]=="Bleu Marine":
            matgraph[k]="darkblue"
        elif matgraph[k]=="Bleu Cyan":
            matgraph[k]="cyan"
        elif matgraph[k]=="Vert":
            matgraph[k]="lime"
        elif matgraph[k]=="Noir":
            matgraph[k]="black"
    Lmatgraph.append(matgraph)
    Lpoids.append(poids)
    Lmatgraph2.append(matgraph2)
    return ""


def graph(G,depart,arrivé):
    inddep=Lmatgraph2[0].index(départ)
    indarr=Lmatgraph2[0].index(arrivé)
    L=[]
    for k in Lpoids[0]:
        L.append(str(k))
    fig = plt.figure()
    ax = fig.add_subplot()
    w=3
    h=3
    rect1 = Rectangle((0,0), w, h, color=Lmatgraph[0][6])
    rect2 = Rectangle((0,5), w, h, color=Lmatgraph[0][3])
    rect3 = Rectangle((0,10), w, h, color=Lmatgraph[0][0])

    rect4 = Rectangle((5,0), w, h, color=Lmatgraph[0][7])
    rect5 = Rectangle((5,5), w, h, color=Lmatgraph[0][4])
    rect6 = Rectangle((5,10), w, h, color=Lmatgraph[0][1])

    rect7 = Rectangle((10,0), w, h, color=Lmatgraph[0][8])
    rect8 = Rectangle((10,5), w, h, color=Lmatgraph[0][5])
    rect9 = Rectangle((10,10), w, h, color=Lmatgraph[0][2])

    ax.add_patch(rect1)
    ax.add_patch(rect2)
    ax.add_patch(rect3)
    ax.add_patch(rect4)
    ax.add_patch(rect5)
    ax.add_patch(rect6)
    ax.add_patch(rect7)
    ax.add_patch(rect8)
    ax.add_patch(rect9)
    if inddep==0:
        plt.scatter(1.5, 11.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==1:
        plt.scatter(6.5, 11.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==2:
        plt.scatter(11.5, 11.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==3:
        plt.scatter(1.5, 6.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==4:
        plt.scatter(6.5, 6.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==5:
        plt.scatter(11.5, 6.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==6:
        plt.scatter(1.5, 1.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==7:
        plt.scatter(6.5, 1.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black')
    elif inddep==8:
        plt.scatter(11.5, 1.5,c='white',marker='s',s=200,label='Point de départ',edgecolors='black') 
    if indarr==0:
        plt.scatter(1.5, 11.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==1:
        plt.scatter(6.5, 11.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==2:
        plt.scatter(11.5, 11.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==3:
        plt.scatter(1.5, 6.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==4:
        plt.scatter(6.5, 6.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==5:
        plt.scatter(11.5, 6.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==6:
        plt.scatter(1.5, 1.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==7:
        plt.scatter(6.5, 1.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black')
    elif indarr==8:
        plt.scatter(11.5, 1.5,c='white',marker='X',s = 400,label="Point d'arrivée",edgecolors='black') 
    
    ta = np.array([[[ 3,  1.5],[5,   1.5]],
                   [[ 8,  1.5],[10,   1.5]],
                   [[ 3,  6.5],[5,   6.5]],
                   [[ 8,  6.5],[10,   6.5]],
                   [[ 3,  11.5],[5,   11.5]],
                   [[ 8,  11.5],[10,   11.5]],
                   [[ 1.5,  3],[1.5,   5]],
                   [[ 1.5,  8],[1.5,   10]],
                   [[ 6.5,  3],[6.5,   5]],
                   [[ 6.5,  8],[6.5,  10]],
                   [[ 11.5,  3],[11.5,  5]],
                   [[ 11.5,  8],[11.5,   10]]]) 
    x, y = ta.T
    plt.text(1, 4, L[7], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(1, 9,L[2] , horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(6, 4, L[8], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(6, 9, L[3], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(11, 4, L[9], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(11, 9, L[4], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(3.9, 2, L[10], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(3.9, 7, L[5], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(3.9, 12, L[0], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(8.9, 2, L[11], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(8.9, 7, L[6], horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(8.9, 12, L[1], horizontalalignment = 'center', verticalalignment = 'center')
    plt.margins(0.005)
    plt.gcf().subplots_adjust(left = 0.3, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0.9, hspace = 0.5)
    plt.plot(x, y, linewidth=2, color='black')
    #plt.legend(fontsize = 10)
    plt.axis('off')
    #plt.axis('equal')

    plt.show()
    print("\nVoici le graphe de votre circuit ! Le carré blanc est le point de départ, la croix blanche est le point d'arrivé. ")
    return ""
    
###################################################################################################################
    
##############################-Fonction qui détermine le plus court chemin-########################################

def dictionnaire():
    print("---------Bienvenue sur un algorithme déterminant le plus court chemin pour un vehicule autonome !---------\n\nVoici la liste des sommets du parcours: Rouge, Jaune, Rose, Orange, Gris, Bleu Marine, Bleu Cyan, Vert et Noir\n(La bonne orthograpes des couleurs et les majuscules sont primordiales !)\n\nNous allons utiliser la notion de poids entre deux sommets. Le poids est une modélisation de la distance et du temps à effectuer pour aller d'un point A à un point B, il peut être égal à 2,3 ou 4")
    rep=0
    D={}
    while rep!=" ":
        rep=input("\nCliquez une fois sur espace et sur entré lorsque vous êtes prêt ! ")
    #Rouge
    dicRouge={}
    nbrvoisRouge=input("Combien de voisins à la couleur Rouge ? ")
    if nbrvoisRouge=='2':
        voisRouge1=input("Donnez un voisin de la couleur Rouge : ")
        poidsRouge1=input("Quel est son poids ? ")
        dicRouge[voisRouge1]=int(poidsRouge1)
        voisRouge2=input("Donnez l'autre voisin de la couleur Rouge : ")
        poidsRouge2=input("Quel est son poids ? ")
        dicRouge[voisRouge2]=int(poidsRouge2)
    elif nbrvoisRouge=='3':
        voisRouge1=input("Donnez un voisin de la couleur Rouge : ")
        poidsRouge1=input("Quel est son poids ? ")
        dicRouge[voisRouge1]=int(poidsRouge1)
        voisRouge2=input("Donnez un autre voisin de la couleur Rouge : ")
        poidsRouge2=input("Quel est son poids ? ")
        dicRouge[voisRouge2]=int(poidsRouge2)
        voisRouge3=input("Donnez le dernier voisin de la couleur Rouge : ")
        poidsRouge3=input("Quel est son poids ? ")
        dicRouge[voisRouge3]=int(poidsRouge3)
    elif nbrvoisRouge=='4':
        voisRouge1=input("Donnez un voisin de la couleur Rouge : ")
        poidsRouge1=input("Quel est son poids ? ")
        dicRouge[voisRouge1]=int(poidsRouge1)
        voisRouge2=input("Donnez un autre voisin de la couleur Rouge : ")
        poidsRouge2=input("Quel est son poids ? ")
        dicRouge[voisRouge2]=int(poidsRouge2)
        voisRouge3=input("Donnez un autre voisin de la couleur Rouge : ")
        poidsRouge3=input("Quel est son poids ? ")
        dicRouge[voisRouge3]=int(poidsRouge3)
        voisRouge4=input("Donnez le dernier voisin de la couleur Rouge : ")
        poidsRouge4=input("Quel est son poids ? ")
        dicRouge[voisRouge4]=int(poidsRouge4)
    D['Rouge']=dicRouge
    #Jaune
    dicJaune={}
    nbrvoisJaune=input("\nCombien de voisins à la couleur Jaune ? ")
    if nbrvoisJaune=='2':
        voisJaune1=input("Donnez un voisin de la couleur Jaune : ")
        poidsJaune1=input("Quel est son poids ? ")
        dicJaune[voisJaune1]=int(poidsJaune1)
        voisJaune2=input("Donnez l'autre voisin de la couleur Jaune : ")
        poidsJaune2=input("Quel est son poids ? ")
        dicJaune[voisJaune2]=int(poidsJaune2)
    elif nbrvoisJaune=='3':
        voisJaune1=input("Donnez un voisin de la couleur Jaune : ")
        poidsJaune1=input("Quel est son poids ? ")
        dicJaune[voisJaune1]=int(poidsJaune1)
        voisJaune2=input("Donnez un autre voisin de la couleur Jaune : ")
        poidsJaune2=input("Quel est son poids ? ")
        dicJaune[voisJaune2]=int(poidsJaune2)
        voisJaune3=input("Donnez le dernier voisin de la couleur Jaune : ")
        poidsJaune3=input("Quel est son poids ? ")
        dicJaune[voisJaune3]=int(poidsJaune3)
    elif nbrvoisJaune=='4':
        voisJaune1=input("Donnez un voisin de la couleur Jaune : ")
        poidsJaune1=input("Quel est son poids ? ")
        dicJaune[voisJaune1]=int(poidsJaune1)
        voisJaune2=input("Donnez un autre voisin de la couleur Jaune : ")
        poidsJaune2=input("Quel est son poids ? ")
        dicJaune[voisJaune2]=int(poidsJaune2)
        voisJaune3=input("Donnez un autre voisin de la couleur Jaune : ")
        poidsJaune3=input("Quel est son poids ? ")
        dicJaune[voisJaune3]=int(poidsJaune3)
        voisJaune4=input("Donnez le dernier voisin de la couleur Jaune : ")
        poidsJaune4=input("Quel est son poids ? ")
        dicJaune[voisJaune4]=int(poidsJaune4)
    D['Jaune']=dicJaune
    #Rose
    dicRose={}
    nbrvoisRose=input("\nCombien de voisins à la couleur Rose ? ")
    if nbrvoisRose=='2':
        voisRose1=input("Donnez un voisin de la couleur Rose : ")
        poidsRose1=input("Quel est son poids ? ")
        dicRose[voisRose1]=int(poidsRose1)
        voisRose2=input("Donnez l'autre voisin de la couleur Rose : ")
        poidsRose2=input("Quel est son poids ? ")
        dicRose[voisRose2]=int(poidsRose2)
    elif nbrvoisRose=='3':
        voisRose1=input("Donnez un voisin de la couleur Rose : ")
        poidsRose1=input("Quel est son poids ? ")
        dicRose[voisRose1]=int(poidsRose1)
        voisRose2=input("Donnez un autre voisin de la couleur Rose : ")
        poidsRose2=input("Quel est son poids ? ")
        dicRose[voisRose2]=int(poidsRose2)
        voisRose3=input("Donnez le dernier voisin de la couleur Rose : ")
        poidsRose3=input("Quel est son poids ? ")
        dicRose[voisRose3]=int(poidsRose3)
    elif nbrvoisRouge=='4':
        voisRose1=input("Donnez un voisin de la couleur Rose : ")
        poidsRose1=input("Quel est son poids ? ")
        dicRose[voisRose1]=int(poidsRose1)
        voisRose2=input("Donnez un autre voisin de la couleur Rose : ")
        poidsRose2=input("Quel est son poids ? ")
        dicRose[voisRose2]=int(poidsRose2)
        voisRose3=input("Donnez un autre voisin de la couleur Rose : ")
        poidsRose3=input("Quel est son poids ? ")
        dicRose[voisRose3]=int(poidsRose3)
        voisRose4=input("Donnez le dernier voisin de la couleur Rose : ")
        poidsRose4=input("Quel est son poids ? ")
        dicRose[voisRose4]=int(poidsRose4)
    D['Rose']=dicRose
    #Orange
    dicOrange={}
    nbrvoisOrange=input("\nCombien de voisins à la couleur Orange ? ")
    if nbrvoisOrange=='2':
        voisOrange1=input("Donnez un voisin de la couleur Orange : ")
        poidsOrange1=input("Quel est son poids ? ")
        dicOrange[voisOrange1]=int(poidsOrange1)
        voisOrange2=input("Donnez l'autre voisin de la couleur Orange : ")
        poidsOrange2=input("Quel est son poids ? ")
        dicOrange[voisOrange2]=int(poidsOrange2)
    elif nbrvoisOrange=='3':
        voisOrange1=input("Donnez un voisin de la couleur Orange : ")
        poidsOrange1=input("Quel est son poids ? ")
        dicOrange[voisOrange1]=int(poidsOrange1)
        voisOrange2=input("Donnez un autre voisin de la couleur Orange : ")
        poidsOrange2=input("Quel est son poids ? ")
        dicOrange[voisOrange2]=int(poidsOrange2)
        voisOrange3=input("Donnez le dernier voisin de la couleur Orange : ")
        poidsOrange3=input("Quel est son poids ? ")
        dicOrange[voisOrange3]=int(poidsOrange3)
    elif nbrvoisOrange=='4':
        voisOrange1=input("Donnez un voisin de la couleur Orange : ")
        poidsOrange1=input("Quel est son poids ? ")
        dicOrange[voisOrange1]=int(poidsOrange1)
        voisOrange2=input("Donnez un autre voisin de la couleur Orange : ")
        poidsOrange2=input("Quel est son poids ? ")
        dicOrange[voisOrange2]=int(poidsOrange2)
        voisOrange3=input("Donnez un autre voisin de la couleur Orange : ")
        poidsOrange3=input("Quel est son poids ? ")
        dicOrange[voisOrange3]=int(poidsOrange3)
        voisOrange4=input("Donnez le dernier voisin de la couleur Orange : ")
        poidsOrange4=input("Quel est son poids ? ")
        dicOrange[voisOrange4]=int(poidsOrange4)
    D['Orange']=dicOrange
    #Gris
    dicGris={}
    nbrvoisGris=input("\nCombien de voisins à la couleur Gris ? ")
    if nbrvoisGris=='2':
        voisGris1=input("Donnez un voisin de la couleur Gris : ")
        poidsGris1=input("Quel est son poids ? ")
        dicGris[voisGris1]=int(poidsGris1)
        voisGris2=input("Donnez l'autre voisin de la couleur Gris : ")
        poidsGris2=input("Quel est son poids ? ")
        dicGris[voisGris2]=int(poidsGris2)
    elif nbrvoisGris=='3':
        voisGris1=input("Donnez un voisin de la couleur Gris : ")
        poidsGris1=input("Quel est son poids ? ")
        dicGris[voisGris1]=int(poidsGris1)
        voisGris2=input("Donnez un autre voisin de la couleur Gris : ")
        poidsGris2=input("Quel est son poids ? ")
        dicGris[voisGris2]=int(poidsGris2)
        voisGris3=input("Donnez le dernier voisin de la couleur Gris : ")
        poidsGris3=input("Quel est son poids ? ")
        dicGris[voisGris3]=int(poidsGris3)
    elif nbrvoisGris=='4':
        voisGris1=input("Donnez un voisin de la couleur Gris : ")
        poidsGris1=input("Quel est son poids ? ")
        dicGris[voisGris1]=int(poidsGris1)
        voisGris2=input("Donnez un autre voisin de la couleur Gris : ")
        poidsGris2=input("Quel est son poids ? ")
        dicGris[voisGris2]=int(poidsGris2)
        voisGris3=input("Donnez un autre voisin de la couleur Gris : ")
        poidsGris3=input("Quel est son poids ? ")
        dicGris[voisGris3]=int(poidsGris3)
        voisGris4=input("Donnez le dernier voisin de la couleur Gris : ")
        poidsGris4=input("Quel est son poids ? ")
        dicGris[voisGris4]=int(poidsGris4)
    D['Gris']=dicGris
    #Bleu Marine
    dicBleuMarine={}
    nbrvoisBleuMarine=input("\nCombien de voisins à la couleur Bleu Marine ? ")
    if nbrvoisBleuMarine=='2':
        voisBleuMarine1=input("Donnez un voisin de la couleur Bleu Marine : ")
        poidsBleuMarine1=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine1]=int(poidsBleuMarine1)
        voisBleuMarine2=input("Donnez l'autre voisin de la couleur Bleu Marine : ")
        poidsBleuMarine2=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine2]=int(poidsBleuMarine2)
    elif nbrvoisBleuMarine=='3':
        voisBleuMarine1=input("Donnez un voisin de la couleur Bleu Marine : ")
        poidsBleuMarine1=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine1]=int(poidsBleuMarine1)
        voisBleuMarine2=input("Donnez un autre voisin de la couleur Bleu Marine : ")
        poidsBleuMarine2=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine2]=int(poidsBleuMarine2)
        voisBleuMarine3=input("Donnez le dernier voisin de la couleur Bleu Marine : ")
        poidsBleuMarine3=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine3]=int(poidsBleuMarine3)
    elif nbrvoisBleuMarine=='4':
        voisBleuMarine1=input("Donnez un voisin de la couleur Bleu Marine : ")
        poidsBleuMarine1=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine1]=int(poidsBleuMarine1)
        voisBleuMarine2=input("Donnez un autre voisin de la couleur Bleu Marine : ")
        poidsBleuMarine2=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine2]=int(poidsBleuMarine2)
        voisBleuMarine3=input("Donnez un autre voisin de la couleur Bleu Marine : ")
        poidsBleuMarine3=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine3]=int(poidsBleuMarine3)
        voisBleuMarine4=input("Donnez le dernier voisin de la couleur Bleu Marine : ")
        poidsBleuMarine4=input("Quel est son poids ? ")
        dicBleuMarine[voisBleuMarine4]=int(poidsBleuMarine4)
    D['Bleu Marine']=dicBleuMarine
    #Bleu Cyan
    dicBleuCyan={}
    nbrvoisBleuCyan=input("\nCombien de voisins à la couleur Bleu Cyan ? ")
    if nbrvoisBleuCyan=='2':
        voisBleuCyan1=input("Donnez un voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan1=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan1]=int(poidsBleuCyan1)
        voisBleuCyan2=input("Donnez l'autre voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan2=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan2]=int(poidsBleuCyan2)
    elif nbrvoisBleuCyan=='3':
        voisBleuCyan1=input("Donnez un voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan1=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan1]=int(poidsBleuCyan1)
        voisBleuCyan2=input("Donnez un autre voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan2=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan2]=int(poidsBleuCyan2)
        voisBleuCyan3=input("Donnez le dernier voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan3=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan3]=int(poidsBleuCyan3)
    elif nbrvoisBleuCyan=='4':
        voisBleuCyan1=input("Donnez un voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan1=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan1]=int(poidsBleuCyan1)
        voisBleuCyan2=input("Donnez un autre voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan2=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan2]=int(poidsBleuCyan2)
        voisBleuCyan3=input("Donnez un autre voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan3=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan3]=int(poidsBleuCyan3)
        voisBleuCyan4=input("Donnez le dernier voisin de la couleur Bleu Cyan : ")
        poidsBleuCyan4=input("Quel est son poids ? ")
        dicBleuCyan[voisBleuCyan4]=int(poidsBleuCyan4)
    D['Bleu Cyan']=dicBleuCyan
    #Vert
    dicVert={}
    nbrvoisVert=input("\nCombien de voisins à la couleur Vert ? ")
    if nbrvoisVert=='2':
        voisVert1=input("Donnez un voisin de la couleur Vert : ")
        poidsVert1=input("Quel est son poids ? ")
        dicVert[voisVert1]=int(poidsVert1)
        voisVert2=input("Donnez l'autre voisin de la couleur Vert : ")
        poidsVert2=input("Quel est son poids ? ")
        dicVert[voisVert2]=int(poidsVert2)
    elif nbrvoisVert=='3':
        voisVert1=input("Donnez un voisin de la couleur Vert : ")
        poidsVert1=input("Quel est son poids ? ")
        dicVert[voisVert1]=int(poidsVert1)
        voisVert2=input("Donnez un autre voisin de la couleur Vert : ")
        poidsVert2=input("Quel est son poids ? ")
        dicVert[voisVert2]=int(poidsVert2)
        voisVert3=input("Donnez le dernier voisin de la couleur Vert : ")
        poidsVert3=input("Quel est son poids ? ")
        dicVert[voisVert3]=int(poidsVert3)
    elif nbrvoisVert=='4':
        voisVert1=input("Donnez un voisin de la couleur Vert : ")
        poidsVert1=input("Quel est son poids ? ")
        dicVert[voisVert1]=int(poidsVert1)
        voisVert2=input("Donnez un autre voisin de la couleur Vert : ")
        poidsVert2=input("Quel est son poids ? ")
        dicVert[voisVert2]=int(poidsVert2)
        voisVert3=input("Donnez un autre voisin de la couleur Vert : ")
        poidsVert3=input("Quel est son poids ? ")
        dicVert[voisVert3]=int(poidsVert3)
        voisVert4=input("Donnez le dernier voisin de la couleur Vert : ")
        poidsVert4=input("Quel est son poids ? ")
        dicVert[voisVert4]=int(poidsVert4)
    D['Vert']=dicVert
    #Noir
    dicNoir={}
    nbrvoisNoir=input("\nCombien de voisins à la couleur Noir ? ")
    if nbrvoisNoir=='2':
        voisNoir1=input("Donnez un voisin de la couleur Noir : ")
        poidsNoir1=input("Quel est son poids ? ")
        dicNoir[voisNoir1]=int(poidsNoir1)
        voisNoir2=input("Donnez l'autre voisin de la couleur Noir : ")
        poidsNoir2=input("Quel est son poids ? ")
        dicNoir[voisNoir2]=int(poidsNoir2)
    elif nbrvoisNoir=='3':
        voisNoir1=input("Donnez un voisin de la couleur Noir : ")
        poidsNoir1=input("Quel est son poids ? ")
        dicNoir[voisNoir1]=int(poidsNoir1)
        voisNoir2=input("Donnez un autre voisin de la couleur Noir : ")
        poidsNoir2=input("Quel est son poids ? ")
        dicNoir[voisNoir2]=int(poidsNoir2)
        voisNoir3=input("Donnez le dernier voisin de la couleur Noir : ")
        poidsNoir3=input("Quel est son poids ? ")
        dicNoir[voisNoir3]=int(poidsNoir3)
    elif nbrvoisNoir=='4':
        voisNoir1=input("Donnez un voisin de la couleur Noir : ")
        dicNoir[voisNoir1]=int(poidsRouge1)
        poidsNoir1=input("Quel est son poids ? ")
        voisNoir2=input("Donnez un autre voisin de la couleur Noir : ")
        poidsNoir2=input("Quel est son poids ? ")
        dicNoir[voisNoir2]=int(poidsNoir2)
        voisNoir3=input("Donnez un autre voisin de la couleur Noir : ")
        poidsNoir3=input("Quel est son poids ? ")
        dicNoir[voisNoir3]=int(poidsNoir3)
        voisNoir4=input("Donnez le dernier voisin de la couleur Noir : ")
        poidsNoir4=input("Quel est son poids ? ")
        dicNoir[voisNoir4]=int(poidsNoir4)
    D['Noir']=dicNoir
    return D

def moore_dijkstra_1(G, s):
    """
     FONCTION QUI CALCULE TOUS LES PLUS COURTS CHEMINS DE L'ENTREE A CHACUN DES SOMMETS
    """
    inf = sum(sum(G[sommet][i] for i in G[sommet]) for sommet in G) + 1
    global s_explore
    global s_a_explorer
    s_explore = {s : [0, [s]]}
    s_a_explorer = {j : [inf, ""] for j in G if j != s}
    for suivant in G[s]:
        s_a_explorer[suivant] = [G[s][suivant], s]

    while s_a_explorer and any(s_a_explorer[k][0] < inf for k in s_a_explorer):
        s_min = min(s_a_explorer, key = s_a_explorer.get)
        longueur_s_min, precedent_s_min = s_a_explorer[s_min]
        for successeur in G[s_min]:
            if successeur in s_a_explorer:
                dist = longueur_s_min + G[s_min][successeur]
                if dist < s_a_explorer[successeur][0]:
                    s_a_explorer[successeur] = [dist, s_min]
        s_explore[s_min] = [longueur_s_min, s_explore[precedent_s_min][1] + [s_min]]
        del s_a_explorer[s_min]

    return s_explore


def affichage(G, entree, sortie):
    """
    FONCTION D'AFFICHAGE DU PLUS COURT CHEMIN ENTRE L'ENTREE ET LA SORTIE DU GRAPHE
    """
    moore_dijkstra_1(G, entree)
    '''

    print("Dans le graphe d\'origine {} dont les arcs sont :".format(entree))
    for k in MonGraphe:
        print(k, ":", MonGraphe[k])
    '''
    print()

    for k in s_explore:
        if sortie == k:
            print("Le plus court chemin menant de {} à {} est ".format(entree, sortie), end="")
            print("->".join(s_explore[k][1]))
            chemin.append(s_explore[k][1])
            print("Son poids est égal à {}".format(s_explore[k][0]))

    for k in s_a_explorer:
        if sortie == k:
            print("Il n\'existe aucun chemin de {} à {}".format(entree, sortie))

#########################################################################################################

#########################################-Fonctions Moteurs-##########################################
                                                                                                     
def droite():                                                                                        
    board.pwm_write(DA,HIGH) #tourner à droite                                                       
    board.pwm_write(DB,LOW)                                                                          
    board.pwm_write(GA,LOW)                                                                          
    board.pwm_write(GB,HIGH)                                                                         
                                                                                                     
def arret():
    board.pwm_write(DA,LOW) #stop                                                                   
    board.pwm_write(DB,LOW)
    board.pwm_write(GA,LOW)
    board.pwm_write(GB,LOW)

def toutdroit():
    board.pwm_write(DA,LOW) #avancer tout droit
    board.pwm_write(DB,HIGH)
    board.pwm_write(GA,LOW)
    board.pwm_write(GB,HIGH)

def gauche():
    board.pwm_write(DA,LOW) #tourner à gauche
    board.pwm_write(DB,HIGH)
    board.pwm_write(GA,HIGH)
    board.pwm_write(GB,LOW)

def gauche90():
    gauche()
    time.sleep(0.7)
    arret()
    time.sleep(0.5)

def droite90():
    droite()
    time.sleep(0.7)
    arret()
    time.sleep(0.5)

def r180():
    x=random.randint(0,1)
    if x==0:
        droite()
        time.sleep(1.3)
        arret()
        time.sleep(0.5)
    elif x==1:
        gauche()
        time.sleep(1.3)
        arret()
        time.sleep(0.5)

def avancer():
    toutdroit()
    time.sleep(0.3)
    arret()
    time.sleep(0.5)
    while (valeurIRd[-1]>45) and( valeurIRg[-1]>45):
        valueD,time_stamp=board.analog_read(RIGHT)
        valeurIRd.append(valueD)
        valueG,time_stamp=board.analog_read(LEFT)
        valeurIRg.append(valueG)
        if (valeurIRd[-1]<=45) and (valeurIRg[-1]<=45):
            toutdroit()
        elif (valeurIRd[-1]<=45) and (valeurIRg[-1]>45):
            gauche()
        elif (valeurIRd[-1]>45) and (valeurIRg[-1]<=45):
            droite()
    toutdroit()
    time.sleep(0.3)
    arret()
    time.sleep(0.5)
    return ""
####################################################################################################################

#####################################-Fonction qui oriente le véhicule autonome-####################################
def manuelle(G):
    v=[]
    Voisin=0
    for cle,valeur in G.items():
        if cle==départ:
            for a,o in valeur.items():
                v.append(a)
    if len(v)==2:
        while True:
            Voisin=input(f"\nAfin d'initialiser votre véhicule autonome, orientez votre véhicule autonome vers une de ces couleurs et indiquez votre choix:\n{v[0]} ou {v[1]}: ")
            if (Voisin==v[0]) or (Voisin==v[1]):
                break
    elif len(v)==3:
        while True:
            Voisin=input(f"\nAfin d'initialiser votre véhicule autonome, orientez votre véhicule autonome vers une de ces couleurs et indiquez votre choix:\n{v[0]}, {v[1]} ou {v[2]}: ")
            if (Voisin==v[0]) or (Voisin==v[1]) or (Voisin==v[2]):
                break
    elif len(v)==4:
        while True:
            Voisin=input(f"\nAfin d'initialiser votre véhicule autonome, orientez votre véhicule autonome vers une de ces couleurs et indiquez votre choix:\n{v[0]}, {v[1]}, {v[2]} ou {v[3]}: ")
            if (Voisin==v[0]) or (Voisin==v[1]) or (Voisin==v[2]) or (Voisin==v[3]):
                break
    LVoisin.append(Voisin)
    a=0
    while a!=" ":
        a=input("\nLorsque votre véhicule est orienté, cliquez une fois sur espace : ")
    while True:
        qmc5883l(board)
        if len(ang)>=1:
            break
        print("non")
    Direction.append(ang[-1])
    print("Début du parcours..")
    ang.clear()
    return ""

def vecteur():
    "Renvoie les 4 vecteurs sous la forme d'une liste [x,y,-x,-y]"
    inddep=Lmatgraph2[0].index(départ)
    inddir=Lmatgraph2[0].index(LVoisin[0])
    if inddep==0:
        if inddir==1:
            vect[0]=Direction[0]
            vect[1]=Direction[0]-90
        elif inddir==3:
            vect[0]=Direction[0]-90
            vect[1]=Direction[0]-180
    elif inddep==1:
        if inddir==0:
            vect[0]=Direction[0]+180
            vect[1]=Direction[0]+90
        elif inddir==2:
            vect[0]=Direction[0]
            vect[1]=Direction[0]-90
        elif inddir==4:
            vect[0]=Direction[0]-90
            vect[1]=Direction[0]-180
    elif inddep==2:
        if inddir==1:
            vect[0]=Direction[0]-180
            vect[1]=Direction[0]+90
        elif inddir==5:
            vect[0]=Direction[0]-90
            vect[1]=Direction[0]-180
    elif inddep==3:
        if inddir==0:
            vect[0]=Direction[0]+90
            vect[1]=Direction[0]
        elif inddir==4:
            vect[0]=Direction[0]
            vect[1]=Direction[0]-90
        elif inddir==6:
            vect[0]=Direction[0]-90
            vect[1]=Direction[0]-180
    elif inddep==4:
        if inddir==3:
            vect[0]=Direction[0]-180
            vect[1]=Direction[0]+90
        elif inddir==1:
            vect[0]=Direction[0]+90
            vect[1]=Direction[0]
        elif inddir==5:
            vect[0]=Direction[0]
            vect[1]=Direction[0]-90
        elif inddir==7:
            vect[0]=Direction[0]-90
            vect[1]=Direction[0]-180
    elif inddep==5:
        if inddir==2:
            vect[0]=Direction[0]+90
            vect[1]=Direction[0]
        elif inddir==4:
            vect[0]=Direction[0]-180
            vect[1]=Direction[0]+90
        elif inddir==8:
            vect[0]=Direction[0]-90
            vect[1]=Direction[0]-180
    elif inddep==6:
        if inddir==3:
            vect[0]=Direction[0]+90
            vect[1]=Direction[0]
        elif inddir==7:
            vect[0]=Direction[0]
            vect[1]=Direction[0]-90
    elif inddep==7:
        if inddir==6:
            vect[0]=Direction[0]-180
            vect[1]=Direction[0]+90
        elif inddir==4:
            vect[0]=Direction[0]+90
            vect[1]=Direction[0]
        elif inddir==8:
           vect[0]=Direction[0]
           vect[1]=Direction[0]-90
    elif inddep==8:
        if inddir==5:
            vect[0]=Direction[0]+90
            vect[1]=Direction[0]
        elif inddir==7:
            vect[0]=Direction[0]-180
            vect[1]=Direction[0]+90
    if vect[0]>360:
        vect[0]=vect[0]-360
    elif vect[0]<0:
        vect[0]=vect[0]+360
    if vect[1]>360:
        vect[1]=vect[1]-360
    elif vect[1]<0:
        vect[1]=vect[1]+360  
    if 0<vect[0]<180:
        vect[2]=vect[0]+180
    elif 180<vect[0]<360:
        vect[2]=vect[0]-180
    if 0<vect[1]<180:
        vect[3]=vect[1]+180
    elif 180<vect[1]<360:
        vect[3]=vect[1]-180
    return ""

def coordonnée(sommet):      
    coord=[0,0]
    T = [Lmatgraph2[0][idx: idx+3] for idx in range(0, 9, 3)]
    T[0],T[2]=T[2],T[0]
    for k in T:
        for j in k:
            if j==sommet:
                coord[0]=k.index(j)
                coord[1]=T.index(k)
                break
    return coord

def Haut():
    while True:
        qmc5883l(board)
        if len(ang)>=1:
            break
        print("haut")
    vecteuractuel=ang[-1]
    ang.clear()
    if 0<vecteuractuel<180:
        vecteuropposé=vecteuractuel+180
        if vecteuractuel<vect[1]<vecteuropposé:
            if 80<=(vect[1]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vecteuractuel-vect[1])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
    elif 180<vecteuractuel<360:
        vecteuropposé=vecteuractuel-180
        if vecteuropposé<vect[1]<vecteuractuel:
            if 80<=(vecteuractuel-vect[1])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vect[1]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""
        
def Bas():
    while True:
        qmc5883l(board)
        if len(ang)>=1:
            break
        print("haut")
    vecteuractuel=ang[-1]
    ang.clear()
    if 0<vecteuractuel<180:
        vecteuropposé=vecteuractuel+180
        if vecteuractuel<vect[3]<vecteuropposé:
            if 80<=(vect[3]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vecteuractuel-vect[3])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
    elif 180<vecteuractuel<360:
        vecteuropposé=vecteuractuel-180
        if vecteuropposé<vect[3]<vecteuractuel:
            if 80<=(vecteuractuel-vect[3])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vect[3]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""

def Droite():
    while True:
        qmc5883l(board)
        if len(ang)>=1:
            break
        print("haut")
    vecteuractuel=ang[-1]
    ang.clear()
    if 0<vecteuractuel<180:
        vecteuropposé=vecteuractuel+180
        if vecteuractuel<vect[0]<vecteuropposé:
            if 80<=(vect[0]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vecteuractuel-vect[0])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
    elif 180<vecteuractuel<360:
        vecteuropposé=vecteuractuel-180
        if vecteuropposé<vect[0]<vecteuractuel:
            if 80<=(vecteuractuel-vect[0])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vect[0]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""

def Gauche():
    while True:
        qmc5883l(board)
        if len(ang)>=1:
            break
        print("haut")
    vecteuractuel=ang[-1]
    ang.clear()
    if 0<vecteuractuel<180:
        vecteuropposé=vecteuractuel+180
        if vecteuractuel<vect[2]<vecteuropposé:
            if 80<=(vect[2]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vecteuractuel-vect[2])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
    elif 180<vecteuractuel<360:
        vecteuropposé=vecteuractuel-180
        if vecteuropposé<vect[2]<vecteuractuel:
            if 80<=(vecteuractuel-vect[2])<=100:
                mvm.append("gauche90")
                return ""
            else:
                mvm.append("r180")
                return ""
        else:
            if 80<=(vect[2]-vecteuractuel)<=100:
                mvm.append("droite90")
                return ""
            else:
                mvm.append("r180")
                return ""
                
                
def Direct(coordActuelle,coordProchainVoisin):
    if coordActuelle[0]==coordProchainVoisin[0]:
        if coordActuelle[1]<coordProchainVoisin[1]:
            Haut()
        elif coordActuelle[1]>coordProchainVoisin[1]:
            Bas()
    elif coordActuelle[1]==coordProchainVoisin[1]:
        if coordActuelle[0]<coordProchainVoisin[0]:
            Droite()
        elif coordActuelle[0]>coordProchainVoisin[0]:
            Gauche()  
    return ""

###################################################################################################################

#########################################-Fonction Boussole-##########################################

def the_call_back(data):
    """
    This is the callback function will return the Azimuth read from the device.
    :param data: [pin_type, Device address, device read register, x LSB, x MSB,
                  Y LSB, Y MSB, Z LSB, Z MSB]
    """
    # print the raw data returned
    #print(data)
    # indices into data to get values:
    x = data[3] + (data[4] << 8)
    y = data[5] + (data[6] << 8)
    # z = data[7] + (data[8] << 8)
    x1=(x*Xsf)+Xoff
    y1=(y*Ysf)+Yoff
    azimuth = (math.atan2(y1, x1) * 180.0 / math.pi)+declinationmagnetique
    if azimuth<0:
        azimuth+=360
    ang.append(azimuth)
  
def qmc5883l(my_board):
    """Renvoie l'angle de direction"""
    # device address = 13
    my_board.set_pin_mode_i2c()
    # initialize the qmc5883l
    # this is the equivalent of void QMC5883LCompass::init() in the library.
    # https://github.com/mprograms/QMC5883LCompass/blob/9f627ec5fcad7e7ddc15d7ed63c8bcc9ab940947/src/QMC5883LCompass.cpp#L69
    # write a value of 1 to register 0xb of the device
    # the first byte is the device address and next 2 bytes are what is being written
    # to the device. 11 is the 0xB register, and 1 is the value we are writing.
    my_board.i2c_write(13, [11, 1])
    time.sleep(.1)
    # now we need to set the device mode.
    # we will set the mode using the same values used by the Arduino library.
    MODE = 1
    ODR = 12  # output data rate
    RANGE = 16
    OSR = 0  # OVER_SAMPLE_RATION
    CONTROL_REGISTER_1 = 9
    MODE_DATA = MODE | ODR | RANGE | OSR
    # write the data to control register 1
    my_board.i2c_write(13, [CONTROL_REGISTER_1, MODE_DATA])
    time.sleep(.1)
    # read the xyz registers - data will be returned in the callback
    # the call back will calculate the azimuth
    my_board.i2c_read(13, 0, 6, the_call_back)

######################################################################################################

#########################################-Execution du code-##########################################

try:
    board.set_pin_mode_servo(Servo_pin)
    board.set_pin_mode_sonar(trig,echo)
    board.set_pin_mode_analog_input(RIGHT)
    board.set_pin_mode_analog_input(LEFT)
    board.set_pin_mode_pwm_output(GA)
    board.set_pin_mode_pwm_output(GB)
    board.set_pin_mode_pwm_output(DA)
    board.set_pin_mode_pwm_output(DB)
    time.sleep(1)
    #G=dictionnaire()
    G2=G.copy()
    départ=depart()
    arrivé=arrivée()
    matrice(G)
    #graph(G,départ,arrivé)
    affichage(G, départ, arrivé)
    manuelle(G)
    vecteur()
    while len(chemin[0])!=1:
        time.sleep(0.07)
        print(f"\nVous êtes sur le sommet {chemin[0][0]}")
        Direct(coordonnée(chemin[0][0]),coordonnée(chemin[0][1]))
        if mvm[0]=="r180":
            r180()
            board.servo_write(Servo_pin,anglec)
        elif mvm[0]=="gauche90":
            board.servo_write(Servo_pin,angleg)
        elif mvm[0]=="droite90":
            board.servo_write(Servo_pin,angled)
        time.sleep(0.5)
        while len(distance)<=3:
            (dist,temp)=board.sonar_read(trig)
            distance.append(dist)
        board.servo_write(Servo_pin,anglec)
        if distance[-1]>25:
            if mvm[0]=="droite90":
                droite90()
            elif mvm[0]=="gauche90":
                gauche90()
            avancer()
            del(chemin[0][0])
        else:
            print("\nCette route est bloquée, nous allons procéder à un changement d'itinéraire: ")
            for cle,valeur in G2.items():
                if cle==chemin[0][0]:
                    for k,j in valeur.items():
                        if k==chemin[0][1]:
                            j=float('inf')
            chemin2=chemin.copy()
            chemin.clear()
            affichage(G,chemin2[0][0],arrivé)
            G2=G
        distance.clear()
        mvm.clear()
    print("Vous êtes arrivé(e) à destination !") 
    while True:
        if 1>float("inf"):
            print("")
except KeyboardInterrupt: #ctrl+c
    arret()
    board.shutdown()
    sys.exit(0)    

########################################################################################################################
