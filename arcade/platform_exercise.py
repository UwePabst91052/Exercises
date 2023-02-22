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
SCREEN_TITLE = "My Exercise Game"
SPRITE_SCALING = 0.5
GRID_PIXEL_SIZE = 64


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

        self.center_x = 400
        self.center_y = 64
        self.delta_x = 0
        self.delta_y = 0
        self.angle = 0
        self.radius = 70
        self.delta_radius = 1
        self.player_sprite = None
        self.jump_sound = arcade.load_sound("./resources/Sounds/jump1.wav")
        self.box_list = None
        self.player_list = None
        self.moving_wall_list = None
        self.all_tiles_list = None
        self.physics_engine = None

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.box_list = arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()

        self.all_tiles_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Create floor
        for x in range(32, SCREEN_WIDTH, GRID_PIXEL_SIZE):
            box = arcade.Sprite("./resources/images/tiles/boxCrate.png", SPRITE_SCALING)
            box.center_x = x
            box.center_y = GRID_PIXEL_SIZE // 2
            self.box_list.append(box)
            self.all_tiles_list.append(box)

        self.player_sprite = arcade.Sprite("./resources/images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = self.center_x
        self.player_sprite.bottom = self.center_y
        self.player_list.append(self.player_sprite)

        # set up horizontal moving wall
        wall = arcade.Sprite("./resources/images/tiles/dirtHalf.png", SPRITE_SCALING)
        wall.center_x = 4 * GRID_PIXEL_SIZE
        wall.center_y = 4 * GRID_PIXEL_SIZE
        wall.boundary_top = 5 * GRID_PIXEL_SIZE
        wall.boundary_bottom = 3 * GRID_PIXEL_SIZE
        wall.boundary_left = 4 * GRID_PIXEL_SIZE
        wall.boundary_right = 11 * GRID_PIXEL_SIZE
        wall.change_y = -2 * SPRITE_SCALING
        wall.change_x = 2 * SPRITE_SCALING
        self.moving_wall_list.append(wall)
        self.all_tiles_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.all_tiles_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.player_sprite.center_x = self.center_x
        self.player_sprite.center_y = self.center_y
        self.player_sprite.draw()
        self.all_tiles_list.draw()

        if self.center_x < 64 or self.center_x > SCREEN_WIDTH - 64:
            self.delta_x = 0
        if self.center_y < 64 or self.center_y > SCREEN_HEIGHT - 64:
            self.delta_y = 0
            self.center_y = 64
        if self.radius < 30 or self.radius > 70:
            self.delta_radius *= -1
        self.radius += self.delta_radius

        arcade.draw_text("center_y: {0:03.2f} delta_y: {1: 03}".format(self.center_y, self.delta_y),
                         10, 30, arcade.color.WHITE)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        hit_list = self.physics_engine.update()
        if len(hit_list) > 0:
            if self.player_sprite.change_y != 0:
                self.player_sprite.change_y = 0
                self.player_sprite.change_x = 0
                self.delta_y = 0
                self.delta_x = 0
        self.center_x += self.delta_x * delta_time
        self.center_y += self.delta_y * delta_time
        if self.center_y > 35.0:
            self.delta_y -= 2

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP:
            self.delta_y = 200
            arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT:
            self.delta_x = -100
        elif key == arcade.key.RIGHT:
            self.delta_x = 100

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP:
            pass
        elif key == arcade.key.LEFT:
            self.delta_x = 0
        elif key == arcade.key.RIGHT:
            self.delta_x = 0

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
