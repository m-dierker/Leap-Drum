import leap.Leap as Leap
from time import time, sleep
import subprocess

vel_tracker = {}
required_frame_count = 2

class DrumListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected to Leap"

        self.drums = []
        self.drums.append('snare.wav')
        self.drums.append('kick.wav')


        self.last_drum_hit = []
        for x in xrange(len(self.drums)):
            self.last_drum_hit.append(0)

        self.ready_to_play = {}


    def on_frame(self, controller):
        global pointer_radius, x_range, required_frame_count

        frame = controller.frame()

        for hand in frame.hands:
            pos = hand.palm_position
            vel = hand.palm_velocity
            id = hand.id

            if vel.z < -350 and not id in self.ready_to_play:
                # Moving forward at a certain speed
                # print vel

                # See if we're tracking the current hand
                if not id in vel_tracker:
                    vel_tracker[id] = []

                count = len(vel_tracker[id])

                print str(count) + " for ID " + str(id)

                # Clear any old frames
                if count >= 1:
                    first_time = vel_tracker[id][0][2]
                    # See if the difference is too much so we don't keep old frames around
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

                    self.ready_to_play[id] = drum_x
            # We might be moving backwards, so we should hit the drum
            elif vel.z > -100 and id in self.ready_to_play:
                drum_x = self.ready_to_play[id]
                # Make sure we aren't playing too fast
                if time() - self.last_drum_hit[drum_x] < .05:
                    print "Playing too fast on ID " + str(id)
                else:
                    print "hit"
                    subprocess.Popen(["afplay", self.drums[drum_x]])
                    self.last_drum_hit[drum_x] = time()

                del self.ready_to_play[id]



def main():
    global screen_size

    leap_controller = Leap.Controller()
    listener = DrumListener()

    leap_controller.add_listener(listener)


    sleep(.1)

    finished = False
    while not finished:
        sleep(.1)

    leap_controller.remove_listener(listener)

if __name__ == '__main__':
    main()

