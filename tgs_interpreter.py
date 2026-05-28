import sys
import os
import random
import subprocess
import re

class TGSInterpreter:
    def __init__(self, debug=False, banner=False):
        self.variables = {}
        self.labels = {}
        self.lines = []
        self.pc = 0
        self.debug = debug
        self.max_iterations = 10000
        self.iteration_count = 0
        if banner:
            self.show_banner()
    
    def show_banner(self):
        print("=" * 50)
        print("TGS Interpreter v1.0.0")
        print("Terminal Generative Script")
        print("=" * 50)
    
    def substitute_vars(self, text):
        """Заменяет $variable на значение"""
        def replace_var(match):
            var_name = match.group(1)
            if var_name in self.variables:
                return str(self.variables[var_name])
            return match.group(0)
        
        # Находим все $variable и заменяем
        return re.sub(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', replace_var, text)
    
    def execute_string(self, code_string):
        lines = code_string.split('\\n')
        self.lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                self.lines.append(line)
        
        self.pc = 0
        self.iteration_count = 0
        while self.pc < len(self.lines):
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                print(f"Error: Maximum iterations ({self.max_iterations}) exceeded.")
                break
            line = self.lines[self.pc]
            if line.endswith(':'):
                self.pc += 1
                continue
            if self.debug:
                print(f"[DEBUG] Executing: {line}")
            self.execute_line(line)
            self.pc += 1
    
    def execute_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.lines = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.lines.append(line)
        
        # Поиск меток
        for idx, line in enumerate(self.lines):
            if line.endswith(':'):
                self.labels[line[:-1]] = idx
        
        if self.debug:
            print(f"[DEBUG] Labels: {self.labels}")
        
        self.pc = 0
        self.iteration_count = 0
        while self.pc < len(self.lines):
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                print(f"Error: Maximum iterations ({self.max_iterations}) exceeded.")
                break
            line = self.lines[self.pc]
            if line.endswith(':'):
                self.pc += 1
                continue
            if self.debug:
                print(f"[DEBUG] PC={self.pc}: {line}")
            self.execute_line(line)
            self.pc += 1
    
    def execute_line(self, line):
        parts = line.split()
        if not parts:
            return
        
        cmd = parts[0]
        
        if cmd == 'print':
            # Берем всё после print
            text = ' '.join(parts[1:])
            # Убираем кавычки в начале и конце
            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1]
            # Подставляем переменные
            text = self.substitute_vars(text)
            print(text)
        
        elif cmd == 'input':
            if len(parts) > 1:
                var_name = parts[1].lstrip('$')
                value = input()
                self.variables[var_name] = value
                if self.debug:
                    print(f"[DEBUG] input ${var_name} = '{value}'")
        
        elif cmd == 'set':
            if len(parts) < 3:
                print(f"Error: Invalid set: {line}")
                return
            
            var_name = parts[1].lstrip('$')
            
            # Арифметика: set $var $var + 1
            if len(parts) == 5 and parts[3] in ['+', '-', '*', '/']:
                left_var = parts[2].lstrip('$')
                op = parts[3]
                right_val = parts[4]
                
                left = self.variables.get(left_var, 0)
                if right_val.isdigit():
                    right = int(right_val)
                elif right_val.startswith('$'):
                    right = self.variables.get(right_val[1:], 0)
                else:
                    right = 0
                
                if op == '+':
                    value = left + right
                elif op == '-':
                    value = left - right
                elif op == '*':
                    value = left * right
                elif op == '/':
                    value = left // right if right != 0 else 0
                else:
                    value = right
            else:
                # Обычное присваивание
                value = ' '.join(parts[2:])
                if value.isdigit():
                    value = int(value)
                elif value.startswith('$'):
                    value = self.variables.get(value[1:], '')
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
            
            self.variables[var_name] = value
            if self.debug:
                print(f"[DEBUG] set ${var_name} = {value}")
        
        elif cmd == 'goto':
            if len(parts) > 1:
                label = parts[1]
                if label in self.labels:
                    self.pc = self.labels[label] - 1
                else:
                    print(f"Error: Label '{label}' not found")
        
        elif cmd == 'if':
            # Формат: if $var == value label
            if len(parts) < 5:
                print(f"Error: Invalid if: {line}")
                return
            
            left = parts[1].lstrip('$')
            op = parts[2]
            right = parts[3]
            label = parts[4]
            
            # Получаем значение левой части
            left_val = self.variables.get(left, '')
            
            # Преобразуем правую часть
            if right.isdigit():
                right_val = int(right)
            elif right.startswith('"') and right.endswith('"'):
                right_val = right[1:-1]
            else:
                right_val = right
            
            # Преобразуем левую часть в число если нужно
            if isinstance(left_val, str) and left_val.isdigit():
                left_val = int(left_val)
            
            # Проверяем условие
            cond = False
            if op == '==':
                cond = left_val == right_val
            elif op == '!=':
                cond = left_val != right_val
            elif op == '>':
                cond = left_val > right_val
            elif op == '<':
                cond = left_val < right_val
            elif op == '>=':
                cond = left_val >= right_val
            elif op == '<=':
                cond = left_val <= right_val
            
            if cond:
                if self.debug:
                    print(f"[DEBUG] Condition true, jumping to {label}")
                if label in self.labels:
                    self.pc = self.labels[label] - 1
                else:
                    print(f"Error: Label '{label}' not found")
        
        elif cmd == 'generate':
            # generate 5 numbers from 1 to 10 into $var
            try:
                if len(parts) >= 8 and parts[2] == 'numbers' and parts[3] == 'from':
                    count = int(parts[1])
                    low = int(parts[4])
                    high = int(parts[6])
                    out_var = parts[8].lstrip('$')
                    
                    result = [random.randint(low, high) for _ in range(count)]
                    self.variables[out_var] = result
                    if self.debug:
                        print(f"[DEBUG] Generated {result}")
            except (ValueError, IndexError) as e:
                print(f"Error in generate: {e}")
        
        elif cmd == 'list':
            if len(parts) > 1:
                var_name = parts[1].lstrip('$')
                if var_name in self.variables:
                    value = self.variables[var_name]
                    if isinstance(value, list):
                        for i, item in enumerate(value):
                            print(f"{i}: {item}")
                    else:
                        print(value)
                else:
                    print(f"${var_name} is not defined")
        
        elif cmd == 'run':
            if len(parts) > 1:
                script = ' '.join(parts[1:])
                subprocess.run(script, shell=True)
        
        elif cmd == 'exit':
            sys.exit(0)
        
        elif cmd == 'help':
            self.show_help()
        
        else:
            print(f"Unknown command: {cmd}")
    
    def show_help(self):
        print("""
TGS Commands:
  print "text" or $var     - Print text or variable
  input $var               - Read user input
  set $var value           - Assign value
  set $var $var + 1        - Math operations
  goto label               - Jump to label
  if $var == value label   - Conditional jump
  generate N numbers from X to Y into $var - Random numbers
  list $var                - Show variable content
  run command              - Run system command
  exit                     - Quit
  help                     - Show this help

Labels: label_name:
Comments: # comment
        """)