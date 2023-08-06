from __future__ import annotations

import abc

from HarmonyDecoder.function import *
from HarmonyDecoder.possiblenotes import possible_notes
from HarmonyDecoder.scale import scale

class rule_manager:
    def __init__(self):
        self._active_rules:list[rule] = [
            voice_crossing(),
            parallel_fifth(),
            parallel_octave(),
            one_direction(),
            seventh_down(),
            third_up(),
            ninth_down(),
            fifth_on_one(),
            ninth_as_root()
        ]

        self.__rules:list[rule] = self._active_rules.copy()

# public:
    def activate_rule(self, name:str) -> None: self.__set_rule_state(name, True)
    def deactivate_rule(self, name:str) -> None: self.__set_rule_state(name, False)    

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        for r in self._active_rules:
            if not r.check_if_fulfilled(function1, function2):
                return False
            
        return True
    
    def str_to_possible_nexts(self, prev:(function | None), symbol:str_symbol, tonation_param:scale, beat:int, measure_length:int) -> list[function]:
        result:list[function] = []
        
        if 'm' in symbol.symbol and tonation_param.mode == 'major':
            tonation:scale = scale(tonation_param.name, 'minor')
        elif 'm' not in symbol.symbol and tonation_param.mode == 'minor':
            tonation:scale = scale(tonation_param.name, 'major')
        else:
            tonation:scale = tonation_param.copy()

        octave:int = 4

        root_index:int = symbol_degree[symbol.symbol]
        root:note = note(tonation[root_index], octave, ROOT_ROLE)
        third:note = note(tonation[root_index + 2], octave, THIRD_ROLE)
        fifth:note = note(tonation[root_index + 4], octave, FIFTH_ROLE)
        sixth:note = note(tonation[root_index + 5], octave, SIXTH_ROLE)
        seventh:note = note(tonation[root_index + 6], octave, SEVENTH_ROLE)
        ninth:note = note(tonation[root_index + 8], octave, NINTH_ROLE)
        
        candidate_notes:possible_notes = possible_notes([[root, third, fifth, sixth, seventh, ninth]])

        if '6>' not in symbol.added_notes and '6' not in symbol.added_notes:
            candidate_notes.remove(sixth)

        if '9>' not in symbol.added_notes and '9' not in symbol.added_notes and '9<' not in symbol.added_notes:
            if '7>' not in symbol.added_notes and '7' not in symbol.added_notes and '7<' not in symbol.added_notes:
                candidate_notes.remove(seventh)

            candidate_notes.remove(ninth)

        if symbol.deleted_note == 1:
            candidate_notes.remove(root)
        elif symbol.deleted_note == 5:
            candidate_notes.remove(fifth)

        if symbol.alterations is not None:
            for component in symbol.alterations.keys():
                match component:
                    case '1':
                        candidate_notes.remove(root)
                        copy:note = root
                    case '3' | '3>':
                        candidate_notes.remove(third)
                        copy:note = third
                    case '5':
                        candidate_notes.remove(fifth)
                        copy:note = fifth
                
                for signs in symbol.alterations[component]:
                    copy = copy.copy()

                    for sign in signs:
                        if sign == '#':
                            copy.add_sharp()
                        else:
                            copy.add_flat()
                            
                    if len(candidate_notes[0]) >= 4:
                        try: 
                            candidate_notes.remove(fifth)                        
                        except ValueError:
                            pass
                    
                        if len(candidate_notes[0]) >= 4:
                            try:
                                candidate_notes.remove(root)
                            except ValueError:
                                pass

                    candidate_notes.append(copy)                
        
        if len(candidate_notes[0]) < 4:
            if symbol.root == symbol.position:
                if symbol.position == 1:
                    candidate_notes.append(root)
                elif symbol.position == 5:
                    candidate_notes.append(fifth)
                elif symbol.position == 7:
                    candidate_notes.append(seventh)

            if len(candidate_notes[0]) < 4:
                if symbol.deleted_note != 5:
                    candidate_notes.append_to_copy(0, fifth)

                if '7>' in symbol.added_notes or '7' in symbol.added_notes or '7<' in symbol.added_notes: 
                    candidate_notes.append_to_copy(0, seventh)   

                if symbol.deleted_note != 1:
                    candidate_notes.append_to(0, root)

        for item in candidate_notes.notes:
            if len(item) < 4:
                candidate_notes.notes.remove(item)

        perms:list[list[note]] = candidate_notes.permutations()

        for item in perms:            
            match symbol.position:
                case 1:
                    if not item[3].is_root():
                        continue
                case 3:
                    if not item[3].is_third():
                        continue  
                case 5:
                    if not item[3].is_fifth():
                        continue
                case 7:
                    if not item[3].is_seventh():
                        continue
                case 9:
                    if not item[3].is_ninth():
                        continue
                case None:
                    pass

            match symbol.root:
                case 1:
                    if not item[0].is_root():
                        continue
                case 3:
                    if not item[0].is_third():
                        continue  
                case 5:
                    if not item[0].is_fifth():
                        continue
                case 7:
                    if not item[0].is_seventh():
                        continue
                case None:
                    pass

            if prev is not None:
                set_octave_to_closest(item[0], prev.bass)
                set_octave_to_closest(item[1], prev.tenore)
                set_octave_to_closest(item[2], prev.alto)
                set_octave_to_closest(item[3], prev.soprano)             

            for i in range(3):
                while item[i] > item[i + 1]:
                    item[i + 1].octave += 1
            
            to_append:function = function(symbol.symbol, prev, item, beat, measure_length)
            
            if self.check_if_fulfilled(prev, to_append):
                result.append(to_append)

        return result
    
# private:
    def __set_rule_state(self, name:str, state : bool) -> None:
        for rule in self.__rules:
            if name == rule.__class__.__name__:
                rule.active = state
                break

        self._active_rules.clear()

        for rule in self.__rules:
            if rule.active:
                self._active_rules.append(rule) 


    def __get_active_rules(self) -> list[rule]:
        return self._active_rules

# properties:
    active_rules:list[rule] = property(__get_active_rules)


class rule(abc.ABC):
    def __init__(self, description:str="Sume rule.", active:bool=True):
        self._description:str = description
        self._active:str = active

    def __str__(self) -> str: return self.__class__.__name__
    def __repr__(self) -> str: return self.__class__.__name__
    
# public:
    @abc.abstractmethod
    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        ...    

# private:
    def __get_active(self) -> bool:
        return self._active
    
    def __get_description(self) -> str:
        return self._description
    
    def __set_active(self, new_active:bool) -> None:
        if new_active is None:
            self._active = False

        self._active = new_active

# properties:
    active:bool = property(__get_active, __set_active)
    description:str = property(__get_description)


class voice_crossing(rule):
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        if function2.bass > function1.tenore:
            function2.bass.octave -= 1
        
        if function2.tenore > function1.alto or function2.alto > function1.soprano:
            return False
        
        if function2.tenore < function1.bass or function2.alto < function1.tenore or function2.soprano < function1.alto:
            return False
        
        return True


class parallel_fifth(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        notes_1:list[note] = [function1.bass, function1.tenore, function1.alto, function1.soprano]
        notes_2:list[note] = [function2.bass, function2.tenore, function2.alto, function2.soprano]

        for i in range(4):
            for j in range(i + 1, 4):
                semitones_1:int = semitones_between(notes_1[i], notes_1[j])
                semitones_2:int = semitones_between(notes_2[i], notes_2[j])

                if semitones_1 == 7 and semitones_2 == 7:
                    return False
                
        return True


class parallel_octave(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        notes_1:list[note] = [function1.bass, function1.tenore, function1.alto, function1.soprano]
        notes_2:list[note] = [function2.bass, function2.tenore, function2.alto, function2.soprano]

        for i in range(4):
            for j in range(i + 1, 4):
                semitones_1:int = semitones_between(notes_1[i], notes_1[j])
                semitones_2:int = semitones_between(notes_2[i], notes_2[j])

                if semitones_1 == 0 and semitones_2 == 0 and notes_1[i].name != notes_2[i].name:
                    return False
                
        return True


class one_direction(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        count_lower:int = 0
        count_higher:int = 0

        for index in range(4):
            if function2.notes[index] > function1.notes[index]:
                count_higher += 1
            elif function2.notes[index] < function1.notes[index]:
                count_lower += 1

        if count_higher == 4 or count_lower == 4:
            return False

        return True


class seventh_down(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        for index in range(4):
            if function1.notes[index].is_seventh():
                if semitones_between(function1.notes[index], function2.notes[index]) > 2:
                    return False

        return True


class third_up(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None or function1.symbol[0] != 'D':
            return True
        
        for index in range(4):
            if function1.notes[index].is_third():
                if semitones_between(function1.notes[index], function2.notes[index]) > 1:
                    return False
        
        return True


class sixth_up(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        for index in range(4):
            if function1.notes[index].is_sixth():
                if not function2.notes[index].is_third():
                    return False
        
        return True


class ninth_down(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None or function2 is None:
            return True
        
        for index in range(4):
            if function1.notes[index].is_ninth():
                if not function2.notes[index].is_fifth():
                    return False
        
        return True


class fifth_on_one(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None and function2 is None:
            return True
        
        if function2 is None:
            if function1.bass.is_fifth() and function1.beat == 1:
                return False
                  
        if function2.bass.is_fifth() and function2.beat == 1:
            return False
            
        return True


class ninth_as_root(rule): 
    def __init__(self, description:str="Sume rule.", active:bool=True):
        rule.__init__(self, description, active)

    def check_if_fulfilled(self, function1:(function | None), function2:(function | None)) -> bool:
        if function1 is None and function2 is None:
            return True

        if function2 is None:
            if function1.bass.is_ninth():
                return False
              
        if function2.bass.is_ninth():
            return False
            
        return True