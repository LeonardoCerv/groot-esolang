"""
Groot Programming Language Interpreter
Main entry point for the Groot language interpreter.
"""

from parser import GrootParser
from interpreter import GrootInterpreter

def main():
    """Run the Groot esolang"""
    print("""
  ___       ___    __  __       _____   _____    _____   _____   _____    _   _   _ 
 |_ _|     / _ \  |  \/  |     / ____| |  __ \  |  _  | |  _  | |_   _|  | | | | | |
  | |     / /_\ \ | |\/| |    | |  __  | |__) | | | | | | | | |   | |    | | | | | |
  | |     |  _  | | |  | |    | | |_ | |  _  /  | | | | | | | |   | |    |_| |_| |_|
  | |     | | | | | |  | |    | |__| | | | \ \  | |_| | | |_| |   | |     _   _   _
 |___|    |_| |_| |_|  |_|     \_____| |_|  \_\ |_____| |_____|   |_|    |_| |_| |_|
          """)
    print("Type 'exit' to quit")
    
    parser = GrootParser()
    interpreter = GrootInterpreter()
    
    while True:
        try:
            user_input = input("groot> ")
            if user_input.lower() == 'exit':
                break
            
            tokens = parser.tokenize(user_input)
            print(f"Tokens: {tokens}")
            
            # TODO: Parse and interpret tokens
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()