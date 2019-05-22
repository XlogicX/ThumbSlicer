import curses
import re

win = curses.initscr()
curses.noecho()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) # machine
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK) # immediate
curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW) # 1st register
curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK) # 2nd register
curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_YELLOW) # 3rd register
curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(10, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # AMR v8
curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLACK) # Don't Care
curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_BLACK) # Conditional
curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_RED) # Binary Instruction Input
curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_BLUE) # Hex Instruction Input
curses.init_pair(15, curses.COLOR_GREEN, curses.COLOR_GREEN) # Regex Mode
def bincolor(x, op, mode):
  binary = op[2][x]
  instruction = op[1][x]

  # LSL/LSR/ASR/(MOV) Immediate
  # Assembly Format: op rx, rx, #n
  if binary.startswith('00000') or binary.startswith('00001') or binary.startswith('00010'):
    # Parse Binary ( x  x| x  x  x |     imm5     |   Rm   |   Rd )
    matches = re.match(r'([01]{5})([01]{5})([01]{3})([01]{3})', binary)
    if matches.group(1) == '00000' and matches.group(2) == '00000':
      # If Imm is zero, this is actually a MOV instruction...
      # Display Binary
      win.addstr(x+3, 20, '0000000000', curses.color_pair(3))
      win.addstr(x+3, 30, matches.group(3), curses.color_pair(6))
      win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
      win.addstr(x+3,37," ",curses.color_pair(mode))
      # Parse Instruction
      matches = re.match(r'(\S+)\s(\S+)\s(\S+)', instruction)
      # Instruction
      win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
      win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
      win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
      return 1
    else:
      # Display Binary
      win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
      win.addstr(x+3, 25, matches.group(2), curses.color_pair(4))
      win.addstr(x+3, 30, matches.group(3), curses.color_pair(6))
      win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
      win.addstr(x+3,37," ",curses.color_pair(mode))
      # Parse Instruction
      matches = re.match(r'(\S+)\s(\S+)\s(\S+)\s(\S+)', instruction)
      # Instruction
      win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
      win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
      win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
      win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))
      return 1

  # ADD/SUB Register
  # Assembly Format: op rx, rx, rx
  elif binary.startswith('0001100') or binary.startswith('0001101'):
    # Parse Binary ( x  x | x  x  x  x  x |   Rm   |   Rn   |   Rd)
    matches = re.match(r'([01]{7})([01]{3})([01]{3})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 27, matches.group(2), curses.color_pair(8))
    win.addstr(x+3, 30, matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(8))
    return 1

  # ADD/SUB imm3
  # Assembly Format: op rx, rx, #n
  elif binary.startswith('0001110') or binary.startswith('0001111'):
    # Parse Binary ( x  x | x  x  x  x  x |  imm3  |   Rn   |   Rd)
    matches = re.match(r'([01]{7})([01]{3})([01]{3})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 27, matches.group(2), curses.color_pair(4))
    win.addstr(x+3, 30, matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))
    return 1

  # MOV/CMP/ADD/SUB imm8 
  # Assembly Format: op rx, #n
  elif binary.startswith('00100') or binary.startswith('00101') or binary.startswith('00110') or binary.startswith('00111'):
    # Parse Binary ( x  x | x  x  x |   Rd   |         imm8)
    matches = re.match(r'([01]{5})([01]{3})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 28, matches.group(3), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(4))
    return 1

  # AND/EOR/LSL/LSR/ASR/ADC/SBC/ROR/TST/RSB(NEGS)/CMP/CMN/ORR/MUL/BIC/MVN/SXTH/SXTB/UXTH/UXTB/REV/REV16/REVSH (register)
  # Assembly Format: op rx, rx
  elif binary.startswith('0100000000') or binary.startswith('0100000001') or binary.startswith('0100000010') or binary.startswith('0100000011') or binary.startswith('0100000100') or binary.startswith('0100000101') or binary.startswith('0100000110') or binary.startswith('0100000111') or binary.startswith('0100001000') or binary.startswith('0100001001') or binary.startswith('0100001010') or binary.startswith('0100001011') or binary.startswith('0100001100') or binary.startswith('0100001101') or binary.startswith('0100001110') or binary.startswith('0100001111') or binary.startswith('1011001000') or binary.startswith('1011001001') or binary.startswith('1011001010') or binary.startswith('1011001011') or binary.startswith('1011101000') or binary.startswith('1011101001') or binary.startswith('1011101011'):
    # Parse Binary ( x  x  x  x  x  x  x  x  x  x |   Rm   |   Rdn)
    matches = re.match(r'([01]{10})([01]{3})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 30, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(3), curses.color_pair(7))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
    return 1

  # NOP
  # Assembly Format: nop
  elif binary.startswith('0100011011000000'):
    # Parse Binary ( x  x  x  x  x  x  x  x | R|     Rm    |   Rdn )
    matches = re.match(r'([01]{8})([01]{1})([01]{4})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 28, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 29, matches.group(3), curses.color_pair(7))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(6))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Instruction
    win.addstr(x+3, 39, 'nop (mov ', curses.color_pair(3))
    win.addstr(x+3, 48, 'r8, ', curses.color_pair(7))
    win.addstr(x+3, 52, 'r8', curses.color_pair(6))
    win.addstr(x+3, 54, ')', curses.color_pair(3))
    return 1

  # ADD/CMP/MOV (register)
  # Assembly Format: op rx, rx
  elif binary.startswith('01000100') or binary.startswith('01000101') or binary.startswith('01000110'):
    # Parse Binary ( x  x  x  x  x  x  x  x | R|     Rm    |   Rdn )
    matches = re.match(r'([01]{8})([01]{1})([01]{4})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 28, matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 29, matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
    return 1

  # BX/BLX (register)
  # Assembly Format: op(ns)? rx (Non-Standard Don't-Care Bits)?
  elif binary.startswith('010001110') or binary.startswith('010001111'):
    # Parse Binary ( x  x  x  x  x  x| x  x  x|     Rm    | x (0)(0) )
    matches = re.match(r'([01]{9})([01]{4})([01]{1})([01]{2})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 29, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(3), curses.color_pair(10))
    win.addstr(x+3, 34, matches.group(4), curses.color_pair(11))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)', instruction)
    # Instruction
    if 'ns' in matches.group(1):
      submatches = re.match(r'(.+)ns', matches.group(1))
      win.addstr(x+3, 39, submatches.group(1), curses.color_pair(3))
      win.addstr(x+3, 39+len(submatches.group(1)), 'ns', curses.color_pair(10))
      win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
      if 'Standard' in instruction:
        win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), "Non-Standard Don't-Care Bits", curses.color_pair(11))
    else:
      win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
      win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
      if 'Standard' in instruction:
        win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), "Non-Standard Don't-Care Bits", curses.color_pair(11))
    return 1

  # LDR lit imm8 
  # Assembly Format: op rx, [rx, #n] 
  elif binary.startswith('01001'):
    # Parse Binary ( x  x | x  x  x |   Rd   |         imm8)
    matches = re.match(r'([01]{5})([01]{3})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 28, matches.group(3), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\[[^]]+?\])', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(4))
    return 1

  # STR/LDR
  # Assembly Format: op rx, [rx, rx]
  elif binary.startswith('0101000') or binary.startswith('0101001') or binary.startswith('0101010') or binary.startswith('0101011') or binary.startswith('0101100') or binary.startswith('0101101') or binary.startswith('0101110') or binary.startswith('0101111'):
    # Parse Binary ( x  x | x  x  x  x  x |   Rm   |   Rn   |   Rd)
    matches = re.match(r'([01]{7})([01]{3})([01]{3})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 27, matches.group(2), curses.color_pair(8))
    win.addstr(x+3, 30, matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\[\S+)\s(\S+\])', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(8))
    return 1

  # LDR/STR imm
  # Assembly Format: op rx, [rx, #n]
  if binary.startswith('01100') or binary.startswith('01101') or binary.startswith('01110') or binary.startswith('01111') or binary.startswith('10000') or binary.startswith('10001'):
    # Parse Binary ( x  x| x  x  x |     imm5     |   Rm   |   Rd )
    matches = re.match(r'([01]{5})([01]{5})([01]{3})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(4))
    win.addstr(x+3, 30, matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(7))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\[\S+)\s(\S+\])', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(6))
    win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))
    return 1

  # LDR/STR imm SP rel
  # Assembly Format: op rx, [sp, #n]
  elif binary.startswith('1001'):
    # Parse Binary ( x  x | x  x  x |   Rd   |         imm8)
    matches = re.match(r'([01]{5})([01]{3})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 28, matches.group(3), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\[\S+)\s(\S+\])', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))
    return 1
	 
  # ADR/ADDsp
  # Assembly Format: op rx, pc/sp, #n
  elif binary.startswith('1010'):
    # Parse Binary ( x  x | x  x  x |   Rd   |         imm8)
    matches = re.match(r'([01]{5})([01]{3})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 28, matches.group(3), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(7))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 42+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))
    return 1

  # ADD/SUB (SP + imm)
  # Assembly Format: op sp, #n
  elif binary.startswith('101100000') or binary.startswith('101100001'):
    # Parse Binary ( x  x  x  x  x  x  x  x  x |         imm7)
    matches = re.match(r'([01]{9})([01]{7})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 29, matches.group(2), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+\s\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    return 1

  # CBZ
  # Assembly Format: cbnz rx, <pc + (n*2)>
  elif re.match(r'^101100.1', binary):
    # Parse Binary ( x  x  x  x| x| x| i| x|     imm5     |   Rn)
    matches = re.match(r'([01]{6})([01]{1})([01]{1})([01]{5})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 26, matches.group(2), curses.color_pair(4))
    win.addstr(x+3, 27, matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 28, matches.group(4), curses.color_pair(4))
    win.addstr(x+3, 33, matches.group(5), curses.color_pair(6))        
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(cbz)\s(\S+)\s+([^(]+\()([^*]+)(.+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))    
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2))+len(matches.group(3))+len(matches.group(4)), matches.group(5), curses.color_pair(3))
    return 1 

  # PUSH/POP
  # Assembly Format: op {,}
  elif binary.startswith('1011010') or binary.startswith('1011110'):
    # Parse Binary ( x  x  x  x | x  x  x | M|     regiser_list)
    matches = re.match(r'([01]{7})([01]{9})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 27, matches.group(2), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\{[^}]*\})', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    return 1

  # SETPAN/SETEND
  # Assembly Format: op arg
  if binary.startswith('10110110000') or binary.startswith('10110110010'):
    # If SETPAN, use V8 color, otherwise use V7 color for SETEND
    if binary.startswith('10110110000'):
      color = 10
    else:
      color = 3
    # Parse Binary ( x  x  x  x| x  x  x  x| x  x  x|(1) x |(0)(0)(0) )
    matches = re.match(r'([01]{11})([01])([01])([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(color))
    win.addstr(x+3, 31, matches.group(2), curses.color_pair(11))
    win.addstr(x+3, 32, matches.group(3), curses.color_pair(4))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(11))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)(\s\S+)?', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(color))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    if matches.group(3):
      win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(11))
    return 1

  # CPS
  # Assembly Format: op args
  if binary.startswith('10110110011'):
    # Parse Binary ( x  x  x  x| x  x  x  x  x  x  x |im|(0) A| I| F )
    matches = re.match(r'([01]{11})([01])([01])([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 31, matches.group(2), curses.color_pair(4))
    win.addstr(x+3, 32, matches.group(3), curses.color_pair(11))
    win.addstr(x+3, 33, matches.group(4), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)(\s[^(]*)?(.*\))?', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    if matches.group(2):
      win.addstr(x+3, 39+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    if matches.group(3):
      win.addstr(x+3, 39+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(11))
    return 1

  # CBNZ
  # Assembly Format: cbnz rx, <pc + (n*2)>
  elif re.match(r'^101110.1', binary):
    # Parse Binary ( x  x  x  x| x| x| i| x|     imm5     |   Rn)
    matches = re.match(r'([01]{6})([01]{1})([01]{1})([01]{5})([01]{3})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 26, matches.group(2), curses.color_pair(4))
    win.addstr(x+3, 27, matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 28, matches.group(4), curses.color_pair(4))
    win.addstr(x+3, 33, matches.group(5), curses.color_pair(6))        
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(cbnz)\s(\S+)\s+([^(]+\()([^*]+)(.+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))    
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2))+len(matches.group(3))+len(matches.group(4)), matches.group(5), curses.color_pair(3)) 
    return 1 

  # HLT
  # Assembly Format: hlt 0xn
  elif binary.startswith('1011101010'):
    # Parse Binary ( x  x  x  x  x  x  x  x  x  x |         imm6)
    matches = re.match(r'([01]{10})([01]{6})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 30, matches.group(2), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    return 1

  # BKPT
  # Assembly Format: bkpt 0xn
  elif binary.startswith('10111110') or binary.startswith('11011110') or binary.startswith('11011111'):
    # Parse Binary ( x  x  x  x  x  x  x  x |         imm8)
    matches = re.match(r'([01]{8})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 28, matches.group(2), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    return 1    

  # If-Then
  # Assembly Format: optype arg
  elif binary.startswith('10111111'):
    # Parse Binary ( x  x  x  x| x  x  x  x | firstcont |   mask)
    matches = re.match(r'([01]{8})([01]{4})([01]{4})', binary)
    # Display Binary
    if matches.group(3) != '0000':
      win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
      win.addstr(x+3, 28, matches.group(2), curses.color_pair(4))
      win.addstr(x+3, 32, matches.group(3), curses.color_pair(4))
      win.addstr(x+3,37," ",curses.color_pair(mode))
      # Parse Instruction
      matches = re.match(r'(it)(\S*)\s+(\S+)', instruction)
      # Instruction
      win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
      win.addstr(x+3, 39+len(matches.group(1)), matches.group(2), curses.color_pair(4))
      win.addstr(x+3, 40+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(4))
      return 1	 
    elif binary == '1011111100000000':
      win.addstr(x+3, 20, '1011111100000000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nop", curses.color_pair(3))
      return 1
    elif binary == '1011111100010000':
      win.addstr(x+3, 20, '1011111100010000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "yield", curses.color_pair(3))
      return 1
    elif binary == '1011111100100000':
      win.addstr(x+3, 20, '1011111100100000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "wfe", curses.color_pair(3))
      return 1
    elif binary == '1011111100110000':
      win.addstr(x+3, 20, '1011111100110000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "wfi", curses.color_pair(3))
      return 1
    elif binary == '1011111101000000':
      win.addstr(x+3, 20, '1011111101000000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "sev", curses.color_pair(3))
      return 1
    elif binary == '1011111101010000':
      win.addstr(x+3, 20, '1011111101010000', curses.color_pair(10))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "sevl", curses.color_pair(10))
      return 1
    elif binary == '1011111101100000':
      win.addstr(x+3, 20, '1011111101100000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "noppl", curses.color_pair(3))
      return 1
    elif binary == '1011111101110000':
      win.addstr(x+3, 20, '1011111101110000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nopvs", curses.color_pair(3))
      return 1
    elif binary == '1011111110000000':
      win.addstr(x+3, 20, '1011111110000000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nopvc", curses.color_pair(3))
      return 1
    elif binary == '1011111110010000':
      win.addstr(x+3, 20, '1011111110010000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nophi", curses.color_pair(3))
      return 1
    elif binary == '1011111110100000':
      win.addstr(x+3, 20, '1011111110100000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nopls", curses.color_pair(3))
      return 1
    elif binary == '1011111110110000':
      win.addstr(x+3, 20, '1011111110110000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nopge", curses.color_pair(3))
      return 1
    elif binary == '1011111111000000':
      win.addstr(x+3, 20, '1011111111000000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "noplt", curses.color_pair(3))
      return 1
    elif binary == '1011111111010000':
      win.addstr(x+3, 20, '1011111111010000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nopgt", curses.color_pair(3))
      return 1
    elif binary == '1011111111100000':
      win.addstr(x+3, 20, '1011111111100000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nople", curses.color_pair(3))
      return 1
    elif binary == '1011111111110000':
      win.addstr(x+3, 20, '1011111111110000', curses.color_pair(3))
      win.addstr(x+3, 37, " ", curses.color_pair(mode))
      win.addstr(x+3, 39, "nopal", curses.color_pair(3))
      return 1                                                                                          

  # STM/LDM
  # Assembly Format: op rx, {..}
  elif binary.startswith('1100'):
    # Parse Binary ( x  x  x  x  x|   Rn   |     regiser_list)
    matches = re.match(r'([01]{5})([01]{3})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 28, matches.group(3), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(\S+)\s(\S+)\s(.+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 40+len(matches.group(1)), matches.group(2), curses.color_pair(6))
    win.addstr(x+3, 41+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(4))
    return 1

  # B Conditional
  # Assembly Format: bcond.n <pc - (n*2)>
  elif binary.startswith('1101'):
    # Parse Binary ( x  x  x  x |   cond   |         imm8)
    matches = re.match(r'([01]{4})([01]{4})([01]{8})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 24, matches.group(2), curses.color_pair(12))
    win.addstr(x+3, 28, matches.group(3), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'(b)([^.]+?)(\.[^(]+\()([^*]+)(.+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 39+len(matches.group(1)), matches.group(2), curses.color_pair(12))
    win.addstr(x+3, 39+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(3))
    win.addstr(x+3, 39+len(matches.group(1))+len(matches.group(2))+len(matches.group(3)), matches.group(4), curses.color_pair(4))    
    win.addstr(x+3, 39+len(matches.group(1))+len(matches.group(2))+len(matches.group(3))+len(matches.group(4)), matches.group(5), curses.color_pair(3))    
    return 1

  # B Unconditional
  # Assembly Format: b.n <pc + (n*2)>
  elif binary.startswith('11100'):
    # Parse Binary ( x  x  x  x  x  x  x  x |         imm11)
    matches = re.match(r'([01]{5})([01]{11})', binary)
    # Display Binary
    win.addstr(x+3, 20, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 25, matches.group(2), curses.color_pair(4))
    win.addstr(x+3,37," ",curses.color_pair(mode))
    # Parse Instruction
    matches = re.match(r'([^(]+\()([^*]+)(.+)', instruction)
    # Instruction
    win.addstr(x+3, 39, matches.group(1), curses.color_pair(3))
    win.addstr(x+3, 39+len(matches.group(1)), matches.group(2), curses.color_pair(4))
    win.addstr(x+3, 39+len(matches.group(1))+len(matches.group(2)), matches.group(3), curses.color_pair(3))
    return 1  

  else: return 0