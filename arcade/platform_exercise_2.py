"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Platform Exercise 2"
SPRITE_SCALING = 0.5
PLAYER_SCALING = 0.7
GRID_PIXEL_SIZE = 64
MAX_SPEED = 5.0
JUMP_SPEED = 12
GRAVITY = 0.5
# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 7

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 64
TOP_VIEWPORT_MARGIN = 100


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
        self.jumping = False
        self.is_on_ladder = False
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
        self.jump_texture_pair = load_texture_pair(f"{player_path}_jump.png")
        # Load falling texture
        self.fall_texture_pair = load_texture_pair(f"{player_path}_fall.png")

        # Load climbing textures
        self.climb_textures = []
        for i in range(2):
            texture = arcade.load_texture(f"{player_path}_climb{i}.png")
            self.climb_textures.append(texture)

        self.texture = self.idle_texture_pair[RIGHT_FACING]
        self.scale = PLAYER_SCALING

    def update(self):

        # apply facing direction
        if self.change_x > 0 and not self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING
        elif self.change_x < 0 and not self.character_face_direction == LEFT_FACING:
            self.character_face_direction = LEFT_FACING

    def update_animation(self, delta_time: float = 1 / 60):
        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > UPDATES_PER_FRAME:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climb_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    def move_mode_to_text(self):
        if self.jumping:
            move_mode = "Jump"
        elif self.climbing:
            move_mode = "Climb"
        else:
            move_mode = "Idle"
        return move_mode


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

        # tile paths
        grass_mid = ":resources:images/tiles/grassMid.png"
        grass_center = ":resources:images/tiles/grassCenter.png"
        grass_corner_left = ":resources:images/tiles/grassCorner_left.png"
        grass_corner_right = ":resources:images/tiles/grassCorner_right.png"
        grass_hill_left = ":resources:images/tiles/grassHill_left.png"
        grass_hill_right = ":resources:images/tiles/grassHill_right.png"
        # grass_ = ":resources:images/tiles/"

        # init floor tile list
        # 0  1  2   3   4   5   6   7   8   9   10  11  12  13  14  15  16   17   18   19
        # 32 96 160 224 288 352 416 480 544 608 672 736 800 864 928 992 1056 1120 1184 1248
        self.floor_line_3 = [(224, 160, grass_hill_right),
                             (288, 160, grass_mid),
                             (352, 160, grass_mid),
                             (928, 160, grass_mid),
                             (992, 160, grass_mid),
                             (1056, 160, grass_hill_left)]
        self.floor_line_2 = [(160, 96, grass_hill_right),
                             (224, 96, grass_corner_right),
                             (288, 96, grass_center),
                             (352, 96, grass_center),
                             (928, 96, grass_center),
                             (992, 96, grass_center),
                             (1056, 96, grass_corner_left),
                             (1120, 96, grass_hill_left)]
        self.floor_line_1 = [(32, 32, grass_mid),
                             (96, 32, grass_mid),
                             (160, 32, grass_corner_right),
                             (224, 32, grass_center),
                             (288, 32, grass_center),
                             (352, 32, grass_center),
                             (416, 32, grass_mid),
                             (480, 32, grass_mid),
                             (544, 32, grass_mid),
                             (608, 32, grass_mid),
                             (672, 32, grass_mid),
                             (736, 32, grass_mid),
                             (800, 32, grass_mid),
                             (864, 32, grass_mid),
                             (928, 32, grass_center),
                             (992, 32, grass_center),
                             (1056, 32, grass_center),
                             (1120, 32, grass_corner_left),
                             (1184, 32, grass_mid),
                             (1248, 32, grass_mid)]

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.player_sprite = None
        self.jump_sound = arcade.load_sound("./resources/Sounds/jump1.wav")
        self.box_list = None
        self.moving_wall_list = None
        self.all_tiles_list = None
        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # horizontal speed before and after physics engine
        self.speed_before = 0
        self.speed_after = 0

    def setup_floor(self, floor_line):
        for line in floor_line:
            tile = arcade.Sprite(line[2], SPRITE_SCALING)
            tile.center_x = line[0]
            tile.center_y = line[1]
            self.box_list.append(tile)
            self.all_tiles_list.append(tile)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.box_list = arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()
        self.all_tiles_list = arcade.SpriteList()

        # Create floor
        self.setup_floor(self.floor_line_1)
        self.setup_floor(self.floor_line_2)
        # self.setup_floor(self.floor_line_3)

        # set up player
        self.player_sprite = Player()
        self.player_sprite.center_x = 4 * GRID_PIXEL_SIZE
        self.player_sprite.center_y = 3 * GRID_PIXEL_SIZE

        # set platforms
        wall = arcade.Sprite("./resources/images/tiles/bridgeB.png", SPRITE_SCALING)
        wall.center_x = 6 * GRID_PIXEL_SIZE + 32
        wall.center_y = 1 * GRID_PIXEL_SIZE + 32
        wall.boundary_left = 6 * GRID_PIXEL_SIZE
        wall.boundary_right = 14 * GRID_PIXEL_SIZE
        wall.change_x = 2
        self.moving_wall_list.append(wall)
        self.all_tiles_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.all_tiles_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # draw background circles
        # for x in range(-650, 1250, 100):
        #    for y in range(114, 1014, 100):
        #        arcade.draw_circle_outline(x, y, 50, arcade.color.AZURE, 5)

        # Call draw() on all your sprite lists below
        self.player_sprite.draw()
        self.all_tiles_list.draw()

        # Draw text
        text_pos_x = self.view_left + 32
        text_pos_y = self.view_bottom + SCREEN_HEIGHT - 20
        text_1 = f"speed_before: {self.speed_before:3.2f}"
        text_2 = f"speed_after: {self.speed_after:3.2f}"
        arcade.draw_text(text_1, text_pos_x, text_pos_y, arcade.color.BLACK)
        arcade.draw_text(text_2, text_pos_x, text_pos_y - 20, arcade.color.BLACK)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.speed_before = self.player_sprite.change_x
        self.physics_engine.update()
        self.speed_after = self.player_sprite.change_x

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def process_key_change(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = MAX_SPEED
            elif self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -MAX_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MAX_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MAX_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True

        self.process_key_change()

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
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

        self.process_key_change()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

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
