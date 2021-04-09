from main import *

def test_detect_language()->None:
    assert detect_language("samples/rust") == "RUST"
    assert detect_language("samples/c") == "C"
    assert detect_language("samples/cpp") == "C++"
    assert detect_language("samples/go") == "GO"
    assert detect_language("samples/sample.c") == "NOT ELF"

def test_strings():
    assert len(strings("samples/go", 4)[0]) >= 4
    assert len(strings("samples/go", 4,10)[0]) in list(range(4,10))

if __name__=="__main__":
    sys.exit(main)
