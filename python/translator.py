import sys 

class BrailleTranslator: 

    def __init__(self, input):
        # Mappings from Braille to English
        self.braille_alpha = {
            "O.....": "a",
            "O.O...": "b",
            "OO....": "c",
            "OO.O..": "d",
            "O..O..": "e",
            "OOO...": "f",
            "OOOO..": "g",
            "O.OO..": "h",
            ".OO...": "i",
            ".OOO..": "j",
            "O...O.": "k",
            "O.O.O.": "l",
            "OO..O.": "m",
            "OO.OO.": "n",
            "O..OO.": "o",
            "OOO.O.": "p",
            "OOOOO.": "q",
            "O.OOO.": "r",
            ".OO.O.": "s",
            ".OOOO.": "t",
            "O...OO": "u",
            "O.O.OO": "v",
            ".OOO.O": "w",
            "OO..OO": "x",
            "OO.OOO": "y",
            "O..OOO": "z",
            ".....O": "capital follows",
            ".O.OOO": "number follows",
            "......": "space"
        }

        self.braille_nums = {
            "O.....": "1",
            "O.O...": "2",
            "OO....": "3",
            "OO.O..": "4",
            "O..O..": "5",
            "OOO...": "6",
            "OOOO..": "7",
            "O.OO..": "8",
            ".OO...": "9",
            ".OOO..": "0",
        }

        # Special Braille indicators for capitalization and numbers
        self.special_braille_characters = {
            "capital follows": ".....O",  
            "number follows": ".O.OOO"  
        }

        # Reverse mapping for English to Braille
        self.english_alpha = {v: k for k, v in self.braille_alpha.items() if v not in self.special_braille_characters.values()}
        self.reverse_braille_numbers = {v: k for k, v in self.braille_nums.items()}

        self.input = input
        self.lang = self.detect_lang(input)

    def detect_lang(self, input):
        if set(input).issubset({'O', '.'}):  # Braille uses only 'O' and '.'
            return 'braille'
        return 'english'
    
    def translate(self):
        if self.lang == 'braille':
            return self.translate_to_english()
        return self.translate_to_braille()
    
    def translate_to_english(self):
        text = []
        is_next_number = False
        is_next_capital = False

        braille_chars = [self.input[i:i+6] for i in range(0, len(self.input), 6)]

        for braille_char in braille_chars:

            # Handle capitalization
            if braille_char == self.special_braille_characters["capital follows"]:
                is_next_capital = True
                continue

            # Handle numbers
            elif braille_char == self.special_braille_characters["number follows"]:
                is_next_number = True
                continue

            # Handle spaces
            elif braille_char == self.special_braille_characters["space"]:
                text.append(" ")
                is_next_capital = False
                is_next_number = False
                continue

            if is_next_number:
                if braille_char in self.braille_nums:
                    text.append(self.braille_nums[braille_char])
                is_next_number = False 
            else:
                if braille_char in self.braille_alpha:
                    letter = self.braille_alpha[braille_char]
                    if is_next_capital:
                        letter = letter.upper()
                    text.append(letter)
                is_next_capital = False 
        
        return "".join(text)
    
    def translate_to_braille(self):
        text = []
        is_next_number = False

        for char in self.input:
            if char.isdigit():  # If it's a digit, switch to number mode
                if not is_next_number:
                    text.append(self.special_braille_characters['number follows'])
                    is_next_number = True
                text.append(self.reverse_braille_numbers[char])
            elif char.isalpha():  # If it's an alphabetic character
                if is_next_number:
                    is_next_number = False  # Reset number mode after a number block
                if char.isupper():
                    text.append(self.special_braille_characters['capital follows'])
                    text.append(self.english_alpha[char.lower()])
                else:
                    text.append(self.english_alpha[char.lower()])
            elif char == ' ':  # Handle spaces
                text.append('......')
                is_next_number = False  # Reset number mode on space

        return ''.join(text)

def main():
    if len(sys.argv) > 1: 
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = input("Enter Braille or English: ")
    
    translator = BrailleTranslator(input_text)
    result = translator.translate()
    print(f"{result}")

if __name__ == "__main__":
    main()