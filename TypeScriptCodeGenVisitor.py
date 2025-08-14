from ASRParser import ASRParser
from ASRListener import ASRListener
from antlr4 import ParseTreeWalker

class TypeScriptCodeGenVisitor(ASRListener):
    def __init__(self):
        self.code_lines = []

    def enterParam(self, ctx):
        param_id = ctx.ID().getText() if ctx.ID() else None
        param_value = ctx.DEFAULTVALUE().getText() if ctx.DEFAULTVALUE() else None
        # Remove quotes if it's a string
        if param_value and param_value.startswith('"') and param_value.endswith('"'):
            param_value = param_value[1:-1]
            param_value = f'"{param_value}"'  # keep as TypeScript string literal
        # TypeScript: let <id>: any = <value>; console.log(`<id>: ${<id>}`);
        self.code_lines.append(f"let {param_id}: any = {param_value};\nconsole.log(`{param_id}: ${{{param_id}}}`);")

    def get_code(self):
        return '\n'.join(self.code_lines)

if __name__ == "__main__":
    import sys
    from antlr4 import FileStream, CommonTokenStream
    if len(sys.argv) != 2:
        print("Usage: python TypeScriptCodeGenVisitor.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    input_stream = FileStream(input_file)
    from ASRLexer import ASRLexer
    lexer = ASRLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    from ASRParser import ASRParser
    parser = ASRParser(token_stream)
    tree = parser.r()
    visitor = TypeScriptCodeGenVisitor()
    walker = ParseTreeWalker()
    walker.walk(visitor, tree)
    code = visitor.get_code()
    print(code)
