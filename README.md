---

# StackerdMath (stdm.py)

## Overview

StackerdMath (stdm) is a stack-based shell with a variety of commands for mathematical operations, file management, and more. It features stack manipulation commands, a simple browser (`sweb`), a text editor (`cord`), and additional utilities like `ping` and `loading` screens. This shell is built in Python and provides a minimalistic yet functional command-line environment.

## Features

- **Stack Operations:** Push, pop, add, sub, mul, div, and more.
- **File Management:** Show stack contents, list `.rffm` files, and edit files.
- **User System:** Register, login, and manage users.
- **Simple Browser:** Basic text-based web browsing with `sweb`.
- **Text Editor:** Edit text files within the shell using `cord`.
- **Ping Command:** Check the reachability of hosts.
- **Conditional Jumps:** Control the flow of commands using labels and jumps.
- **Loading Screen:** Display a progress indicator during startup.

## Commands

### Stack Operations

- **push <number>:** Push a number onto the stack.
- **pop:** Remove and display the top item from the stack.
- **add:** Pop the top two items, add them, and push the result.
- **sub:** Pop the top two items, subtract them, and push the result.
- **mul:** Pop the top two items, multiply them, and push the result.
- **div:** Pop the top two items, divide them, and push the result.
- **print:** Display the top item from the stack.
- **jump <label>:** Jump to the specified label.
- **ss:** Show the current stack.
- **save <filename>:** Save the current stack to a `.rffm` file.

### File Management

- **sf:** Show `.rffm` files and their sizes.
- **cord:** Enter a text editor to edit a file.
- **ping <host>:** Ping a specified host.

### User System

- **register <username> <password>:** Register a new user.
- **login <username> <password>:** Log in as a user.
- **logout:** Log out the current user.

### Browser (`sweb`)

- **open <URL>:** Open a specified URL.
- **search <query>:** Search for a query using Google.
- **exit:** Exit the browser.

### Utility

- **clk:** Show the current time and date.
- **clear:** Clear the terminal screen.
- **loading:** Display a loading screen during startup.

## Usage

1. **Running the Shell:**

   To start the StackerdMath shell, run the following command in your terminal:

   ```bash
   python stdm.py
   ```

2. **Basic Example:**

   ```plaintext
   stdm> push 5
   stdm> push 10
   stdm> add
   stdm> print
   15
   ```

3. **Saving and Loading Files:**

   ```plaintext
   stdm> push 3
   stdm> push 7
   stdm> add
   stdm> save myfile.rffm
   ```

4. **Using the Browser:**

   ```plaintext
   stdm> sweb
   sweb> open https://example.com
   ```

5. **Editing Files:**

   ```plaintext
   stdm> cord
   Enter file name to edit: myfile.txt
   line> Hello, World!
   ```

6. **User Management:**

   ```plaintext
   stdm> register alice password123
   stdm> login alice password123
   stdm> logout
   ```

## License

This project is licensed under the KICENCE License. See the [LICENSE](LICENSE.ki) file for details.

---
