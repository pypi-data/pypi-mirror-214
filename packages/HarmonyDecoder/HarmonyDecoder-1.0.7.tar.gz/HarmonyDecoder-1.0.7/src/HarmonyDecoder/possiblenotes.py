from HarmonyDecoder.note import note
from itertools import permutations

class possible_notes():
    def __init__(self, initializer_list:list[list[note]]=[[]]) -> None:
        self.__notes:list[list[note]] = initializer_list
        self.__max_length:int = 4

    def __len__(self) -> int: return len(self.__notes)
    def __getitem__(self, index:int) -> list[note]: return self.__notes[index]
    def __str__(self) -> str: return str(self.notes)
    def __repr__(self) -> str: return repr(self.notes)    

# public:
    def min_length(self) -> int:
        min = len(self.__notes[0])
        
        for item in self.__notes:
            if len(item) < min:
                min = len(item)

        return min

    def append(self, what:note) -> None:
        for item in self.__notes:
            if len(item) < self.__max_length:
                item.append(what.copy())
            else:
                print(f"Cannot append {what} to {item} - cell is full.")

    def append_to(self, index:int, what:note) -> None:
        if index >= len(self.__notes):
            raise IndexError("possible_notes index out of range.")
        
        if len(self.__notes[index]) < self.__max_length:
            self.__notes[index].append(what.copy())

    def append_to_copy(self, index:int, what:note) -> None:
        if index >= len(self.__notes):
            raise IndexError("possible_notes index out of range.")
        
        if len(self.__notes[index]) >= 4:
            print(f"Cannot append {what} to {self.__notes[index]} - cell is full.")
        else:   
            self.__notes.insert(index + 1, self.__notes[index].copy())
            self.__notes[index + 1].append(what.copy())        

    def remove(self, what:note) -> None:
        for item in self.__notes:
            try: 
                item.remove(what)
            except ValueError:
                print(f"Could not remove note {what} from {item}.")

    def remove_from(self, index:int, what:note) -> None:
        if index >= len(self.__notes):
            raise IndexError("possible_notes index out of range.")
        
        try:
            self.__notes[index].remove(what)
        except ValueError:
            print(f"Could not remove note {what} from {self.__notes[index]}.")

    def set_note(self, what:str, to:str) -> None:
        for help_list in self.__notes:
            for item in help_list:
                if item.name == what:
                    item.name = to
                    break

    def permutations(self) -> list[list[note]]:
        result:list[list[note]] = []
        buffer:list[list[note]] = []

        for item in self.__notes:
            perm = list(permutations(item))

            for x in perm:
                copied:list[note] = []

                for y in x:
                    copied.append(y.copy())

                buffer.append(copied)

        for item in buffer:
            if item not in result:
                result.append(item)

        return result

# private:
    def __get_notes(self) -> list[list[note]]: return self.__notes

# properties:
    notes:list[list[note]] = property(__get_notes, doc="List of all possible versions of notes in function.")