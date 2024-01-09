import function2
import threading
import time

done = False



def thread_function():
    # counter = 0
    while not done:
        function2.functionTest()
        time.sleep(1)




def function22():
    input("Press Enter to stop the thread")
    global done
    done = True

threading.Thread(target=thread_function).start()
threading.Thread(target=function22).start()