import re

class PassportValidator:
    @staticmethod
    def length(number):
        return len(number) == 9
    
    @staticmethod
    def numeric(number):
        return not number.isdigit()

    @staticmethod
    def validate(number):
        if PassportValidator.length(number) and PassportValidator.numeric(number):
            pattern = r"\b[A-NP-Z]{2}[A-NP-Z0-9]{6}[0-9]\b"
            match = re.match(pattern, number)
            return bool(match)

        return False

validator = PassportValidator()
ispassport = validator.validate
