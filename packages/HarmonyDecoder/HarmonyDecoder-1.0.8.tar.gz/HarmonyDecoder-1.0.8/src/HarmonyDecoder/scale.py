from __future__ import annotations

from HarmonyDecoder.note import all_notes

scale_notes : list[str] = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
modes:list[str] = ["minor", "major"]

sharps : list[int] = [3, 0, 4, 1, 5, 2, 6, 3, 0, 4, 1, 5, 2, 6]
flats : list[int] = [6, 2, 5, 1, 4, 0, 3, 6, 2, 5, 1, 4, 0, 3]

sharps_by_major_key : dict[str, int] = {'C' : 0, 'G' : 1, 'D' : 2, 'A' : 3, 'E' : 4, 'B' : 5, 'F#' : 6, 'C#' : 7}
sharps_by_minor_key : dict[str, int] = {'A' : 0, 'E' : 1, 'B' : 2, 'F#' : 3, 'C#' : 4, 'G#' : 5, 'D#' : 6, 'A#' : 7}
flats_by_major_key : dict[str, int] = {'C' : 0, 'F' : 1, 'Bb' : 2, 'Eb' : 3, 'Ab' : 4, 'Db' : 5, 'Gb' : 6, 'Cb' : 7}
flats_by_minor_key : dict[str, int] = {'A' : 0, 'D' : 1, 'G' : 2, 'C' : 3, 'F' : 4, 'Bb' : 5, 'Eb' : 6, 'Ab' : 7}

class scale:
    def __init__(self, root:str, mode:str):
        if root not in list(all_notes.keys()):
            raise ValueError("Note does not exist")
        
        if mode not in modes:
            raise ValueError(f"Invalid mode. Modes of a scale: {modes}")

        self.__notes:list[str] = []
        self.__mode:str = mode        

        sharps = 0; flats = 0

        if mode == "major":
            if root in list(flats_by_major_key.keys()): 
                flats = flats_by_major_key[root]
            elif root in list(sharps_by_major_key.keys()): 
                sharps = sharps_by_major_key[root]
            else:
                raise ValueError(f"Tonation {root} {mode} not found")
        else:
            if root in list(flats_by_minor_key.keys()): 
                flats = flats_by_minor_key[root]
            elif root in list(sharps_by_minor_key.keys()):
                sharps = sharps_by_minor_key[root]
            else:
                raise ValueError(f"Tonation {root} {mode} not found")
        
        self.__notes = self.__create_scale(root, sharps, flats)     

    def __str__(self): return f"{self.__get_name()} {self.__get_mode()}"
    def __repr__(self): return f"{self.__get_name()} {self.__get_mode()}"
    def __getitem__(self, index : int) -> str: return self.__notes[index % len(self.__notes)]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, scale):
            return other.name == self.name and other.__mode == self.__mode
        else:
            raise TypeError()
        
    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def copy(self) -> scale:
        return scale(self.name, self.mode)

# private:
    def __get_name(self) -> str:
        return self.__notes[0]
    
    def __get_mode(self) -> str:
        return self.__mode
    
    def __get_notes(self) -> list[str]:
        return self.__notes
    
    def __set_mode(self, value:str) -> None:
        if value not in ['minor', 'major']:
            raise ValueError("Only [minor, major] modes are available.")

    @staticmethod
    def __add_signs_to_scale(sign_count, sign, result) -> None:
        for i in range(sign_count):
            if sign == '#': to_find:str = scale_notes[sharps[i]]
            elif sign == 'b': to_find:str = scale_notes[flats[i]]
            else: raise ValueError("Only [#, b] chromatic signs are avaiable")

            j = 0
            while j < len(result) and result[j] != to_find:
                j += 1

            result[j] += sign

    @staticmethod
    def __create_scale(first_note:str, sharp_count:int = 0, flat_count:int=0) -> list[str]:
        if sharp_count != 0 and flat_count != 0:
            raise ValueError("Scale cannot have sharps and flats simultainously")
        
        result : list[str] = []

        start_index : int = scale_notes.index(first_note[0])
        length = len(scale_notes)

        for i in range(length):
            index = (start_index + i) % length
            result.append(scale_notes[index])

        if sharp_count != 0: scale.__add_signs_to_scale(sharp_count, '#', result)
        elif flat_count != 0: scale.__add_signs_to_scale(flat_count, 'b', result)

        return result            

# properties:
    name:str = property(__get_name, doc="Name of this scale.")
    mode:str = property(__get_mode, __set_mode, doc="Mode of this scale.")
    notes:list[str] = property(__get_notes, doc="Notes in this scale")