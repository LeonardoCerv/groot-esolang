from parser import GrootParser
from interpreter import GrootInterpreter

def main():
    print(r"""
                 ___       ___    __  __       _____   _____    _____   _____   _____    _   _   _ 
                |_ _|     / _ \  |  \/  |     / ____| |  __ \  |  _  | |  _  | |_   _|  | | | | | |
                 | |     / /_\ \ | |\/| |    | |  __  | |__) | | | | | | | | |   | |    | | | | | |
                 | |     |  _  | | |  | |    | | |_ | |  _  /  | | | | | | | |   | |    |_| |_| |_|
                 | |     | | | | | |  | |    | |__| | | | \ \  | |_| | | |_| |   | |     _   _   _
                |___|    |_| |_| |_|  |_|     \_____| |_|  \_\ |_____| |_____|   |_|    |_| |_| |_|
          """)
    print("Groot Language Interpreter")
    print("Commands:")
    print("  'exit' - Quit the interpreter")
    print("  'run <filename>' - Execute a .groot file")
    print("  'vars' - Show current variable values")
    print("  'reset' - Reset interpreter state")
    print("  'help' - Show a help message")
    print()

    parser = GrootParser()
    interpreter = GrootInterpreter()

    while True:
        try:
            user_input = input("groot> ").strip()

            # Exit the interpreter
            if user_input.lower() == 'exit':
                print("I am Groot! (Goodbye!)")
                break

            # Show current variable values
            elif user_input.lower() == 'vars':
                state = interpreter.get_variable_state()
                print(f"GROOT = {state['GROOT']}")
                print(f"groot = {state['groot']}")
                continue

            # Reset interpreter state
            elif user_input.lower() == 'reset':
                interpreter.reset()
                print("Interpreter state reset")
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
                        print(f"Running file: {filename}")
                    execute_code(code, parser, interpreter)
                except FileNotFoundError:
                    print(f"Error: File '{filename}' not found")
                except Exception as e:
                    print(f"Error reading file: {e}")
                continue

            # Execute single line or multi-line input as Groot code
            if user_input:
                execute_code(user_input, parser, interpreter)

        except KeyboardInterrupt:
            print("\nI am Groot! (Goodbye!)")
            break
        except EOFError:
            print("\nI am Groot! (Goodbye!)")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def execute_code(code: str, parser: GrootParser, interpreter: GrootInterpreter):
    """
    Tokenize, parse, and execute Groot code.
    Handles syntax errors gracefully.
    """
    try:
        tokens = parser.tokenize(code)
        if not tokens:
            return
        ast = parser.parse(tokens)
        interpreter.interpret(ast)
    except Exception as e:
        print(f"-rocket: \"syntax error: {e}\"")

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