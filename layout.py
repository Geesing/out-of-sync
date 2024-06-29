"""CS 108 A Final Project

Part of the model for the "Out of Sync" parallel-dimensional 2D platforming
puzzle, supplying the Layout class for usage in creating and playing levels;
uses lists and files.

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

from level_graphics_objects import Block, Spikes, LevelEnding, Avatar

class Layout:
    """Represents a level layout of Block, Spikes, LevelEnding, and Avatar
       objects."""
    
    def __init__(self, file_name, drawing, avatar_color):
        """Receives and reads a file to initialize and store every
           LevelGraphicsObject in the layout; receives a drawing on which to
           draw the LevelGraphicsObjects and the color with which to draw its
           Avatar; expects last file line to contain the Avatar's desired
           starting coordinates in the format '#, #', without parentheses, and
           sets layout width based on the length of the top line in the file."""
        
        self.UNIT = 50
        
        self.drawing = drawing
        self.avatar_color = avatar_color
        self.avatar = None
        self.avatar_graphic = None
        self.blocks = []
        self.exits = []
        self.spikes = []
        self.beaten = False

        with open(file_name) as level_map:
            # Store file's contents to iterate through later.
            map_lines = level_map.readlines()
            
            # Set the layout dimensions in layout units based on the length of
            # the top line of the file and the number of lines in the file.
            self.width_in_layout_units = len(map_lines[0].strip())
            self.height_in_layout_units = len(map_lines) - 1
            
            # Iterate through the indexes of each line in the file.
            for line_index in range(len(map_lines) - 1):
                
                # Remove newline character from each file line to allow accurate
                # count of block spaces.
                map_lines[line_index].strip()
                
                # Iterate through the indexes of each character in each line.
                for char_index in range(len(map_lines[line_index])):
                    
                    # Initialize a Block when the '#' symbol is encountered in
                    # the file, with the same relative scaled coordinates as the
                    # relative location of the '#' among the other characters.
                    if map_lines[line_index][char_index] == '#':
                        
                        # Initialize the Block object at the correct relative
                        # position.
                        block = Block(x_pos=self.UNIT * char_index + self.UNIT/2,
                                      y_pos=self.UNIT * line_index + self.UNIT/2,
                                      size=self.UNIT)
                        
                        # Store the Block in a list to be accessed later.
                        self.blocks.append(block)
                    
                    
                    # Initialize a Spike when the '^' symbol is encountered in
                    # the file, with the same relative scaled coordinates as the
                    # relative location of the '^' among the other characters.
                    elif map_lines[line_index][char_index] == '^':
                        
                        # Initialize the Spike object at the correct relative
                        # position.
                        spike = Spikes(x_pos=self.UNIT * char_index + self.UNIT/2,
                                       y_pos=self.UNIT * line_index + self.UNIT/2,
                                       size=self.UNIT)
                        
                        # Store the Spike in a list to be accessed later.
                        self.spikes.append(spike)
                    
                    
                    # Initialize an Exit when the '@' symbol is encountered in
                    # the file, with the same relative scaled coordinates as the
                    # relative location of the '@' among the other characters.
                    elif map_lines[line_index][char_index] == '@':
                        
                        # Initialize the Exit object at the correct relative
                        # position.
                        exit_portal = LevelEnding(x_pos=self.UNIT * char_index + self.UNIT/2,
                                                  y_pos=self.UNIT * line_index + self.UNIT/2,
                                                  size=self.UNIT)
                        
                        
                        # Store the Exit in a list to be accessed later.
                        self.exits.append(exit_portal)
            
            
            # Determine the Avatar's starting x and y coordinates from the
            # bottom line of the file.
            avatar_coords = map_lines[-1].split(',')
            avatar_x = float(avatar_coords[0].strip())
            avatar_y = self.height_in_layout_units - float(avatar_coords[1].strip()) - 1
            
            # Create the Avatar at the desired position with the desired color.
            self.avatar = Avatar(x_pos=self.UNIT * avatar_x + self.UNIT/2,
                                 y_pos =self.UNIT * avatar_y + self.UNIT/2,
                                 size=self.UNIT, color=self.avatar_color
                                 )
                        
        self.layout_width = self.UNIT * self.width_in_layout_units + 1
        self.layout_height = self.UNIT * self.height_in_layout_units + 1
                        

    def draw(self):
        """Draws the layout's LevelGraphicsObjects on the Layout Drawing."""
        
        self.drawing.width = self.layout_width
        self.drawing.height = self.layout_height
        self.drawing.bg = 'light gray'
        
        # Add line to separate the bottom of the layout Drawing from additional
        # widgets.
        self.drawing.line(0, self.layout_height - 1,
                          self.layout_width, self.layout_height - 1)
        
        # Draw level map.               
        for exit_portal in self.exits:
            exit_portal.draw(self.drawing)
            
        for block in self.blocks:
            block.draw(self.drawing)
                
        for spike in self.spikes:
            spike.draw(self.drawing)
        
        self.avatar_graphic = self.avatar.draw(self.drawing)
        
        
    def clear_avatar(self):
        """Removes the current GuiZero Drawing of the Avatar."""
        
        self.drawing.delete(self.avatar_graphic)