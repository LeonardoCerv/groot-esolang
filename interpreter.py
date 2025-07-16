from typing import Dict, Any, Optional

# Custom exception for all Groot language errors
class GrootError(Exception):
    pass

class GrootInterpreter:
    def __init__(self):
        # Initialize interpreter state: two variables, optional function, error state
        self.variables = {
            'GROOT': 0,
            'groot': 0
        }
        self.function = None
        self.in_try_catch = False
        self.current_error = None
        
    def interpret(self, ast: Dict[str, Any]) -> None:
        """Interpret the AST and execute the program"""
        try:
            # First, collect function definition if present
            if ast.get('function'):
                self.function = ast['function']

            # Then, execute all top-level statements
            for statement in ast['statements']:
                self._execute_statement(statement)

        except GrootError as e:
            self._handle_error(str(e))
        except Exception as e:
            # Catch-all for unexpected runtime errors
            self._handle_error(f"Runtime error: {str(e)}")

    def _execute_statement(self, stmt: Dict[str, Any]) -> Optional[int]:
        """Execute a single statement from the AST."""
        try:
            stype = stmt['type']
            if stype == 'INCREMENT':
                return self._increment_variable(stmt['variable'])
            elif stype == 'DECREMENT':
                return self._decrement_variable(stmt['variable'])
            elif stype == 'PRINT':
                return self._print_variable(stmt['variable'])
            elif stype == 'ASSIGN':
                return self._assign_variable(stmt['left'], stmt['right'])
            elif stype == 'FUNC_ASSIGN':
                return self._function_assign(stmt['variable'])
            elif stype == 'ADD':
                return self._add_variables(stmt['left'], stmt['right'])
            elif stype == 'SUBTRACT':
                return self._subtract_variables(stmt['left'], stmt['right'])
            elif stype == 'FUNCTION_CALL':
                return self._call_function()
            elif stype == 'TRY_CATCH':
                return self._execute_try_catch(stmt)
            elif stype == 'RETURN':
                return self.variables[stmt['variable']]
        except GrootError as e:
            # If not in try-catch, handle error; otherwise, propagate
            if not self.in_try_catch:
                self._handle_error(str(e))
            else:
                raise e
        return None

    def _increment_variable(self, var_name: str) -> int:
        """Increment a variable by 1"""
        self.variables[var_name] += 1
        return self.variables[var_name]

    def _decrement_variable(self, var_name: str) -> int:
        """Decrement a variable by 1 (raises GrootError if result < 0)"""
        if self.variables[var_name] <= 0:
            raise GrootError("negative value prevented")
        self.variables[var_name] -= 1
        return self.variables[var_name]

    def _print_variable(self, var_name: str) -> int:
        """Print the value of a variable"""
        value = self.variables[var_name]
        print(value)
        return value

    def _assign_variable(self, left_var: str, right_var: str) -> int:
        """Assign the value of right var to left var"""
        self.variables[left_var] = self.variables[right_var]
        return self.variables[left_var]

    def _function_assign(self, var_name: str) -> int:
        """Assign the return value of function to variable"""
        if self.function is None:
            raise GrootError("function undefined")
        result = self._call_function()
        self.variables[var_name] = result
        return result

    def _add_variables(self, left_var: str, right_var: str) -> int:
        """Add right var value to left var"""
        self.variables[left_var] += self.variables[right_var]
        return self.variables[left_var]

    def _subtract_variables(self, left_var: str, right_var: str) -> int:
        """Subtract right var value from left var"""
        result = self.variables[left_var] - self.variables[right_var]
        if result < 0:
            raise GrootError("negative value prevented")
        self.variables[left_var] = result
        return result
    
    def _call_function(self) -> int:
        """Call the defined function"""
        if self.function is None:
            raise GrootError("function undefined")

        saved_vars = self.variables.copy()  # Save current state for rollback
        try:
            result = 0
            for stmt in self.function['body']:
                if stmt['type'] == 'RETURN':
                    # Return the value of the specified variable
                    result = self.variables[stmt['variable']]
                    break
                else:
                    self._execute_statement(stmt)
            return result
        except GrootError as e:
            # Restore variables on error
            self.variables = saved_vars
            raise e

    def _execute_try_catch(self, stmt: Dict[str, Any]) -> None:
        """
        Execute a try-catch block.
        If an error occurs in the try block, execute the catch block.
        """
        self.in_try_catch = True
        error_occurred = False
        try:
            # Try block: execute each statement
            for try_stmt in stmt['try_body']:
                self._execute_statement(try_stmt)
        except GrootError as e:
            error_occurred = True
            self.current_error = str(e)
            # Catch block: handle error and run catch statements
            for catch_stmt in stmt['catch_body']:
                if catch_stmt['type'] == 'ERROR_OUTPUT':
                    print(f"-rocket: \"{self.current_error}\"")
                else:
                    self._execute_statement(catch_stmt)
        self.in_try_catch = False

        # If no error occurred but catch block has error output, print last value
        if not error_occurred:
            for catch_stmt in stmt['catch_body']:
                if catch_stmt['type'] == 'ERROR_OUTPUT':
                    # Find the last variable value that was used
                    last_value = self.variables['groot']  # Default to groot
                    print(f"rocket: \"{last_value}\"")
                    break

    def _handle_error(self, error_message: str) -> None:
        """Print error messages"""
        print(f"rocket: Something went wrong! \"{error_message}\"")

    def get_variable_state(self) -> Dict[str, int]:
        """Get current state of all variables"""
        return self.variables.copy()

    def reset(self) -> None:
        """Reset interpreter state"""
        self.variables = {
            'GROOT': 0,
            'groot': 0
        }
        self.function = None
        self.in_try_catch = False
        self.current_error = None