import time
import traceback
import json
import ingescape as igs
import Othello

#Lancement LINUX : python3 OthelloAgent.py --device wlp2s0 --port 5670 pour debug : (--verbose)
#Lancement WINDOWS : py OthelloAgent.py --device "Loopback Pseudo-Interface 1"  --port 5670 --verbose

class OthelloAgent:
    def __init__(self):
        self.agent_name = "OthelloAgent"
        self.device = "Loopback Pseudo-Interface 1" # Windows 
        # self.device = "wlp2s0" # Linux
        # self.device = "enp0s31f6" # Linux 
        self.port = 5670
        
        self.start_x = 100.0
        self.start_y = 100.0
        self.cell_size = 60.0
        self.board_size = 8
        
        self.elt_ids_by_token = {
            "PIECE_TOKEN": [],
            "ACTIVE_PLAYER_STATIC_TOKEN": [],
            "ACTIVE_PLAYER_TOKEN": [],
            "MOVE_INDICATOR_TOKEN": [],
            "SCORES_TOKEN": [],
        }
        self.player_txt_shape_id = None

        self.game = Othello.Othello(self.board_size, self.board_size)

    def init_igs(self):
        igs.service_call("Whiteboard", "clear", (), None)
        igs.agent_set_name(self.agent_name)
        igs.definition_set_version("1.0")
        
        igs.observe_agent_events(self.on_agent_event_callback, self)
        
        igs.input_create("click", igs.STRING_T, None)
        igs.observe_input("click", self.on_update_click, None)
        igs.mapping_add("click", "Whiteboard", "click")
        
        igs.service_init("resetGame", self.reset_game, None)

        # getters for game state
        igs.service_init("getPlateau", self.game.get_plateau, None)
        igs.service_init("getPossibleMoves", self.game.get_coups_possibles, None)
        igs.service_init("getScores", self.game.get_scores, None)
        igs.service_init("getTurn", self.game.get_tour, None)
        igs.service_init("isGameOver", self.game.is_partie_terminee, None)

        igs.service_init("elementCreated", self.on_element_created, None)
        igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)

        igs.start_with_device(self.device, self.port)
        print(f"{self.agent_name} started on {self.device}:{self.port}")

    def start(self):
        self.init_igs()
        self.draw_grid_static()

        while True:
            time.sleep(1)

    def stop(self):
        print("Stopping agent...")
        igs.stop()
        print("Agent stopped.")
        sys.exit(0)

    def draw_grid_static(self):
        """Draws the static background grid and UI text"""
        print("Clearing whiteboard...")
        igs.service_call("Whiteboard", "clear", (), None)

        print("Drawing Static Grid...")
        board_width = self.cell_size * self.board_size
        igs.service_call("Whiteboard", "addText", ("Blancs : ", self.start_x, self.start_y - 50.0, "black"), None)
        igs.service_call("Whiteboard", "addText", ("Noirs : ", self.start_x + 300, self.start_y - 50.0, "black"), None)

        igs.service_call("Whiteboard", "addText", ("Au tour des : ", self.start_x + 100, self.start_y - 100.0, "black"), "ACTIVE_PLAYER_STATIC_TOKEN")

        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.start_x + (col * self.cell_size)
                y = self.start_y + (row * self.cell_size)
                igs.service_call("Whiteboard", "addShape", ("rectangle", x, y, self.cell_size, self.cell_size, "green", "black", 2.0), None)

        # Draw initial pieces and scores
        self.draw_state()

    def draw_state(self, etat="jeu"):
        """Draws the current state of the game on the whiteboard"""
        print("Drawing game state...")
        # redraw scores
        self.removeElements("SCORES_TOKEN")
        blancs_score, noirs_score = self.game.get_scores()
        igs.service_call("Whiteboard", "addText", (str(blancs_score), self.start_x + 140, self.start_y - 50.0, "black"), "SCORES_TOKEN")
        igs.service_call("Whiteboard", "addText", (str(noirs_score), self.start_x + 420, self.start_y - 50.0, "black"), "SCORES_TOKEN")

        # draw end game or update active player
        if etat == "terminee":
            # delete active player text
            self.removeElements("ACTIVE_PLAYER_STATIC_TOKEN")
            self.removeElements("ACTIVE_PLAYER_TOKEN")

            # display end game text
            winner = "Blancs" if self.game.get_scores()[0] - self.game.get_scores()[1] > 0 else "Noirs"
            igs.service_call("Whiteboard", "addText", (f"Fin de la partie ! Les {winner} ont gagné.", self.start_x , self.start_y - 100.0, "black"), "END")
        else:
            # update active player text
            self.removeElements("ACTIVE_PLAYER_TOKEN")
            turn = self.game.get_tour().value
            igs.service_call("Whiteboard", "addText", (turn, self.start_x + 310, self.start_y - 100.0, "black"), "ACTIVE_PLAYER_TOKEN")

            # redraw pieces and possible moves
            self.redraw_pieces_from_state()

    def redraw_pieces_from_state(self):
        """Redraws all pieces"""
        print("Redrawing pieces from state...")
        
        # On doit supprimer tous les pions avant de les redessiner
        self.removeElements("PIECE_TOKEN")
        
        plateau = self.game.get_plateau()
        
        #Pieces
        for row in range(self.board_size):
            for col in range(self.board_size):
                val = plateau[row][col]
                if val == Othello.Turn.NOIRS:
                    self.add_piece(row, col, "black")
                elif val == Othello.Turn.BLANCS:
                    self.add_piece(row, col, "white")

        #Coups possibles
        #Faudrait que add_piece permette + de libertés sinon tant pis comme ça ça marche
        self.removeElements("MOVE_INDICATOR_TOKEN")
        coups_possibles = self.game.get_coups_possibles()
        for row, col in coups_possibles:
            self.add_possible_move_indicator(row, col)

    def removeElements(self, token):
        """Removes all elements with the given token from the whiteboard"""
        if token in self.elt_ids_by_token:
            for elt_id in self.elt_ids_by_token[token]:
                igs.service_call("Whiteboard", "remove", elt_id, None)
            self.elt_ids_by_token[token] = []

    def add_piece(self, row, col, color):
        padding = 5.0
        size = self.cell_size - (padding * 2)
        x = self.start_x + (col * self.cell_size) + padding
        y = self.start_y + (row * self.cell_size) + padding
       
        igs.service_call("Whiteboard", "addShape", 
            ("ellipse", x, y, size, size, color, "black", 1.0), 
            "PIECE_TOKEN") 
    
    def add_possible_move_indicator(self, row, col):
        padding = self.cell_size / 2 - 5  # petit cercle au centre de la case
        size = 10.0  # rayon du cercle rouge
        x = self.start_x + (col * self.cell_size) + padding
        y = self.start_y + (row * self.cell_size) + padding
        igs.service_call("Whiteboard", "addShape", ("ellipse", x, y, size, size, "red", "black", 1.0), "MOVE_INDICATOR_TOKEN")

    def reset_game(self, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
        """Service: Clears board and resets state"""
        print("Service 'resetGame' called.")
        self.game.reinitialiser_partie(self.board_size, self.board_size)
        self.draw_grid_static()

    def on_update_click(self, io_type, name, value_type, value, my_data):
        """
        Input: update_board (String)
        Parses a JSON string representing the click.
        Example JSON: "{"x":869.984375,"y":304.69921875}"
        """
        print(f"Input 'click' received",value)
        try:
            click = json.loads(value)
            
            if len(click) == 2 and "x" in click and "y" in click:
                x = click["x"]
                y = click["y"]
                
                col = int((x - self.start_x) // self.cell_size)
                row = int((y - self.start_y - (self.cell_size / 2)) // self.cell_size)
                
                if 0 <= row < self.board_size and 0 <= col < self.board_size:
                    print(f"Click at board position: Row {row}, Col {col}")
                    
                    coups_possibles = self.game.get_coups_possibles()
                    print(f"coups possibles : {coups_possibles}")
                    print(f"row : {row}, col : {col}")

                    if (row,col) in coups_possibles:
                        # Jouer le coup
                        pions_retournes = self.game.jouer_tour(row, col)
                        etat = self.game.fin_tour()
                        print(f"Etat après fin de tour : {etat}")

                        self.draw_state(etat)
                    else:
                        print("Cell already occupied.")
                else:
                    print("Click outside board area.")
            else:
                print("Error: Invalid board dimensions received.")
        except json.JSONDecodeError:
            print("Error: Could not parse board state JSON.")
        except Exception as e:
            print(f"Error updating board: {e}")


    def on_agent_event_callback(self, event, uuid, name, event_data, my_data):
        try:
            if name == "Whiteboard":
                if event == igs.AGENT_KNOWS_US:
                    print("Whiteboard connected. Initializing...")
                    self.reset_game(None, None, None, None, None, None)
                    igs.service_call("Whiteboard", "hideLabels", None, None)
                elif event == igs.AGENT_EXITED:
                    print("Whiteboard disconnected.")
                    for token in self.elt_ids_by_token:
                        self.elt_ids_by_token[token] = []
        except:
            print(traceback.format_exc())

    def on_element_created(self, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
        new_id = tuple_args[0]
        if token in self.elt_ids_by_token:
            self.elt_ids_by_token[token].append(new_id)


if __name__ == "__main__":
    try:
        print("Starting Othello Agent...")
        if hasattr(igs, 'set_command_line'):
            import sys
            igs.set_command_line(sys.executable + " " + " ".join(sys.argv))
        agent = OthelloAgent()
        agent.start()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Stopping agent...")
        agent.stop()