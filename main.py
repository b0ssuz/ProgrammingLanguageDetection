import sys
import string
from subprocess import call
import matplotlib.pyplot as plt

EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
DEBUG: bool = True


def main()->int:
    lang_guess = detect_language("samples/rust")
    print(f"samples/rust: {lang_guess}")
    lang_guess = detect_language("samples/c")
    print(f"samples/c: {lang_guess}")
    lang_guess = detect_language("samples/cpp")
    print(f"samples/cpp: {lang_guess}")
    lang_guess = detect_language("samples/go")
    print(f"samples/go: {lang_guess}")

    return EXIT_SUCCESS

def debug(msg: str)->None:
    '''Function for debug messages'''
    if DEBUG == True:
        print(f"DEBUG: {msg}")


def detect_language(binary_file: bytes)->str:
    ''' Guesses programming language of given binary'''

    if DEBUG:
        call(["strip", binary_file])

    patterns = {
            "c": [["printf","libc.so"], 0],
            "rust": [["rustc","rust",".rs"], 0],
            "c++": [["libstdc++.so","libgcc_s.so"], 0],
            "go": [["fmt.Println", "malloc.go","fmt"], 0]
            }

    string_list = strings(binary_file,1)

    pattern_found = False

    for c in string_list:
        for key in patterns:
            for index in range(len(patterns[key][0])):
                if patterns[key][0][index] in c:
                    patterns[key][1] +=1
                    pattern_found = True

    debug(patterns)

    max_count, max_key = 0, None 

    for key in patterns:
        if patterns[key][1] >= max_count:
            max_count, max_key = patterns[key][1], key

    ### start plotting
    plt.bar([key for key in patterns],[patterns[key][1] for key in patterns])
    plt.show()
    #### end plotting

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
