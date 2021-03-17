from main import *

def test_detect_language()->None:
    assert detect_language("samples/rust") == "rust"
    assert detect_language("samples/c") == "c"
    assert detect_language("samples/cpp") == "c++"
    assert detect_language("samples/go") == "go"

def test_strings():
    assert len(strings("samples/go", 4)[0]) >= 4
    assert len(strings("samples/go", 4,6)[0]) in [4,5,6]
    assert len(strings("samples/go", 5,5)[0]) == 5


if __name__=="__main__":
    sys.exit(main)
