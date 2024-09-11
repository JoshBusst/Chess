from numbers import Number



VERBOSE = True



def error(msg: str) -> None:
    print(msg)
    print("Program terminating...")
    exit()

def log(value: any) -> None:
    print(f"DEBUG LOG: {str(value)}")

def cprint(msg: str) -> None:
    if VERBOSE: print(msg)

def odd(num: Number) -> bool:
    return bool(num % 2)

def even(num: Number) -> bool:
    return not (num % 2)

def clip(x: Number, low: Number, high: Number) -> Number:
    return min(max(x, low), high)
