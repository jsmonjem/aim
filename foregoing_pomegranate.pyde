
def generarObjetivo(velx,vely): #definir las coordenadas donde se encuentra el objetivo.
    x = map(sin(velx*TWO_PI*millis()/(12000.0)),-1,1, 100, width-100) #icion en x 
    y = map(sin(vely*TWO_PI*millis()/(14000.0)),-1,1, 100, height-100) #icion en y
    z = map(sin(TWO_PI*millis()/(50000.0)),-1,1, 45, 50) #icion en z (tamaño)
    return x, y, z
        
def impacto(x,y,z): #determinar si la mira esta sobre el objetivo.
    return sqrt((mouseX - x)**2 + (mouseY - y)**2) <= z / 2
   
def dibujarObjetivo(x, y, z, filling=0):
    noStroke()
    for i in range(5, 0, -1):
        fill(filling + i * 12)
        circle(x, y, z * (i / 5.0))

def mira(sens=0.5): #dibuar la mira en el canvassss.
    fill(255,32,9)
    algo=5
    for i in range(5, 0, -1):
        fill(255*algo/i, 32*algo/i, 9*algo/i)
        circle(mouseX, mouseY, 10 * (i / 5.0))
    
def mostrarpuntaje(puntaje): #dibujar un puntaje en el canvassss
    fill(0)
    textSize(32)
    textAlign(LEFT, CENTER)
    text("puntaje: "+ str(puntaje), width/20, height/20)    

def menuPrincipal():
    global esPrimeraVez1, jugando
    if esPrimeraVez1: #creo tres objetivos solo al iniciar la funcion.
        for i in range(3):
            listaJuegos.append((width/6+(width)/3*i,height/2,25))
        esPrimeraVez1 = False
    if jugando != None: # si estoy jugando,
        # creo un boton para volver al menu. 
        background(230)
        dibujarObjetivo(width-(width/20),height/20,25)
        if mousePressed and mouseButton==RIGHT and impacto(width-(width/20),height/20,25): 
            jugando = None
        
        if jugando ==0:
            jugarTracking()
        elif jugando ==1:
            jugarPunteria()
        elif jugando ==2:
            jugarEntrePuntos()
    else: #si no estoy jugando
        background(230)
        for i in range(3):
            dibujarObjetivo(*listaJuegos[i])
            mira()
            if mousePressed and mouseButton==LEFT and impacto(*listaJuegos[i]):
                if i==0:
                    jugando=0
                    resetGlobal()    
                    return                        
                elif i ==1:
                    jugando=1
                    resetGlobal()
                    return
                elif i == 2:
                    jugando=2
                    resetGlobal()
                    


def resetGlobal():
    global posX, posY, tamZ, listaObjetivos, listaJuegos, puntaje
    global trackingTime, umbralTracking, lastCheck
    global esPrimeraVez, esPrimeraVez1, objetivoInicializado, enMovimiento
    
    jugando = None
    posX, posY, tamZ = 0, 0, 0
    listaObjetivos=[]
    listaJuegos=[]
    puntaje = 0
    trackingTime = 0      # cuanto tiempo llevás siguiéndolo
    umbralTracking = 1000  # milisegundos necesarios para sumar puntaje
    lastCheck = 0         # para controlar el tiempo
    esPrimeraVez=True
    esPrimeraVez1=True
    objetivoInicializado=True
    enMovimiento = False

###################
####MINIGAMES######
###################


def jugarTracking(): # con el objetivo en movimiento(x,y,z), sumar puntos segun el tiempo de impacto. 
    global puntaje, trackingTime, lastCheck, umbralTracking
    
    x,y,z = generarObjetivo(2,2)
    dibujarObjetivo(x,y,z)
    mira()
    
    ahora = millis()
    delta = ahora - lastCheck
    lastCheck = ahora

    if impacto(x,y,z):
        trackingTime += delta #Le sumo al trackingTime un pequeño delta.
        if trackingTime >= umbralTracking: 
            puntaje += 1
            trackingTime = 0  # vuelvo a empezar a llenar...
    else:
        trackingTime = 0  # perdi el objetivo
    mostrarpuntaje(puntaje)
        
def jugarPunteria():
    global puntaje, esPrimeraVez, posX, posY, tamZ
    if esPrimeraVez:
        esPrimeraVez=False
        posX, posY, tamZ = generarObjetivo(random(10),random(10))
        
    dibujarObjetivo(posX, posY, tamZ)
    mira()
    if mousePressed and mouseButton==LEFT and impacto(posX, posY, tamZ):
        puntaje+=1
        posX, posY, tamZ = generarObjetivo(random(10),random(10))

    mostrarpuntaje(puntaje)
    
    
#Actualiza x,y,z  entre los Objetivos 1 y 2.
def easing(x1,y1,z1, x2,y2,z2, velocidad=0.08):
    global enMovimiento, posX, posY, tamZ, objetivoInicializado, listaObjetivos, puntaje
    
    if objetivoInicializado: #Guardar en las variables globales la icion esPrimeraVez del objetivo. 
        posX, posY, tamZ = x1, y1, z1
        objetivoInicializado=False
        puntaje = puntaje + 1
    #Si ya llegó al objetivo, baja la bandera "enMovimiento", borra el objetivo que ya se clickeo 
    #y añade otro objetivo a "listaObjetivos".
    if (abs(x2 - posX) < 1 and abs(y2 - posY) < 1 and abs(z2 - tamZ) < 1):
        enMovimiento = False
        objetivoInicializado=True
        listaObjetivos.pop(0)
        listaObjetivos.append(generarObjetivo(random(10),random(10)))
    else: #si no ha llegado, actualiza su posicion
        posX += (x2 - posX) * velocidad
        posY += (y2 - posY) * velocidad
        tamZ += (z2 - tamZ) * velocidad

def jugarEntrePuntos():
    global listaObjetivos, esPrimeraVez, enMovimiento, posX, posY, tamZ, puntaje
    
    if esPrimeraVez: ## Agregar los primeros dos listaObjetivos solo una vez
        for i in range(2):
            listaObjetivos.append(generarObjetivo(random(10),random(10)))    
        esPrimeraVez=False
    else:
        #si golpeo el primer objetivo, subo el flag para esPrimeraVezizar la animacion: enMovimiento
        if (mousePressed and mouseButton==LEFT and 
            impacto(listaObjetivos[0][0],listaObjetivos[0][1],listaObjetivos[0][2])):
            enMovimiento=True
            
        #mientras estamos animando (actualizando x,y,z), dibujo el objetivo en movimiento, mira y puntaje.
        if enMovimiento: #mientras estemos animando, actualizo x,y,z, y dibujo objetivo, mira y puntaje.
            easing(listaObjetivos[0][0],listaObjetivos[0][1],listaObjetivos[0][2],
                   listaObjetivos[1][0],listaObjetivos[1][1],listaObjetivos[1][2])

            dibujarObjetivo(posX, posY, tamZ)
            mira()
            mostrarpuntaje(puntaje)
            
        #y si no estamos animando, igual dibujo primer objetivo, mira y puntaje.
        else:
            dibujarObjetivo(listaObjetivos[0][0],listaObjetivos[0][1],listaObjetivos[0][2])
            mira()
            mostrarpuntaje(puntaje)
        
### VARIABLES GLOBALES ###
jugando = None
posX, posY, tamZ = 0, 0, 0
listaObjetivos=[]
listaJuegos=[]
puntaje = 0
trackingTime = 0      # cuanto tiempo llevás siguiéndolo
umbralTracking = 1000  # milisegundos necesarios para sumar puntaje
lastCheck = 0         # para controlar el tiempo
esPrimeraVez=True
esPrimeraVez1=True
objetivoInicializado=True
enMovimiento = False


#################################################################################
    
def setup():
    #fullScreen()
    #size(600,400)
    size(1366,768)
    
    noCursor()
    frameRate(144)
    
def draw():
    #background(230)
    menuPrincipal()

    
    
