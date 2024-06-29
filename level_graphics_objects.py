"""CS 108 A Final Project

Part of the model for the "Out of Sync" parallel-dimensional 2D platforming
puzzle, supplying the classes LevelGraphicObject, Block, Spikes, LevelEnding,
and Avatar for usage in creating and playing level layouts.

FEATURES ADDED SINCE WALKTHROUGH
 - Avatar movement, both in response to player input and due to gravity
 - Collision detection to prevent the Avatars from phasing through level
   environments
 - Impalation detection to restart the level when the Avatar touches a spike
 - The ability to restart the level, resetting the positions of both a level's
   Avatars
 - "Ending" detection to end the level when the Avatar enters the same space
   as an exit portal.
 - The ability to end the level, returning to the menu with a congratulatory
   message.
 - A death counter to inform the user of how many times the Avatars have died in
   the current level attempt.
 - A "fewest attempts" counter which stores and displays the fewest attempts
   ever needed to beat the current level.
   
TO ADD/CREATE A LEVEL
 - Create a text file named with the format 'level#.txt' (for the main level
   layout) and a text file named with the format 'level#a.txt' (for the alt
   level layout).
      - In each file, enter a text block of spacing characters to represent
        empty spaces in the layouts (any character other than #, @, and ^ may be
        used). Do not leave any empty lines.
      - The length of the top line will be used to determine the width
        of the displayed layout.
      - Use # to represent a block, @ to represent an exit portal (finish line),
        and ^ to represent fatal spikes, positioning the characters within the
        text block at the same relative positions they should appear in the
        level.
      - Underneath the text block, write the desired starting coordinates for
        each layout's avatar in the format '#, #', without parentheses.
 - Create an empty text file named with the format 'min_attempts#.txt' (to store
   the record of fewest attempts needed to beat the corresponding level).
 - Change NUM_LEVELS under the create_menu method to the number of desired
   levels.

@author: Jason Chew (jgc23)
@author: Serita Nelesen (smn4)
@author: Keith Vander Linden (kvlinden)
@date: Fall, 2021

"""


class LevelGraphicObject:
    """Represents any object contained in a level layout."""
    
    def __init__(self, x_pos, y_pos, size):
        """Initialize position and size attributes for the LevelObject."""
        
        self.x = x_pos
        self.y = y_pos
        self.size = size
        
        
class Block(LevelGraphicObject):
    """Represents a square Block LevelObject."""
    
    def __init__(self, x_pos, y_pos, size):
        """Constructor for Block."""
        LevelGraphicObject.__init__(self, x_pos, y_pos, size)
            
    def draw(self, drawing):
        """Draw the Block on the received GuiZero drawing, centered on its x and
           y coordinates and with side length equal to its size. Returns the
           Block's Drawing ID (int) for reference."""
        
        return drawing.rectangle(self.x - self.size/2, self.y - self.size/2,
                                 self.x + self.size/2, self.y + self.size/2,
                                 color = 'white', outline=True)
                
        
class Spikes(LevelGraphicObject):
    """Represents a three-pronged Spike LevelObject."""
    
    def __init__(self, x_pos, y_pos, size):
        """Constructor for Spikes."""
        LevelGraphicObject.__init__(self, x_pos, y_pos, size)
        
    def draw(self, drawing):
        """Draw the Spikes on the received GuiZero drawing, centered on its x
           coordinate and placed at the bottom end of its y coordinate, with
           horizontal length equal to its size and spike height equal to half
           its size. Returns a list of the Spikes's Drawing IDs (int) for
           reference."""
        
        return [
                # Draw the spike base.
                drawing.rectangle(self.x - self.size/2, self.y + self.size*0.4,
                                  self.x + self.size/2 + 1, self.y + self.size/2,
                                  color = 'black'),
        
                # Draw the left spike.
                drawing.triangle(
                                 # Right spike, bottom left corner
                                 self.x - self.size/2, self.y + self.size/2,
                                 # Right spike, bottom right corner
                                 self.x - self.size/6, self.y + self.size/2,
                                 # Right spike, center point
                                 self.x - self.size/3, self.y
                                 ),
        
                # Draw the middle spike.
                drawing.triangle(
                                 # Middle spike, bottom left corner
                                 self.x - self.size/6, self.y + self.size/2,
                                 # Middle spike, bottom right corner
                                 self.x + self.size/6, self.y + self.size/2,
                                 # Middle spike, center point
                                 self.x, self.y
                                 ),
        
                # Draw the right spike.
                drawing.triangle(
                                 # Right spike, bottom left corner
                                 self.x + self.size/6, self.y + self.size/2,
                                 # Right spike, bottom right corner
                                 self.x + self.size/2, self.y + self.size/2,
                                 # Right spike, center point
                                 self.x + self.size/3, self.y
                                 )
                ]
        
        
class LevelEnding(LevelGraphicObject):
    """Represents an ovular exit (finish line) to a level layout."""
    
    def __init__(self, x_pos, y_pos, size):
        """Constructor for LevelEnding."""
        LevelGraphicObject.__init__(self, x_pos, y_pos, size)
        
    def draw(self, drawing):
        """Draw a portrait-orientation oval on the received GuiZero drawing,
           centered on its x and y coordinates to represent the exit doorway.
           Returns the LevelEnding's Drawing ID (int) for reference."""
        
        return drawing.oval(self.x - self.size/3, self.y - self.size//1.5,
                            self.x + self.size/3, self.y + self.size//1.5,
                            color = 'black', outline=True)
    
    
class Avatar(LevelGraphicObject):
    """Represents the player-controlled Avatar in a level layout."""
    
    def __init__(self, x_pos, y_pos, size, color='gray'):
        """Initialize Avatar characteristics (visual/positional)."""
        
        LevelGraphicObject.__init__(self, x_pos, y_pos, size)
        
        self.color = color
        self.starting_x = x_pos
        self.starting_y = y_pos
        self.GROUND_X_SPEED = 4
        self.JUMP_VEL = -14
        self.x_vel = 0
        self.y_vel = 0
        self.in_air = None
    
    
    def draw(self, drawing):
        # Draw the Avatar on the received GuiZero drawing, centered on its x and
        # y coordinates and with side length equal to its size. Returns the
        # Avatar's Drawing ID for reference.
        
        return drawing.rectangle(self.x - self.size/2, self.y - self.size/2,
                                 self.x + self.size/2, self.y + self.size/2,
                                 color = self.color, outline=True)
    
    
    def move(self, drawing):
        """Receives a GuiZero drawing; increments the Avatar's x-position by its
           x-velocity and its y-position by its y-velocity, unless doing so
           would cause it to move past the right, left, or bottom boundaries of
           the drawing."""
        
        self.x += self.x_vel
        self.y += self.y_vel
        
        # Stop the Avatar from moving past the horizontal drawing bounds.
        if self.x + self.size/2 > drawing.width:
            self.x = drawing.width - self.size/2
            self.x_vel = 0
        if self.x - self.size/2 < 0:
            self.x = self.size/2
            self.x_vel = 0

        # Stop the Avatar from falling through the floor.
        if self.y + self.size/2 + 1 >= drawing.height:
            self.y_vel = 0
            self.y = drawing.height - self.size/2 - 1
            self.in_air = False
        
        
    def apply_gravity(self):
        """Increments the Avatar's downward velocity by 1 up to its terminal
           velocity."""
        
        TERMINAL_VELOCITY = 10
        if self.y_vel < TERMINAL_VELOCITY:
            self.y_vel += 1
            
        self.in_air = True
    
    
    def prevent_obstructed_motion(self, block):
        """Prevent the Avatar from moving through the received Block."""

        self.y -= self.y_vel
        if self.colliding_with_block(block):
            if self.x_vel > 0:
                self.x = block.x - block.size/2 - self.size/2
#                 print('pushed back by block at   ', block.x/50 + 0.5, block.y/50 + 0.5)
            elif self.x_vel < 0:
                self.x = block.x + block.size/2 + self.size/2
#                 print('pushed forward by block at', block.x/50 + 0.5, block.y/50 + 0.5)
            self.x_vel = 0
        self.y += self.y_vel
        
        
        self.x -= self.x_vel
        if self.colliding_with_block(block):
            if self.y_vel > 0:
                self.y = block.y - block.size/2 - self.size/2
#                 print('pushed up by block at     ', block.x/50 + 0.5, block.y/50 + 0.5)
                self.in_air = False
            if self.y_vel < 0:
                self.y = block.y + block.size/2 + self.size/2
#                 print('pushed down by block at   ', block.x/50 + 0.5, block.y/50 + 0.5)
            self.y_vel = 0
        self.x += self.x_vel
                
    
    def colliding_with_block(self, block):
        """Receives a Block object and returns whether or not any of the
           Avatar's edges are positioned within the Block's boundaries."""
        
        return (block.x - block.size/2 < self.x + self.size/2 and
                block.x + block.size/2 > self.x - self.size/2 and
                block.y - block.size/2 < self.y + self.size/2 and
                block.y + block.size/2 > self.y - self.size/2)
    
    
    def is_impaled(self, spikes):
        """Receives a Spikes object and returns whether or not any of the
           Avatar's edges are positioned within the Spikes's boundaries."""
        
        return (spikes.x - spikes.size/2 < self.x + self.size/2 and
                spikes.x + spikes.size/2 > self.x - self.size/2 and
                spikes.y + spikes.size/2 > self.y - self.size/2 and
                spikes.y < self.y + self.size/2)
    
    
    def reached_exit(self, exit_portal):
        """Receives a LevelEnding object and returns whether or not the Avatar's
           position is sufficiently 'inside' of it."""
        
        return (exit_portal.x - exit_portal.size/4 <=
                self.x <= exit_portal.x + exit_portal.size/4 and
                exit_portal.y - exit_portal.size/4 <=
                self.y <= exit_portal.y + exit_portal.size/4)
            
            
    def respawn(self):
        """Resets the Avatar to its initial position (spawn point) and sets its
           velocities back to 0."""
        
        self.x = self.starting_x
        self.x_vel = 0
        
        self.y = self.starting_y
        self.y_vel = 0