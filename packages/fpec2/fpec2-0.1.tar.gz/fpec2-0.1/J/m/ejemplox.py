import random
import calculo
import time
import Simpy
from calculo import Tkinter
from Numpy import Numpy
from Simpy import Simpy

class Juego():
    categorias = ["tkinter","Numpy","simpy"]
    jugadores = []
    Puntajes ={}
    

    def __init__(self):
        
        self.n=int(input("ingrese el numero de jugadores"))
        for i in range(self.n ):
            self.a=input("ingrese su username")
            self.jugadores.append(self.a)
            self.Puntajes[self.a]=0
        self.comienzo_de_juego()    
   

    def comienzo_de_juego(self): 
        v=0
        print(self.Puntajes)       
        self.aleatorio1 = random.choice(self.jugadores)
        if self.Puntajes[self.aleatorio1]>=10:
            print("el jugador",self.aleatorio1,"ha ganado") 
            time.sleep(10)     
        print("turno del jugador ",self.aleatorio1)
        self.aleatorio2 = random.choice(self.categorias)
        print("categoría designada ",self.aleatorio2)
        self.entrada=str(input('ingrece la categoria que le toco'))
        if self.entrada=="tkinter":
            Tkinter.H(self)
    
        elif self.entrada=="Numpy":
            Numpy.H(self) 
        elif self.entrada=="simpy":
            Simpy.H(self)

        else :
            self.comienzo_de_juego()    


    def seguir_juego(self):  
        v=0 
        print(self.Puntajes)   
        if self.Puntajes[self.aleatorio1]>=30:
            print("el jugador",self.aleatorio1,"ha ganado")  
                
        print("turno del jugador ",self.aleatorio1)
        self.aleatorio2 = random.choice(self.categorias)
        print("categoría designada ",self.aleatorio2)
        self.entrada=str(input('ingrece la categoria que le toco'))
        if self.entrada=="tkinter":
            Tkinter.H(self)
    
        elif self.entrada=="Numpy":
            Numpy.H(self)  
        elif self.entrada=="simpy":
            Simpy.H(self)             
        
    def calculo(self):
        self.r=int(input('1. ¿cual es el único número primo par?'))
        if self.r==2:
            print('jajaja')
            self.b=str(input('2. ¿Cómo se llama también el perímetro de un círculo? (circunferencia/radio)'))
            if self.b=='circunferencia':
                self.e=int(input('3. ¿Cuál es el número neto real después de 7?'))
                if self.e==11:
                    self.g=int(input('4.¿Cuántos segundos hay en un día?'))
                    if self.g==86400:
                        self.i=int(input('5. ¿Cuántos milímetros hay en un litro?'))
                        if self.i==1000:
                            print('ganaste')
                            
                            
                        else:
                            self.comienzo_de_juego()
                    else:
                        self.comienzo_de_juego()
                        
                else:
                    self.comienzo_de_juego()
            else:
                self.comienzo_de_juego()
        else:
            self.comienzo_de_juego()
            
a=Juego()
