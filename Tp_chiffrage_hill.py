import numpy
import math
import random
from numpy import matrix
from numpy import linalg


def modMatInv(A,p):       # Finds the inverse of matrix A mod p
  n=len(A)
  A=matrix(A)
  adj=numpy.zeros(shape=(n,n))
  for i in range(0,n):
    for j in range(0,n):
      adj[i][j]=((-1)**(i+j)*int(round(linalg.det(minor(A,j,i)))))%p
  return (modInv(int(round(linalg.det(A))),p)*adj)%p
def modInv(a,p):          # Finds the inverse of a mod p, if it exists
  for i in range(1,p):
    if (i*a)%p==1:
      return i
  #raise ValueError(str(a)+" has no inverse mod "+str(p))
  print("La matrice entrée n'est pas inversible, donc non conforme...");
  exit(0);
def minor(A,i,j):    # Return matrix A with the ith row and jth column deleted
  A=numpy.array(A)
  minor=numpy.zeros(shape=(len(A)-1,len(A)-1))
  p=0
  for s in range(0,len(minor)):
    if p==i:
      p=p+1
    q=0
    for t in range(0,len(minor)):
      if q==j:
        q=q+1
      minor[s][t]=A[p][q]
      q=q+1
    p=p+1
  return minor

def FormatageHill(message, p):     #retourne le message avec une longueur multiple de p (en ajoutant des "#")
    longueur = len(message);
    while(longueur%p != 0):
        message+="#";
        longueur +=1;
    return message;

def MultiplicationMatriceVecteur(A , V, p): #retourne le vecteur resultat de (matrice A * Vecteur V) le tout modulo 127
    Vc = [];
    
    for l in range (0,p,1):
        temp = 0;
        for m in range (0,p,1):
            temp += A[l][m]*V[m];
        Vc.append(temp%127);
    return Vc;

def RemplirMatrice(strMatrice,p):   #remplis une matrice a partir d'une chaine de caractere avec des espaces entre chaque terme
    A = []; #initialisation matrice d'encodage A
    SpaceCompt=0;
    iterateur =0;
    for i in range (0,p,1):
        listetemp = []; #liste temporaire permettant de créer la matrice A
        nbrtemp ="";
        while (SpaceCompt < p):
            while (strMatrice[iterateur] != " "):
                nbrtemp += strMatrice[iterateur];
                iterateur +=1;
                if (iterateur == len(strMatrice)):
                    listetemp.append(int(nbrtemp));
                    A.append(listetemp);
                    return A;
            iterateur +=1;
            SpaceCompt +=1;
            listetemp.append(int(nbrtemp));
            nbrtemp ="";
        A.append(listetemp);
        SpaceCompt = 0;
    return A;

def TestEntreeMatrice(strMatrice,p): #test si la saisie utilisateur est correcte
    SpaceCompt=0;
    for i in range (0,len(strMatrice),1): #boucle de test du nombre de termes entrés (sont ils en accord avec la dimension de la matrice ?)
        if (strMatrice[i]==" "):        
            SpaceCompt +=1;     #comte le nombre d'espaces
    if (SpaceCompt != (p*p-1)): #si le nombre d'espace est incorrect, le programme s'arrete avec le code d'erreur 0
        print("entrée incorecte (nombre de caractère incompatible avec la dimension de la matrice");
        exit(0);

def Hill(MessageNonCripte,p,B):   #retourne le message crypté (si matrice codante) ou décrypté (si matrice inverse mod 127 )
    MessageCripte = "";
    Vb=[];
    for i in range(0,len(MessageNonCripte),p):  #decoupage du texte en vecteurs contenant 5 codes ascii
        for j in range (0,p,1):
            Vb.append(ord(MessageNonCripte[i+j]));       #vecteur contenant 5 codes ascii
                 
        
        Vc = MultiplicationMatriceVecteur(B , Vb,p);    #nouveau vecteur des codes ascii qui ont étés multipliés par A modulo 127
        Vb=[];
        for k in range(0,p,1):                 #le vecteur se vide dans la chaine receptrice sous forme de caracteres
            MessageCripte += chr(int(Vc[k]));
    return MessageCripte;

def AfficherMatrice(A): #affiche la matrices sur plusieurs lignes dans la console
    for i in range (0,len(A)):
        for j in range (0,len(A)):
            print(A[i][j],end=' ');
        print();

def CreerMatrice(p):    #construit une matrice carrée d'ordre p avec des nombres aléatoires entre 1 et 100
    A = [];
    for i in range (0,p):
        templist = [];
        for j in range (0,p):
            templist.append(random.randint(1, 101));
        A.append(templist);
    return A;

GoodChoice = False; 
while(GoodChoice != True):
    p = int(input("Quelle est la taille des blocs d'encodage ? (7 maximum)\n")); #demande utilisateur de la dimension
    if(p > 7):
        print("Les blocs ne peuvent pas etre plus grands que 7...")
    else:
        GoodChoice = True;
print("Si vous voulez entrer une matrice tapez 1, si vous voulez qu'elle soit genrée automatiquement tapez 2 ");
choice = int(input("dans ce dernier cas, la matrice peut s'averer non inversible et vous devrez relancer le programme...)\n"));
if(choice==1):  #l'utilisateur veut entrer une matrice
    print("\nEntrez chaque terme de la matrice ",p,"x",p," séparés par des espaces :");   
    strMatrice = str(input());  #input des termes de la matrice
    TestEntreeMatrice(strMatrice,p);    #test de la saisie utilisateur
    A = RemplirMatrice(strMatrice,p);   #la matrice A est créée
if(choice==2):  #l'utilisateur laisse la matrice se generer aléatoirement
    A = CreerMatrice(p);    #création d'une matrice d'ordre p aléatoire
if(choice != 1 and choice != 2):    #saisie differente de 1 et de 2 (invalide)
    print("\nla saisie est invalide...\n");
    exit(0);

B = modMatInv(A,127);      #matrice B = A^-1  (matrice de décodage)

FichierSource = open("ressources\crypt.txt");   #cible du fichier du texte à encoder
MessageNonCripteNonFormate = FichierSource.read();  #transfert du fichier dans une chaine de caractere
MessageNonCripte = FormatageHill(MessageNonCripteNonFormate,p);   #le message a maintenant une longueur multiple de p
MessageCripte = Hill(MessageNonCripte,p,A);     #Application du chiffrage de hill (avec A donc pour coder)
MessageDecripte = Hill(MessageCripte,p,B);      #Application du chiffrage de hill (avec B donc pour Décoder)
#affichage console des messages initial, crypté et décrypté :
print("\nMessage initial :\n",MessageNonCripteNonFormate,"\n\nMessage cripté :\n",MessageCripte,"\n\nMessage Décripté :\n",MessageDecripte,"\n\nCe code a été réalisié avec la matrice codante :");
AfficherMatrice(A);
print();


    

