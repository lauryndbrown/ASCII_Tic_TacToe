from ascii_game.game import Game, Choice
from tic_tac_toe.game_entities import TicTacToe
from tic_tac_toe.tic_tac_toe_display import TicTacToeDisplay
from tic_tac_toe.player import *
"""
TicTacToe Game Class
"""
class TicTacToeGame(Game):
    """
    TicTacToe Game Class
    Inherits from the Game class
    It builds the in-game menus and makes appropriate calls to related classes 
    in order to display information onto the screen and facilitate the TicTacToe game play.
    """
    #Game Modes
    STANDARD_MODE = "Standard"
    WILD_MODE = "Wild"
    #Menu Names
    START_MENU_NAME = "Start"
    GAME_MENU_NAME = "Game"
    GAME_OVER_MENU_NAME = "Game Over"
    SETTINGS_MENU_NAME = "Settings"
    #Option Names
    BACK_OPTION = "Back"
    #Win/Lose
    GAME_OVER = "game over"
    def __init__(self, display, player1, player2):
        """
        Initializes in game menus and Game object
        """
        super().__init__(display, player1, player2)
        self.turn = 0
        self.game_board = TicTacToe()
        start_menu = []
        game_menu = []
        game_over_menu = []
        settings_menu = []
        #Start Menu
        start_menu.append(Choice("Start Game",self.display.game_screen, (self,), self.GAME_MENU_NAME))
        start_menu.append(Choice("Settings",self.display.settings_screen, (self,), self.SETTINGS_MENU_NAME))
        start_menu.append(Choice("Exit TicTacToe",self.exit_game, None, None))
        #Game Menu
        game_menu.append(Choice("Make Next Move", self.move, (), None))
        game_menu.append(Choice("End Game",self.end_current_game, (), self.START_MENU_NAME))
        #Game Over Menu
        game_over_menu.append(Choice("End Game",self.end_current_game, (), self.START_MENU_NAME))
        game_over_menu.append(Choice("New Game", self.new_game, (),  self.GAME_MENU_NAME))
        #Settings Menu
        settings_menu.append(Choice(self.BACK_OPTION,self.display.start_menu, (self,), self.START_MENU_NAME))
        settings_menu.append(Choice("Change Play Mode",self.change_play_mode, (), None))
        settings_menu.append(Choice("Toggle Computer Thinking Animation",self.toggle_computer_thinking, (), None))
        self.menus = {self.START_MENU_NAME:start_menu, self.GAME_MENU_NAME:game_menu, 
                        self.SETTINGS_MENU_NAME:settings_menu, self.GAME_OVER_MENU_NAME:game_over_menu}
        #Current menu is pointed to by self.menu
        self.menu = start_menu
        #Because the game has just started the previous menu is None
        self.prev_menu = None
        self.current_player = self.player_1
        self.mode = self.STANDARD_MODE
    def start(self):
        """
        Display the start menu to the user
        Start the Game
        """
        self.display.start_menu(self)
        super().start()
    def move(self):
        """
        Makes a move in the game. The user goes first followed by the Computer Player.
        At each stage, the game is checked for a winner. And the GAME_OVER menu is
        chosen if the game has come to an end.
        """
        def computer_player():
            print("Computer Player", self.current_player.__class__, self.current_player==self.player_2)
            if self.current_player.is_computer():
                print("is computer")
                self.display.computer_move(self)
                if self.mode==self.STANDARD_MODE:
                    row, col = self.current_player.move(self.game_board, self.turn)    
                    value = self.current_player.value
                else:
                    row, col, value = self.current_player.move(self.game_board, self.turn)    
                self.game_board.move((row,col), value)
        def game_over():
            if self.game_board.has_won():
                self.menu = self.menus[self.GAME_OVER_MENU_NAME]
                self.display.game_screen(game, self.GAME_OVER)
                return True
            if not self.game_board.avalible_moves():
                self.current_player = None
                self.menu = self.menus[self.GAME_OVER_MENU_NAME]
                self.display.game_screen(game, self.GAME_OVER)
                return True
            return False
        self.turn+=1
        if self.mode==self.STANDARD_MODE:
            row, col = self.display.move(self.game_board.avalible_moves(), self)
            value = self.current_player.value
        else:
            row, col, value = self.display.move(self.game_board.avalible_moves(), self)
        self.game_board.move((row,col), value)
        if not game_over():
            self._switch_player()
            computer_player()
            if not game_over():
                self._switch_player()
                self.display.game_screen(game)
    def _switch_player(self):
        """
        Toggles the current_player variable between player_1 and player_2
        The current_player denotes the player who's turn is next.
        """
        print("Switch Player")
        if self.current_player==self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1
    def change_play_mode(self):
        """
        Toggles Game Mode
        """
        if self.mode==self.STANDARD_MODE:
            self.mode = self.WILD_MODE
            self.player_1 =  WildTicTacToePlayer(self.player_1.name)
            self.player_2 =  WildComputerPlayer(self.player_2.name)
        else:
            self.mode = self.STANDARD_MODE
            self.player_1 =  StandardTicTacToePlayer(self.player_1.name, TicTacToe.X)
            self.player_2 =  RandomComputerPlayer(self.player_2.name, TicTacToe.O)
        self.current_player = self.player_1
        self.display.settings_screen(self)
    def toggle_computer_thinking(self):
        self.display.toggle_computer_thinking()
        self.display.settings_screen(self)
    def new_game(self):
        """
        Creates a new game and resets the board and player.
        """
        self.reset_game()
        self.display.game_screen(self)
    def exit_game(self):
        """
        Exits TicTacToe
        """
        self.display.exit_screen()
    def reset_game(self):
        """
        Resets the game board and turns counter
        """
        self.current_player = self.player_1
        self.turn = 0
        self.game_board.empty_board()

    def end_current_game(self):
        """
        Ends the current game and returns to start menu.
        """
        self.reset_game()
        self.display.start_menu(self)
if __name__=="__main__":
    display = TicTacToeDisplay()
    player1 = StandardTicTacToePlayer("Player1",TicTacToe.X)
    player2 = RandomComputerPlayer("Player2", TicTacToe.O)
    game = TicTacToeGame(display, player1, player2)
    game.start()

