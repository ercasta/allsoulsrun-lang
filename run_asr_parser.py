
import sys
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from ASRLexer import ASRLexer
from ASRParser import ASRParser
from TypeScriptCodeGenVisitor import TypeScriptCodeGenVisitor

# Usage: python run_asr_parser.py <input_file>
def main():
    if len(sys.argv) != 2:
        print("Usage: python run_asr_parser.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    input_stream = FileStream(input_file)
    lexer = ASRLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ASRParser(token_stream)
    tree = parser.r()
    visitor = TypeScriptCodeGenVisitor()
    walker = ParseTreeWalker()
    walker.walk(visitor, tree)
    code = visitor.get_code()
    # Write to engine/src/<input_file>.ts
    import os
    out_dir = os.path.join(os.path.dirname(__file__), 'engine', 'src')
    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.basename(input_file)
    if base_name.lower().endswith('.asr'):
        ts_name = base_name[:-4] + '.ts'
    else:
        ts_name = base_name + '.ts'
    out_path = os.path.join(out_dir, ts_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"TypeScript code written to {out_path}")

if __name__ == "__main__":
    main()
