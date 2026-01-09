import time
import random
import threading
import traceback
import json
import ingescape as igs

#Lancement LINUX : python3 OthelloAgent.py --device wlp2s0 --port 5670 pour debug : (--verbose)
#Lancement WINDOWS : py OthelloAgent.py --device "Loopback Pseudo-Interface 1"  --port 5670 --verbose

class OthelloAgent:
    def __init__(self):
        self.agent_name = "OthelloAgentG"
        #self.device = "wlp2s0" #ordi Gauthier : Linux
        self.device = "Loopback Pseudo-Interface 1" #ordi Alex : windows 
        self.port = 5670
        
        self.piece_ids = []  

        self.start_x = 100.0
        self.start_y = 150.0
        self.cell_size = 60.0
        self.board_size = 8
        
        self.board_state = [[0]*8 for _ in range(8)]

    def start(self):
        
        igs.agent_set_name(self.agent_name)
        igs.definition_set_version("1.0")
        
        igs.observe_agent_events(self.on_agent_event_callback, self)
        
        igs.input_create("click", igs.STRING_T, None)
        igs.observe_input("click", self.on_update_click, None)
        igs.mapping_add("click","Whiteboard","click")
        
        igs.service_init("resetGame", self.service_reset_game, None)
        
        igs.service_init("elementCreated", self.on_element_created, None)
        igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)

        igs.start_with_device(self.device, self.port)
        print(f"{self.agent_name} started on {self.device}:{self.port}")
        
        time.sleep(2) 
        self.draw_grid_static() 

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def clean_ids(self):
        """Resets the piece ID list if we lose connection or reset game"""
        self.piece_ids = []

    def draw_grid_static(self):
        """Draws the static background grid and UI text (does not clear pieces if not asked)"""
        print("Drawing Static Grid...")
        
        igs.service_call("Whiteboard", "clear", (), None)
        self.clean_ids()
        time.sleep(0.5)

        igs.service_call("Whiteboard", "addText", ("Player 1 (Black)", self.start_x, self.start_y - 50.0, "black"), None)
        board_width = self.cell_size * self.board_size
        igs.service_call("Whiteboard", "addText", ("Player 2 (White)", self.start_x + board_width - 150.0, self.start_y - 50.0, "black"), None)

        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.start_x + (col * self.cell_size)
                y = self.start_y + (row * self.cell_size)
                igs.service_call("Whiteboard", "addShape", 
                    ("rectangle", x, y, self.cell_size, self.cell_size, "green", "black", 2.0), 
                    None)
        
        
        self.redraw_pieces_from_state()

    def redraw_pieces_from_state(self):
        """Redraws all pieces based on self.board_state"""
        print("Redrawing pieces from state...")
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                val = self.board_state[row][col]
                if val == 1:
                    self.add_piece(row, col, "black")
                elif val == 2:
                    self.add_piece(row, col, "white")

    def add_piece(self, row, col, color):
        padding = 5.0
        size = self.cell_size - (padding * 2)
        x = self.start_x + (col * self.cell_size) + padding
        y = self.start_y + (row * self.cell_size) + padding
        
        igs.service_call("Whiteboard", "addShape", 
            ("ellipse", x, y, size, size, color, "black", 1.0), 
            "PIECE_TOKEN") 

    def service_reset_game(self, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
        """Service: Clears board and resets state"""
        print("Service 'resetGame' called.")
        self.board_state = [[0]*8 for _ in range(8)]
        self.board_state[3][3] = 2 
        self.board_state[3][4] = 1 
        self.board_state[4][3] = 1 
        self.board_state[4][4] = 2 
        
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
                row = int((y - self.start_y) // self.cell_size)
                
                if 0 <= row < self.board_size and 0 <= col < self.board_size:
                    print(f"Click at board position: Row {row}, Col {col}")
                    
                    if self.board_state[row][col] == 0:
                        print("Placing and calculating board state...")
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
                    self.service_reset_game(None, None, None, None, None, None)
                    igs.service_call("Whiteboard", "hideLabels", None, None)
                elif event == igs.AGENT_EXITED:
                    print("Whiteboard disconnected.")
                    self.clean_ids()
        except:
            print(traceback.format_exc())

    def on_element_created(self, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
        new_id = tuple_args[0]
        if token == "PIECE_TOKEN":
            self.piece_ids.append(new_id)

if __name__ == "__main__":
    if hasattr(igs, 'set_command_line'):
        import sys
        igs.set_command_line(sys.executable + " " + " ".join(sys.argv))
    agent = OthelloAgent()
    agent.start()