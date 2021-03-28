import sys
import string
from subprocess import call
import matplotlib.pyplot as plt
import re
from pathlib import Path

EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
DEBUG: bool = False
STRIP: bool = False
SHOW_GRAPH: bool = False


def main()->int:

    stats = {
                "C": 0,
                "C++": 0,
                "RUST": 0,
                "GO": 0,
                "OTHER/FAIL": 0
            }

    paths = Path("/usr/bin/").glob('*')

    for path in paths:
        try:
            stats[testing(path)] += 1
        except:
            print("TEST FAILED")

    debug("\n\n\nFINISHED !!!!")
    debug(stats)

    return EXIT_SUCCESS

def testing(path: str)->str:
    print(f"{path} {detect_language(path)}")
    return detect_language(path)

def debug(msg: str)->None:
    '''Function for debug messages'''
    if DEBUG == True:
        print(f"DEBUG: {msg}")


def detect_language(binary_file: bytes)->str:
    ''' Guesses programming language of given binary'''

    if STRIP:
        call(["strip", binary_file])

    patterns = {
            "C": [["printf"], 0],
            "RUST": [["rustc","rust",".rs"], 0],
            "C++": [["libstdc++.so",r"libgcc_s.so"], 0],
            "GO": [["fmt.Println", "malloc.go","fmt."], 0]
            }

    string_list = strings(binary_file,1)
    debug(string_list)

    pattern_found = False

    for c in string_list:
        for key in patterns:
            for index in range(len(patterns[key][0])):
                if patterns[key][0][index] in c:
                    if patterns[key][0][index] == "libstdc++.so":
                        patterns[key][1] += 10
                        continue
                    patterns[key][1] += 1
                    pattern_found = True

    debug(patterns)

    max_count, max_key = 0, None 

    for key in patterns:
        if patterns[key][1] >= max_count:
            max_count, max_key = patterns[key][1], key

    if SHOW_GRAPH:
        plt.title(f"I THINK {binary_file} IS WRITTEN IN {max_key}")
        plt.bar([key for key in patterns],[patterns[key][1] for key in patterns])
        plt.show()

    if pattern_found:
        return max_key
    else:
        return "COULD NOT DETECT PROGRAMMING LANGUAGE"


def strings(binary_file: bytes, min: int, max: int = float("inf"))->list[str]:
    with open(binary_file,errors="ignore") as bf:
        results = []
        result = ""
        for c in bf.read():
            if c in string.printable:
                result += c
                continue

            if len(result) >= min and len(result) <= max:
                    results.append(result)
            result = ""
        if len(result) >= min and len(result <= max):
            results.append(result)
    return results

if __name__=="__main__":
    sys.exit(main())
