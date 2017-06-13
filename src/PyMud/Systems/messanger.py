'''
Created on 2011-08-13

@author: Nich
'''
import logging
from multiprocessing import Process, Queue
import inspect
from PyMud.messages.message_types import *

class Messanger(object):
    '''
    Provides a mechanism for sending messages between objects
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def send(self, someone, message):
        logging.info("Messanger sending"+message)


def start_queue_process(queue, handler_dict):
    #print("hmm")
    process = Process(target=process_queue, args=[queue, handler_dict])
    process.start()
    return process

#    
def stop_queue_process(process, q):
    q.put(PoisonPill())
    if process:
        process.join() 
 
def process_queue(queue, handler_dict):
    while True:
        #logging.info("Well...")
        #print("...")
        msg = queue.get()
        if msg.__class__.__name__ == "PoisonPill":
            return
        
        classes = inspect.getmro(msg.__class__)
        ###print([cls.__name__ for cls in classes])
        #print(handler_dict)
        handlers = []
        #Because of LSP, handlers should handle messages subclassed from the same type. 
        #This lets us handle messages in broad strokes, while also handling very particular messages
        for cls in classes:
            if cls.__name__ in handler_dict:
                handlers.extend(handler_dict[cls.__name__])
        for handler in handlers:
            handler.put(msg, False) 
 
class MessagePassingModule(object):
    
    
    def __init__(self, message_queue):
        #Queue holding messages
        self.queue = message_queue
        self.handler_dict = {}
        
    def sendAVMessage(self, msg_type, text, location, source_id, message_templates, target=None):
        self.queue.put(AVMessage(msg_type, text, location, source_id, message_templates, target))
    
                
    def register_handler(self, msg_class, handler):
        if not msg_class in self.handler_dict:
            self.handler_dict[msg_class] = []
        self.handler_dict[msg_class].append(handler)
        
                
class PoisonPill():
    pass    
        
class PrintMessage(object):
    def __init__(self, msg):
        self.msg = msg

class PrintMessageHandler(object):
    
    def __init__(self):
        self.q = Queue()
    
    def handle_print_messages(self):
        #print("Handle ALL the things")
        while not self.q.empty():
            print(self.q.get().msg)
            
      
if __name__ == "__main__":
    #print("TRiplehmm")
    
    
    import time
    q = Queue()
    
    mpm = MessagePassingModule(q)
    pmh = PrintMessageHandler()
    
    q2 = pmh.q
    
    pm = PrintMessage("hello world")
        
    mpm.register_handler(pm.__class__.__name__, pmh.q)
    
    process = start_queue_process(mpm.queue, mpm.handler_dict)
    
    
    
    
    
   
    q.put(pm)
    q.put(pm)
    q.put(pm)
    #pmh.handle_print_messages()
    
    
   
    q.put(pm)
    q.put(pm)
    q.put(pm)
    
    
    
   
    q.put(pm)
    q.put(pm)
    q.put(pm)
    #pmh.handle_print_messages()
    
    
    
    q.put(pm)
    q.put(pm)
    q.put(pm)
    
    print(q.qsize())
    print(q2.qsize())
    
    time.sleep(10)
    print(q.qsize())
    print(q2.qsize())
    pmh.handle_print_messages()
    time.sleep(10)
   
    
    stop_queue_process(process, q)
    pmh.handle_print_messages()
    
    
    
    
    
    
    
        
  
