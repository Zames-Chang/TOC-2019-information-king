from transitions.extensions import GraphMachine
import threading
from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        self.id = ""
        self.Q1_count = 0
    def fun_timer(self):
        self.move()
    def start_game(self):
        if(self.state == 'init'):
            self.start()
            return True
        else:
            print("error when starting")
            return False
    def move_next(self):
        if(self.state != 'init' or self.state != 'final'):
            self.move()
            return True
        else:
            print("error when moving")
            return False
    def end_gmae(self):
        self.end()
        return True
    def for_demo(self):
        self.demo()
    def point(self):
        point_table = {
            'point0': 0,
            'point1': 1,
            'point2': 2,
            'point3': 3,
            'final': 4
        }
        return point_table[self.state]
