import threading
import time
from graphviz import Digraph

class SimpleThreadTracer:
    def __init__(self):
        self.events = []
    
    def log(self, action):
        self.events.append({
            'thread': threading.current_thread().name,
            'action': action,
            'time': time.time()
        })
    
    def show_graph(self):
        dot = Digraph()
        
        for i, event in enumerate(self.events):
            node_id = f"node_{i}"
            label = f"{event['thread']}\n{event['action']}"
            dot.node(node_id, label)
            
            if i > 0:
                dot.edge(f"node_{i-1}", node_id)
        
        dot.render('simple_trace', view=True)

# Использование
tracer = SimpleThreadTracer()

def task():
    tracer.log("start")
    time.sleep(1)
    tracer.log("work")
    time.sleep(1)
    tracer.log("end")

threading.Thread(target=task, name="Thread-1").start()
threading.Thread(target=task, name="Thread-2").start()

time.sleep(3)
tracer.show_graph()