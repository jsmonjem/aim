
def generarObjetivo(velx,vely): #Devuelve x,y,z donde se encuentra el objetivo.
    t = 50
    x = map(sin(vely*TWO_PI*millis()/(8000.0)),     -1,   1,   t/2,                width-t/2) #posicion en x
    y = map(sin(vely*TWO_PI*millis()/(16000.0)),    -1,   1,   t/2,               height-t/2) #posicion en y
    z = map(sin(vely*TWO_PI*millis()/(24000.0)),    -1,   1,   t/2, ((width+height)*0.5)-t/2) #posicion en z 

    return x, y, z, t

def impacto(x, y, z, t):
    x2d,y2d,escalaMax=proyectarEnCanvas(x, y, z, t)
    return dist(mouseX, mouseY, x2d, y2d) <= escalaMax / 2

def proyectarEnCanvas(x, y, z, t):
    escalaMax=map(z,0,(width+height)*0.5,t,t*sqrt(escala))
    #si la profundidad es maxima, x2d esta entre XIzq y XDer
    #si la profundidad es 0, x2d esta entre 0 y width
    x2d=map(x,0, width,
            map(z, 0, (width+height)*0.5,     0, XIzq),
            map(z, 0, (width+height)*0.5, width, XDer)
            )
    #si la profundidad es maxima, y2d esta entre YSup y YInf
    #si la profundidad es 0, y2d esta entre 0 y height
    y2d=map(y,0, height,
            map(z, 0, (width+height)*0.5,      0, YSup),
            map(z, 0, (width+height)*0.5, height, YInf)
            )
    return x2d,y2d,escalaMax


def dibujarObjetivo1(x, y, z, t, filling=(80,80,80)): #Dibujar circulos en x, y de tamaño t.
    noStroke()
    for i in range(5, 0, -1):
        fill(filling [0] + i * 12,filling[1] + i * 12,filling[2] + i * 12)
        circle(x, y, t * (i / 5.0))

def dibujarObjetivo(x, y, z, t,filling=(80,80,80)):
    dibujarSombra(x, y, z, t)
    x2d, y2d, escalaMax = proyectarEnCanvas(x, y, z, t)    
    for i in range(10, 0, -1):
        fill(filling[0] - i * 12, filling[1] - i * 12, filling[2] - i * 12)
        circle(x2d, y2d, (i / 10.0)*escalaMax)
  

def dibujarSombra(x, y, z, t):
    global XIzq,YInf,XDer,YInf,escala
    # Sombra
    noStroke()
    fill(0, 50)
    
    #el tamaño depende de la profundidad
    escalaMax=map(z,0,(width+height)*0.5,t,t*sqrt(escala))

    #si la profundidad es maxima, x, esta entre XIzq y XDer
    #si la profundidad es 0,      x, esta entre 0 y width
    x2d=map(x,0, width,
            map(z, 0, (width+height)*0.5,     0, XIzq),
            map(z, 0, (width+height)*0.5, width, XDer)
            )
    
    #si la profundidad es maxima, y, es YInf
    #si la profundidad es         0, y es height  
    y2d=map(z,0, (width+height)*0.5,
            height, YInf)
                
    ellipse(x2d, y2d, 
            1.0 * map(z, 0, (width+height)*0.5, t, escalaMax), 
            0.3 * map(z, 0, (width+height)*0.5, t, escalaMax))  # elíptica y más achatada

def mira():
    dibujarObjetivo1(mouseX, mouseY, 0 , 7, filling=(255, 32, 9))
    
def mostrarpuntaje(puntaje): #dibujar un puntaje en el canvassss
    fill(0)
    textSize(32)
    textAlign(LEFT, CENTER)
    text("Puntaje: "+ str(puntaje), width/20, height/20)

def fondoPerspectiva():
    global XIzq, XDer, YSup, YInf, escala
    background(230)
    stroke(100)
    escalaFondo=sqrt(escala)
    
    XIzq= width * (1 - escalaFondo) / 2
    XDer= width * (1 + escalaFondo) / 2
    
    YSup= height * (1 - escalaFondo) / 2
    YInf= height * (1 + escalaFondo) / 2
    
    # Techo
    fill( 166, 172, 175)
    stroke(100)
    quad(0,0,width,0, XDer,YSup,XIzq,YSup)

    # Pared de fondo
    fill( 202, 207, 210)
    quad(XIzq,YSup,XDer,YSup, 
         XDer,YInf,XIzq,YInf)

    # Pared derecha
    quad(XDer,YSup,width,0, 
         width,height,XDer,YInf)

    # Pared izquierda
    quad(0,0,XIzq,YSup, 
         XIzq,YInf,0,height)

    # Pared de abajo
    fill(  215, 219, 221 )
    quad(XIzq,YInf,XDer,YInf, 
         width,height,0,height)


def menuPrincipal():
    global esPrimeraVez1, jugando
    if esPrimeraVez1: #creo tres objetivos solo al iniciar la funcion.
        for i in range(3):
            listaJuegos.append((width/6+(width)/3*i,height/2,(width+height)*0.25))
        esPrimeraVez1 = False
    if jugando != None: # si estoy jugando,
        # creo un boton para volver al menu.
        fondoPerspectiva()
        dibujarObjetivo(width-(width/20), height/20, 15, 30, filling=(0,0,255))
        if mousePressed and mouseButton==RIGHT and impacto(width-(width/20),height/20,15, 30):
            jugando = None

        if jugando ==0:
            jugarTracking()
        elif jugando ==1:
            jugarPunteria()
        elif jugando ==2:
            jugarEntrePuntos()
    else: #si no estoy jugando
        fondoPerspectiva()
        for i in range(3):
            dibujarObjetivo(listaJuegos[i][0],listaJuegos[i][1],listaJuegos[i][2], 50, filling=(100,100,100)) #TAMA;O DE 50
            mira()
            if mousePressed and mouseButton==LEFT and impacto(listaJuegos[i][0],listaJuegos[i][1],listaJuegos[i][2], 50):
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
    global posX, posY, posZ, listaObjetivos, listaJuegos, puntaje
    global trackingTime, umbralTracking, lastCheck
    global esPrimeraVez, esPrimeraVez1, objetivoInicializado, enMovimiento

    jugando = None
    posX, posY, posZ = 0, 0, 0
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

    x,y,z,t= generarObjetivo(2,2)
    dibujarObjetivo(x,y,z,t)
    mira()

    ahora = millis()
    delta = ahora - lastCheck
    lastCheck = ahora

    if impacto(x,y,z,t):
        trackingTime += delta #Le sumo al trackingTime un pequeño delta.
        if trackingTime >= umbralTracking:
            puntaje += 1
            trackingTime = 0  # vuelvo a empezar a llenar...
    else:
        trackingTime = 0  # perdi el objetivo
    mostrarpuntaje(puntaje)

def jugarPunteria():
    global puntaje, esPrimeraVez, posX, posY, posZ, t
    if esPrimeraVez:
        esPrimeraVez=False
        posX, posY, posZ, t = generarObjetivo(random(10),random(10))

    dibujarObjetivo(posX, posY, posZ, t)
    mira()
    if mousePressed and mouseButton==LEFT and impacto(posX, posY, posZ, t):
        puntaje+=1
        posX, posY, posZ, t= generarObjetivo(random(10),random(10))

    mostrarpuntaje(puntaje)

#Actualiza x,y,z  entre los Objetivos 1 y 2.
def easing(x1,y1,z1, x2,y2,z2, velocidad=0.08):
    global enMovimiento, posX, posY, posZ, t, objetivoInicializado, listaObjetivos, puntaje

    if objetivoInicializado: #Guardar en las variables globales la icion esPrimeraVez del objetivo.
        posX, posY, posZ = x1, y1, z1
        objetivoInicializado=False
        puntaje = puntaje + 1
    #Si ya llegó al objetivo, baja la bandera "enMovimiento", borra el objetivo que ya se clickeo
    #y añade otro objetivo a "listaObjetivos".
    if (abs(x2 - posX) < 1 and abs(y2 - posY) < 1 and abs(z2 - posZ) < 1):
        enMovimiento = False
        objetivoInicializado=True
        listaObjetivos.pop(0)
        listaObjetivos.append(generarObjetivo(random(10),random(10)))
    else: #si no ha llegado, actualiza su posicion
        posX += (x2 - posX) * velocidad
        posY += (y2 - posY) * velocidad
        posZ += (z2 - posZ) * velocidad

def jugarEntrePuntos():
    global listaObjetivos, esPrimeraVez, enMovimiento, posX, posY, posZ, puntaje, t

    if esPrimeraVez: ## Agregar los primeros dos listaObjetivos solo una vez
        for i in range(2):
            listaObjetivos.append(generarObjetivo(random(10),random(10)))
        esPrimeraVez=False
    else:
        #si golpeo el primer objetivo, subo el flag para esPrimeraVezizar la animacion: enMovimiento
        if (mousePressed and mouseButton==LEFT and
            impacto(listaObjetivos[0][0],listaObjetivos[0][1],listaObjetivos[0][2],listaObjetivos[0][3])):
            enMovimiento=True

        #mientras estamos animando (actualizando x,y,z), dibujo el objetivo en movimiento, mira y puntaje.
        if enMovimiento: #mientras estemos animando, actualizo x,y,z, y dibujo objetivo, mira y puntaje.
            easing(listaObjetivos[0][0],listaObjetivos[0][1],listaObjetivos[0][2],
                   listaObjetivos[1][0],listaObjetivos[1][1],listaObjetivos[1][2])

            dibujarObjetivo(posX, posY, posZ, 50)
            mira()
            mostrarpuntaje(puntaje)

        #y si no estamos animando, igual dibujo primer objetivo, mira y puntaje.
        else:
            dibujarObjetivo(listaObjetivos[0][0],listaObjetivos[0][1],listaObjetivos[0][2], 50)
            mira()
            mostrarpuntaje(puntaje)

### VARIABLES GLOBALES ###
escala=0.5
jugando = None
posX, posY, posZ = 0, 0, 0
listaObjetivos=[]
listaJuegos=[]
puntaje = 0
trackingTime = 0       # cuanto tiempo llevas siguiéndolo
umbralTracking = 1000  # milisegundos necesarios para sumar puntaje
lastCheck = 0          # para controlar el tiempo
esPrimeraVez=True
esPrimeraVez1=True
objetivoInicializado=True
enMovimiento = False

#################################################################################

def setup():
    fullScreen()
    #size(600,400)
    #size(1366,768)
    noCursor()
    frameRate(150)


def draw():
    menuPrincipal()
    global escala
    if keyPressed == True:
        if key=="i":
            escala=escala-0.001
        elif key =="k":
            escala=escala+0.001

    
    
    
    
    
    
    
    
    
    
