"""test for coroutine"""

def consumer():
    print("[Consumer] Init Consumer...")
    r = "init ok"
    while True:
        n = yield r
        print("[Consumer] consume n = %s, r = %s" % (n, r))
        r = "consumer %s OK" % n

def produce(c):
    print("[Producer] Init Producer ...")
    r = c.send(None)
    print("[Producer] Start Consumer, return %s" % r)
    n = 0
    while n < 5:
        n += 1
        print("[Producer] While, Producing %s..." % n)
        r = c.send(n)
        print("[Producer] Consumer return: %s" % r)
    c.close()
    print("[Producer] Close Producer...")

if __name__ == "__main__":
    produce(consumer())
