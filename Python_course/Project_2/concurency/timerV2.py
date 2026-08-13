# Custom thread class

import threading
from time import sleep


class MyThread(threading.Thread):
    
    def __init__(self, name = None, daemon = None, target:function|None = None, run_parameter:int | None = 0):
        # super().__init__(name=name, daemon=daemon, target=target) 
        super().__init__(name=name, daemon=daemon)
        self.target = target
        self.par1 = run_parameter
        self.__do_stop = False
        pass
    
    def run(self): # Thread task  
            
        print(f"{self.name=}  {self.daemon=} {self.par1=} {self.target=}")
        # if self.target != None: print(self.target)
        if self.target != None: 
            self.target()
        self.__inner_task()
        pass
    
    def stop(self):
        self.__do_stop = True
        pass
    
    def __inner_task(self):
        # TO some additional task 
        while True:
            print("Working ...")
            sleep(0.5)
            if self.__do_stop: break
        
        pass
    
    pass

t1 = MyThread(
    name="MyNewThread", 
    daemon=False, 
    run_parameter=22)
t1.start()
'''
MyThread(
    name="MyNewThread", 
    daemon=False, 
    target=lambda:print('First TARGET FUNCTION CALLED!!'), 
    run_parameter=66).start()


MyThread(
    name="MyNewThread", 
    daemon=False, 
    target=lambda:print('Second TARGET FUNCTION CALLED!!'), 
    run_parameter=55).start()

'''

sleep(5)
t1.stop()