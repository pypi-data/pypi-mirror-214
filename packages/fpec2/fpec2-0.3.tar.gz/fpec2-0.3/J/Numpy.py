class Numpy():
    def nada(self):
        print("nada")
    def H(self):
        v=0
        self.r=str(input('El principal beneficio de NumPy es que permite una generación y manejo de datos extremadamente rápido. NumPy tiene su propia estructura de datos incorporada llamado:(arreglo/Diccionario)'))
        if self.r=="arreglo":
            v=v+1
            
            self.b=str(input('2. ¿cual es el alias más común para la librería? (np/lgn)'))
            if self.b=='np':
                v=v+1
                self.e=str(input('3. ¿cual es la función que se usa para crear arreglos? [ array() / Arreglo() ]'))
                
                if self.e=="array()":
                    v=v+1
                    self.g=str(input("""4.¿Cuál es el resultado de la siguiente linea de codigo?
        np.arange(0,5)

        a)[1,2,3,4,5]
        b)[0,1,2,3,4]
"""))
                    
                    if self.g=="b":
                        v=v+1
                        self.i=str(input("""5. ¿Qué hace la siguiente linea de código?
np.zeros(5,5)
a)Crear una matriz de ceros con dimensiones 5x5
b)Crear una matriz 5x5 llena de unos
"""))
                        if self.i=="a":
                            
                            v=v+1
                            self.Puntajes[self.aleatorio1]=(self.Puntajes[self.aleatorio1]+v)
                            self.seguir_juego()
                            
                            
                            
                        else:
                            print("incorrecto")
                            self.Puntajes[self.aleatorio1]=(self.Puntajes[self.aleatorio1]+v)
                            self.comienzo_de_juego()
                            
                    else:
                        print("incorrecto")
                        self.Puntajes[self.aleatorio1]=(self.Puntajes[self.aleatorio1]+v)
                        self.comienzo_de_juego()
                        
                else:
                    print("incorrecto")
                    self.Puntajes[self.aleatorio1]=(self.Puntajes[self.aleatorio1]+v)
                    self.comienzo_de_juego()
                    
            else:
                print("incorrecto")
                self.Puntajes[self.aleatorio1]=(self.Puntajes[self.aleatorio1]+v)
                self.comienzo_de_juego()
                
        else:
            print("incorrecto")
            self.Puntajes[self.aleatorio1]=(self.Puntajes[self.aleatorio1]+v)
            self.comienzo_de_juego()
            
          