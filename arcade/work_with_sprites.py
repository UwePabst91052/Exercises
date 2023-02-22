"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

SPRITE_SCALING = 0.5
GRID_PIXEL_SIZE = 64
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Starting Template"
MAX_SPEED = 5.0
JUMP_SPEED = 14
ACCELERATION_RATE = 0.1
GRAVITY = 0.5
# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 7


def load_texture_pair(filename):
    return [arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
            ]


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state
        self.walk_right = False
        self.walk_left = False
        self.jumping = False
        self.falling = False
        self.climbing = False

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # path to player sprite
        player_path = "./resources/images/animated_characters/female_person/femalePerson"

        # Load idle texture
        self.idle_texture_pair = load_texture_pair(f"{player_path}_idle.png")

        # Load walking textures
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{player_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load jumping texture
        self.jump_texture = arcade.load_texture(f"{player_path}_jump.png")
        # Load falling texture
        self.fall_texture = arcade.load_texture(f"{player_path}_fall.png")

        # Load climbing texture
        self.climb_textures = []
        for i in range(2):
            texture = arcade.load_texture(f"{player_path}_climb{i}.png")
            self.climb_textures.append(texture)

        self.texture = self.idle_texture_pair[RIGHT_FACING]
        self.scale = 0.8

    def update(self):

        if self.change_y == 0:
            if self.change_x > 0:
                self.set_move_mode(right=True)
                self.character_face_direction = RIGHT_FACING
            elif self.change_x < 0:
                self.set_move_mode(left=True)
                self.character_face_direction = LEFT_FACING
            else:
                self.set_move_mode()
                self.character_face_direction = RIGHT_FACING

        # check to see if we hit the horizontal edge
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
            self.change_x = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.walk_right or self.walk_left:
            self.cur_texture += 1
            if self.cur_texture > 7 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
        elif self.jumping:
            self.texture = self.jump_texture
        elif self.falling:
            self.texture = self.fall_texture
        elif self.climbing:
            if self.change_y != 0:
                self.cur_texture += 1
                if self.cur_texture > UPDATES_PER_FRAME:
                    self.cur_texture = 0
            else:
                self.cur_texture = 0
            self.texture = self.climb_textures[self.cur_texture // UPDATES_PER_FRAME]
        else:
            self.texture = self.idle_texture_pair[self.character_face_direction]

    def set_move_mode(self, right=False, left=False,
                      jump=False, fall=False):
        self.walk_left = left
        self.walk_right = right
        self.jumping = jump
        self.falling = fall


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.box_list = None
        self.moving_wall_list = None
        self.player_sprite = None
        self.outer_box = None
        self.player_list = None
        self.ladder_ist = None
        self.all_tiles_list = None
        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.pause_game = False
        self.hit_list = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.box_list = arcade.SpriteList()
        self.ladder_ist = arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()
        self.all_tiles_list = arcade.SpriteList()

        # Create boxes
        for x in range(32 + 5 * GRID_PIXEL_SIZE, SCREEN_WIDTH, GRID_PIXEL_SIZE):
            box = arcade.Sprite("./resources/images/tiles/boxCrate_double.png", SPRITE_SCALING)
            box.center_x = x
            box.center_y = 5 * GRID_PIXEL_SIZE
            if box.center_x != 8 * GRID_PIXEL_SIZE - 32:
                self.box_list.append(box)
                self.all_tiles_list.append(box)
            else:
                self.outer_box = box

        # Create floor
        for x in range(32, SCREEN_WIDTH, GRID_PIXEL_SIZE):
            box = arcade.Sprite("./resources/images/tiles/boxCrate.png", SPRITE_SCALING)
            box.center_x = x
            box.center_y = GRID_PIXEL_SIZE // 2
            self.box_list.append(box)
            self.all_tiles_list.append(box)

        # Create ladder
        for y in range(96, 400, 50):
            if y < 382:
                ladder = arcade.Sprite("./resources/images/items/ladderMid.png", SPRITE_SCALING)
            else:
                ladder = arcade.Sprite("./resources/images/items/ladderTop.png", SPRITE_SCALING)
            ladder.center_x = 8 * GRID_PIXEL_SIZE - 32
            ladder.center_y = y
            self.ladder_ist.append(ladder)

        # set up vertical moving wall
        wall = arcade.Sprite("./resources/images/tiles/dirtHalf.png", SPRITE_SCALING)
        wall.center_x = 2 * GRID_PIXEL_SIZE
        wall.center_y = 5 * GRID_PIXEL_SIZE
        wall.boundary_top = 8 * GRID_PIXEL_SIZE
        wall.boundary_bottom = 2 * GRID_PIXEL_SIZE
        wall.change_y = 2 * SPRITE_SCALING
        self.moving_wall_list.append(wall)
        self.all_tiles_list.append(wall)

        # set up horizontal moving wall
        wall = arcade.Sprite("./resources/images/tiles/dirtHalf.png", SPRITE_SCALING)
        wall.center_x = 4 * GRID_PIXEL_SIZE
        wall.center_y = 8 * GRID_PIXEL_SIZE
        wall.boundary_top = 9 * GRID_PIXEL_SIZE
        wall.boundary_bottom = 7 * GRID_PIXEL_SIZE
        wall.boundary_left = 4 * GRID_PIXEL_SIZE
        wall.boundary_right = 11 * GRID_PIXEL_SIZE
        wall.change_y = -2 * SPRITE_SCALING
        wall.change_x = 2 * SPRITE_SCALING
        self.moving_wall_list.append(wall)
        self.all_tiles_list.append(wall)

        # set up the player
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = 200
        self.player_sprite.bottom = GRID_PIXEL_SIZE
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.all_tiles_list,
                                                             ladders=self.ladder_ist)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.outer_box.draw()
        self.box_list.draw()
        self.ladder_ist.draw()
        self.player_list.draw()
        self.moving_wall_list.draw()

        # Draw text
        if self.player_sprite.walk_left:
            move_mode = "Left"
        elif self.player_sprite.walk_right:
            move_mode = "Right"
        elif self.player_sprite.jumping:
            move_mode = "Jump"
        elif self.player_sprite.falling:
            move_mode = "Fall"
        elif self.player_sprite.climbing:
            move_mode = "Climb"
        else:
            move_mode = "Idle"
        arcade.draw_text("Movement mode: " + move_mode,
                         10, SCREEN_HEIGHT - 30,
                         arcade.color.BLACK, 14)
        arcade.draw_text(f"change_y: {self.player_sprite.change_y}",
                         10, SCREEN_HEIGHT - 40,
                         arcade.color.BLACK)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.pause_game:
            return

        # Detect climbing mode
        if self.physics_engine.is_on_ladder():
            if not self.player_sprite.climbing:
                self.player_sprite.climbing = True
                # self.right_pressed = self.left_pressed = False
        elif self.player_sprite.climbing:
            self.player_sprite.climbing = False

        # apply horizontal movement on the keys pressed
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MAX_SPEED
            self.player_sprite.set_move_mode(left=True)
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MAX_SPEED
            self.player_sprite.set_move_mode(right=True)
        else:
            self.player_sprite.change_x = 0
            if self.player_sprite.walk_right or \
                    self.player_sprite.walk_left:
                self.player_sprite.set_move_mode()

        # apply jump or climb movement on the up key pressed
        if self.up_pressed and not self.down_pressed:
            if self.player_sprite.climbing:
                self.player_sprite.change_y = MAX_SPEED
            elif self.physics_engine.can_jump():
                self.physics_engine.jump(JUMP_SPEED)
                self.player_sprite.set_move_mode(jump=True)
        elif self.down_pressed and not self.up_pressed:
            if self.player_sprite.climbing:
                self.player_sprite.change_y = -MAX_SPEED
        else:
            if self.player_sprite.climbing:
                self.player_sprite.change_y = 0
                self.player_sprite.set_move_mode()

        # detect falling mode
        if self.player_sprite.change_y < 0:
            if not self.player_sprite.climbing:
                if len(self.hit_list) == 1:
                    tile = self.hit_list[0]
                    if tile.change_x != 0 or tile.change_y != 0:
                        self.player_sprite.set_move_mode()
                else:
                    self.player_sprite.set_move_mode(fall=True)

        # Call update to move the sprite
        self.hit_list = self.physics_engine.update()
        if self.player_sprite.change_y == 0.0:
            if not self.player_sprite.walk_left and not \
                    self.player_sprite.walk_right:
                self.player_sprite.set_move_mode()
        self.player_sprite.update()
        self.player_sprite.update_animation()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.LEFT:
            self.left_pressed = True
            self.player_sprite.texture_index = 1
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.player_sprite.texture_index = 9
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.pause_game = not self.pause_game

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
