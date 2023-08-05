class Simpy():
    def nada(self):
        print("nada")
    def H(self):
        v=0
        self.r=str(input('función que se usa en numpy para que un evento se lleve a cabo despues de un tiempo determinado o un evento determinad:(timeout/process)'))
        if self.r=="timeout":
            v=v+1
            
            self.b=str(input('2. metodo característico de simpy (yield/kield)'))
            if self.b=='yield':
                v=v+1
                self.e=str(input('3. ¿cual es el parametro usado en simpy para ejecutar una simulación? [ environment / process ]'))
                
                if self.e=="environment":
                    v=v+1
                    self.g=str(input("""4.¿Cuál es el resultado de las siguientes lineas de codigo?
        def car(env):
           while true:
           print("start parking at %d" % env.now)
           parking_duration = 5
           yield env.timeout(parking_duration)

           print("start driving at %d" % env.now)
           trip_duration = 2
           yield.envtimeout(trip_duration)

           

        a)muestra la hora en la que estacionó el auto 
        b)simula un pequeño trayecto donde sale del estacionamiento y viaja tiempo determinado
        c)todas las anteriores
"""))
                    
                    if self.g=="c":
                        v=v+1
                        self.i=str(input("""5. La función interrupt en simpy sirve para:
a)Detener una acción que se está ejecutando
b)aumentar el tiempo de espera entre una acción y otra de forma indefinida
c)ninguna de las anteriores
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
            
          