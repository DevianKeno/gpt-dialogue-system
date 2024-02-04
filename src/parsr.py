
import sys
import msvcrt
import time

CPS = 32
""" Characters per second. """
NARRATE_MARKER = '#'
CHOICE_MARKER = '*'
SKIP_MARKER = '>'
COMMENT_MARKER = '//'

class DialogueSystem:
    """ Simple screenplay dialogue parser.
    """
    
    def __init__(self) -> None:
        self.progress: int = 0
        self.lines = []        
        self.previous_name = ''
        self.choices = []
    
    def read_script(self, filepath):        
        with open(filepath) as file:
            self.lines = file.readlines()
            
    def next(self) -> True:
        i = self.progress
        line = self.lines[self.progress].strip()
                
        if line == '' or line.startswith(COMMENT_MARKER):
            self.progress = i + 1
            return False
        
        if line.startswith(SKIP_MARKER):
            num = int(line[1:])
            self.progress = num            
            return False
        
        if line.startswith(NARRATE_MARKER):
            for char in line.strip('#').strip('"'):
                sys.stdout.write(char)
                
                if char == '.':
                    time.sleep(0.6)
                if char == ',':
                    time.sleep(0.3)
                else:
                    time.sleep(1 / CPS)
            
            self.progress = i + 1
            return True
        
        if line.startswith(CHOICE_MARKER): # choice
            self.previous_name = ''
            self.choices.append(line)
            self.progress = i + 1
            return False
                
        if self.choices:
            for i, c in enumerate(self.choices):
                quote = '"'
                print(f'[{i + 1}] {c[1 + c.find(quote): c.rfind(quote)]}')
            
            while True:
                sys.stdin.flush()
                response = input('> ')
                if response.isdecimal() and 1 <= int(response) <= len(self.choices):
                    idx = int(response)
                    self.progress = int(self.choices[idx - 1].split(SKIP_MARKER)[-1].strip()) - 1
                    self.choices = []
                    break
            return
                
        line = self.lines[i].split(':')
        
        if not line[0] == self.previous_name:
            self.previous_name = line[0] 
            sys.stdout.writelines(line[0].strip().strip('"') + ': ')
            
        for char in line[1].strip().strip('"'):
            sys.stdout.write(char)
            
            if char == '.':
                time.sleep(0.6)
            if char == ',':
                time.sleep(0.3)
            else:
                time.sleep(1 / CPS)
        
        self.progress = i + 1
        return True
                
    def start(self):        
        while self.progress < len(self.lines):
            if self.next():
                sys.stdin.readline()
                
        print('\n-- END --')