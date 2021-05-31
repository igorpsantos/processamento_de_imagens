from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
from PIL.Image import *

# variavel utilizada para iniciar o tamanho da janela
w, h = 40, 30
posicao = 20
# variavel utilizada para o inicializador de pontos
pontos = 0
# variavel p/ pausar o jogo quando houver uma colisao
gameover = 0
# variavel p/ iniciar o jogo
start = 0
# variaveis utilizadas para recuperar o valor de y da nave
posicao_nave_y = 8.0
posicao_nave_x = 20.0
# variaveis utilizadas para recuperar o valor de y dos objetos
posicao_obj1_y, posicao_obj2_y, posicao_obj3_y = 0.0,0.0,0.0
# cria uma nova esfera
esfera = gluNewQuadric()
# variavel utilizado para mudar o cenario
changecolor = 0
# variavel auxiliar p/ utilização da textura
imageID = 0

def loadImage( imageName ):
    #"""Load an image file as a 2D texture using PIL"""
    im = open(imageName)
    try:
        ix, iy, image = im.size[0], im.size[1], \
            im.tobytes("raw", "RGB", 0, -1)
    except SystemError:
        ix, iy, image = im.size[0], im.size[1], \
            im.tobytes("raw", "RGBX", 0, -1)
        
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0,\
    GL_RGB, GL_UNSIGNED_BYTE, image )
    
    return ID

def init_textura():
    global imageID
    glEnable ( GL_TEXTURE_2D )
    imageID = loadImage("nave.jpg")
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

class Objetos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velx = 0.5
        self.vely = 0.5
        self.sinalx = 0
        self.sinaly = -1
        self.origemx = x
        self.origemy = y

    def draw(self):
        global changecolor
        glPushMatrix()
        glTranslatef(self.x,self.y,0)
        if changecolor == 0:
            glColor3d(0.0,0.8,0)
        else:
           glColor3d(0.1,0.1,0)
        gluQuadricTexture(esfera, True) # habilita textura na esfera
        gluSphere(esfera, 1.0, 32, 16) # desenha a esfera
        glPopMatrix()
    
    def timer(self):
        if self.y >= 0:
            self.x = self.x + self.velx * self.sinalx
            self.y = self.y + self.vely * self.sinaly
        else:
            self.x = random.randint(5,35) #self.x + self.velx * (self.sinalx + 0.5)
            self.y = self.origemy
    
    def getValueY(self):
        return self.y
        
    def getValueX(self):
        return self.x
    
    def reseta(self):
        self.x = random.randint(5,35)
        self.y = self.origemy

# instacia objetos p/ utilização na tela
obj1 = Objetos(5,30)
obj2 = Objetos(20,30)
obj3 = Objetos(35,30)

def nave():
    # define variavel global
    global posicao
    global changecolor

    glPushMatrix()
    glTranslatef(posicao,8,0)

    if changecolor == 0:
        glColor3d(1,0.5,0) # define nave como laranja
    else:
        glColor3d(0,0.1,0)

    # cria nave
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0); glVertex2f(-1, -1)
    glTexCoord2f(0.0, 1.0); glVertex2f(1, -1)
    glTexCoord2f(1.0, 1.0); glVertex2f(0, 1)    
    glEnd()
    glPopMatrix()

def criaEstrelas():
    global changecolor
    glPushMatrix()

    if changecolor == 0:
        glColor3f(1.0, 0.5, 1.0)
    else:
        glColor3f(0.0, 0.1, 1.0)

    glPointSize(5.0)
    glBegin(GL_POINTS)
    glVertex2f(5,15)
    glVertex2f(8,25)
    glVertex2f(10,10)
    glVertex2f(12,5)
    glVertex2f(14,15)
    glVertex2f(16,25)
    glVertex2f(18,10)
    glVertex2f(20,5)
    glVertex2f(22,15)
    glVertex2f(24,25)
    glVertex2f(26,10)
    glVertex2f(28,5)
    glVertex2f(30,15)
    glVertex2f(32,25)
    glVertex2f(34,10)
    glVertex2f(36,5)
    glEnd()
    glPopMatrix()

def glut_print( x,  y,  font,  text, r,  g , b):
    blending = False 
    if glIsEnabled(GL_BLEND) :
        blending = True

    glColor3f(r,g,b)
    glRasterPos2f(x,y)
    for ch in text :
        glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )
        
    if not blending :
        glDisable(GL_BLEND) 

def timer(valor):
    global gameover
    global start
    global posicao_nave_y
    global posicao_obj1_y
    global posicao_obj2_y
    global posicao_obj3_y

    glutPostRedisplay()

    if start == 1:
        ContaPontos()
        obj1.timer()
        obj2.timer()
        obj3.timer()

    #recupera os valores do eixo y
    posicao_obj1_y = obj1.getValueY()
    posicao_obj2_y = obj2.getValueY()
    posicao_obj3_y = obj3.getValueY()

    # se houver colisao seta a variavel gameover como 1
    print(posicao_nave_y, posicao_obj1_y, posicao_obj2_y, posicao_obj3_y)
    if posicao_nave_y == posicao_obj1_y and posicao_nave_x == obj1.getValueX():
        gameover = 1
    elif posicao_nave_y == posicao_obj2_y and posicao_nave_x == obj2.getValueX():
        gameover = 1
    elif posicao_nave_y == posicao_obj3_y and posicao_nave_x == obj3.getValueX():
        gameover = 1

    # seta o timer apenas se não tiver gameover
    if gameover == 0 and start == 1:
        glutTimerFunc(33, timer, 1)

def ContaPontos():
    global pontos
    global changecolor
    pontos = pontos + 1

    if pontos == 500:
        changecolor = 1
    elif pontos == 1000:
        changecolor = 0
    elif pontos == 1500:
        changecolor = 1
    elif pontos == 2000:
        changecolor = 0


def RenderizaTextos():
    global pontos
    global gameover
    global start
    glut_print( 36, 28, GLUT_BITMAP_9_BY_15, str(pontos), 1.0 , 0.0 , 0.0)

    # caso perca o jogo, escreve o texto de game over
    if gameover == 1:
        glut_print( 18, 24, GLUT_BITMAP_9_BY_15 , 'GAME OVER!', 1.0 , 0.0 , 0.0)
        glut_print( 15.5, 22, GLUT_BITMAP_9_BY_15 , 'PRESSIONE F2 PARA REINICIAR!!', 1.0 , 0.0 , 0.0)
    # caso seja o inicio do jogo, escreve o texto de inicio de jogo
    if start == 0:
        glut_print( 15, 24, GLUT_BITMAP_9_BY_15 , 'PRESSIONE F1 PARA INICIAR O JOGO!', 1.0 , 0.0 , 0.0)

def keyboardglut(key, x, y):
    global posicao
    global posicao_nave_x
    global start
    global gameover
    global obj1
    global obj2
    global obj3
    global pontos
    
    # movimenta o eixo x para a esquerda
    if key == GLUT_KEY_LEFT and posicao > 3:
        posicao = posicao - 1.0
        posicao_nave_x = posicao
        print('posicao esq = ', posicao)
    # movimenta o eixo x para a direita
    elif key == GLUT_KEY_RIGHT and posicao < 37:
        posicao = posicao + 1.0
        posicao_nave_x = posicao
        print('posicao dir = ', posicao)
    # inicia o jogo
    elif key == GLUT_KEY_F1:
        start = 1
        time.sleep(1)
        glutTimerFunc(33, timer, 1)
    # reinicia o jogo
    elif key == GLUT_KEY_F2:
        start = 1
        gameover = 0
        posicao = 20
        pontos = 0
        obj1.reseta()
        obj2.reseta()
        obj3.reseta()
        time.sleep(1)
        glutTimerFunc(33, timer, 1)

def init():
    global changecolor
    if changecolor == 0:
        glClearColor(0,0,0,1.0) # branco
    else:
        glClearColor(1,1,1,1.0) # branco
    glViewport(0,0,w*30,h*20)
    init_textura()

def reshape( x, y ):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, 0, h, 0.0, 1.0)

def display():
    global gameover
    global start
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()

    nave()
    RenderizaTextos()
    criaEstrelas()

    if gameover == 0 or start == 1:
        obj1.draw()
        obj2.draw()
        obj3.draw()
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode( GLUT_RGB | GLUT_DOUBLE )
    glutInitWindowSize( w*30, h*20 )
    glutInitWindowPosition( 0, 0 )
    wind = glutCreateWindow("Prova")

    init()
    # call back functions
    glutDisplayFunc( display )
    glutReshapeFunc( reshape )
    glutSpecialFunc(keyboardglut)
    glutTimerFunc(33, timer, 1)

    glutMainLoop()

if __name__=="__main__":
    main()
