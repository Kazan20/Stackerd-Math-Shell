import os
import sys
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from num2words import num2words
import subprocess

class StackerdMath:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.pointer = 0
        self.commands = {
            'push': self.push,
            'pop': self.pop,
            'add': self.add,
            'sub': self.sub,
            'mul': self.mul,
            'div': self.div,
            'print': self.print,
            'mov': self.mov,
            'jump': self.jump,
            'save': self.save,
            'clk': self.clk,
            'book': self.book,
            'play': self.play_game,
            'play_prize_check': self.play_prize_check,
            'register': self.register_user,
            'login': self.login_user,
            'logout': self.logout_user,
            'ss': self.show_stack,
            'sweb': self.launch_sweb,
            'sf': self.show_files,
            'clear': self.clear,
            'cord': self.cord,
            'ping': self.ping
        }
        self.command_docs = {
            'push': 'Pushes a value onto the stack. Usage: push <value>',
            'pop': 'Removes the top value from the stack. Usage: pop',
            'add': 'Adds the top two values from the stack. Usage: add',
            'sub': 'Subtracts the top value from the second-to-top value. Usage: sub',
            'mul': 'Multiplies the top two values from the stack. Usage: mul',
            'div': 'Divides the second-to-top value by the top value. Usage: div',
            'print': 'Prints the top value of the stack. Usage: print',
            'mov': 'Moves the top value of the stack to a variable. Usage: mov <var_name>',
            'jump': 'Jumps to a label in the command list. Usage: jump <label>',
            'save': 'Saves the current stack to a file. Usage: save <filename>',
            'clk': 'Displays the current date and time. Usage: clk',
            'book': 'Shows help information for commands. Usage: book [command]',
            'play': 'Starts a number guessing game. Usage: play',
            'play_prize_check': 'Starts the Prize Check game. Usage: play_prize_check',
            'register': 'Registers a new user. Usage: register <username> <password>',
            'login': 'Logs in a user. Usage: login <username> <password>',
            'logout': 'Logs out the current user. Usage: logout',
            'ss': 'Shows the current stack in a formatted view. Usage: ss',
            'sweb': 'Launches the sweb text-based web browser. Usage: sweb',
            'sf': 'Shows .rffm files in the current directory and their sizes. Usage: sf',
            'clear': 'Clears the console screen. Usage: clear',
            'cord': 'Starts the text editor. Usage: cord',
            'ping': 'Pings a host to check connectivity. Usage: ping <host>'
        }
        self.game_active = False
        self.target_number = None
        self.current_user = None
        self.user_data_file = 'users.json'
        self.scores_file = 'scores.json'
        self.loading_complete = False
        self.labels = {}  # To store label positions

        # Load existing user data
        self.load_user_data()
        # Load existing scores data
        self.load_scores()

    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as file:
                self.user_data = json.load(file)
        else:
            self.user_data = {}

    def save_user_data(self):
        with open(self.user_data_file, 'w') as file:
            json.dump(self.user_data, file)

    def load_scores(self):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as file:
                self.scores = json.load(file)
        else:
            self.scores = {}

    def update_score(self, username, score):
        if username in self.scores:
            self.scores[username] += score
        else:
            self.scores[username] = score
        self.save_scores()

    def save_scores(self):
        with open(self.scores_file, 'w') as file:
            json.dump(self.scores, file)

    def ping(self, host):
        if not host:
            print("Usage: ping <host>")
            return
        try:
            result = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
        except FileNotFoundError:
            print("Error: Ping command not found. Ensure it is installed and accessible.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def push(self, value):
        self.stack.append(float(value))
    
    def pop(self, _):
        if self.stack:
            return self.stack.pop()
        else:
            print("Error: Stack is empty.")
    
    def add(self, _):
        if len(self.stack) < 2:
            print("Error: Not enough values on the stack.")
            return
        b = self.pop(None)
        a = self.pop(None)
        self.push(a + b)
    
    def sub(self, _):
        if len(self.stack) < 2:
            print("Error: Not enough values on the stack.")
            return
        b = self.pop(None)
        a = self.pop(None)
        self.push(a - b)
    
    def mul(self, _):
        if len(self.stack) < 2:
            print("Error: Not enough values on the stack.")
            return
        b = self.pop(None)
        a = self.pop(None)
        self.push(a * b)
    
    def div(self, _):
        if len(self.stack) < 2:
            print("Error: Not enough values on the stack.")
            return
        b = self.pop(None)
        a = self.pop(None)
        if b == 0:
            print("Error: Division by zero.")
            self.push(a)
            self.push(b)
        else:
            self.push(a / b)
    
    def print(self, _):
        if self.stack:
            print(self.stack[-1])
        else:
            print("Error: Stack is empty.")
    
    def mov(self, var_name):
        if self.stack:
            self.variables[var_name] = self.stack.pop()
        else:
            print("Error: Stack is empty.")
    
    def jump(self, label):
        if label in self.labels:
            self.pointer = self.labels[label]
        else:
            print(f"Error: Label '{label}' not found.")
    
    def save(self, filename):
        if not filename.endswith('.rffm'):
            filename += '.rffm'
        with open(filename, 'w') as file:
            json.dump(self.stack, file)
        print(f"Stack saved to {filename}.")
    
    def clk(self, _):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Current date and time:", current_time)
    
    def book(self, command=None):
        if command:
            if command in self.command_docs:
                print(self.command_docs[command])
            else:
                print(f"Error: Unknown command '{command}'")
        else:
            for cmd, desc in self.command_docs.items():
                print(f"{cmd}: {desc}")
    
    def play_game(self, _):
        if self.game_active:
            print("Game already in progress.")
            return
        
        self.game_active = True
        self.target_number = random.randint(1, 100)
        print("Guess the number between 1 and 100.")
        
        while self.game_active:
            guess = input("Enter your guess: ")
            try:
                guess = int(guess)
                if guess < self.target_number:
                    print("Too low!")
                elif guess > self.target_number:
                    print("Too high!")
                else:
                    print("Congratulations! You've guessed the number!")
                    self.game_active = False
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def play_prize_check(self, _):
        number = random.randint(1, 100)
        spelled_number = num2words(number)
        print(f"Spell the number: {number}")
        user_input = input("Your answer: ").strip().lower()

        if user_input == spelled_number:
            print("Correct! You win!")
            if self.current_user:
                self.update_score(self.current_user, 1)
        else:
            print("Incorrect. Try again!")
    
    def register_user(self, user_info):
        try:
            username, password = user_info.split()
        except ValueError:
            print("Usage: register <username> <password>")
            return
        
        if not self.load_user_data():
            self.user_data = {}
        
        if username in self.user_data:
            print(f"User '{username}' already exists.")
            return
        
        self.user_data[username] = password
        self.save_user_data()
        print(f"User '{username}' registered successfully.")
    
    def login_user(self, user_info):
        try:
            username, password = user_info.split()
        except ValueError:
            print("Usage: login <username> <password>")
            return
        
        if username in self.user_data and self.user_data[username] == password:
            self.current_user = username
            print(f"User '{username}' logged in.")
        else:
            print("Invalid username or password.")
    
    def logout_user(self, _):
        if self.current_user:
            print(f"User '{self.current_user}' logged out.")
            self.current_user = None
        else:
            print("No user currently logged in.")
    
    def show_stack(self, _):
        print("Current Stack:")
        for index, item in enumerate(self.stack):
            print(f"{index}: {item}")
    
    def show_files(self, _):
        for filename in os.listdir():
            if filename.endswith('.rffm'):
                size = os.path.getsize(filename)
                print(f"{filename} - {size} bytes")
    
    def launch_sweb(self, _):
        browser = Sweb()
        browser.run()
    
    def clear(self, _):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def loading_screen(self):
        print("Loading", end=" ")
        for i in range(10):
            time.sleep(0.7)
            print(f"[{'/' * i}{' ' * (10 - i)}]", end="\r")
        print("Loading complete.")
    
    def cord(self, _):
        filename = input("Enter file name to edit: ").strip()
        if not filename:
            print("Error: No file name provided.")
            return
        
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []
        
        print(f"Editing {filename}. Press Ctrl+C to exit.")
        while True:
            try:
                line = input("line> ")
                if line == '':
                    break
                lines.append(line + '\n')
            except KeyboardInterrupt:
                break
        
        with open(filename, 'w') as file:
            file.writelines(lines)
        print(f"File '{filename}' saved.")
    
    def ping(self, host):
        if not host:
            print("Usage: ping <host>")
            return
        try:
            result = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
        except FileNotFoundError:
            print("Error: Ping command not found. Ensure it is installed and accessible.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def execute(self, commands):
        while self.pointer < len(commands):
            cmd = commands[self.pointer].strip()
            if not cmd:
                self.pointer += 1
                continue
            
            if ':' in cmd:
                # It's a label
                label = cmd.split(':')[0].strip()
                self.labels[label] = self.pointer
                self.pointer += 1
                continue
            
            parts = cmd.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else None
            
            if command in self.commands:
                try:
                    self.commands[command](args)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print(f"Error: Unknown command '{command}'")
            
            self.pointer += 1

    def run(self):
        self.loading_screen()
        while True:
            try:
                user_input = input("stdm> ").strip()
                if user_input.lower() == 'exit':
                    break
                
                commands = user_input.split(';')
                self.pointer = 0
                self.execute(commands)
                
            except Exception as e:
                print(f"An error occurred: {e}")

class Sweb:
    def __init__(self):
        self.commands = {
            'open': self.open_url,
            'search': self.search,
            'exit': self.exit_browser
        }
        self.running = True

    def open_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.display_content(response.text)
            else:
                print(f"Error: Unable to fetch {url}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: {e}")

    def search(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                self.display_content(response.text)
            else:
                print(f"Error: Unable to search. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: {e}")

    def exit_browser(self, _):
        self.running = False
        print("Exiting sweb.")

    def display_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        print("\n" + "="*80)
        print(text)
        print("="*80 + "\n")

    def run(self):
        print("sweb - Simple Text-Based Web Browser")
        print("Commands: open <URL>, search <query>, exit")
        while self.running:
            try:
                command = input("sweb> ").strip().split(maxsplit=1)
                cmd = command[0].lower()
                if len(command) > 1:
                    args = command[1]
                else:
                    args = ""
                
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"Error: Unknown command '{cmd}'")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    shell = StackerdMath()
    shell.run()
