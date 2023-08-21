from threading import *





class Testthread:

    def __init__(self, global_vars):
        self.global_vars = global_vars
        print("Entering thread")


    def threading(self):
        t1 = Thread(target=self.count, name="RecordingThread")
        t1.start()


    def count(self):
        i = 0
        while not self.global_vars.all_stop:
            i = i + 1
            print(i)
