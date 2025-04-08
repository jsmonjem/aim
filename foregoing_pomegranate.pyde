def coordObjetivo(velx,vely):
    posx = map(sin(velx*TWO_PI*millis()/(12000.0)),-1,1, 100, width-100) #posicion en x 
    posy = map(sin(vely*TWO_PI*millis()/(14000.0)),-1,1, 100, height-100) #posicion en y
    posz = map(sin(TWO_PI*millis()/(50000.0)),-1,1, 40, 60) #posicion en z (tamaño)
    return posx, posy, posz
    
def dibujarObjetivo(posx,posy,posz):
    fill(0)
    stroke(0)
    circle(posx, #posicion en x 
           posy, #posicion en y
           posz) #posicion en z (tamaño)
    
def mira():
    fill(255,32,9)
    stroke(255,199,191)
    circle(mouseX,mouseY,10)
    
def impacto(x,y,z):
    if sqrt((mouseX-x)**2+(mouseY-y)**2) <= z/2:
        return True
    return False
    
def setup():
    size(1366,768)
    noCursor()
    frameRate(144)
    
def draw():
    background(230)
    
    x,y,z = coordObjetivo(2,2)
    dibujarObjetivo(x,y,z)
    mira()
    
    
    #print(frameRate)
    #print(frameCount)
    #print("")
