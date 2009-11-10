### By Gonzalo Odiard, 2006 godiard at gmail.com
### GPL License - http://www.gnu.org/copyleft/gpl.html

# inicializacion
MARGEN = 0
SIZE_WORLD = 800			 # 700
CANT_TILES =  25 			 #  30
print "*** calculo SIZE "
SIZE_TILE = int((SIZE_WORLD - MARGEN * 2) / CANT_TILES)
print "Size tile:", SIZE_TILE

EVENT_DEATH = 10

class RabbitData:
    edadMaxima = 100
    madurezSexual = 20
    frecuenciaSexual = 10
    nivelCadenaAlimenticia = 1
    minFrecuenciaAlimentacion = 10
    maxFrecuenciaAlimentacion = 1
    maxNumeroCrias = 5
        
class WorldEvent:
    def __init__ (self,x,y,event):
        self.x = x
        self.y = y
        self.event = event;
        
		
class FoxData:
    edadMaxima = 150
    madurezSexual = 20
    frecuenciaSexual = 10
    nivelCadenaAlimenticia = 2
    minFrecuenciaAlimentacion = 20
    maxFrecuenciaAlimentacion = 3
    maxNumeroCrias = 3

class World:
    initialGreen = 10
    initialRabbits = 10
    initialFoxs = 10
    playState = False
    state = []
    events = []
    animals = []
    rain_value = 1
    
    rabbit_data = RabbitData()
    fox_data = FoxData()

	
    def animalsNear(self,x,y):
        animalsNear = []
        for n in range(len(self.animals)):
            animal = self.animals[n]
            if ((abs(animal.posX-x) == 1) and 
                (abs(animal.posY-y) == 1)):
                animalsNear.append(animal) 
                #print "Encuentra",x,y,animal.posX,animal.posY
        return animalsNear
        
        

