class BSNValidator:
    @classmethod
    def length(cls, number):
        return len(number) == 9
    
    @classmethod
    def numeric(cls, number):
        return number.isdigit()

    @staticmethod
    def validate(number):
        if BSNValidator.length(number) and BSNValidator.numeric(number):
            digits = [int(n) for n in number]

            # Calculate the checksum
            checksum = 0
            for i, digit in enumerate(digits[:-1]):
                weighted_digit = (9 - i) * digit
                checksum += weighted_digit

            remainder = checksum % 11
            last_digit = digits[-1]
            is_bsn = remainder - last_digit

            if is_bsn == 0:
                return True

        return False

validator = BSNValidator()
isbsn = validator.validate
