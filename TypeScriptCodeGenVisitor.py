
from ASRParser import ASRParser
from ASRVisitor import ASRVisitor
from antlr4 import ParseTreeVisitor

class TypeScriptCodeGenVisitor(ParseTreeVisitor):
    def __init__(self):
        self.code_lines = []

    def visitR(self, ctx):
        # Visit all param children
        for param_ctx in ctx.param():
            self.visit(param_ctx)
        return '\n'.join(self.code_lines)

    def visitParam(self, ctx):
        param_id = ctx.ID().getText() if ctx.ID() else None
        param_value = self.visit(ctx.literal()) if ctx.literal() else None
        # Remove quotes if it's a string
        if param_value and param_value.startswith('"') and param_value.endswith('"'):
            param_value = param_value[1:-1]
            param_value = f'"{param_value}"'  # keep as TypeScript string literal
        self.code_lines.append(f"let {param_id}: any = {param_value};\nconsole.log(`{param_id}: ${{{param_id}}}`);")
    def get_code(self):
        return '\n'.join(self.code_lines)

    def visitEntity(self, ctx):
        entity_name = ctx.ID().getText() if ctx.ID() else None
        # Collect all entity fields and add them to the interface
        fields = []
        
        fields = []
        for field_ctx in ctx.entityfield():
            field_name = field_ctx.ID().getText()
            field_type = field_ctx.TYPE().getText() if field_ctx.TYPE() else "any"
            fields.append(f"  {field_name}: {field_type};")
        self.code_lines.append(f"interface {entity_name} {{\n" + "\n".join(fields) + "\n}")
        self.code_lines.append(f"interface {entity_name} {{}}")

    def visitLiteral(self, ctx:ASRParser.LiteralContext):
        return ctx.getText() if ctx else None

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
    visitor.visit(tree)
    code = visitor.get_code()
    print(code)
