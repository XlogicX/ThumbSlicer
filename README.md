# ThumbSlicer

<img src=https://github.com/XlogicX/ThumbSlicer/blob/master/thumbslicer_logo.png width="90" height="100">

Slice Thumbs

# CLI Help
usage: thumbslicer3.py [-h] [-w WHITELIST] [-b BLACKLIST] [-c]

Slice and Dice ARM Thumb encoded instructions (and filter "bad" bytes)

optional arguments:
  -h, --help            show this help message and exit
  -w WHITELIST, --whitelist WHITELIST
                        Whitelist file
  -b BLACKLIST, --blacklist BLACKLIST
                        Blacklist file
  -c                    disable color parsing
  
# Runtime Help

Keys/Modes in runtime
! - Integer Input Mode
@ - ASCII Hex Machine Input Mode
% - Binary Input Mode
& - Assembly Input Mode (Default)
J - Regex Input parsing
j - Literal Input parsing (Default)
