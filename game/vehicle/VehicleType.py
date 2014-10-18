'''
Created on Oct 17, 2014

@author: vbms
'''

from abc import ABCMeta, abstractmethod
from OpenGL.GL import *
from OpenGL.GLUT import *
import config
from reportlab.lib.pdfencrypt import padding
from Vector3d import Vec3
from math import cos, sin, degrees, atan2, radians

class VehicleType:
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    speed = None
    rotateSpeed = None
    armor = None
    damage = None
    position = None
    turretDirection = Vec3(1,0,0)
    travelDirection = Vec3(1,0,0)
    aimDirection = Vec3(1,0,0)
    cameraOffset = [0.5, 0.105]
    
    weapons = None
    selectedWeapon = None
    
    boundingBox = None
    
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @abstractmethod
    def update (self):
        pass
    
    @abstractmethod
    def paint (self):
        pass
    
    def turnLeft (self):
        
        amount = self.rotateSpeed / 1000.0 * config.game.millis
        newDirection = ((degrees(atan2(self.travelDirection.y, self.travelDirection.x)) + 360) % 360) + amount
        self.travelDirection = Vec3(cos(radians(newDirection)), sin(radians(newDirection)), 0)
    
    def turnRight (self):
        
        amount = self.rotateSpeed / 1000.0 * config.game.millis
        newDirection = ((degrees(atan2(self.travelDirection.y, self.travelDirection.x)) + 360) % 360) - amount
        self.travelDirection = Vec3(cos(radians(newDirection)), sin(radians(newDirection)), 0)
    
    def moveForwald (self):
        
        self.move(self.travelDirection.normalized())
        
    def moveBackwald (self):
        
        self.move(-self.travelDirection.normalized())
    
    def move (self, direction):
        
        direction *= self.speed / 1000 * config.game.millis
        
        if direction.x < 0:
            newX = self.position[0] + direction.x
            if not config.game.level.isRoad(newX, self.position[1]) or not config.game.level.isRoad(newX, self.position[1] + self.boundingBox[1]):
                direction.x = 0;
        
        if direction.x > 0:
            newX = self.position[0] + direction.x + self.boundingBox[0]
            if not config.game.level.isRoad(newX, self.position[1]) or not config.game.level.isRoad(newX, self.position[1] + self.boundingBox[1]):
                direction.x = 0;
        
        if direction.y < 0:
            newY = self.position[1] + direction.y
            if not config.game.level.isRoad(self.position[0], newY) or not config.game.level.isRoad(self.position[0] + self.boundingBox[0], newY):
                direction.y = 0;
        
        if direction.y > 0:
            newY = self.position[1] + direction.y + self.boundingBox[1]
            if not config.game.level.isRoad(self.position[0], newY) or not config.game.level.isRoad(self.position[0] + self.boundingBox[0], newY):
                direction.y = 0;
        
        self.position[0] = self.position[0] + direction.x
        self.position[1] = self.position[1] + direction.y
    
    def moveAim (self, x, y):
        
        amountX = x * config.mouseSensitifiy;
        amountY = y * config.mouseSensitifiy;
        newDirectionX = self.aimDirection.getHorizontalAngle() + amountX
        newDirectionY = self.aimDirection.getVerticalAngle() + amountY
        
        x = cos(radians(newDirectionX))
        y = sin(radians(newDirectionX))
        z = sin(radians(newDirectionY))
        verticalCos = cos(radians(newDirectionY))
        
        self.aimDirection = Vec3(x * verticalCos, y * verticalCos, z)
    
    def getCameraPosition (self):
        
        vehicleCenter = (self.position[0] + self.boundingBox[0] / 2, self.position[1] + self.boundingBox[1] / 2, self.position[2] + self.boundingBox[2] / 2)
        horizontalDirection = Vec3(self.aimDirection.x, self.aimDirection.y, 0).normalized();
        negDirection = -horizontalDirection
        
        x = self.cameraOffset[0] * negDirection.x + vehicleCenter[0]
        y = self.cameraOffset[0] * negDirection.y + vehicleCenter[1]
        z = self.cameraOffset[1] + vehicleCenter[2]
        
        return (x, y, z)
    
    def paintBoundingBox (self):
        
        glBegin(GL_LINES)
        
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, self.boundingBox[2])
        glVertex3f(self.boundingBox[0], 0, 0)
        glVertex3f(self.boundingBox[0], 0, self.boundingBox[2])
        glVertex3f(0, 0, 0)
        glVertex3f(self.boundingBox[0], 0, 0)
        glVertex3f(0, 0, self.boundingBox[2])
        glVertex3f(self.boundingBox[0], 0, self.boundingBox[2])
        
        glVertex3f(0, self.boundingBox[1], 0)
        glVertex3f(0, self.boundingBox[1], self.boundingBox[2])
        glVertex3f(self.boundingBox[0], self.boundingBox[1], 0)
        glVertex3f(self.boundingBox[0], self.boundingBox[1], self.boundingBox[2])
        glVertex3f(0, self.boundingBox[1], 0)
        glVertex3f(self.boundingBox[0], self.boundingBox[1], 0)
        glVertex3f(0, self.boundingBox[1], self.boundingBox[2])
        glVertex3f(self.boundingBox[0], self.boundingBox[1], self.boundingBox[2])
        
        glVertex3f(0, 0, 0)
        glVertex3f(0, self.boundingBox[1], 0)
        glVertex3f(0, 0, self.boundingBox[2])
        glVertex3f(0, self.boundingBox[1], self.boundingBox[2])
        glVertex3f(self.boundingBox[0], 0, 0)
        glVertex3f(self.boundingBox[0], self.boundingBox[1], 0)
        glVertex3f(self.boundingBox[0], 0, self.boundingBox[2])
        glVertex3f(self.boundingBox[0], self.boundingBox[1], self.boundingBox[2])
        
        glEnd()
    
    def paintBox (self, xPos, yPos, zPos, xDim, yDim, zDim):
        
        glPushMatrix()
        glTranslate(xPos, yPos, zPos)
        #glScalef(xDim * scale, yDim * scale, zDim * scale)
        
        glBegin(GL_QUADS)
        
        glNormal3f(0, 0, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5 * xDim, -0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.5, 0.0); glVertex3f(0.5 * xDim, -0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.5, 0.5); glVertex3f(0.5 * xDim, 0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.0, 0.5); glVertex3f(-0.5 * xDim, 0.5 * yDim, 0.5 * zDim)
        
        glNormal3f(0, 0, -1)
        glTexCoord2f(0.5, 0.0); glVertex3f(-0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.5, 0.5); glVertex3f(-0.5 * xDim, 0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.0, 0.5); glVertex3f(0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.0, 0.0); glVertex3f(0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        
        glNormal3f(0, 1, 0)
        glTexCoord2f(0.0, 0.5); glVertex3f(-0.5 * xDim, 0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5 * xDim, 0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.5, 0.0); glVertex3f(0.5 * xDim, 0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.5, 0.5); glVertex3f(0.5 * xDim, 0.5 * yDim, -0.5 * zDim)
        
        glNormal3f(0, -1, 0)
        glTexCoord2f(0.5, 0.5); glVertex3f(-0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.0, 0.5); glVertex3f(0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.0, 0.0); glVertex3f(0.5 * xDim, -0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.5, 0.0); glVertex3f(-0.5 * xDim, -0.5 * yDim, 0.5 * zDim)
        
        glNormal3f(1, 0, 0)
        glTexCoord2f(0.5, 0.0); glVertex3f(0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.5, 0.5); glVertex3f(0.5 * xDim, 0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.0, 0.5); glVertex3f(0.5 * xDim, 0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.0, 0.0); glVertex3f(0.5 * xDim, -0.5 * yDim, 0.5 * zDim)
        
        glNormal3f(-1, 0, 0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5 * xDim, -0.5 * yDim, -0.5 * zDim)
        glTexCoord2f(0.5, 0.0); glVertex3f(-0.5 * xDim, -0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.5, 0.5); glVertex3f(-0.5 * xDim, 0.5 * yDim, 0.5 * zDim)
        glTexCoord2f(0.0, 0.5); glVertex3f(-0.5 * xDim, 0.5 * yDim, -0.5 * zDim)
        
        glEnd()
        
        glPopMatrix()
    
    