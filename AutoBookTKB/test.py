from threading import Timer
def hello():
    print "hello, world"

# Timer(10.0, hello).start()
t = Timer(2.0, hello)
t.start()
