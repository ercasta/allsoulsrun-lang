from ASRParser import ASRParser
from antlr4 import ParserRuleContext

class PythonCodeGenParser(ASRParser):
    def __init__(self, input_stream, output=None):
        super().__init__(input_stream, output)

    def generate_python_code(self, output_filename=None):
        tree = self.r()  # Start from the root rule
        code_lines = []
        for param_ctx in tree.param():
            code_lines.append(self._param_to_python(param_ctx))
        code_str = '\n'.join(code_lines)
        if output_filename:
            if output_filename.lower().endswith('.py'):
                output_filename = output_filename[:-3]
            output_filename = output_filename + '.py'
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(code_str)

    def _param_to_python(self, ctx):
        # Extract ID and DEFAULTVALUE tokens
        param_id = ctx.ID().getText() if ctx.ID() else None
        param_value = ctx.DEFAULTVALUE().getText() if ctx.DEFAULTVALUE() else None
        # Remove quotes if it's a string
        if param_value and param_value.startswith('"') and param_value.endswith('"'):
            param_value = param_value[1:-1]
            param_value = f'"{param_value}"'  # keep as Python string literal
        return f"{param_id} = {param_value}\r\nprint(F\"{param_id}: {{{param_id}}}\")"

if __name__ == "__main__":
    import sys
    from antlr4 import FileStream, CommonTokenStream
    if len(sys.argv) != 2:
        print("Usage: python PythonCodeGenParser.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    input_stream = FileStream(input_file)
    from ASRLexer import ASRLexer
    lexer = ASRLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PythonCodeGenParser(token_stream)
    code = parser.generate_python_code()
    print(code)
