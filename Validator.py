class Validator:
    @staticmethod
    def validate_number(x) -> bool:
        if x.isdigit():
            return True
        elif x == "":
            return True
        else:
            return False
