symbol_degree : dict[str, int] = {
    "T" : 0, "mT" : 0,
    "Sii" : 1, "mSii" : 1,
    "Tiii" : 2, "mTiii" : 2, "Diii" : 2, "mDiii" : 2,
    "S" : 3, "mS" : 3,
    "D" : 4, "mD" : 4,
    "Tvi" : 5, "mTvi" : 5, "Svi" : 5, "mSvi" : 5,
    "Dvii" : 6, "mDvii" : 6, "Svii" : 6, "mSvii" : 6
}

#region syntax: 
# Symbol^Position/Root+Added notes+-Deleted notes-*alteration*=suspention= eg mTiii^3/5+7<+--*5#,1b*==, T^/++-5-**==
# Symbol must be from symbol_degree.keys()
# Position must be from [1, 3, 5, 7]
# Root must be from [1, 3, 5, 7] and for alterated or sixth/seventh/ninth chords with all notes it must be different from Position, it may implicit doubled note
# Added notes are just additional interval symbols, it may implicit doubled note
# Deleted notes must be from [x1, x5]
# Alteration consists of two parts: <note><alteration>, eg. 7#, 5b, 3bb, 1#, number of alterations may implicit doubled note
# Suspended notes are in form =[from_1, to_1],[from_2, to_2],...=, eg =6 to 5,4 to 3= is suspension 64 to 53
#endregion
class str_symbol:
    def __init__(self, whole:str) -> None:
        if whole is None:
            raise ValueError("Whole symbol cannot be None!")

        try:
            self.__whole:str = whole
            self.__symbol:str = self.__read_symbol()
            self.__position:(int | None) = self.__read_position()
            self.__root:(int | None) = self.__read_root()
            self.__deleted_note:(int | None) = self.__read_deleted_note()
            self.__added_notes:(list[str]) = self.__read_added_notes()            
            self.__alterations:(dict[str, list[str]]) = self.__read_alterations()
            self.__suspentions:(list[tuple[str, str]]) = self.__read_suspensions()
        except ValueError as ve:
            print("Invalid function symbol syntax.")
            print("Details: ", ve.args)

    def __str__(self) -> str: return self.__whole
    def __repr__(self) -> str: return f"Symbol: {self.__symbol},\n\
        Position: {self.__position},\n\
        Root: {self.__root},\n\
        Added notes: {self.__added_notes},\n\
        Deleted notes: {self.__deleted_note},\n\
        Alterations: {self.__alterations},\n\
        Suspensions: {self.__suspentions}"

#private:
    def __get_whole(self) -> str:
        return self.__whole
    
    def __get_symbol(self) -> str:
        return self.__symbol
    
    def __get_position(self) -> (int | None):
        return self.__position
    
    def __get_root(self) -> (int | None):
        return self.__root
    
    def __get_added_notes(self) -> (list[str] | None):
        return self.__added_notes
    
    def __get_deleted_note(self) -> (int | None):
        return self.__deleted_note
    
    def __get_alterations(self) -> (dict[str, list[str]] | None):
        return self.__alterations
    
    def __get_suspensions(self) -> (list[tuple[str, str]] | None):
        return self.__suspentions

    def __read_symbol(self) -> str:
        index:int = 0
        buffer:str = ""

        while index < len(self.__whole) and self.__whole[index] != "^":
            buffer += self.__whole[index]
            index += 1

        if buffer in symbol_degree.keys():
            return buffer
        else:
            raise ValueError("Invalid function symbol")

    def __read_position(self) -> (int | None):
        index:int = 0
        
        while self.__whole[index] != '^': 
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")
            
        index += 1

        if index >= len(self.__whole) or self.__whole[index] == "/": return None
        else: return int(self.__whole[index])

    def __read_root(self) -> (int | None):
        index:int = 0
        
        while self.__whole[index] != '/': 
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")
            
        index += 1

        if index >= len(self.__whole) or self.__whole[index] == "+": return None
        else: return int(self.__whole[index])

    def __read_added_notes(self) -> (list[str] | None):
        index:int = 0
        buffer:str = ""

        while self.__whole[index] != '+': 
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")
        index += 1        

        while self.__whole[index] != '+':
            buffer += self.whole[index]
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")

        if len(buffer.strip()) > 0 and self.__position == self.__root and self.__position is not None and self.__deleted_note is not None:
            raise ValueError("Cannot add dissonant notes when there are some doubled ones.")

        result:list[str] = buffer.split(',')

        if len(result) > 2:
            raise ValueError("Cannot add more than 2 dissonant notes at once.")        
        elif result == ['']:
            return []
        
        for item in result:
            if item[0] not in ['6', '7', '9']:
                raise ValueError("Cannot add other notes than versions of [6, 7, 9].")
            
            if item[0] == '9':
                self.__deleted_note = 5
            
            item = item.strip()

        return result
    
    def __read_deleted_note(self) -> (int | None):
        index:int = 0
        buffer:str = ""

        while self.__whole[index] != '-':
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")
            
        index += 1

        while self.__whole[index] != '-':
            buffer += self.__whole[index]
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")

        if len(buffer) > 1:
            raise ValueError("Cannot delete more than 1 note.")

        str_result:str = buffer.strip()

        if str_result == "": 
            return None        
            
        if str_result not in ['1', '5']: 
            raise ValueError("Only root and fifth of the function can be deleted.")

        result = int(str_result)

        if self.__position == result or self.__root == result: 
            raise ValueError("Function cannot have position or root same as deleted note.")

        return result
    
    def __read_alterations(self) -> (dict[str, list[str]] | None):
        index:int = 0
        buffer:str = ""
        result:dict[str, list[str]] = {}

        while self.__whole[index] != '*':
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")
            
        index += 1

        while self.__whole[index] != '*':
            buffer += self.__whole[index]
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")

        if buffer == "":
            return {}

        list_buffer:list[str] = buffer.split(',')

        for item in list_buffer:
            item = item.strip()

            if item[0] not in ['1', '3', '5']:
                raise ValueError("Only root, third and fifth can get additionaly altered.")

            if item[0] not in result.keys():
                result[item[0]] = []

            result[item[0]].append(item[1:])

            if len(result[item[0]]) > 2:
                raise ValueError("Cannot alterate one component more than 2 times.")

        if len(result.keys()) > 4:
            raise ValueError("Maximum of 4 notes can be altered.")

        return result

    def __read_suspensions(self) -> (list[tuple[str, str]] | None):
        index:int = 0
        buffer:str = ""

        while self.__whole[index] != '=':
            index += 1

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")
            
        index += 1

        while self.__whole[index] != '=':
            index += 1
            buffer += self.whole[index]

            if index == len(self.__whole):
                raise ValueError("Invalid syntax.")

        if buffer == "":
            return []
        
        individual_suspensions:list[str] = buffer.split(',')
        result:list[tuple[str, str]] = []

        for item in individual_suspensions:
            to_check:tuple = item.split(" to ")

            if len(to_check) != 2:
                raise ValueError("Suspension consists of 2 parts - suspension and resolution.")
            
            result.append()

        if len(result) > 4:
            raise ValueError("Maximum of 4 suspensions is allowed.")

        return result

#properties:
    whole:str = property(__get_whole, doc="Whole symbol function")
    symbol:str = property(__get_symbol, doc="Function's symbol")
    position:(int | None) = property(__get_position, doc="Function's position")
    root:(int | None) = property(__get_root, doc="Function's root")
    added_notes:(list[str]) = property(__get_added_notes, doc="Function's added notes")
    deleted_note:(int | None) = property(__get_deleted_note, doc="Fuction's deleted notes")
    alterations:(dict[str, list[str]]) = property(__get_alterations, doc="Function's alterations")
    suspensions:(list[tuple[str, str]]) = property(__get_suspensions, doc="Function's suspensions")
