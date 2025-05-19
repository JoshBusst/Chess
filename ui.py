
from lib import cprint, error




MOUSE_BUTTONS = {'mouse': ('lup','ldown','mup','mdown','rup','rdown')}


prev_click: tuple[bool] = (False, False, False)


def getMouseButtonStr(buttons: tuple[bool]):
    global prev_click

    if buttons == prev_click: return

    triggerButton: tuple[bool] = tuple([buttons[i] != prev_click[i] for i in range(3)])
    
    ind: int = triggerButton.index(True)
    tButtonState: bool = buttons[ind]

    prev_click = buttons

    return MOUSE_BUTTONS['mouse'][2*ind + int(tButtonState)]



def getUserInput(validInputs: list[str], startMsg: str, errorMsg: str='') -> str:
    if errorMsg == '': errorMsg = f"*Please select a valid option from {validInputs}."
    
    print(startMsg)
    data: str = input("").lower()

    while data not in validInputs:
        print(errorMsg)
        data = input("").lower()

    return data