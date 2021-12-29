
class OCRCharacter:
    def recognize(character):
        for key, value in OCRCharacter.CHARACTERS.items():
            if value == character:
                return key[0]

    CHARACTERS = {
        'A' : [
            " ##  ",
            "#  # ",
            "#  # ",
            "#### ",
            "#  # ",
            "#  # "
        ],
    
        'B' : [
            "###  ",
            "#  # ",
            "###  ",
            "#  # ",
            "#  # ",
            "###  "
        ],
    
        'C' : [
            " ##  ",
            "#  # ",
            "#    ",
            "#    ",
            "#  # ",
            " ##  "
        ],
    
        'D' : [
            "###  ",
            "#  # ",
            "#  # ",
            "#  # ",
            "#  # ",
            "###  "
        ],
    
        'E' : [
            "#### ",
            "#    ",
            "###  ",
            "#    ",
            "#    ",
            "#### "
        ],
    
        'F' : [
            "#### ",
            "#    ",
            "###  ",
            "#    ",
            "#    ",
            "#    "
        ],
    
        'G' : [
            " ##  ",
            "#    ",
            "#    ",
            "# ## ",
            "#  # ",
            " ##  "
        ],

        'G2' : [
            " ##  ",
            "#  # ",
            "#    ",
            "# ## ",
            "#  # ",
            " ### "
        ],
    
        'H' : [
            "#  # ",
            "#  # ",
            "#### ",
            "#  # ",
            "#  # ",
            "#  # "
        ],
    
        'I' : [
            " ### ",
            "  #  ",
            "  #  ",
            "  #  ",
            "  #  ",
            " ### "
        ],
    
        'J' : [
            "  ## ",
            "   # ",
            "   # ",
            "   # ",
            "#  # ",
            " ##  "
        ],
    
        'K' : [
            "#  # ",
            "# #  ",
            "##   ",
            "# #  ",
            "# #  ",
            "#  # "
        ],
    
        'L' : [
            "#    ",
            "#    ",
            "#    ",
            "#    ",
            "#    ",
            "#### "
        ],
    
        'M' : [
            "#   #",
            "## ##",
            "# # #",
            "#   #",
            "#   #",
            "#   #"
        ],
    
        'N' : [
            "#   #",
            "##  #",
            "# # #",
            "# # #",
            "#  ##",
            "#   #"
        ],
    
        'O' : [
            " ##  ",
            "#  # ",
            "#  # ",
            "#  # ",
            "#  # ",
            " ##  "
        ],
    
        'P' : [
            "###  ",
            "#  # ",
            "#  # ",
            "###  ",
            "#    ",
            "#    "
        ],
    
        'Q' : [
            " ##  ",
            "#  # ",
            "#  # ",
            "# ## ",
            "#  # ",
            " ## #"
        ],
    
        'R' : [
            "###  ",
            "#  # ",
            "#  # ",
            "###  ",
            "# #  ",
            "#  # "
        ],
    
        'S' : [
            " ### ",
            "#    ",
            "#    ",
            " ##  ",
            "   # ",
            "###  "
        ],
    
        'T' : [
            "#####",
            "  #  ",
            "  #  ",
            "  #  ",
            "  #  ",
            "  #  "
        ],
    
        'U' : [
            "#  # ",
            "#  # ",
            "#  # ",
            "#  # ",
            "#  # ",
            " ##  "
        ],
    
        'V' : [
            "#   #",
            "#   #",
            "#   #",
            " # # ",
            " # # ",
            "  #  "
        ],
    
        'W' : [
            "#   #",
            "#   #",
            "# # #",
            "# # #",
            "# # #",
            " # # "
        ],
    
        'X' : [
            "#   #",
            " # # ",
            "  #  ",
            " # # ",
            " # # ",
            "#   #"
        ],
    
        'Y' : [
            "#   #",
            "#   #",
            " # # ",
            "  #  ",
            "  #  ",
            "  #  "
        ],
    
        'Z' : [
            "#### ",
            "   # ",
            "  #  ",
            " #   ",
            "#    ",
            "#### "
        ]
    }