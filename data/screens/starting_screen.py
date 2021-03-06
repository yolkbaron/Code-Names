import pygame as pg
import random
from ..game_components import button
from ..game_components import text_box
from ..game_components import word_card
from .. import setup, tools
from .. import constants as c
from .. import game_sound


class StartingScreen(tools.GameState):

    def __init__(self):
        tools.GameState.__init__(self)
        self.name = c.STARTING_SCREEN
        self.fonts = setup.FONTS

    def start(self, current_time, game_info):
        self.start_time = current_time
        self.game_info = game_info
        self.next = self.get_next_screen()

        self.set_background()
        self.set_textboxes()
        self.set_buttons()

    def set_background(self):
        self.background = setup.SPRITES["background2"]
        font = pg.font.Font(setup.FONTS["Top Secret"], int(100 * self.multiplier))
        team_blue = font.render("Team blue", True, c.BLUE)
        team_red = font.render("Team red", True, c.RED)
        self.background = pg.transform.scale(self.background, c.SCREEN_SIZE)
        self.background.blit(team_blue, (int(260 * self.multiplier), int(270 * self.multiplier)))
        self.background.blit(team_red, (int(1100 * self.multiplier), int(100 * self.multiplier)))

    def set_buttons(self):
        start_button = button.Button(
            int(180 * self.multiplier),
            int(840 * self.multiplier),
            int(600 * self.multiplier),
            int(200 * self.multiplier),
            "START",
            int(150 * self.multiplier),
            "Top Secret"
        )
        start_button.set_inactive(c.GRAY)
        start_button.set_active(c.RED)
        self.buttons["start"] = start_button

    def set_textboxes(self):
        spy1 = text_box.InputBox(
            int(220 * self.multiplier),
            int(455 * self.multiplier),
            int(650 * self.multiplier),
            int(80 * self.multiplier),
            c.BLUE,
            int(80 * self.multiplier),
            "top secret text",
            max_length=12
        )
        spy2 = text_box.InputBox(
            int(1050 * self.multiplier),
            int(270 * self.multiplier),
            int(600 * self.multiplier),
            int(80 * self.multiplier),
            c.RED,
            int(80 * self.multiplier),
            "top secret text",
            max_length=12
        )
        team1_operative1 = text_box.InputBox(
            int(220 * self.multiplier),
            int(575 * self.multiplier),
            int(650 * self.multiplier),
            int(80 * self.multiplier),
            c.BLUE,
            int(80 * self.multiplier),
            "top secret text",
            max_length=12
        )
        team2_operative1 = text_box.InputBox(
            int(1050 * self.multiplier),
            int(390 * self.multiplier),
            int(600 * self.multiplier),
            int(80 * self.multiplier),
            c.RED,
            int(80 * self.multiplier),
            "top secret text",
            max_length=12
        )
        team1_operative2 = text_box.InputBox(
            int(220 * self.multiplier),
            int(695 * self.multiplier),
            int(650 * self.multiplier),
            int(80 * self.multiplier),
            c.BLUE,
            int(80 * self.multiplier),
            "top secret text",
            max_length=12
        )
        team2_operative2 = text_box.InputBox(
            int(1050 * self.multiplier),
            int(510 * self.multiplier),
            int(600 * self.multiplier),
            int(80 * self.multiplier),
            c.RED,
            int(80 * self.multiplier),
            "top secret text",
            max_length=12
        )
        self.text_boxes["team1_spy"] = spy1
        self.text_boxes["team2_spy"] = spy2
        self.text_boxes["team1_operative1"] = team1_operative1
        self.text_boxes["team2_operative1"] = team2_operative1
        self.text_boxes["team1_operative2"] = team1_operative2
        self.text_boxes["team2_operative2"] = team2_operative2

    def update(self, surface, keys, mouse, current_time):
        surface.blit(self.background, (0, 0))
        self.cursor_pos = pg.mouse.get_pos()
        self.update_text_boxes()
        self.update_buttons()

        self.update_spy()
        self.update_operative()

        self.draw_buttons(surface)
        self.draw_text_boxes(surface)

    def update_text_boxes(self):
        for key in self.text_boxes.keys():
            self.text_boxes[key].update()

    def update_buttons(self):
        for key in self.buttons.keys():
            if self.buttons[key].check_crossing(self.cursor_pos) and self.game_info[c.TEAM1].is_complete() and \
                    self.game_info[c.TEAM2].is_complete():
                self.buttons[key].active = True
            else:
                self.buttons[key].active = False
            if self.buttons[key].pressed:
                self.buttons[key].pressed = False
                if key == "start" and self.game_info[c.TEAM1].is_complete() and self.game_info[c.TEAM2].is_complete():
                    self.game_info[c.WORD_CARDS] = generate_word_cards()
                    self.done = True

    def draw_buttons(self, surface):
        for key in self.buttons.keys():
            self.buttons[key].draw(surface)

    def draw_text_boxes(self, surface):
        for key in self.text_boxes.keys():
            self.text_boxes[key].draw(surface)

    def update_spy(self):
        if len(self.text_boxes["team1_spy"].text) > 0:
            self.game_info[c.TEAM1].set_spy(self.text_boxes["team1_spy"].text)
        else:
            self.game_info[c.TEAM1].set_spy(None)

        if len(self.text_boxes["team2_spy"].text) > 0:
            self.game_info[c.TEAM2].set_spy(self.text_boxes["team2_spy"].text)
        else:
            self.game_info[c.TEAM2].set_spy(None)

    def update_operative(self):
        if len(self.text_boxes["team1_operative1"].text) > 0:
            self.game_info[c.TEAM1].set_operative(self.text_boxes["team1_operative1"].text, 0)
            self.game_info[c.TEAM1].set_operative(self.text_boxes["team1_operative2"].text, 1)
        elif len(self.text_boxes["team1_operative2"].text) > 0:
            self.game_info[c.TEAM1].set_operative(self.text_boxes["team1_operative2"].text, 0)
            self.game_info[c.TEAM1].set_operative(None, 1)
        else:
            self.game_info[c.TEAM1].set_operative(None, 0)
            self.game_info[c.TEAM1].set_operative(None, 1)

        if len(self.text_boxes["team2_operative1"].text) > 0:
            self.game_info[c.TEAM2].set_operative(self.text_boxes["team2_operative1"].text, 0)
            self.game_info[c.TEAM2].set_operative(self.text_boxes["team2_operative2"].text, 1)
        elif len(self.text_boxes["team2_operative2"].text) > 0:
            self.game_info[c.TEAM2].set_operative(self.text_boxes["team2_operative2"].text, 0)
            self.game_info[c.TEAM2].set_operative(None, 1)
        else:
            self.game_info[c.TEAM2].set_operative(None, 0)
            self.game_info[c.TEAM2].set_operative(None, 1)


def generate_word_cards():
    words = setup.WORDS["words_list"]
    random.shuffle(words)
    types = [c.BLUE_CARD] * 7 + [c.RED_CARD] * 6 + [c.BYSTANDER] * 6 + [c.ASSASSIN]
    random.shuffle(types)

    word_cards = []

    for i in range(4):
        for j in range(5):
            word = word_card.WordCard(
                int((190 + 310 * j) * c.MULTIPLIER),
                int((400 + 160 * i) * c.MULTIPLIER),
                int(300 * c.MULTIPLIER),
                int(150 * c.MULTIPLIER),
                types[5 * i + j],
                words[5 * i + j].upper(),
                int(40 * c.MULTIPLIER),
                "top secret text"

            )
            word_cards.append(word)
    return word_cards
