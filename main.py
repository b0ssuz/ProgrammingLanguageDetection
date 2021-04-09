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


'''
stichproben machen
regex?
rustc -> trustcert (problem)

nach ada programmiersprache suchen (Verwendung in der luftfahrt)

vortrag:

false positives
warum thema interessant/wichtig
related work
was wurde gemacht
problem?->lösung
evaluation (verhältnis verschiedener programmiersprachen in firmware)
zusammenfassung (eigene arbeit -> was gibt es schon -> was muss noch gemacht werden (weitere programmiersprachen hinzufügen?))


code am ende als .zip schicken mit schriftlichem berricht (bis 09.04.2021 23:59)
'''

def main()->int:
    '''Main'''

    stats = {
                "C": 0,
                "C++": 0,
                "RUST": 0,
                "GO": 0,
                "COULD NOT DETECT PROGRAMMING LANGUAGE": 0,
                "NOT ELF": 0
            }

    paths = Path("/usr/bin/").glob('*')
    
    #paths = Path("samples/").glob('*')


    for path in paths:
        try:
            tmp_detection = detect_language(path)
            stats[tmp_detection] += 1
            print(f"{path} {tmp_detection}")
        except:
            continue

    print(stats)

    return EXIT_SUCCESS

def debug(msg: str)->None:
    '''Function for debug messages'''

    if DEBUG == True:
        print(f"DEBUG: {msg}")

def is_elf_file(file: str)->bool:
    '''Checks if a given file is an elf file'''

    with open(file, mode="rb") as f:
        return f.read(4).decode("UTF-8") == '\x7fELF'

def detect_language(binary_file: bytes)->str:
    ''' Guesses programming language of given binary'''

    if not is_elf_file(binary_file):
        #print(f"{binary_file} is not an ELF file")
        return "NOT ELF"

    if STRIP:
        call(["strip", binary_file])

    patterns = {
            "C": [
                [("printf", 5)], 
                0
                ],
            "RUST": [
                [("rustc",5),("rust",1),(".rs",5)], 
                0
                ],
            "C++": [
                [("libstdc++.so",50),("libgcc_s.so",5)], 
                0
                ],
            "GO": [
                [("fmt.Println", 10), ("malloc.go",30),("fmt.", 1)]
                , 0
                ]
            }

    string_list = strings(binary_file,1)
    #debug(string_list)
    pattern_found = False

    '''
    for c in string_list:
        for key in patterns:
            for index in range(len(patterns[key][0])):
                if patterns[key][0][index] in c:
                    if patterns[key][0][index] == "libstdc++.so":
                        patterns[key][1] += 10
                        continue

                    patterns[key][1] += 1
                    pattern_found = True
    '''

    for key in patterns:
        for pattern in patterns[key][0]:
            for string in string_list:
                if pattern[0] in string:
                    patterns[key][1] += pattern[1]
                    pattern_found = True
                    debug(string)
                
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
    '''strings implementation in python'''

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
