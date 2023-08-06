import sys


def albhed(text: str) -> str:
    cha_english = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cha_albhed = "ypltavkrezgmshubxncdijfqowYPLTAVKREZGMSHUBXNCDIJFQOW"
    return text.translate(str.maketrans(cha_english, cha_albhed))


def cli() -> str:
    print(albhed(" ".join(sys.argv[1:])))
