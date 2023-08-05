class Tkinter():
    def nada(self):
        print("nada")
    def H(self):
        v=0
        self.r=str(input("""1. ¿cual de los siguientes elementos no está relacionado con tkinter?
a)Master
b)Primary key
c)Child"""))
        if self.r=="b":
            v=v+1
            print('jajaja')
            self.b=str(input('2. ¿cual es el alias más común para la librería? (np/tk)'))
            if self.b=='tk':
                v=v+1
                self.e=str(input("""3. ¿para que sirve la función Label?
a)crear cuadros de texto
b)crear ventanas
c)crear letreros con texto
"""))
                if self.e=="c":
                    v=v+1
                    self.g=str(input("""4.¿Que hace la siguiente linea de codigo?
Tk.messagebox:

a)crea un cuadro de texto
b)crea una nueva ventana
c)ninguna de las anteriores"""))
                    if self.g=="a":
                        v=v+1
                        self.i=str(input("""5. ¿la función button sirve para ? :
a)crear un botton
b)crear un frame
c)añadir una ventana emergente """))
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
            
          