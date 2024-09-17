from numbers import Number
import pygame as p


VERBOSE = False



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

def loadImage(imagePath: str, size: tuple[int]=(100,100)) -> p.Surface:
    return p.transform.scale(p.image.load(imagePath), size)

# makes colour1 appear more like colour2 by a percentage defined by opacity
def blendColours(colour1: tuple, colour2: tuple, opacity: float=0.5) -> tuple:
    return (int((1 - opacity) * colour1[0] + opacity * colour2[0]),  # R component
            int((1 - opacity) * colour1[1] + opacity * colour2[1]),  # G component
            int((1 - opacity) * colour1[2] + opacity * colour2[2]),   # B component
    )
