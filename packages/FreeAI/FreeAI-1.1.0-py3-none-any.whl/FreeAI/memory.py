import json
from datetime import datetime
from dateutil import parser
import os

MEMORY_FILE = 'conversation_memory.json'


class Memory:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            self.memory = {}
        else:
            with open(MEMORY_FILE, 'r') as file:
                self.memory = json.load(file)

    def save(self, prompt, response):
        timestamp = str(datetime.now())
        self.memory[timestamp] = {'prompt': prompt, 'response': response}
        with open(MEMORY_FILE, 'w') as file:
            json.dump(self.memory, file)

    def get_last_prompt(self):
        if self.memory:
            last_timestamp = max(self.memory.keys())
            return self.memory[last_timestamp]['prompt']
        else:
            return None


memory = Memory()
