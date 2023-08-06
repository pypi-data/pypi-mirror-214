from HarmonyDecoder.rules import rule_manager
from HarmonyDecoder.function import function, quality
from HarmonyDecoder.scale import scale
from HarmonyDecoder.note import note
from HarmonyDecoder.strdecoder import str_symbol
from HarmonyDecoder.logger import logger
from threading import Thread

class program:
    def __init__(self, logger:logger, input:str = "", tonation:(scale | None) = None, measure_length:int = 1):
        self.measure_length:int = measure_length
        self.__input:str = input

        if input is None:
            self.__input = ""

        self.__tonation:(scale | None) = tonation
        self.rules:rule_manager = rule_manager()
        self.__logger = logger

        self.task:list[str_symbol] = []
        
        if input != "":
            for item in input.split(' '):
                self.task.append(str_symbol(item))

        self.beginning:list[function] = []
        self.solution:tuple[list[function]] = ()

# public:
    def print_solution(self) -> None:
        for item in self.beginning:
            item.print_as_tree()
            print()

    def clear(self) -> None:
        self.__input = ""
        self.task = []
        self.beginning = []
        self.solution = ()

    def solve(self) -> None:
        self.beginning = []
        
        self.__logger.log("Generating all possible results...")

        if self.__tonation is None or self.task == []:
            self.__logger.log("Task is not specified!\n")
            return

        def add_next(func:function, what:(str_symbol | None), index:int, measure_length:int) -> None:
            if what is None:
                func.add_next(None)
                return

            possible_nexts:list[function] = self.rules.str_to_possible_nexts(func, what, self.__tonation, (index + 1) % measure_length, measure_length)

            for possible_next in possible_nexts:
                func.add_next(possible_next)

        def sub_solve(current:function, task:list[str_symbol], index:int, measure_length:int) -> None:
            if index >= len(task):
                add_next(current, None, index, measure_length)
                return
            
            add_next(current, task[index], index, measure_length)

            for item in current.next:
                sub_solve(item, task, index + 1, measure_length)
            
        self.beginning = self.rules.str_to_possible_nexts(None, self.task[0], self.__tonation, 1, self.measure_length)

        for item in self.beginning:
            sub_solve(item, self.task, 1, self.measure_length)

        self.__logger.log("Results generated successfully.\n")

    def get_all_solutions(self) -> list[tuple[function]]:
        self.__logger.log("Converting all solutions...")

        if self.__tonation is None:
            self.__logger.log("Task is not specified!\n")
            return [[]]

        if self.beginning == []:
            return [[]]

        def traverse(func:function) -> list[list[function]]:
            if func is None:
                return [[]]
            
            return [[func] + path for child in func._next for path in traverse(child)]
        
        result:list[tuple[function]] = []

        for item in self.beginning:
            for func in traverse(item):
                result.append(tuple(func))

        self.__logger.log("Results converted successfully.\n")
        self.solution = result
        return result
    
    def evaluate_all_solutions(self) -> dict[tuple[function], float]:
        self.__logger.log("Evaluating results...")

        if self.__tonation is None:
            self.__logger.log(f"Task is not specified!\n")
            return {}

        if self.beginning == []:
            return {}
        
        result:dict[list[function], float] = {}
        solutions:list[tuple[function]] = self.get_all_solutions()

        for solution in solutions:
            current:float = 0.0

            for index in range(1, len(solution)):
                current += quality(solution[index - 1].notes, solution[index].notes)
            
            result[solution] = current

        result = dict(sorted(result.items(), key = lambda x: x[1]))
        self.solution = list(result.keys())        
        self.__logger.log("Results evaluated successfully.\n")
        return result
    
    def set_best_solutions(self) -> None:
        self.__logger.log("Calculating best solutions...")

        if self.__tonation is None or self.task == []:
            self.__logger.log("Task is not specified!\n")
            return

        if self.beginning == []:
            return
        
        all_solutions:dict[tuple[function], float] = self.evaluate_all_solutions()
        help:list[tuple[function]] = []
        current_best:float = 1000.0

        for item in list(all_solutions.keys()):
            to_check:float = all_solutions[item]

            if to_check < current_best:
                current_best = to_check

        for item in list(all_solutions.keys()):
            to_check:float = all_solutions[item]

            if to_check == current_best:
                help.append(item)

        self.__logger.log("Best results calculated successfully.")
        self.__logger.log(f"Best result quality: {current_best}\n.")
        self.solution = tuple(help)

    def add_to_task(self, what:(str_symbol | None)) -> None:
        self.solution = ()
        self.beginning = []
        
        if what is None:
            return

        self.task.append(what)
        self.__input += f" {what.whole}"
        self.__input = self.input.strip()

# private:
    def __get_input(self) -> str:
        return self.__input
    
    def __set_input(self, new_input:str) -> None:        
        self.task = []

        if new_input is None:
            self.__input = ""
            return
        
        self.__input = new_input

        if new_input != "":
            for item in new_input.split(' '):
                self.task.append(str_symbol(item))

    def __get_tonation(self) -> (scale | None):
        return self.__tonation
    
    def __set_tonation(self, new_tonation:(scale | None)) -> None:
        if self.__tonation != new_tonation:
            self.__tonation = new_tonation

            self.beginning = []
            self.solution = ()

    def __get_logger(self) -> logger:
        return self.__logger

# properties:
    input:str = property(__get_input, __set_input)
    tonation:(scale | None) = property(__get_tonation, __set_tonation)
    program_logger:logger = property(__get_logger)


def print_function_list(to_print:list[function]) -> None:
    print("Best solutions:")

    soprano:list[note] = []
    alto:list[note] = []
    tenore:list[note] = []
    bass:list[note] = []

    for func in to_print:
        soprano.append(func.soprano)
        alto.append(func.alto)
        tenore.append(func.tenore)
        bass.append(func.bass)

    for item in soprano:
        print("{0:<5}".format(str(item)), end="")

    print()

    for item in alto:
        print("{0:<5}".format(str(item)), end="")

    print()

    for item in tenore:
        print("{0:<5}".format(str(item)), end="")

    print()

    for item in bass:
        print("{0:<5}".format(str(item)), end="")

    print()

