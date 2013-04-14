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
required_frame_count = 5

class DrumListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected to Leap"

        self.drums = []
        self.drums.append(Sound('snare.wav'))
        self.drums.append(Sound('kick.wav'))


        self.last_drum_hit = []
        for x in xrange(len(self.drums)):
            self.last_drum_hit.append(0)


    def on_frame(self, controller):
        global pointer_radius, x_range, required_frame_count

        frame = controller.frame()

        for hand in frame.hands:
            pos = hand.palm_position
            vel = hand.palm_velocity
            id = hand.id

            if vel.z < -350:
                # Moving forward at a certina speed
                print vel

                # See if we're tracking the current hand
                if not id in vel_tracker:
                    vel_tracker[id] = []

                count = len(vel_tracker[id])

                # Clear any old frames
                if count >= 1:
                    first_time = vel_tracker[id][0][2]
                    # 100ms difference is too much
                    if time() - first_time > .8:
                        print "Clearing ID " + str(id)
                        del vel_tracker[id]
                        vel_tracker[id] = []

                # Add in the frame
                if count < required_frame_count:
                    vel_tracker[id].append((vel, pos, time()))
                else:
                    # We have enough frames and we know they're valid
                    vel_tracker[id] = []

                    # Play the appropriate drum in the array
                    drum_x = pos.x + 500
                    drum_x  = drum_x / 1000.0 * len(self.drums)
                    drum_x = int(drum_x)

                    # Make sure we aren't playing too fast
                    if time() - self.last_drum_hit[drum_x] < .25:
                        print "Playing too fast on ID " + str(id)
                    else:
                        self.drums[drum_x].play()
                        self.last_drum_hit[drum_x] = time()


def main():
    global screen_size
    # Pygame init
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Leap Drawing')

    leap_controller = Leap.Controller()
    listener = DrumListener()

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
