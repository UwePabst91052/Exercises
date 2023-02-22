"""
Platform Exercise

I will develop a platform game step by step.

Step 1: position a player on the floor
Step 2: enable the player to walk left and right
Step 3: enable player to jump
Step 4: animate the player. Therefore use a player class
Step 5: Add static platform
Step 6: Move platform
Step 7: Load static platform from map

"""
import arcade

SPRITE_SCALING = 0.5
PLAYER_SCALING = 0.7
GRID_PIXEL_SIZE = 64
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Platform Exercise"
MAX_SPEED = 5.0
JUMP_SPEED = 12
ACCELERATION_RATE = 0.1
GRAVITY = 0.5
# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 7

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 100
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

        # path to tiles sprites
        self.tile_path = "./resources/images/tiles/"
        self.map_path = "./resources/maps/"
        self.sound_path = ":resources:sounds/"

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.all_sprites_list = None
        self.player_list = None
        self.floor_list = None
        self.coin_list = None
        self.ladder_list = None
        self.background_list = None
        self.foreground_list = None
        self.moving1_list = None
        self.platform_list = None
        self.player_sprite = None
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(f"{self.sound_path}coin1.wav")
        self.jump_sound = arcade.load_sound(f"{self.sound_path}jump1.wav")

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.all_sprites_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()

        # Create player
        self.player_sprite = Player()
        self.player_sprite.left = 32 * GRID_PIXEL_SIZE
        self.player_sprite.bottom = GRID_PIXEL_SIZE
        self.player_list.append(self.player_sprite)

        # Create floor
        map_name = f"{self.map_path}map.tmx"
        platform_layer_name = 'Platforms'
        coin_layer_name = 'Coins'
        back_layer_name = 'Background'
        fore_layer_name = 'Foreground'
        moving1_layer_name = 'Moving_1'
        ladder_layer_name = "Ladders"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.floor_list = arcade.tilemap.process_layer(map_object=my_map,
                                                       layer_name=platform_layer_name,
                                                       scaling=SPRITE_SCALING,
                                                       use_spatial_hash=True)
        for item in self.floor_list:
            self.all_sprites_list.append(item)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=coin_layer_name,
                                                      scaling=SPRITE_SCALING,
                                                      use_spatial_hash=True)

        # -- background objects
        self.background_list = arcade.tilemap.process_layer(map_object=my_map,
                                                            layer_name=back_layer_name,
                                                            scaling=SPRITE_SCALING,
                                                            use_spatial_hash=True)

        # -- foreground objects
        self.foreground_list = arcade.tilemap.process_layer(map_object=my_map,
                                                            layer_name=fore_layer_name,
                                                            scaling=SPRITE_SCALING,
                                                            use_spatial_hash=True)

        # -- moving platforms
        self.moving1_list = arcade.tilemap.process_layer(map_object=my_map,
                                                         layer_name=moving1_layer_name,
                                                         scaling=SPRITE_SCALING,
                                                         use_spatial_hash=True)
        for tile in self.moving1_list:
            self.all_sprites_list.append(tile)

        # -- ladders
        self.ladder_list = arcade.tilemap.process_layer(map_object=my_map,
                                                        layer_name=ladder_layer_name,
                                                        scaling=SPRITE_SCALING,
                                                        use_spatial_hash=True)

        # set up platform engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.all_sprites_list,
                                                             gravity_constant=GRAVITY,
                                                             ladders=self.ladder_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.background_list.draw()
        self.ladder_list.draw()
        self.player_list.draw()
        self.foreground_list.draw()
        self.coin_list.draw()
        self.moving1_list.draw()
        self.all_sprites_list.draw()

        self.player_sprite.draw_hit_box()
        for sprite in self.moving1_list:
            sprite.draw_hit_box()

        # Draw text
        text_pos_x = self.view_left + 32
        text_pos_y = self.view_bottom + SCREEN_HEIGHT - 20
        text_1 = f"change_x: {self.player_sprite.change_x:3.2f}"
        text_2 = f"change_y: {self.player_sprite.change_y:3.2f}"
        text_3 = self.player_sprite.move_mode_to_text()
        arcade.draw_text(text_1, text_pos_x, text_pos_y, arcade.color.BLACK)
        arcade.draw_text(text_2, text_pos_x, text_pos_y - 20, arcade.color.BLACK)
        arcade.draw_text(text_3, text_pos_x, text_pos_y - 40, arcade.color.BLACK)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Update animations
        self.player_sprite.can_jump = self.physics_engine.can_jump()

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_key_change()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_key_change()

        self.player_sprite.update()
        self.player_sprite.update_animation()

        # Move the player with the physics engine
        self.physics_engine.update()

        # collect coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

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
