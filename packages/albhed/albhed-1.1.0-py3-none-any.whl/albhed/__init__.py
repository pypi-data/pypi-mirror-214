class AlBhed:
    def __init__(self, text: str) -> None:
        self.cha_english = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.cha_albhed = "ypltavkrezgmshubxncdijfqowYPLTAVKREZGMSHUBXNCDIJFQOW"
        self.text = text

    def translate(self) -> str:
        return self.text.translate(str.maketrans(self.cha_english, self.cha_albhed))

    def revert(self) -> str:
        return self.text.translate(str.maketrans(self.cha_albhed, self.cha_english))
