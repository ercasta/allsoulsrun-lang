
import sys
from antlr4 import FileStream, CommonTokenStream
from ASRLexer import ASRLexer
from PythonCodeGenParser import PythonCodeGenParser

# Usage: python run_asr_parser.py <input_file>
def main():
    if len(sys.argv) != 2:
        print("Usage: python run_asr_parser.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    input_stream = FileStream(input_file)
    lexer = ASRLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PythonCodeGenParser(token_stream)
    filename = sys.argv[1]
    if filename.endswith(".asr"):
        filename = filename[:-5]
    parser.generate_python_code(filename)  

if __name__ == "__main__":
    main()
