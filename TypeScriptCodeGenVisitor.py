
from ASRParser import ASRParser
from ASRVisitor import ASRVisitor
from antlr4 import ParseTreeVisitor

class TypeScriptCodeGenVisitor(ASRVisitor):
    def __init__(self):
        self.code_lines = []

    # def visitR(self, ctx):
    #     # Visit all param children
    #     for param_ctx in ctx.param():
    #         self.visit(param_ctx)
    #     for param_ctx in ctx.param():
    #         self.visit(param_ctx)
    #     return '\n'.join(self.code_lines)

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

    def visitComponent(self, ctx:ASRParser.ComponentContext):
        component_name = ctx.ID().getText() if ctx.ID() else None
        # Collect all component fields and add them to the interface
        self.fields = []
        self.visitChildren(ctx)
        self.code_lines.append(f"interface {component_name} " + '{')

        for field in self.fields:
            self.code_lines.append(f"  {field['name']}: {field['type']}\n")
            if field['default']:
                self.code_lines.append(f"//  TODO Default: {field['default']};")

        self.code_lines.append('}')
        return None

    def visitLiteral(self, ctx:ASRParser.LiteralContext):
        return ctx.getText() if ctx else None

    def visitComponentfielddecl(self, field_ctx: ASRParser.ComponentfielddeclContext):
        
            field_name = field_ctx.ID().getText()
            field_type = field_ctx.TYPE().getText()
            field_default = field_ctx.literal() if field_ctx.literal() else None

            self.fields.append({'name':field_name, 'type': field_type, 'default':field_default})

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
