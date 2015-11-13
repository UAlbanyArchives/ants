from threading import Thread
from time import sleep

def threaded_function(arg):
    for i in range(arg):
        print "running"
        sleep(1)



thread = Thread(target = threaded_function, args = (10, ))
thread.start()
for i in range(4):
    print "doing other things"
    sleep(2)

thread.join()
print "thread finished...exiting"