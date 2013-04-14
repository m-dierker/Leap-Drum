import pygame
from pygame.locals import *
import pygame.gfxdraw
import leap.Leap as Leap
from time import time, sleep
import pygame.mixer
from pygame.mixer import Sound

pointer_radius = 4
x_range = 200
screen_size = (10, 10)
vel_tracker = {}
frame_count = 5

class LeapListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected to Leap"

        self.snare = Sound('snare.wav')
        self.kick = Sound('kick.wav')

    def on_frame(self, controller):
        global pointer_radius, x_range, frame_count

        frame = controller.frame()

        for hand in frame.hands:
            pos = hand.palm_position
            vel = hand.palm_velocity
            id = hand.id

            if vel.z < -350:
                print vel
                if not id in vel_tracker:
                    vel_tracker[id] = []
                if id in vel_tracker:
                    count = len(vel_tracker[id])
                    if count < frame_count:
                        vel_tracker[id].append((vel, pos, time()))
                    else:
                        vel_copy = vel_tracker[id][:]
                        for (vel, pos, trigger_time) in vel_copy:
                            if time() - trigger_time >= 100:
                                vel_tracker[id].remove((vel, pos, trigger_time))
                        if len(vel_tracker[id]) >= frame_count:
                            last_vel = vel_tracker[id][-1:][0][0]
                            vel_tracker[id] = []
                            if pos.x < 0:
                                self.snare.play()
                            else:
                                self.kick.play()


def main():
    global screen_size
    # Pygame init
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Leap Drawing')

    leap_controller = Leap.Controller()
    listener = LeapListener()

    leap_controller.add_listener(listener)


    sleep(.1)

    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                finished = True

        # renderer.render()
        pygame.time.wait(10)
        # time.sleep(.015)

    leap_controller.remove_listener(listener)

if __name__ == '__main__':
    main()
