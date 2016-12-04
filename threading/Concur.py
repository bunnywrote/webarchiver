import threading
import time

class Concur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.iterations = 0
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()

    def run(self):
        self.resume() # unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff
            time.sleep(.1)
            self.iterations += 1

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait

class KeepRunning(object):
    def __init__(self, seconds=10):
        self.run_time = seconds
        self.start_time = time.time()

    @property
    def condition(self):
        return time.time()-self.start_time < self.run_time

# running = KeepRunning()
# concur = Concur()
# concur.start() # calls run() method
#
# while running.condition:
#   concur.resume()
#
#   #after some operation
#   concur.pause()
#   #some other operation
#
# print('concur.iterations == {}'.format(concur.iterations))  # show thread executed