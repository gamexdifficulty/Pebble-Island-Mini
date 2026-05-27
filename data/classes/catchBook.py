from frostlight_engine import *
from typing import TYPE_CHECKING
from data.classes.font import Font

if TYPE_CHECKING:
    from main import Game

FISH_DATABASE = {
    "Sonnenschuppen Karpfen": {
        "name": "Sonnenschuppen Karpfen",
        "time": (500, 1900),
        "day": (0, 30),
        "wind": (0, 6),
        "rarity": "common",
        "biting_hold_time": 3.5,
    },

    "Kiesel Fisch": {
        "name": "Kiesel Fisch",
        "time": (0, 2400),
        "day": (0, 30),
        "wind": (0, 10),
        "rarity": "common",
        "biting_hold_time": 4.0,
    },

    "Dämmerrochen": {
        "name": "Dämmerrochen",
        "time": (1700, 2300),
        "day": (3, 30),
        "wind": (2, 8),
        "rarity": "rare",
        "biting_hold_time": 2.5,
    },

    "Mondflossen Aal": {
        "name": "Mondflossen Aal",
        "time": (2000, 400),
        "day": (5, 30),
        "wind": (0, 4),
        "rarity": "rare",
        "biting_hold_time": 1.8,
    },

    "Sturm Schnapper": {
        "name": "Sturm Schnapper",
        "time": (0, 2400),
        "day": (8, 30),
        "wind": (7, 10),
        "rarity": "very rare",
        "biting_hold_time": 1.2,
    },

    "Goldener Koi": {
        "name": "Goldener Koi",
        "time": (600, 900),
        "day": (10, 18),
        "wind": (0, 2),
        "rarity": "very rare",
        "biting_hold_time": 1.0,
    },

    "Leerenfisch": {
        "name": "Leerenfisch",
        "time": (2300, 200),
        "day": (13, 17),
        "wind": (8, 10),
        "rarity": "legendary",
        "biting_hold_time": 0.6,
    },

    "Glut Thunfisch": {
        "name": "Glut Thunfisch",
        "time": (1200, 1700),
        "day": (15, 30),
        "wind": (3, 7),
        "rarity": "rare",
        "biting_hold_time": 2.0,
    },

    "Frostkiefer": {
        "name": "Frostkiefer",
        "time": (300, 800),
        "day": (20, 30),
        "wind": (0, 3),
        "rarity": "very rare",
        "biting_hold_time": 0.9,
    },

    "Uralter Fisch": {
        "name": "Uralter Fisch",
        "time": (0, 2400),
        "day": (29, 30),
        "wind": (9, 10),
        "rarity": "legendary",
        "biting_hold_time": 0.4,
    },
    "Wolfsbarsch": {
        "name": "Wolfsbarsch",
        "time": (0, 2400),
        "day": (0, 30),
        "wind": (0, 10),
        "rarity": "common",
        "biting_hold_time": 4.2,
    },

    "Stachelmakrele": {
        "name": "Stachelmakrele",
        "time": (0, 2400),
        "day": (0, 30),
        "wind": (1, 8),
        "rarity": "common",
        "biting_hold_time": 3.8,
    },

    "Karausche": {
        "name": "Karausche",
        "time": (400, 1800),
        "day": (0, 20),
        "wind": (0, 5),
        "rarity": "common",
        "biting_hold_time": 3.6,
    },

    "Gelbbarsch": {
        "name": "Gelbbarsch",
        "time": (600, 1900),
        "day": (5, 30),
        "wind": (0, 6),
        "rarity": "common",
        "biting_hold_time": 3.1,
    },

    "Kliesche": {
        "name": "Kliesche",
        "time": (800, 2200),
        "day": (3, 30),
        "wind": (2, 7),
        "rarity": "rare",
        "biting_hold_time": 2.4,
    },

    "Kalmar": {
        "name": "Kalmar",
        "time": (1800, 400),
        "day": (10, 30),
        "wind": (1, 6),
        "rarity": "rare",
        "biting_hold_time": 1.9,
    },

    "Streifen-Kugelfisch": {
        "name": "Streifen-Kugelfisch",
        "time": (900, 1600),
        "day": (12, 30),
        "wind": (0, 4),
        "rarity": "rare",
        "biting_hold_time": 1.7,
    },

    "Riemenfisch": {
        "name": "Riemenfisch",
        "time": (0, 500),
        "day": (18, 30),
        "wind": (0, 3),
        "rarity": "very rare",
        "biting_hold_time": 0.8,
    },

    "Quastenflosser": {
        "name": "Quastenflosser",
        "time": (0, 2400),
        "day": (22, 30),
        "wind": (8, 10),
        "rarity": "very rare",
        "biting_hold_time": 0.7,
    },

    "Goldforelle": {
        "name": "Goldforelle",
        "time": (1600, 900),
        "day": (25, 30),
        "wind": (0, 2),
        "rarity": "legendary",
        "biting_hold_time": 0.5,
    },
}

RARITY_WEIGHTS = {
    "common": 60,
    "rare": 25,
    "very rare": 10,
    "legendary": 2
}

class CatchBook:
    def __init__(self, game:"Game"):
        self.game = game
        self.page = 0

        self.catchbook_sprite = Sprite("catchbook.png")
        self.catchbook_icon_sprite = Sprite("catchbook_icon.png")
        self.catchbook_slot_select_sprite = Sprite("catchbook_slot_select.png")
        self.fish_slot_sprite = Sprite("fish_slot.png")
        self.opened = False

        self.font = Font(self.game, 1)

        self.selected_index = 0
        self.selected_fish = None

        self.player_save = {}

        self.fish_keys = list(FISH_DATABASE.keys())
        self.fish_sprites = {
            "Sonnenschuppen Karpfen": Sprite("Sonnenschuppen Karpfen.png"),
        }
        
        self.slot_size = [25,25]
        self.slot_positions = [
            [85, 39],
            [114, 39],
            [85, 68],
            [114, 68]
        ]
        
        self.ui_button_size = [7,6]
        self.ui_positions = [
            [145, 85],
            [154, 85],
            [228, 85]
        ]

    def update(self):
        if self.game.player.x >= 171 and self.game.player.x <= 185:
            if self.game.input.get("accept") and self.game.player.alpha == 1.0 and self.game.player.animation_state == "idle":
                self.opened = True
                self.player_save = self.game.save_manager.load("catchbook","save0",{})

        if not self.opened:
            return
        
        mouse_pos = [(self.game.input.mouse.position[0]/self.game.window.window_size[0])*self.game.window.canvas_size[0], 
                     (self.game.input.mouse.position[1]/self.game.window.window_size[1])*self.game.window.canvas_size[1]]
        mouse_click = self.game.input.get("accept")

        if self.game.input.get("book_close"):
            self.close_book()

        if self.game.input.get("book_left"):
            self.prev_page()

        if self.game.input.get("book_right"):
            self.next_page()

        if self.game.input.get("ui_left"):
            self.selected_index -= 1

        if self.game.input.get("ui_right"):
            self.selected_index += 1

        if self.game.input.get("ui_down"):
            self.selected_index += 2

        if self.game.input.get("ui_up"):
            self.selected_index -= 2
            
        for i in range(4):
            if self.point_in_rect(mouse_pos, self.slot_positions[i], self.slot_size):
                if mouse_click:
                    self.selected_index = i

        if mouse_click:
            if self.point_in_rect(mouse_pos, self.ui_positions[0], self.ui_button_size):
                self.prev_page()

            # right page
            if self.point_in_rect(mouse_pos, self.ui_positions[1], self.ui_button_size):
                self.next_page()

            # close
            if self.point_in_rect(mouse_pos, self.ui_positions[2], self.ui_button_size):
                self.close_book()

        if self.selected_index > 3:
            self.selected_index -= 4
            self.next_page()
        
        elif self.selected_index < 0:
            self.selected_index += 4
            self.prev_page()
            
        self.selected_index = max(0, min(self.selected_index, 3))

        start = self.page * 4
        fish_index = start + self.selected_index
        self.selected_fish = None
        if fish_index < len(self.fish_keys):
            fish_key = self.fish_keys[fish_index]

            # only selectable if caught
            if fish_key in self.player_save:
                self.selected_fish = FISH_DATABASE[fish_key]

    def draw(self):
        if self.game.player.x >= 170 and self.game.player.x <= 185 and self.game.state == "game":
            if self.game.player.alpha == 1.0:
                self.game.window.render(self.catchbook_icon_sprite, [168,81])
        
        if not self.opened:
            return

        self.game.window.render(self.catchbook_sprite, [81, 35])
        start = self.page * 4

        # draw fish slots
        for i in range(4):
            fish_index = start + i
            if fish_index >= len(self.fish_keys):
                continue

            fish_key = self.fish_keys[fish_index]

            if i == self.selected_index:
                self.game.window.render(self.catchbook_slot_select_sprite,[self.slot_positions[i][0] - 1, self.slot_positions[i][1] - 1])

            # only show fish if caught
            if fish_key in self.player_save:
                if fish_key in self.fish_sprites:
                    fish_sprite = self.fish_sprites[fish_key]
                else:
                    fish_sprite = self.fish_slot_sprite
                self.game.window.render(fish_sprite, self.slot_positions[i])
                
        max_pages = math.ceil(len(FISH_DATABASE) / 4)
        self.font.draw(f"{self.page + 1}/{max_pages}",[165, 86])
        self.font.draw(f"Tag {self.game.gameManager.day}",[190, 86])


        # right side info
        if self.selected_fish:
            fish_key = self.fish_keys[start + self.selected_index]
            amount = self.player_save.get(fish_key, 0)
            self.font.draw(self.selected_fish["name"], [147, 44])
            self.font.draw(f'{int(self.selected_fish["time"][0]/100)}-{int(self.selected_fish["time"][1]/100)} Uhr, an Tag {self.selected_fish["day"][0]}-{self.selected_fish["day"][1]}',[147, 57])
            self.font.draw(f'{amount}', [147, 71])
            self.font.draw(f'{self.selected_fish["wind"][0]}-{self.selected_fish["wind"][1]}',[194, 71])

    def next_page(self):
        if self.page == math.ceil(len(FISH_DATABASE) / 4) - 1:
            self.selected_index = 4
        self.page = min(self.page + 1, math.ceil(len(FISH_DATABASE) / 4) - 1)

    def prev_page(self):
        if self.page == 0:
            self.selected_index = 0
        self.page = max(self.page - 1, 0)
        

    def close_book(self):
        self.opened = False
        
    def point_in_rect(self, point, rect_pos, rect_size):
        return (point[0] >= rect_pos[0] and point[0] <= rect_pos[0] + rect_size[0] and point[1] >= rect_pos[1] and point[1] <= rect_pos[1] + rect_size[1])