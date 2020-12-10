from os  import popen, system, path, listdir
from sys import argv, exit
from re  import search, findall, sub

DEFAULT_EDITOR = "/usr/bin/vi"

GREEN = u"\u001b[32;1m"
BLUE = u"\u001b[34m"
RESET_ALL = u"\u001b[0m"

def disable_color():
    global GREEN
    global BLUE
    global RESET_ALL

    GREEN = ""
    BLUE = ""
    RESET_ALL = ""

def default_editor(path):
    system(f"{DEFAULT_EDITOR} '{path}'")

def default_index_input():
    return input("index: ")


class Finder(object):

    COMMAND = ""
    RESULT = []
    index = 0
    BREAK = ""

    def __init__(self, excludes:list=[]):
        self.COMMAND = " ".join([f"| grep -v \"{i}\"" for i in excludes])

    def find(self, index_input=default_index_input, editor=default_editor):
        command_reader = popen(self.COMMAND)
        try:
            while (_file:=command_reader.readline()[:-1]):
                self.process_result(_file)
        except KeyboardInterrupt:
            print(self.BREAK)
        finally:
            return self.result_behaviour(index_input=index_input,
                                         editor=editor)

    def result_behaviour(self, index_input, editor):
        try:
            index = index_input()
            if index.isdigit():
                index = int(index)
                if index in range(len(self.RESULT)):
                    editor(self.RESULT[index])
        except (KeyboardInterrupt, EOFError):
            print(self.BREAK)
        finally:
            return 0

    def process_result(self, value):
        print(value)

class FindByContent(Finder):

    def __init__(self, regex:str, excludes:list=[]):
        super().__init__(excludes=excludes)

        self.COMMAND = "find . -type f " + self.COMMAND
        self.__regex = regex

    def process_result(self, value):
        lines = open(value, encoding="latin1").read().split("\n")
        for num_line, line in enumerate(lines):
            result = search(f".{{0,9}}{self.__regex}.{{0,9}}", line)
            if result:
                print(f"[{self.index:>3}] linenum: {num_line+1} " +
                      f"of {GREEN+value+RESET_ALL}: " +
                      f"{BLUE}... {result.group()} ...{RESET_ALL}")
                self.RESULT.append(value)
                self.index += 1


class FindByName(Finder):

    def __init__(self, regex, excludes:list=[]):
        self.COMMAND = f"find . -type f | grep -P \"{regex}\"" + self.COMMAND
        self.__regex = regex

    def process_result(self, value):
        result = sub(f"({self.__regex})",BLUE+r"\1"+GREEN,value)
        print(f'[{self.index:>3}] {GREEN+result+RESET_ALL}')
        self.RESULT.append(value)
        self.index += 1


def main(args):
    # define it for using this code for vim ext
    somethings = None

    if args[0] == "n":
        somethings = FindByName(args[1], args[2]).find()

    elif args[0] == "c":
        somethings = FindByContent(args[1], args[2]).find()

    return somethings

if __name__ == "__main__":
    args = []
    if argv.__len__() == 1:
        print("Finder was written by Shanenoi!")
        exit(0)

    args.append(argv[1])
    args.append([])

    for ele in argv[2:]:
        if ele == "-v":
            args.append([])
            continue
        if ele:
            args[-1].append(ele)
    
    args[1] = " ".join(args[1])
    args.append([])
    main(args)
