#!/usr/bin/python3
# Thumb Slicer
import subprocess
import re
import curses, curses.ascii
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='Slice and Dice ARM Thumb encoded instructions (and filter "bad" bytes)')
parser.add_argument('-w', '--whitelist', help='Whitelist file')
parser.add_argument('-b', '--blacklist', help='Blacklist file')
parser.add_argument('-c', help='disable color parsing', action='store_true')
args = parser.parse_args()

# Process Blacklist/Whitelist from file. File format is comma seperated characters.
# They can be literal characters or \x and 0x escaped format for non-printables
def buildlist(file):
  with open(file, 'r') as list:
    #Get List Form
    for l in list:
      if len(l) > 1:
        chars = l.split(',')
    #Clear any whitespace
    for i in range(len(chars)):
      chars[i] = chars[i].replace(' ','')
      chars[i] = chars[i].replace('\n','')
    #Sift Escaped from literal
    for i in range(len(chars)):
      if chars[i].startswith('\\x') or chars[i].startswith('0x'):
        chars[i] = bytes.fromhex(chars[i][2:4]).decode('utf-8')
  return chars

# Process lists
# If whitelist selected, those are the only allowed chars
# Otherwise, if blacklist selected, all chars are vaild except for those in blacklist
# If no lists are selected at all, then ALL chars are valid
if args.whitelist != None:
  whitelist = buildlist(args.whitelist)
elif args.blacklist != None:
  blacklist = buildlist(args.blacklist)
  whitelist = []
  for byte in range(256):
    whitelist.append(str(chr(byte)))
  whitelist = [x for x in whitelist if x not in blacklist]
else:
  whitelist = []
  for byte in range(256):
    whitelist.append(str(chr(byte)))

# Build a list of all of the instructions. Elements (in order) are hex, assembly, binary, integer forms
instructions = [[],[],[],[]]  # Init the data structure
# Create list of all available machine code based on character restrictions from whitelist/blacklist
ops = []
for one in whitelist:
  for two in whitelist:
    ops.append('{0:0{1}x}{2:0{3}x}'.format(ord(two),2,ord(one),2))
# Use the machine code list to populate the instruction data structure with the assembly, binary, and integer forms too
with open('instructions.dat', 'r') as fh:
  for line in fh:
    if not line.startswith('#'):
      match = re.match(r'([0-9a-f]{4})\s(.+)', line)
      if (args.whitelist == None and args.blacklist == None) or match.group(1) in ops:
        instructions[0].append(match.group(1))                              # Hex
        instructions[1].append(match.group(2))                              # Assembly Instruction
        instructions[2].append(bin(int(match.group(1), 16))[2:].zfill(16))  # Binary Representation
        instructions[3].append(str(int(match.group(1), 16)))                # Integer Representation

# Given an instruction (inst) of the format (column), it will return a list of (lines) elements of matching instructions
def get_instr(inst, lines, column):
  list = [[],[],[],[]]  # Init the data structure
  index = 0
  for instr in instructions[column]:
    if regex_mode == 2:
      if instr.startswith(inst) or instr == inst:
        list[0].append(instructions[0][index])
        list[1].append(instructions[1][index])
        list[2].append(instructions[2][index])
        list[3].append(instructions[3][index])        
        lines -= 1
      index += 1
      if lines == 0: break
    elif regex_mode == 15:
      try:
        inst_reg = re.compile(inst)
        if inst_reg.match(instr):
          list[0].append(instructions[0][index])
          list[1].append(instructions[1][index])
          list[2].append(instructions[2][index])
          list[3].append(instructions[3][index])        
          lines -= 1
        index += 1
        if lines == 0: break
      except: pass
  return list

def input_char():
  try:
    while True:
      ch = win.getch()
      break
  except: raise
  return ch

# Init Curses
win = curses.initscr()
curses.noecho()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW) # 1st register
curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK) # 2nd register
curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_YELLOW) # 3rd register
curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(10, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # AMR v8
curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLACK) # Don't Care
curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_BLACK) # Conditional
curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_GREEN) # Binary Instruction Input
curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_BLUE) # Hex Instruction Input
curses.init_pair(15, curses.COLOR_GREEN, curses.COLOR_GREEN) # Regex Mode
instruction = ''
win.addstr(0,0,"Type an instruction you would like to use (Enter/Return to quit)")
disp_instr = [[],[]]
mode = 'assembly'
regex_mode = 2
errors = []
from colorize import bincolor
try:
  while True:
    height,width = win.getmaxyx()
    blankline = ' ' * width
    win.addstr(1,0,blankline)
    win.addstr(1,7,"Instruction: ")
    if mode == 'assembly':
      win.addstr(1,20,instruction,curses.color_pair(1))   # assembly
    elif mode == 'binary':
      win.addstr(1,20,instruction,curses.color_pair(13))  # binary
    elif mode == 'hex':
      win.addstr(1,20,instruction,curses.color_pair(14))  # hex
    elif mode == 'int':
      win.addstr(1,20,instruction,curses.color_pair(6))   # int
    
    # Top Separater Bar
    win.addstr(2,0,blankline, curses.color_pair(regex_mode)) # Blue Line
    win.addstr(2,0,"!", curses.color_pair(6))       # Int mode indicator
    win.addstr(2,13,"@", curses.color_pair(14))     # Hex mode indicator
    win.addstr(2,20,"%", curses.color_pair(13))     # Bin mode indicator
    win.addstr(2,39,"&", curses.color_pair(1))      # ASM mode indicator

    #Clear Suggested Instructions Lines
    for line in range(height-4):
      win.addstr(line+3,0,blankline)

    # Get Instructions
    if mode == 'assembly':
      disp_instr = get_instr(instruction, height-3,1)
    elif mode == 'binary':
      disp_instr = get_instr(instruction, height-3,2)
    elif mode == 'hex':
      disp_instr = get_instr(instruction, height-3,0)
    elif mode == 'int':
      disp_instr = get_instr(instruction, height-3,3)

    # Display all of the instructions
    for line in range(height-3):
      try:

        # Print an Int form of machine code as well
        win.addstr(line+3, 0, disp_instr[3][line], curses.color_pair(6))
        win.addstr(line+3, 6," ", curses.color_pair(regex_mode))

        # Get Machine Bytes to represent as extended ASCII
        try:
          if bytes.fromhex(disp_instr[0][line][0:2]).decode('utf-8').isprintable(): win.addstr(line+3, 8, bytes.fromhex(disp_instr[0][line][0:2]).decode('utf-8'), curses.color_pair(9))
          else: win.addstr(line+3, 8, '.', curses.color_pair(9))
        except: win.addstr(line+3, 8, '.', curses.color_pair(9))
        try:
          if bytes.fromhex(disp_instr[0][line][2:4]).decode('utf-8').isprintable(): win.addstr(line+3, 9, bytes.fromhex(disp_instr[0][line][2:4]).decode('utf-8'), curses.color_pair(9))
          else: win.addstr(line+3, 9, '.', curses.color_pair(9))
        except: win.addstr(line+3, 9, '.', curses.color_pair(9))
        win.addstr(line+3, 11," ", curses.color_pair(regex_mode))

        # Machine Code
        win.addstr(line+3,13,disp_instr[0][line], curses.color_pair(14))
        win.addstr(line+3,18," ", curses.color_pair(regex_mode))

        if not args.c:
          if not bincolor(line,disp_instr,regex_mode):
            # Binary
            win.addstr(line+3, 20,disp_instr[2][line])
            win.addstr(line+3,37," ", curses.color_pair(regex_mode))
            # Instruction
            win.addstr(line+3,39,disp_instr[1][line])
        else:
          # Binary
          win.addstr(line+3, 20,disp_instr[2][line])
          win.addstr(line+3,37," ", curses.color_pair(regex_mode))
          # Instruction
          win.addstr(line+3,39,disp_instr[1][line])            

      except Exception as ex:
        errors.append(ex)
        try:
          win.addstr(line+3,0,blankline)
        except: pass

    # Input Parsing
    c = input_char()
    # Exit?
    if chr(c) == "\x0A": break
    # Mode Check
    if chr(c) == '&':
      mode = 'assembly'
    elif chr(c) == '%':
      mode = 'binary'
    elif chr(c) == '@':
      mode = 'hex'
    elif chr(c) == '!':
      mode = 'int'
    elif chr(c) == 'j':
      regex_mode = 2
    elif chr(c) == 'J':
      regex_mode = 15
    else:
      if c == curses.KEY_BACKSPACE or c == curses.ascii.DEL or c == curses.ascii.BS:
        instruction = instruction[0:-1]
      else:
        instruction += chr(c)

  win.refresh()

except(KeyboardInterrupt):
  curses.endwin()
  quit()

curses.endwin()
#pprint(errors)
