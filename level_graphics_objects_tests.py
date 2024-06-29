"""CS 108 A Final Project

Tests for the "Out of Sync" parallel-dimensional 2D platforming puzzle which
ensure that all LevelGraphicsObjects interact properly.

@author: Jason Chew (jgc23)
@author: Serita Nelesen (smn4)
@author: Keith Vander Linden (kvlinden)
@date: Fall, 2021
"""

from level_graphics_objects import Avatar, Block, Spikes, LevelEnding

# The Avatar and Block should not overlap on a side edge, so the Avatar's
# position should not change.
avatar = Avatar(x_pos=25, y_pos=25, size=50)
initial_x = avatar.x
avatar.x_vel = 1
initial_x_vel = avatar.x_vel
block = Block(x_pos=75, y_pos=25, size=50)
assert not avatar.colliding_with_block(block)
avatar.prevent_obstructed_motion(block)
assert avatar.x == initial_x
assert avatar.x_vel == initial_x_vel

# The Avatar and Block should not overlap on a top/bottom edge, so the Avatar's
# position should not change.
avatar = Avatar(x_pos=25, y_pos=25, size=50)
initial_y = avatar.y
avatar.y_vel = 1
initial_y_vel = avatar.y_vel
block = Block(x_pos=25, y_pos=75, size=50)
assert not avatar.colliding_with_block(block)
avatar.prevent_obstructed_motion(block)
assert avatar.y == initial_y
assert avatar.y_vel == initial_y_vel


# The Avatar and Block should overlap on a side edge, so the Avatar's position
# should be corrected.
avatar = Avatar(x_pos=25.01, y_pos=25, size=50)
avatar.x_vel = 1
block = Block(x_pos=75, y_pos=25, size=50)
assert avatar.colliding_with_block(block)
avatar.prevent_obstructed_motion(block)
assert avatar.x == 25
assert avatar.x_vel == 0

# The Avatar and Block should overlap on a top/bottom edge, so the Avatar's
# position should be corrected. The Avatar should be considered "not falling"
# after the correction, since it was "falling" on the top side of the block.
avatar.in_air = True
avatar = Avatar(x_pos=25, y_pos=25.01, size=50)
avatar.y_vel = 1
block = Block(x_pos=25, y_pos=75, size=50)
assert avatar.colliding_with_block(block)
avatar.prevent_obstructed_motion(block)
assert avatar.y == 25
assert avatar.y_vel == 0
assert avatar.in_air == False

# The Avatar should not be impaled on the Spike.
avatar = Avatar(x_pos=25.01, y_pos=50.00, size=50)
spike = Spikes(x_pos=75, y_pos=75, size=50)
assert not avatar.is_impaled(spike)

# The Avatar should be impaled on the Spike.
avatar = Avatar(x_pos=25.01, y_pos=50.01, size=50)
spike = Spikes(x_pos=75, y_pos=75, size=50)
assert avatar.is_impaled(spike)

# The Avatar should not have reached the LevelEnding.
avatar = Avatar(x_pos=62.49, y_pos=62.49, size=50)
end_portal = LevelEnding(x_pos=75, y_pos=75, size=50)
assert not avatar.reached_exit(end_portal)

# The Avatar should have reached the LevelEnding.
avatar = Avatar(x_pos=62.5, y_pos=62.5, size=50)
end_portal = LevelEnding(x_pos=75, y_pos=75, size=50)
assert avatar.reached_exit(end_portal)