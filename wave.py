"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _moveRight: bool to keep track of the direction that aliens move in [True]
    _stepstoFire: the randomnly generated number to keep track of number of steps until alien fire [1 <= int <= BOLT_RATE]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializer: Creates a 2d list of aliens and a ship
        """
        self._aliens = self.alien_wave()
        self._ship = Ship()
        self._dline = GPath(points = [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE], linewidth = 1, linecolor = 'black')
        self._time = 0
        self._moveRight = True
        self._bolts = []
        self._stepsToFire = random.randint(1, BOLT_RATE)
        
    
    def alien_wave(self):
        """
        Returns: The 2d list of alien objects
        
        When this method completes, a wave of aliens is created on the screen
        with the specified rows and columns and the result is stored in the
        _aliens instance attribute.
        """
        aliens = []
        y = GAME_HEIGHT - (ALIEN_ROWS*ALIEN_HEIGHT) - ((ALIEN_ROWS - 1)*(ALIEN_V_SEP)) - ALIEN_CEILING + (ALIEN_HEIGHT/2)
        for row in range(ALIEN_ROWS):
            x = ALIEN_H_SEP + ALIEN_WIDTH/2
            lst = []
            for col in range(ALIENS_IN_ROW): 
                alienType = row%6
                if alienType == 0 or alienType == 1:   
                    lst.append(Alien(x, y, ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_IMAGES[0]))
                elif alienType == 2 or alienType == 3:    
                    lst.append(Alien(x, y, ALIEN_WIDTH,  ALIEN_HEIGHT, ALIEN_IMAGES[1]))
                elif alienType == 4 or alienType == 5:    
                    lst.append(Alien(x, y, ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_IMAGES[2]))
                x = x + ALIEN_H_SEP + ALIEN_WIDTH
            y = y + ALIEN_V_SEP + ALIEN_HEIGHT
            aliens.append(lst)
        aliens.reverse()
        return aliens
                    
  
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Moves the ship right or left every animation frame depending on the
        input received from the keyboard
        
        Parameter input: input taken from keyboard to check if user pressed the
        right or left arrow key
        Precondition: input is a GInput object
        """
        assert isinstance(input, GInput)
        
        if input.is_key_down('left'):
            self._shiftShipLeft()
            
        if input.is_key_down('right'):
            self._shiftShipRight()
        
           
        if input.is_key_down('up') or input.is_key_down('spacebar'):
            if self._playerBoltPresent() == False:
                self._bolts.append(Bolt())
    
        for bolt in self._bolts:
            if bolt.y - BOLT_HEIGHT/2 > GAME_HEIGHT or bolt.y + BOLT_HEIGHT/2 < 0:
                self._bolts.remove(bolt)
            else:
                bolt.y = bolt.y + bolt.getVelocity()
         
        self._time = self._time + dt
        if (self._time > ALIEN_SPEED):
            self._time = 0
            self._moveAliens()
            
            self._stepsToFire = self._stepsToFire - 1
            if self._stepsToFire == 0:
                self._alienToFire()
                
                
            
    
    #Helper Functions
    
    def _alienToFire(self):
        randcol = random.randint(0, ALIENS_IN_ROW-1)
        i = ALIEN_ROWS - 1
        isalienpresent = False
        while isalienpresent == False:
            for i in range(ALIEN_ROWS-1,0,-1):
                if self._aliens[i][randcol] != None:
                    self._bolts.append(Bolt(x=self._aliens[i][randcol].x, y=self._aliens[i][randcol].y-ALIEN_HEIGHT/2, fillcolor = "red", velocity=-1*BOLT_SPEED)) 
                    isalienpresent = True
                    break
                else:
                    i = i - 1
            randcol = random.randint(0, ALIENS_IN_ROW-1)        
        self._stepsToFire = random.randint(1, BOLT_RATE)    
                
                
    def _playerBoltPresent(self):
        for bolt in self._bolts:
            if bolt._isPlayerBolt():
                return True
        return False
        
        
    def _moveAliens(self):
        if self._moveRight:
            if GAME_WIDTH - (self._aliens[0][ALIENS_IN_ROW - 1].x + ALIEN_H_WALK) > ALIEN_H_SEP:
                self._shiftAliensRight()       
            else:
                self._moveRight = False
                self._shiftAliensdown()          
        else:
            if self._aliens[0][0].x - ALIEN_H_WALK > ALIEN_H_SEP:
                self._shiftAliensLeft()         
            else:
                self._moveRight = True
                self._shiftAliensdown()
                            
    def _shiftShipLeft(self):
        self._ship.x = self._ship.x - SHIP_MOVEMENT
        if self._ship.x - SHIP_WIDTH/2 < 0:
            self._ship.x = max(SHIP_WIDTH/2, self._ship.x)
        
    def _shiftShipRight(self):
        self._ship.x = self._ship.x + SHIP_MOVEMENT
        if self._ship.x + SHIP_WIDTH/2 > GAME_WIDTH:
            self._ship.x = min(GAME_WIDTH - SHIP_WIDTH/2, self._ship.x)
                
    def _shiftAliensRight(self):
        for row in self._aliens:
            for alien in row:
                alien.x = alien.x + ALIEN_H_WALK
    
    def _shiftAliensLeft(self):
        for row in self._aliens:
            for alien in row:
                alien.x = alien.x - ALIEN_H_WALK
        
    def _shiftAliensdown(self):
        for row in self._aliens:
            for alien in row:
                alien.y = alien.y - ALIEN_V_WALK
            
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, aliens, defensive line, and bolts to the provided game view
        
        Parameter view: The view to draw to
        Precondition: view is a GView object
        """
        assert isinstance(view, GView)
        
        for a in self._aliens:
            for b in a:
                b.draw(view)
        
        self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
        
    
    
    # HELPER METHODS FOR COLLISION DETECTION
