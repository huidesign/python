"""module to test for yield"""
def yield_test(n):
    for i in range(n):
        yield call(i)
        print("i=", i)
    print("do something")
    print("end.")

def call(i):
    return i * 2

if __name__ == "__main__":
    for i in yield_test(5):
        print(i, ",")
