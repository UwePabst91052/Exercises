"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import arcade.gui
from arcade.gui import UIManager

SCREEN_WIDTH = 896
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Playground from Map"
SPRITE_SCALING = 0.5
GRID_PIXEL_SIZE = 64
MAX_SPEED = 5.0
JUMP_SPEED = 14
ACCELERATION_RATE = 0.1
GRAVITY = 0.5
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100


class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def __init__(self, text, center_x, center_y, width, my_game):
        super().__init__(
            text=text,
            center_x=center_x,
            center_y=center_y,
            width=width
        )
        self.game = my_game

    def on_click(self):
        """ Called when user lets off button """
        self.game.stop_start_moving()


class MyView(arcade.View):
    """
    Main view. Really the only view in this example. """
    def __init__(self, my_game):
        super().__init__()

        self.game = my_game
        self.ui_manager = UIManager()

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        arcade.start_render()

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        # arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        button = MyFlatButton(
            'Start/Stop moving',
            center_x=7 * GRID_PIXEL_SIZE,
            center_y=9 * GRID_PIXEL_SIZE,
            width=250,
            my_game=self.game
            # height=20
        )
        self.ui_manager.add_ui_element(button)


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
        self.player_list = None
        self.bottom_list = None
        self.move_list_1 = None
        self.move_list_2 = None
        self.all_sprite_list = None
        self.player_sprite = None
        self.player_path = "./resources/images/animated_characters/female_person"
        self.stop = False

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.physics_engine = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.bottom_list = arcade.SpriteList()
        self.move_list_1 = arcade.SpriteList()
        self.move_list_2 = arcade.SpriteList()
        self.all_sprite_list = arcade.SpriteList()

        play_map = arcade.tilemap.read_tmx("./resources/maps/playmap.tmx")

        # create player
        self.player_sprite = arcade.Sprite(f"{self.player_path}/femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 160
        self.player_sprite.center_y = 96
        self.player_list.append(self.player_sprite)

        # load bottom sprites
        self.bottom_list = arcade.tilemap.process_layer(map_object=play_map,
                                                        layer_name="Bottom",
                                                        scaling=SPRITE_SCALING,
                                                        use_spatial_hash=True)
        for tile in self.bottom_list:
            self.all_sprite_list.append(tile)

        # load move platform 1
        self.move_list_1 = arcade.tilemap.process_layer(map_object=play_map,
                                                        layer_name="Moving 1",
                                                        scaling=SPRITE_SCALING,
                                                        use_spatial_hash=True)

        for tile in self.move_list_1:
            tile.boundary_left = 0
            tile.boundary_right = 448
            tile.change_x = 1
            self.all_sprite_list.append(tile)

        # load move platform 2
        self.move_list_2 = arcade.tilemap.process_layer(map_object=play_map,
                                                        layer_name="Moving 2",
                                                        scaling=SPRITE_SCALING,
                                                        use_spatial_hash=True)

        for tile in self.move_list_2:
            self.all_sprite_list.append(tile)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.all_sprite_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        # arcade.start_render()

        # draw player
        self.player_list.draw()
        # draw platform tiles
        self.all_sprite_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.physics_engine.update()

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


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP:
            self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MAX_SPEED
        elif key == arcade.key.DOWN:
            pass
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MAX_SPEED

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

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

    def stop_start_moving(self):
        if self.stop:
            change_xy = 1
            self.stop = False
        else:
            change_xy = 0
            self.stop = True
        for tile in self.move_list_1:
            tile.change_x = change_xy
        for tile in self.move_list_2:
            tile.change_y = change_xy


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = MyView(game)
    game.show_view(view)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
