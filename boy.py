from time import sleep
from turtledemo.penrose import start

from pico2d import load_image, get_time
from state_machine import StateMachine, space_down, time_out, right_down, left_up, left_down, right_up, start_event, \
    a_down


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 1
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle : { time_out: Sleep, right_down: Run, left_down: Run,left_up: Run,right_up: Run, a_down: Auto_run},
                Sleep : { space_down: Idle, right_down: Run, left_down: Run,left_up: Run,right_up: Run},
                Run : { right_down: Idle, left_down: Idle,left_up: Idle,right_up: Idle },
                Auto_run : { time_out: Idle, right_down: Run, left_down: Run,left_up: Run,right_up: Run }
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()


# 상태를 클래스를 통해 정의한다.
class Idle:
    @staticmethod
    def enter(boy,e):
        if start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif right_down(e) or left_up(e):
            boy.action = 2
            boy.face_dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.face_dir = 1
        elif time_out(e):
            if boy.face_dir == 1:
                boy.action = 3
            else:
                boy.action = 2

        boy.dir = 0
        boy.frame = 0
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT',0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy,e):
        if start_event(e):
            boy.action = 3
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,3.141562/2, '', boy.x - 25, boy.y - 25,100,100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, -(3.141562 / 2), '', boy.x + 25,
                                          boy.y - 25, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1, 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x += (boy.dir * 5)
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,0,'', boy.x, boy.y,100,100)
        pass

class Auto_run:
    @staticmethod
    def enter(boy, e):
        boy.start_time = get_time()
        boy.dir = boy.face_dir
        pass

    @staticmethod
    def exit(boy, e):
        boy.face_dir = boy.dir
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT',0))
            
        boy.x += (boy.dir * 10)
        boy.frame = (boy.frame + 1) % 8
        if boy.x >= 800:
            boy.dir = -1
        elif boy.x < 0:
            boy.dir = 1
        pass

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y+25,200,200)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 0, 100, 100, 0, '', boy.x, boy.y+25, 200, 200)
        pass