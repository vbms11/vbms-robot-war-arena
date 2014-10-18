import string
import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import config
from game import Game
import time

def initGame ():
    
    global lastFrameTime
    
    config.game = Game()
    config.game.init()
    
    lastFrameTime = int(round(time.time() * 1000))

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    
    lightAmbient = [0.5, 0.5, 0.5, 1.0]  
    lightDiffuse = [1.0, 1.0, 1.0, 1.0]     
    lightPosition = [-10.0, -10.0, 10.0, 1.0]
    glLightfv(GL_LIGHT1, GL_AMBIENT, lightAmbient);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightDiffuse);
    glLightfv(GL_LIGHT1, GL_POSITION,lightPosition);
    glEnable(GL_LIGHT1);
    glEnable(GL_LIGHTING);
    

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)    

# The main drawing function. 
def reRender():
    
    windowWidth = glutGet(GLUT_WINDOW_WIDTH)
    windowHeight = glutGet(GLUT_WINDOW_HEIGHT)
    
    glutWarpPointer(windowWidth / 2, windowHeight / 2)
    
    global game, lastFrameTime

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # Clear The Screen And The Depth Buffer
    glLoadIdentity()                    # Reset The View
    
    currentFrameTime = int(round(time.time() * 1000))
    frameInterval = currentFrameTime - lastFrameTime
    
    try:
        
        config.game.update(frameInterval)
        config.game.paint()
        
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno
        exit()
    
    glutSwapBuffers()
    glutPostRedisplay();
    
    lastFrameTime = currentFrameTime

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed (*args):
    
    # If escape is pressed, kill everything.
    if args[0] == config.ESCAPE:
        sys.exit()
    
    if args[0] == config.key_moveForwald:
        config.game.moveForwald = True
    if args[0] == config.key_moveBackwald:
        config.game.moveBackwald = True
    if args[0] == config.key_straffLeft:
        config.game.straffLeft = True
    if args[0] == config.key_straffRight:
        config.game.straffRight = True
    if args[0] == config.key_turnLeft:
        config.game.turnLeft = True
    if args[0] == config.key_turnRight:
        config.game.turnRight = True

def keyReleased (*args):
    
    if args[0] == config.key_moveForwald:
        config.game.moveForwald = False
    if args[0] == config.key_moveBackwald:
        config.game.moveBackwald = False
    if args[0] == config.key_straffLeft:
        config.game.straffLeft = False
    if args[0] == config.key_straffRight:
        config.game.straffRight = False
    if args[0] == config.key_turnLeft:
        config.game.turnLeft = False
    if args[0] == config.key_turnRight:
        config.game.turnRight = False

def mouseEvents (x, y):
    
    try:
        
        if config.centerMouse:
            
            # windowX = glutGet(GLUT_WINDOW_X)
            # windowY = glutGet(GLUT_WINDOW_Y)
            windowWidth = glutGet(GLUT_WINDOW_WIDTH)
            windowHeight = glutGet(GLUT_WINDOW_HEIGHT)
            
            offsetX = x - windowWidth / 2
            offsetY = y - windowHeight / 2
            
            config.game.moveMouse(offsetX, offsetY);
        else:
            pass
        
    except:
        print "error in mouse move"
        exit()

def main():
    
    global window
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    
    window = glutCreateWindow("Robot War Arena")
    
    #glutFullScreen()
    glutDisplayFunc(reRender)
    glutIdleFunc(reRender)
    
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    
    # Register the function called when the keyboard is pressed.  
    glutKeyboardFunc(keyPressed)
    glutKeyboardUpFunc(keyReleased)
    
    # Register the function called when the mouse is moved
    glutMotionFunc(mouseEvents);
    glutPassiveMotionFunc(mouseEvents);
    
    #
    glutSetCursor(GLUT_CURSOR_NONE);
    
    # Initialize our window. 
    InitGL(640, 480)
    
    initGame()
    
    # Start Event Processing Engine    
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
