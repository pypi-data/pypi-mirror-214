all_notes:dict[str, int] = {        
        'C' : 0,    'Dbb' : 0,  'B#' : 0,
        'C#' : 1,   'Db' : 1,   'B##' : 1,
        'D' : 2,    'Ebb' : 2,  'C##' : 2,
        'D#' : 3,   'Eb' : 3,   'Fbb' : 3,
        'E' : 4,    'Fb' : 4,   'D##' : 4,
        'F' : 5,    'Gbb' : 5,  'E#' : 5,
        'F#' : 6,   'Gb' : 6,   'E##' : 6,
        'G' : 7,   'Abb' : 7, 'F##' : 7,
        'G#': 8,   'Ab' : 8,
        'A' : 9,    'Bbb' : 9,  'G##' : 9,
        'A#' : 10,   'Bb' : 10,   'Cbb' : 10,
        'B' : 11,    'Cb': 11,    'A##' : 11,
    }

ROOT_ROLE = "Root"
THIRD_ROLE = "Third"
FIFTH_ROLE = "Fifth"
SIXTH_ROLE = "Sixth"
SEVENTH_ROLE = "Seventh"
NINTH_ROLE = "Ninth"

class note:
    # Dictionary of all notes and their distance from note 'A' (in semitones)
    def __init__(self, name:str, octave:str, role:(str | None)=None):
        self.__name:str = name
        self.__octave:int = octave
        self.__role:(str | None) = role

    def __gt__(self, other: object) -> bool: 
        if isinstance(other, note):
            return self.determinant() > other.determinant()
        else:
            raise TypeError()
    
    def __lt__(self, other: object) -> bool: 
        if isinstance(other, note):
            return self.determinant() < other.determinant()
        else:
            raise TypeError()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, note):
            return self.determinant() == other.determinant()
        else:
            return False

    def __ge__(self, other: object) -> bool:
        return self == other or self > other
    
    def __le__(self, other: object) -> bool:
        return self == other or self < other
    
    def __ne__(self, other: object) -> bool:
        return not(self == other)
    
    def __str__(self):
        return f"{self.name}{self.octave}"
    
    def __repr__(self):
        return f"({self.name}{self.octave}, {self.__role})"

# public:
    def determinant(self) -> int: return (self.octave * 12) + all_notes[self.name]

    def is_root(self) -> bool: return self.__role == ROOT_ROLE
    def is_third(self) -> bool: return self.__role == THIRD_ROLE
    def is_fifth(self) -> bool: return self.__role == FIFTH_ROLE
    def is_sixth(self) -> bool: return self.__role == SIXTH_ROLE
    def is_seventh(self) -> bool: return self.__role == SEVENTH_ROLE
    def is_ninth(self) -> bool: return self.__role == NINTH_ROLE
    def has_role(self) -> bool: return self.__role is not None
    
    def add_flat(self) -> None:
        if len(self.name) == 3: return

        if len(self.name) > 1:
            if self.name[:-1] == '#': self.name = self.name[:-1]
            else: self.name += 'b'
        else: self.name += 'b'

    def add_sharp(self) -> None: 
        if len(self.name) == 3: return

        if len(self.name) > 1:
            if self.name[:-1] == 'b': self.name = self.name[:-1]
            else: self.name += '#'
        else: self.name += '#'

    def copy(self):
        return note(self.__name, self.__octave, self.__role)

# private:
    def __get_name(self) -> str: return self.__name
    def __get_octave(self) -> int: return self.__octave
    def __get_role(self) -> str: return self.__role

    def __set_name(self, value:str) -> None: self.__name = value
    def __set_octave(self, value:int) -> None:
        if value < 0: raise ValueError("Octave number should not be negative")        
        else: self.__octave = value

    name = property(__get_name, __set_name)
    octave = property(__get_octave, __set_octave)
    role = property(__get_role)