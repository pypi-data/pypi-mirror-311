import sys
import traceback
import ast
import joblib
from pathlib import Path

class TEMD:
    def __init__(self):
        """Initialize TEMD with error handling models."""
        self._original_excepthook = sys.excepthook
        self._load_models()
        
    def _load_models(self):
        """Load the AST and runtime error models."""
        try:
            models_dir = Path(__file__).parent / 'models'
            # Load AST model
            ast_model_data = joblib.load(models_dir / 'ast_error_model.joblib')
            self.ast_model = ast_model_data['model']
            self.ast_vectorizer = ast_model_data['vectorizer']
            
            # Load runtime model
            runtime_model_data = joblib.load(models_dir / 'runtime_error_model.joblib')
            self.runtime_model = runtime_model_data['model']
            self.runtime_vectorizer = runtime_model_data['vectorizer']
            
        except Exception as e:
            # print(f"Error loading models: {e}")
            # print(f"Using fallback error explanations...")
            # Fallback error explanations
            self._setup_fallback_explanations()
    
    def _setup_fallback_explanations(self):
        """Setup fallback error explanations if models fail to load."""
        self.error_explanations = {
            'SyntaxError': 'There is a syntax error in your code',
            'IndentationError': 'Your code is not properly indented',
            'ZeroDivisionError': 'You tried to divide by zero',
            'IndexError': 'You tried to access an index that does not exist',
            'TypeError': 'You tried to perform an operation with incompatible types'
        }
    
    def init(self):
        """Initialize global error handling."""
        sys.excepthook = self.custom_handler
        print("EMD error handling activated!")

    def wrap(self, code_str):
        """Execute code with TEMD error handling."""
        try:
            # Check for syntax errors first
            try:
                ast.parse(code_str)
            except SyntaxError as e:
                return self._handle_syntax_error(e)
            
            # If syntax is okay, execute the code
            compiled_code = compile(code_str, '<string>', 'exec')
            exec(compiled_code)
            
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self._handle_runtime_error(exc_type, exc_value, exc_traceback)

    def _get_explanation(self, error_type, error_code, is_syntax=False):
        """Get error explanation from appropriate model."""
        try:
            if is_syntax:
                features = self.ast_vectorizer.transform([error_code])
                prediction = self.ast_model.predict(features)[0]
            else:
                features = self.runtime_vectorizer.transform([error_code])
                prediction = self.runtime_model.predict(features)[0]
            return prediction['explanation']
        except:
            # Fallback to basic explanations
            return self.error_explanations.get(error_type.__name__, 
                f"An error occurred: {str(error_type.__name__)}")

    def _handle_syntax_error(self, error):
        """Handle syntax and indentation errors using the AST model."""
        error_type = type(error).__name__
        friendly_explanation = self._get_explanation(
            type(error), 
            getattr(error, 'text', ''), 
            is_syntax=True
        )
        
        self._print_error_message(
            error_type=error_type,
            original_msg=str(error),
            friendly_explanation=friendly_explanation,
            line_no=getattr(error, 'lineno', '?'),
            code_context=getattr(error, 'text', ''),
            arrow_pos=getattr(error, 'offset', None)
        )

    def _handle_runtime_error(self, exc_type, exc_value, exc_traceback):
        """Handle runtime errors using the runtime model."""
        tb = traceback.extract_tb(exc_traceback)[-1]
        friendly_explanation = self._get_explanation(
            exc_type, 
            tb.line, 
            is_syntax=False
        )
        
        self._print_error_message(
            error_type=exc_type.__name__,
            original_msg=str(exc_value),
            friendly_explanation=friendly_explanation,
            line_no=tb.lineno,
            code_context=tb.line
        )

    def _print_error_message(self, error_type, original_msg, friendly_explanation, 
                           line_no, code_context, arrow_pos=None):
        """Print a formatted error message."""
        border = "═" * 50
        print(f"\n{border}")
        print("🚨 ERROR DETECTED!")
        print(f"Type: {error_type}")
        print(f"Message: {original_msg}")
        print(f"\n💡 Explanation: {friendly_explanation}")
        print(f"\nLocation: Line {line_no}")
        if code_context:
            print(f"Code: {code_context.rstrip()}")
            if arrow_pos is not None:
                print(" " * (6 + arrow_pos) + "^")
        print(f"{border}\n")

    def custom_handler(self, exc_type, exc_value, exc_traceback):
        """Custom error handler for catching and explaining errors globally."""
        if issubclass(exc_type, SyntaxError) or issubclass(exc_type, IndentationError):
            self._handle_syntax_error(exc_value)
        else:
            self._handle_runtime_error(exc_type, exc_value, exc_traceback)

    def restore(self):
        """Restore the original error handler."""
        sys.excepthook = self._original_excepthook

# Example usage
# if __name__ == "__main__":
#     temd = TEMD()
#     temd.init()
#     my_list = [1, 2, 3]
# for i in range(5):
#     print(my_list[i])
# #     code = """
# # my_list = [1, 2, 3]
# # for i in range(5):
# #     print(my_list[i])
# # """
# #     temd.wrap(code)

