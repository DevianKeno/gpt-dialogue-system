
import os
from parsr import DialogueSystem

if __name__ == '__main__':
    cwd = os.getcwd()
    scriptpath = os.path.join(cwd, 'src', 'test.txt')
    
    dialogue = DialogueSystem()    
    dialogue.read_script(scriptpath)
    
    dialogue.start()