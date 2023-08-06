from __future__ import annotations

from HarmonyDecoder.note import *
from HarmonyDecoder.interval import *
from HarmonyDecoder.strdecoder import *

def quality(notes1:list[note], notes2:list[note]) -> float:
    result:int = 0

    for index in range(4):
        result += semitones_between(notes1[index], notes2[index])

    return result / 4.0

class function: 
    def __init__(self, symbol:str, prev, notes:list[note], beat:int, measure_length:int): 
        self._symbol:str = symbol
        self._prev:function = prev
        self._beat:int = beat
        self._measure_length:int = measure_length

        self._next:list[function] = []
        self._notes:list[note] = notes

        self._sixth:(note | None) = None
        self._seventh:(note | None) = None
        self._ninth:(note | None) = None      

        for item in self._notes:
            if item.role == SIXTH_ROLE:
                self._sixth = item
            elif item.role == SEVENTH_ROLE:
                self._seventh = item
            elif item.role == NINTH_ROLE:
                self._ninth = item  

        self._soprano:note = notes[3]
        self._alto:note = notes[2]
        self._tenore:note = notes[1]
        self._bass:note = notes[0]

    def __len__(self) -> int: return len(self._notes)
    def __str__(self) -> str: return self._symbol
    def __repr__(self) -> str: return f"{self._symbol}({self._bass}, {self._tenore}, {self._alto}, {self._soprano})"

# public:
    def add_note(self, note:note) -> None:
        if len(self._notes) >= 4:
            print("Cannot add more than 4 notes to function.")
        else:
            self._notes.append(note)

    def add_next(self, func) -> None:
        self._next.append(func)

    def remove_next(self, func) -> None:
        try:
            self._next.remove(func)
        except ValueError:
            print("Function not present in next.")

    def print_as_tree(self, spaces:int = 0) -> None:
        print(' ' * spaces, repr(self))

        for item in self._next:
            if item is not None:
                item.print_as_tree(spaces + 5)    

# private:
    def __get_notes(self) -> list[note]: return self._notes
    def __get_next(self) -> (list | None): return self._next
    def __get_symbol(self) -> str: return self._symbol
    def __get_prev(self): return self._prev
    def __get_beat(self) -> int: return self._beat
    def __get_measure_length(self) -> int: return self._measure_length

    def __set_prev(self, value): self._prev = value

    def __get_soprano(self) -> note: return self._soprano
    def __get_alto(self) -> note: return self._alto
    def __get_tenore(self) -> note: return self._tenore
    def __get_bass(self) -> note: return self._bass

    def __set_soprano(self, value : note) -> None:
        if value is None: raise ValueError("Note cannot be NoneType")
        else: self._soprano = value

    def __set_alto(self, value : note) -> None:
        if value is None: raise ValueError("Note cannot be NoneType")
        else: self._alto = value

    def __set_tenore(self, value : note) -> None:
        if value is None: raise ValueError("Note cannot be NoneType")
        else: self._tenore = value

    def __set_bass(self, value : note) -> None:
        if value is None: raise ValueError("Note cannot be NoneType")
        else: self._bass = value

# properties:
    symbol:str_symbol = property(__get_symbol, doc="Function symbol.")
    notes:list[note] = property(__get_notes, doc="Notes of the function, without any particular order.")
    next:list[function] = property(__get_next, doc="All functions that can be as next.")
    prev:function = property(__get_prev, __set_prev, doc="Previous function, might be none.")
    beat:int = property(__get_beat, doc="Beat in bar, on which the function is.")
    measure_length:int = property(__get_measure_length, doc="Length of bar, that the function belongs to.")

    soprano:note = property(__get_soprano, __set_soprano, doc="Soprano note.")
    alto:note = property(__get_alto, __set_alto, doc="Anto note.")
    tenore:note = property(__get_tenore, __set_tenore, doc="Tenore note.")
    bass:note = property(__get_bass, __set_bass, doc="Bass note.")