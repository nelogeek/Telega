# -*- coding: utf-8 -*-

from unittest import TestCase

from database.db_wrapper import DBwrapper
from game.blackJackGame import BlackJackGame
from game.card import Card


class TestBlackJack(TestCase):
    group_chat_id = -123456

    def test_add_player(self):
        chat_id = self.group_chat_id
        user_id, user_id_2, user_id_3 = 8912345, 111222, 1337
        first_name = "Peter"
        message_id = 12345

        # create multiplayer (group) game -> negative chat_id
        self.setup_blackJack_game(user_id=user_id, chat_id=chat_id, message_id=1111, first_name="John", lang_id="en")
        self.blackJackGame.add_player(user_id_2, first_name, message_id)

        # check if adding a user works in multiplayer
        self.assertTrue(len(self.blackJackGame.players) == 2)

        # check if adding an existing user a second time isn't possible
        self.blackJackGame.add_player(user_id_2, first_name, message_id)
        self.assertTrue(len(self.blackJackGame.players) == 2)

        # check if adding doesn't work if game is running
        self.blackJackGame.start_game()
        self.blackJackGame.add_player(user_id_3, first_name, message_id)
        self.assertTrue(len(self.blackJackGame.players) == 2)

    def test_get_user_by_user_id(self):
        chat_id = -122345
        user_id = 234091
        self.setup_blackJack_game(user_id=user_id, chat_id=chat_id, message_id=1111, first_name="John", lang_id="en")
        self.assertEqual(self.blackJackGame.get_player_by_id(user_id).user_id, user_id)
        self.assertEqual(self.blackJackGame.get_player_by_id(user_id).first_name, "John")

        user_id_2 = 892348
        first_name = "Peter"
        message_id = 12345
        self.blackJackGame.add_player(user_id_2, first_name, message_id)
        self.assertEqual(self.blackJackGame.get_player_by_id(user_id_2).user_id, user_id_2)
        self.assertEqual(self.blackJackGame.get_player_by_id(user_id_2).first_name, first_name)

    def test_next_player(self):
        chat_id = -122345
        user_id = 234091
        user_id_2 = 12398

        self.setup_multiplayer_game(user_id, chat_id, message_id=1111, first_name="John", lang_id="en", user_id_2=user_id_2, first_name_2="Carl", message_id_2=5566)
        # before game started, current_player should be 0
        self.assertEqual(self.blackJackGame.current_player, 0)

        # next_player shouldn't do anything when game is not started
        self.blackJackGame.next_player()
        self.assertEqual(self.blackJackGame.current_player, 0)

        # next_player shouldn't do anything when game is not started
        self.blackJackGame.game_running = True
        self.blackJackGame.next_player()
        self.assertEqual(self.blackJackGame.current_player, 1)

    def test_give_player_one(self):
        chat_id = -122345
        user_id = 234091
        self.setup_blackJack_game(user_id=user_id, chat_id=chat_id, message_id=1111, first_name="John", lang_id="en")
        self.blackJackGame.give_player_one()
        players = self.blackJackGame.players
        current_player = self.blackJackGame.current_player

        # At the beginning, the user shouldn't have any cards
        self.assertEqual(players[current_player].get_number_of_cards(), 0)

        # When the game isn't running, the players shouldn't get cards
        self.blackJackGame.give_player_one()
        self.assertEqual(players[current_player].get_number_of_cards(), 0)

        # When the game is running, the players should get cards
        self.blackJackGame.game_running = True
        self.assertFalse(players[current_player].get_number_of_cards(), 0)

    def test_dealers_turn(self):
        # hard to test
        pass

    def test_start_game(self):
        chat_id = -122345
        user_id = 234091
        user_id_2 = 12398
        self.setup_blackJack_game(user_id=user_id, chat_id=chat_id, message_id=1111, first_name="John", lang_id="en")
        # add user to database:
        database = DBwrapper.get_instance()
        database.add_user(user_id, "en", "John", "Doe", "username")
        database.add_user(user_id_2, "en", "Carl", "Doe", "username2")
        self.blackJackGame.start_game()

        # When user is alone in group, he shouldn't be able to play
        self.assertFalse(self.blackJackGame.game_running)
        self.assertEqual(len(self.blackJackGame.players[0].cards), 0)

        # Adding another player to the game
        self.blackJackGame.add_player(user_id_2, "Carl", 555666)

        self.blackJackGame.deck = self.CardDeckMockup("en")

        self.blackJackGame.start_game()
        self.assertTrue(self.blackJackGame.game_running)
        self.assertTrue(len(self.blackJackGame.players[0].cards) > 0)

    def test_evaluation(self):
        # hard to test
        pass

    def test_get_player_overview(self):
        chat_id = -122345
        user_id = 234091
        user_id_2 = 12398

        self.setup_multiplayer_game(user_id, chat_id, message_id=1111, first_name="John", lang_id="en", user_id_2=user_id_2, first_name_2="Carl", message_id_2=5566)

        # the length of the returned text should be equal to 0 as long as the game didn't start
        text = self.blackJackGame.get_player_overview()
        self.assertEqual(len(text), 0)

        self.blackJackGame.game_running = True
        text = self.blackJackGame.get_player_overview()
        self.assertNotEqual(len(text), 0)

        # Singleplayer:

        self.setup_blackJack_game(user_id, chat_id, message_id=1111, first_name="John", lang_id="en")
        text = self.blackJackGame.get_player_overview()
        self.assertEqual(len(text), 0)

        # self.blackJackGame.game_running = True
        # text = self.blackJackGame.get_player_overview()
        # self.assertEqual(len(text), 0)

    def test_analyze_message(self):
        # hard to test
        pass

    def setup_blackJack_game(self, user_id, chat_id, message_id, first_name, lang_id):
        self.blackJackGame = BlackJackGame(chat_id, user_id, lang_id, first_name, self.GameHandlerMockup, message_id, self.send_message_mockup)

    def setup_multiplayer_game(self, user_id, chat_id, message_id, first_name, lang_id, user_id_2, first_name_2, message_id_2=111):
        self.setup_blackJack_game(user_id, chat_id, message_id, first_name, lang_id)
        self.blackJackGame.add_player(user_id_2, first_name_2, message_id_2)

    def send_message_mockup(self, chat_id, text, message_id=None, parse_mode=None, reply_markup=None, game_id=None):
        print("send_message called | text: " + text + "\n---------------")
        pass

    class GameHandlerMockup:
        def gl_remove(self, chat_id):
            print("gl_remove called")

    class CardDeckMockup(object):
        def create_deck(self) -> list:
            deck = []

            for card_id in list([1, 10, 9, 13, 2, 5]):
                deck.append(Card(card_id, self.value_str))

            return deck[:]

        def pick_one_card(self) -> Card:
            return self.deck.pop(0)

        def __init__(self, lang_id: str) -> None:
            self.lang_id = lang_id

            self.value_str = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
            self.deck = self.create_deck()
