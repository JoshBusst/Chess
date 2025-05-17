
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




class PSL_mouse:
    '''
    Cases:
     - ldown on sq1: piecehover
        . LUP on sq1: square selected
        . LUP on sq2: attemptmove sq1 to sq2
        . rdown/RUP/mdown/MUP: deselectall
     - rdown on sq1: none
        . RUP on sq1: highlight sq1
        . RUP on sq2: drawarrow
        . ldown/LUP/mdown/MUP: deselectall
     - mdown/MUP: deselectall
     - release outside game window: deselectall
    
    attemptmove: affirm a piece is on sq1, it can move legally to sq2, and then move it. Else deselectall
    piecehover: attach piece graphic to mouse pointer
    deselectall: deselects all squares and removes piece hover
    drawarrow: draws arrow pointing from sq1 to sq2
    '''

    BUTTONS = {'mouse': ('lup','ldown','mup','mdown','rup','rdown')}



    def __init__(self, triggerMultiple=True) -> None:
        # update sequences to be dict as will be more readable ie sequences['onclick'], sequences['sequence'] instead of list indices which are :(
        self.sequences: list[list[str], callable, callable] = []
        self.activeSequence: list[str] = []
        self.prev: tuple[bool] = (0,0,0)
        self.partialsData: dict[int, any] = {}

    def validSequence(self, sequence: list[str]):
        if not isinstance(sequence, list):
            return False
        
        for entry in sequence:
            if entry not in self.BUTTONS['mouse']:
                return False
            
        return True

    def addSequence(self, sequence: list[str], activation: callable, onclick: callable=None) -> None:
        if self.validSequence(sequence):
            self.sequences.append([sequence, activation, onclick])
        else:
            error(f"Sequence addition is invalid! Sequence must be of type list[str] and have values within:\n{self.BUTTONS['mouse']}...")
        
    def clearSequence(self) -> None:
        self.activeSequence.clear()
        self.partialsData.clear()
        self.prev = (0,0,0)

    def getButtonStr(self, buttonsPressed: tuple[bool]) -> str:
        # determine the button that triggered this interrupt
        triggerButton: tuple[bool] = tuple([buttonsPressed[i] != self.prev[i] for i in range(3)])

        ind: int = triggerButton.index(True)
        tButtonState: bool = buttonsPressed[ind]

        return self.BUTTONS['mouse'][2*ind + int(tButtonState)]

    def addClick(self, buttonsPressed: tuple[bool]) -> None:
        if buttonsPressed == self.prev: # if held or released twice consecutively. Negates mouse scroll wheel triggers
            self.clearSequence()
            return

        triggerButtonStr: str = self.getButtonStr(buttonsPressed)
        self.activeSequence.append(triggerButtonStr)

        self.match()
        self.prev = buttonsPressed

    def deletePartialData(self, partial_ID: int) -> None:
        if partial_ID in self.partialsData.keys():
            del self.partialsData[partial_ID]

    def storePartialData(self, partial_ID: int, data: any) -> None:
        if partial_ID in self.partialsData.keys():
            self.partialsData[partial_ID].append(data)
        else:
            self.partialsData[partial_ID] = [data]

    def handleOnclick(self, partial_ID: int) -> None:
        cprint(f"Full or partial match found! Handling onclick")
        onclick: callable = self.sequences[partial_ID][2]

        if onclick != None:
            cprint("  Onclick command found! Executing")
            self.storePartialData(partial_ID, onclick())
                
    def match(self) -> None:
        reset = True

        for i, [sequence, activation, _] in enumerate(self.sequences):
            overSize: bool = len(self.activeSequence) > len(sequence)

            if overSize:
                self.deletePartialData(i)
                continue

            maxSize: int = min(len(sequence), len(self.activeSequence))
            partialMatch: bool = len(self.activeSequence) < len(sequence)
            match: bool = all([sequence[i] == self.activeSequence[i] for i in range(maxSize)])

            if match:
                self.handleOnclick(i)

                if partialMatch:
                    reset = False
                else:
                    quit: bool = True

                    if i in self.partialsData.keys():
                        quit = activation(self.partialsData[i])
                    else:
                        quit = activation()

                    # ensure integrity of the reset varaible
                    if isinstance(quit, bool) and quit:
                        reset = True
                        break

        if reset: self.clearSequence()



def getUserInput(validInputs: list[str], startMsg: str, errorMsg: str='') -> str:
    if errorMsg == '': errorMsg = f"*Please select a valid option from {validInputs}."
    
    print(startMsg)
    data: str = input("").lower()

    while data not in validInputs:
        print(errorMsg)
        data = input("").lower()

    return data