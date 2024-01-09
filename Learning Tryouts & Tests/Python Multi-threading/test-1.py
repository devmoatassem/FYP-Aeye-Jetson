import threading
import time

done = False

def thread_function():
    counter = 0
    while not done:
        print("Hello from a thread! ",counter)
        counter += 1
        time.sleep(1)




def function2():
    input("Press Enter to stop the thread")
    global done
    done = True

threading.Thread(target=thread_function).start()
threading.Thread(target=function2).start()