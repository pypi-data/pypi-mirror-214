from __future__ import annotations

import os
import sys
from typing import Union

from colors import Color, Format

colorCodes = {
    "&0": Color.BLACK,          "&f": Color.WHITE,
    "&8": Color.DARK_GRAY,      "&7": Color.GRAY,
    "&1": Color.DARK_BLUE,      "&9": Color.BLUE,
    "&2": Color.DARK_GREEN,     "&a": Color.GREEN,
    "&3": Color.DARK_AQUA,      "&b": Color.AQUA,
    "&4": Color.DARK_RED,       "&c": Color.RED,
    "&5": Color.DARK_PURPLE,    "&d": Color.PURPLE,
    "&6": Color.DARK_YELLOW,    "&e": Color.YELLOW,
    
    "&r": Format.RESET,
    "&l": Format.BOLD,
    "&n": Format.UNDERLINE,
    "&m": Format.STRIKETHROUGH,
    "&o": Format.ITALIC,
    "&k": Format.OBFUSCATED,
    "&j": Format.BLINK,
    "&p": Format.OVERLINE,
    "&w": Format.DOUBLE_UNDERLINE,
    "&i": Format.INVERT
}


def echo(*values: object, 
         sep:Union[str, None] = ' ', 
         end:Union[str, None] = "\n") -> None:
    """Prints the colored text to a command prompt.

    ### Arguments
    sep (str): 
        string inserted between values, default a space.
    end (str):
        string appended after the last value, default a newline.
    """
    if sys.platform.lower() == "win32": 
        os.system('color')
    
    text = sep.join(tuple(map(str, values)))

    for code in colorCodes:
        text = text.replace(code, Format.RESET + colorCodes[code])

    sys.stdout.write(u"{}".format(text) + Format.RESET + end)


def info():
    """
    Prints all available formatting codes.
    """
    if sys.platform.lower() == "win32": 
        os.system('color')
    
    echo("""
    Text must be formatted with an ampersand (&).
    ----- Default formatting codes:
    &00            &88            &77            &ff
    &11            &99            &22            &aa
    &33            &bb            &44            &cc
    &55            &dd            &66            &ee
    &rr (reset)&r                 &ll (bold)&r
    &nn (underline)&r             &oo (italic)&r
    &mm (strikethrough)&r             

    ----- Custom formatting codes (not widely supported):
    &jj (blink)&r                 &pp (overline)&r
    &ww (double underline)&r      &ii (invert)&r
    """)