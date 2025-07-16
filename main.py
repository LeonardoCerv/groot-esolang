from parser import GrootParser
from interpreter import GrootInterpreter
from ascii_art import get_colored_rocket, get_colored_groot

def main():
    # Show rocket on startup - "launching" the interpreter
    print("\033[93mLaunching Groot Language Interpreter...\033[0m")
    print()
    print(get_colored_groot())
    print()
    
    print(r"""
                 ___       ___    __  __       _____   _____    _____   _____   _____    _   _   _ 
                |_ _|     / _ \  |  \/  |     / ____| |  __ \  |  _  | |  _  | |_   _|  | | | | | |
                 | |     / /_\ \ | |\/| |    | |  __  | |__) | | | | | | | | |   | |    | | | | | |
                 | |     |  _  | | |  | |    | | |_ | |  _  /  | | | | | | | |   | |    |_| |_| |_|
                 | |     | | | | | |  | |    | |__| | | | \ \  | |_| | | |_| |   | |     _   _   _
                |___|    |_| |_| |_|  |_|     \_____| |_|  \_\ |_____| |_____|   |_|    |_| |_| |_|
          """)
    print("\033[92mGroot Language Interpreter - Ready for Launch! \033[0m")
    print("\033[96mCommands:\033[0m")
    print("  \033[93m'exit'\033[0m - Quit the interpreter")
    print("  \033[93m'run <filename>'\033[0m - Execute a .groot file")
    print("  \033[93m'vars'\033[0m - Show current variable values")
    print("  \033[93m'reset'\033[0m - Reset interpreter state")
    print("  \033[93m'help'\033[0m - Show a help message")
    print("  \033[93m'rocket'\033[0m - Show rocket ASCII art")
    print("  \033[93m'groot'\033[0m - Show groot ASCII art")
    print()

    parser = GrootParser()
    interpreter = GrootInterpreter()

    while True:
        try:
            user_input = input("groot> ").strip()

            # Exit the interpreter
            if user_input.lower() == 'exit':
                print("\033[92m")
                print(get_colored_groot())
                print("\033[0m")
                print("\033[92mI am Groot! (Goodbye!)\033[0m")
                break

            # Show rocket ASCII art
            elif user_input.lower() == 'rocket':
                print("\033[93mRocket Launch Sequence Activated!\033[0m")
                print()
                print(get_colored_rocket())
                print()
                continue

            # Show groot ASCII art
            elif user_input.lower() == 'groot':
                print("\033[92mI am Groot!\033[0m")
                print()
                print(get_colored_groot())
                print()
                continue

            # Show current variable values
            elif user_input.lower() == 'vars':
                state = interpreter.get_variable_state()
                print(f"\033[96mGROOT = \033[93m{state['GROOT']}\033[0m")
                print(f"\033[96mgroot = \033[93m{state['groot']}\033[0m")
                continue

            # Reset interpreter state
            elif user_input.lower() == 'reset':
                interpreter.reset()
                print("\033[94mInterpreter launched fresh! State reset.\033[0m")
                continue

            # Show help message
            elif user_input.lower() == 'help':
                print_help()
                continue

            # Run a Groot program from a file
            elif user_input.startswith('run '):
                filename = user_input[4:].strip()
                try:
                    with open(filename, 'r') as file:
                        code = file.read()
                        print(f"\033[93mLaunching {filename}...\033[0m")
                    execute_code(code, parser, interpreter, show_groot_on_success=True)
                except FileNotFoundError:
                    print(f"\033[91mError: File '{filename}' not found\033[0m")
                except Exception as e:
                    print(f"\033[91mError reading file: {e}\033[0m")
                continue

            # Execute single line or multi-line input as Groot code
            if user_input:
                execute_code(user_input, parser, interpreter)

        except KeyboardInterrupt:
            print("\n\033[92mI am Groot! (Goodbye!)\033[0m")
            break
        except EOFError:
            print("\n\033[92mI am Groot! (Goodbye!)\033[0m")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def execute_code(code: str, parser: GrootParser, interpreter: GrootInterpreter, show_groot_on_success: bool = False):
    """
    Tokenize, parse, and execute Groot code.
    Handles syntax errors gracefully.
    Shows ASCII art on success if requested.
    """
    try:
        tokens = parser.tokenize(code)
        if not tokens:
            return
        ast = parser.parse(tokens)
        interpreter.interpret(ast)
        
        # Show groot on successful execution of files
        if show_groot_on_success:
            print("\033[92mProgram completed successfully!\033[0m")
            print()
            print(get_colored_groot())
            print()
            
    except Exception as e:
        print(f"\033[91msyntax error: {e}\033[0m")

def print_help():
    """
    Print help information about the Groot language syntax and features.
    """
    print("""
Groot Language Syntax:

Variables:
  - I am GROOT    (uppercase variable)
  - I am groot    (lowercase variable)

Operations:
  - I am GROOT!   (increment GROOT)
  - I am groot!   (increment groot)
  - I am GROOT?   (decrement GROOT)
  - I am groot?   (decrement groot)
  - I am GROOT    (print GROOT)
  - I am groot    (print groot)

Assignments:
  - I am groot, I am GROOT         (groot = GROOT)
  - I am GROOT, I am groot         (GROOT = groot)
  - I am groot, I am... Groot      (groot = function())

Arithmetic:
  - I am groot! I am GROOT         (groot += GROOT)
  - I am groot? I am GROOT         (groot -= GROOT)

Functions:
  - I am... Groot,                 (function declaration start)
      [indented statements]
      I am groot.                  (return groot)
  - I am... Groot                  (function call)

Error Handling:
  - I am groot???                  (try block start)
      [indented statements]
  - I am groot!!!                  (catch block start)
      [indented statements]
      I am groot.                  (print error message)

Comments:
  - # This is a comment

Example:
  I am GROOT!
  I am groot!
  I am groot! I am GROOT
  I am groot
""")

if __name__ == "__main__":
    main()