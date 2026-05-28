import sys
import argparse
import os
from tgs_interpreter import TGSInterpreter

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(
        prog='tgs',
        description='TGS (Terminal Generative Script) Interpreter',
        epilog='Example: tgs script.tgs -v'
    )
    
    parser.add_argument('-v', '--version', action='version', version=f'TGS Interpreter v{VERSION}', help='Show version')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-e', '--execute', type=str, help='Execute TGS code directly from string')
    parser.add_argument('--banner', action='store_true', help='Show startup banner (disabled by default)')
    parser.add_argument('file', nargs='?', help='.tgs script file to execute')
    
    args = parser.parse_args()
    
    if args.execute:
        interpreter = TGSInterpreter(debug=args.debug, banner=args.banner)
        interpreter.execute_string(args.execute)
        sys.exit(0)
    
    if not args.file:
        parser.print_help()
        sys.exit(1)
    
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    if not args.file.endswith('.tgs'):
        print(f"Warning: {args.file} doesn't have .tgs extension")
    
    interpreter = TGSInterpreter(debug=args.debug, banner=args.banner)
    interpreter.execute_file(args.file)

if __name__ == "__main__":
    main()