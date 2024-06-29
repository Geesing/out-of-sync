"""CS 108 A Final Project

This GUI view for "Out of Sync" (a parallel-dimensional 2D platforming puzzle)
presents the user with levels consisting of two alternate layouts made of
Block, Spikes, and LevelEnding objects (provided by the model), each layout
containing user-controlled avatars that make simultaneous movements.

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

from guizero import App, Box, Drawing, PushButton, Text
from layout import Layout

class GameWindow:
    
    def __init__(self, app):
        """Receives an app to initialize/open game widgets within, and initializes
           attributes storing level information."""
        
        # Establish app as class attribute for easier access.
        self.app = app
        
        # A box to contain the level selection box, a level completion
        # message box, and the quit button box.
        self.menu_box = Box(self.app)
        
        # A box to contain a centered level completion message.
        self.end_message_box = Box(self.menu_box, visible=False)
        Text(self.end_message_box, text='Level Complete!',
             font='Helvetica', size=25)
        
        # A box to contain the level selection buttons.
        self.level_select_box = Box(self.menu_box, layout='grid')
        
        # A box to contain the quit button.
        self.quit_button_box = Box(self.menu_box, layout='grid', align='bottom')
        
        # A box to contain level graphics (the level layouts and the control
        # panel box).
        self.level_box = Box(self.app, layout='grid', visible=False)
        
        # A box to contain the control panel (containing scores and a 'Return to
        # Menu' button, with a height set to the approximate height of the quit
        # button in pixels)
        self.control_panel_box = Box(self.level_box, layout='grid',
                                     width=1, height=85, grid=[0, 2])
        
        # The base string used in the attempt score Text widget.
        self.attempts_str = 'FEWEST ATTEMPTS\n(ALL TIME)\n'
        # A Text widget detailing the player's number of attempts.
        self.fewest_attempts_score = Text(self.control_panel_box,
                                          text=self.attempts_str, size=8,
                                          width=21, grid=[0, 0])
        
        # The base string used in the death count Text widget.
        self.deaths_str = 'DEATH COUNT\n'
        # A Text widget detailing the player's death count.
        self.death_score = Text(self.control_panel_box, text=self.deaths_str,
                                size=8, width=21, grid=[2, 0])
        
        # A quit button to exit the level and return to the menu.
        PushButton(self.control_panel_box, text='Return to Menu', width=30,
                   height=3, grid=[1, 0], command=self.close_level)
        
        # Initialize class attributes to store Layout objects for main and
        # alternate layouts.
        self.main_layout = None
        self.alt_layout = None

        # Create and open the initial level selection screen.
        self.create_menu()
        self.open_menu()
        
        # Stores movement keys pressed while in a level.
        self.pressed_movement_keys = []
        
        # Death counter, starting at 0.
        self.num_deaths = 0
        
        
    def create_menu(self):
        """Create the level menu, with a variable number of level buttons."""
        
        NUM_LEVELS = 3
        
        BUTTONS_PER_ROW = 10
        
        MIN_BUTTON_WIDTH = 7
        
        QUIT_BUTTON_WIDTH = MIN_BUTTON_WIDTH * 5
        
        # Approximate pixel width of a 7-character-long GuiZero button.
        MIN_BUTTON_WIDTH_PIXELS = 85
        
        # Approximate pixel height of a 1-character-tall GuiZero button.
        BUTTON_HEIGHT_PIXELS = 45
        
        # Determine the number of rows of buttons. Ceiling division idea sourced
        # from DelftStack:
        # https://www.delftstack.com/howto/python/python-round-up/
        NUM_ROWS = -(-NUM_LEVELS//BUTTONS_PER_ROW)
       
        # Determine menu width from approximate pixel width of a 7-character
        # button.
        MENU_WIDTH = MIN_BUTTON_WIDTH_PIXELS * BUTTONS_PER_ROW
        
        # Make menu height a minimum of 3 button heights or higher based on the
        # number of button rows.
        MENU_HEIGHT = BUTTON_HEIGHT_PIXELS * (NUM_ROWS + 2)
        
        # Resize the box responsible for the level select screen so its
        # size can be reliably referenced to reset the app window size.
        self.menu_box.resize(MENU_WIDTH, MENU_HEIGHT)
        
        # Add the number of level buttons specified by NUM_LEVELS.
        for current_num in range(1, NUM_LEVELS + 1):
            
            PushButton(self.level_select_box,
                       
                       # Button width becomes progressively smaller as levels
                       # are added from 1-9, until it reaches a minimum of 7
                       # characters.
                       width=max(MIN_BUTTON_WIDTH, -(-MIN_BUTTON_WIDTH *
                                                     BUTTONS_PER_ROW//
                                                     NUM_LEVELS)
                                 ),
                       height=1,
                       # Add button to the appropriate column based on level
                       # number and specified buttons per row.
                       grid=[((current_num - 1) % BUTTONS_PER_ROW),
                       # Add button to the appropriate row based on level number
                       # and specified buttons per row.
                             (current_num - 1)//BUTTONS_PER_ROW],
                       # Label button with appropriate level number.
                       text='Level ' + str(current_num),
                       # Set the button to open the corresponding level.
                       command=self.open_level, args=[current_num])
        
        # A button to quit the game.
        PushButton(self.quit_button_box, text='Quit Game',
                   width=QUIT_BUTTON_WIDTH, height=2, grid=[0, 0], command=exit)
    
    
    def open_menu(self):
        """Opens the level selection main menu."""
        
        self.update_window_size(self.menu_box)
        self.app.title = 'Out of Sync'
        self.menu_box.show()
        
        
    def open_level(self, level_id):
        """Close the level menu and open the level of the received level ID,
           which is signified by an integer. Expects to find one file with name
           format 'level#.txt'(main level layout file) and another file with
           name format 'level#a.txt' (alt level layout file)."""
        
        # Hide the main menu.
        self.menu_box.hide()
        
        # Set GameWindow attribute main_layout to a Layout object and pass it
        # the main level layout file name of the requested level for reference.
        self.main_layout = Layout(file_name='level' + str(level_id) + '.txt',
                                  # Create a drawing which will contain the main
                                  # layout's graphics and pass it to this main
                                  # Layout object to use.
                                  drawing=Drawing(self.level_box, grid=[0, 1],
                                          visible = False),
                                  # Set the main layout's avatar color to be a
                                  # lighter gray to distinguish it from the alt
                                  # avatar.
                                  avatar_color = 'gray'
                                  )
        
        # Set GameWindow attribute alt_layout to a Layout object and pass it
        # the alt level layout file name of the requested level for reference.
        self.alt_layout = Layout(file_name='level' + str(level_id) + 'a.txt',
                                 # Create a drawing which will contain the alt
                                 # layout's graphics and pass it to this alt
                                 # Layout object to use.
                                 drawing=Drawing(self.level_box, grid=[0, 1],
                                         visible = False),
                                 # Set the alt layout's avatar color to be a
                                 # darker gray to distinguish it from the main
                                 # avatar.
                                 avatar_color = 'dark gray'
                                 )
        
        # Draw both level layouts in their level_box.
        self.main_layout.draw()
        self.alt_layout.draw()
        
        # Tell the app to start executing run_level every 10 milliseconds and
        # pass it the requested level id.
        self.app.repeat(10, self.run_level, args=[level_id])
        
        # Set the commands to execute when a key is pressed.
        self.app.when_key_pressed = self.handle_key_press
        
        # Set the command to execute when a key is released.
        self.app.when_key_released = self.handle_key_release
        
        # Change app title to match the current level.
        self.app.title = 'Level ' + str(level_id)
        
        self.open_layout(self.main_layout)
        
        # Open the file storing the current level's record minimum attempt
        # count for reading.
        with open('min_attempts' + str(level_id) + '.txt') as min_attempts:
            # Display the minimum attempt count stored in the file.
            score = min_attempts.readline()
            self.fewest_attempts_score.value = self.attempts_str + score
            
        
        # Open level layout Box.
        self.level_box.show()
                            
    
    def open_layout(self, layout):
        """Opens the received layout in the game window."""
        
        # Resize the box responsible for displaying the level layouts so its
        # size can be reliably referenced to adjust the app window size.
        self.level_box.resize(layout.drawing.width, layout.drawing.height +
                              self.control_panel_box.height)
        self.update_window_size(self.level_box)
        
        # Show the drawing containing the requested layout.
        layout.drawing.show()
    
    
    def alternate_layout(self):
        """Switch the current level layout Drawing to the alternate level
           layout Drawing."""
         
        # If the main layout is currently open:
        if self.main_layout.drawing.visible:
            self.open_layout(self.alt_layout)
            self.main_layout.drawing.hide()

        # Otherwise, if the alternate layout is currently open:
        elif self.alt_layout.drawing.visible:
            self.open_layout(self.main_layout)
            self.alt_layout.drawing.hide()
            
            
    def run_level(self, level_id):
        """Updates the death count every frame, draws each respective frame
           of the level's layouts as long as the respective layout is not
           beaten, removes avatars from beaten layouts, saves new records to a
           file corresponding to the received level ID (int), and ends the game
           once both layouts are beaten."""
        
        if not self.main_layout.beaten:
            self.draw_frame(self.main_layout)
        else:
            self.main_layout.clear_avatar()
            
        if not self.alt_layout.beaten:
            self.draw_frame(self.alt_layout)
        else:
            self.alt_layout.clear_avatar()
        
        # Update the death count displayed in the level to show the current
        # number of deaths.
        self.death_score.value = self.deaths_str + str(self.num_deaths)
        
        if self.main_layout.beaten and self.alt_layout.beaten:
            self.end_level(level_id)
    
    
    def draw_frame(self, layout):
        """Updates the avatar's position and draws a frame with its updated
           position within the received Layout object."""
        
        layout.clear_avatar()
        
        # If the user is not pressing the 'A' key and is pressing the 'D' key:
        if (not ('a' in self.pressed_movement_keys or
                 'A' in self.pressed_movement_keys) and
            ('d' in self.pressed_movement_keys or
             'D' in self.pressed_movement_keys)):
                        
            # Set the level layout's avatar to move right at a preset speed.
            layout.avatar.x_vel = layout.avatar.GROUND_X_SPEED

        # Else if the user is not pressing the 'D' key and is pressing the 'A'
        # key:
        elif (not ('d' in self.pressed_movement_keys or
                    'D' in self.pressed_movement_keys) and
              ('a' in self.pressed_movement_keys or
               'A' in self.pressed_movement_keys)):
        
            # Set the level layout's avatar to move left at a preset speed.
            layout.avatar.x_vel = -layout.avatar.GROUND_X_SPEED
            
        else:
            layout.avatar.x_vel = 0
            
        if (('w' in self.pressed_movement_keys or
             'W' in self.pressed_movement_keys) and
            (not layout.avatar.in_air)):
                # Set the layout's avatar to move up at a preset speed.
                layout.avatar.y_vel = layout.avatar.JUMP_VEL
        
        # Apply gravity to the avatar, which modifies its y velocity.
        layout.avatar.apply_gravity()
        
        # Change the avatar's internal position based on its current velocities.
        layout.avatar.move(layout.drawing)
        
        # Iterate through all the Block objects in the Layout.
        for block in layout.blocks:
            layout.avatar.prevent_obstructed_motion(block)
        
        # Iterate through all the Spike objects in the Layout.
        for spikes in layout.spikes:
            if layout.avatar.is_impaled(spikes):
                self.num_deaths += 1
                self.restart_level()
                
        # Iterate through all the LevelEnding objects in the Layout.
        for exit_portal in layout.exits:
            if layout.avatar.reached_exit(exit_portal):
                layout.beaten = True
        
        # Draw the avatar with its updated position.
        layout.avatar_graphic = layout.avatar.draw(layout.drawing)

    def restart_level(self):
        """Reset the level to its beginning state."""
        
        self.main_layout.beaten = False
        self.alt_layout.beaten = False
        self.main_layout.avatar.respawn()
        self.alt_layout.avatar.respawn()


    def close_level(self):
        """Close the current level and return to the level selection menu."""
        
        # Tell the app to stop executing run_level. Idea to use "cancel" to stop
        # loop supplied by Anwesha Pradhananga on the CS 108 Piazza forum.
        # Link to post: https://piazza.com/class/ksp2tiztwas2ev?cid=236
        self.app.cancel(self.run_level)
        
        # Close the level layout.
        self.main_layout.drawing.destroy()
        self.alt_layout.drawing.destroy()
        self.level_box.hide()
        
        self.num_deaths = 0
        
        # Reset the "fewest attempts" score display.
        self.fewest_attempts_score.value = self.attempts_str
        
        # Stop the app from responding to key presses.
        self.app.when_key_pressed = None
        self.app.when_key_released = None
        
        # Clear leftover key inputs.
        self.pressed_movement_keys = []
                
        # (Re)open the level menu.
        self.open_menu()
        
        
    def end_level(self, level_id):
        """Briefly shows a success message, saves any new record scores to a
           file corresponding to the received level ID (int), and closes the
           level if the player successfully beats it. Expects to find a file
           with name format 'min_attempts#'"""
        
        # Show the success message.
        self.end_message_box.show()
        
        # Open the file storing the current level's record minimum attempt
        # count for reading and writing.
        with open('min_attempts' + str(level_id) + '.txt', 'r+') as min_attempts:
            
            score = min_attempts.readline()
            # If the file is empty or the player's death count is lower than the
            # established record:
            if score == '' or self.num_deaths < int(score):
                # Delete the current file contents.
                # (Idea to use seek() sourced from Joyce Chew and:
                # https://pynative.com/python-file-seek/)
                min_attempts.seek(0)
                # (Idea to use truncate() sourced from Joyce Chew and:
                # https://www.delftstack.com/howto/python/python-overwrite-file/)
                min_attempts.truncate()
                
                # Update the record minimum attempt count to the player's death
                # count plus 1.
                min_attempts.write(str(self.num_deaths + 1))
                
        self.close_level()
        
        # Schedule the success message to disappear after 400 milliseconds.
        self.app.after(400, self.end_message_box.hide)
   
    
    def update_window_size(self, widget):
        """Updates the window size to match the dimensions of the received
           GuiZero widget."""
        
        self.app.width = widget.width
        self.app.height = widget.height
        
                
    def handle_key_press(self, event):
        """Processes user key inputs from the received event data and responds
           accordingly."""
        
        # If the user has pressed the space bar:
        if event.key == ' ':
            self.alternate_layout()
        
        # Store non-spacebar key inputs in a list for reference.
        elif not event.key in self.pressed_movement_keys:
            self.pressed_movement_keys.append(event.key)
        
     
    def handle_key_release(self, event):
        """Processes the release of user key inputs from the received event data
           and responds accordingly."""
        
        if event.key != ' ':
            # Remove non-spacebar key inputs from the list of pressed keys
            # once the respective keys are released.
            self.pressed_movement_keys.remove(event.key)
            
        
app = App()
GameWindow(app)
app.display()