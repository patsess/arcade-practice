
import arcade
import random


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Top down"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class TopDownWindow(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None
        self.computer_sprite = None
        self.item_list = None
        self.coin_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        self.player_money = 0
        self.computer_money = 0

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.current_state = 'top_down_view_running'
        self.computer_state = 'login'
        self.computer = arcade.load_texture(
            "images/backgrounds/computer_screen.png")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self._create_wall_list()
        self._create_player_list()
        self._setup_player()
        self._create_item_list()
        self._setup_computer()
        self._create_coin_list()

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        self.player_money = 0
        self.computer_money = 0

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        if self.current_state == 'top_down_view_running':
            self._draw_running_top_down_view()
        elif self.current_state == 'computer_running':
            self._draw_running_computer()
        else:
            raise ValueError(f"unrecognised current_state "
                             f"{self.current_state}")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.current_state == 'top_down_view_running':
            self._on_key_press_running_top_down_view(key, modifiers)
        elif self.current_state == 'computer_running':
            self._on_key_press_running_computer(key, modifiers)
        else:
            raise ValueError(f"unrecognised current_state "
                             f"{self.current_state}")

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """
        if self.current_state == 'top_down_view_running':
            self._update_top_down_view_running(delta_time)

    def _create_player_list(self):
        self.player_list = arcade.SpriteList()

    def _setup_player(self):
        self.player_sprite = arcade.AnimatedWalkingSprite()

        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(
            arcade.load_texture("images/player_1/female_stand.png",
                                scale=CHARACTER_SCALING))
        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(
            arcade.load_texture("images/player_1/female_stand.png",
                                scale=CHARACTER_SCALING, mirrored=True))

        self.player_sprite.walk_right_textures = []

        self.player_sprite.walk_right_textures.append(
            arcade.load_texture("images/player_1/female_stand.png",
                                scale=CHARACTER_SCALING))
        self.player_sprite.walk_right_textures.append(
            arcade.load_texture("images/player_1/female_walk1.png",
                                scale=CHARACTER_SCALING))
        self.player_sprite.walk_right_textures.append(
            arcade.load_texture("images/player_1/female_walk2.png",
                                scale=CHARACTER_SCALING))
        self.player_sprite.walk_right_textures.append(
            arcade.load_texture("images/player_1/female_walk1.png",
                                scale=CHARACTER_SCALING))

        self.player_sprite.walk_left_textures = []

        self.player_sprite.walk_left_textures.append(
            arcade.load_texture("images/player_1/female_stand.png",
                                scale=CHARACTER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(
            arcade.load_texture("images/player_1/female_walk1.png",
                                scale=CHARACTER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(
            arcade.load_texture("images/player_1/female_walk2.png",
                                scale=CHARACTER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(
            arcade.load_texture("images/player_1/female_walk1.png",
                                scale=CHARACTER_SCALING, mirrored=True))

        # self.player.texture_change_distance = 20
        self.player_sprite.center_x = int(SCREEN_WIDTH / 2.)
        self.player_sprite.center_y = int(SCREEN_HEIGHT / 2.)
        self.player_list.append(self.player_sprite)

    def _create_wall_list(self):
        # place horizontally (using multiple sprites)
        self.wall_list = arcade.SpriteList()
        for x in range(0, 500):
            for y in [20, 500]:
                wall = arcade.Sprite("images/tiles/foliagePack_leaves_002.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        # place vertically (using multiple sprites)
        for y in range(20, 500):
            wall = arcade.Sprite("images/tiles/foliagePack_leaves_002.png", TILE_SCALING)
            wall.center_x = 0
            wall.center_y = y
            self.wall_list.append(wall)

    def _create_item_list(self):
        self.item_list = arcade.SpriteList()

    def _setup_computer(self):
        self.computer_sprite = arcade.Sprite(
            "images/items/genericItem_color_050.png", scale=0.75)
        self.computer_sprite.center_x = 100
        self.computer_sprite.center_y = 400
        self.item_list.append(self.computer_sprite)

    def _create_coin_list(self):
        self.coin_list = arcade.SpriteList()
        for i in range(50):
            # Create the coin instance
            coin = arcade.Sprite("images/items/bronze_1.png", COIN_SCALING)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            coin_placed_well = True
            for sprite_list in [self.player_list, self.wall_list,
                                self.item_list]:
                for s in sprite_list:
                    if arcade.check_for_collision(coin, s):
                        coin_placed_well = False
                        break

            if coin_placed_well:
                self.coin_list.append(coin)

    def _draw_running_top_down_view(self):
        self.wall_list.draw()
        self.player_list.draw()
        self.item_list.draw()
        self.coin_list.draw()

        self._draw_background_text()

    def _draw_running_computer(self):
        self._draw_background_text()

        page_texture = self.computer
        arcade.draw_texture_rectangle(self.view_left + (SCREEN_WIDTH / 2),
                                      self.view_bottom + (SCREEN_HEIGHT / 2),
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        if self.computer_state == 'login':
            text = ("Log into the website\nof your stocks and\nshares ISA "
                    "provider?\n(y/n)\n")
        elif self.computer_state == 'deposit_question':
            text = (f"Account balance: £{self.computer_money}\n\nDeposit "
                    f"money?\n(y/n)\n")
        elif self.computer_state == 'deposit_amount':
            text = ("How much would you\nlike to deposit?\n\n0 - back\n1 - "
                    "100\n2 - 200\n3 - 500\n4 - 1000\n")
        elif self.computer_state == 'fund_problem':
            text = "Not enough funds.\n\nReturn to deposit screen?\n(y/n)\n"
        else:
            raise ValueError(f"unrecognised computer_state "
                             f"{self.computer_state}")

        arcade.draw_text(text,
                         self.view_left + (SCREEN_WIDTH / 3),
                         self.view_bottom + (SCREEN_HEIGHT / 2),
                         arcade.color.BLACK, 20, bold=True)

    def _on_key_press_running_top_down_view(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def _on_key_press_running_computer(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.current_state = 'top_down_view_running'
            self.player_sprite.center_x = int(SCREEN_WIDTH / 2.)
            self.player_sprite.center_y = int(SCREEN_HEIGHT / 2.)

        if self.computer_state == 'login':
            if key == arcade.key.Y:
                self.computer_state = 'deposit_question'
            elif key == arcade.key.N:
                self.current_state = 'top_down_view_running'
                self.player_sprite.center_x = int(SCREEN_WIDTH / 2.)
                self.player_sprite.center_y = int(SCREEN_HEIGHT / 2.)

        elif self.computer_state == 'deposit_question':
            if key == arcade.key.Y:
                self.computer_state = 'deposit_amount'
            elif key == arcade.key.N:
                self.computer_state = 'login'

        elif self.computer_state == 'deposit_amount':
            if key in [arcade.key.NUM_0, arcade.key.KEY_0]:
                self.computer_state = 'deposit_question'
            elif key in [arcade.key.NUM_1, arcade.key.NUM_2, arcade.key.NUM_3,
                         arcade.key.NUM_4, arcade.key.KEY_1, arcade.key.KEY_2,
                         arcade.key.KEY_3, arcade.key.KEY_4]:
                if key in [arcade.key.NUM_1, arcade.key.KEY_1]:
                    money = 100
                elif key in [arcade.key.NUM_2, arcade.key.KEY_2]:
                    money = 200
                elif key in [arcade.key.NUM_3, arcade.key.KEY_3]:
                    money = 500
                elif key in [arcade.key.NUM_4, arcade.key.KEY_4]:
                    money = 1000
                else:
                    raise ValueError(f"unrecognised key {key}")

                if self.player_money < money:
                    self.computer_state = 'fund_problem'
                else:
                    self.player_money -= money
                    self.computer_money += money
                    self.computer_state = 'deposit_question'

        elif self.computer_state == 'fund_problem':
            if key == arcade.key.Y:
                self.computer_state = 'deposit_amount'
            elif key == arcade.key.N:
                self.computer_state = 'login'

        else:
            raise ValueError(f"unrecognised computer_state "
                             f"{self.computer_state}")

    def _draw_background_text(self):
        arcade.draw_text(f"Money: £{self.player_money}\n",
                         self.view_left + (LEFT_VIEWPORT_MARGIN / 2),
                         self.view_bottom + SCREEN_HEIGHT -
                         (TOP_VIEWPORT_MARGIN / 2),
                         arcade.color.BLACK, 20, bold=True)

    def _update_top_down_view_running(self, delta_time):
        # Call update on all sprites
        self.physics_engine.update()
        self.player_list.update_animation()
        self._handle_coin_collection()
        self._handle_computer_collision()

        # --- Manage Scrolling ---

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

    def _handle_coin_collection(self):
        for c in self.coin_list:
            if arcade.check_for_collision(self.player_sprite, c):
                c.kill()
                self.player_money += 10

    def _handle_computer_collision(self):
        if arcade.check_for_collision(self.player_sprite,
                                      self.computer_sprite):
            self.computer_state = 'login'
            self.current_state = 'computer_running'


def main():
    """ Main method """
    window = TopDownWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
