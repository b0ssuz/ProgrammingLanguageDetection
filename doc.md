---
title: Programming Language Detection
subtitle: Bünyamin Sarikaya
lang: de
---

```python
def foo(bar):
	print(bar)
```

# Brain Storming

- readelf -h <file> 
	- getting information about binary files
- strip <file>
	- removes symboles that are not in the binarys symbol-table

# Methode

- Relevante Sprachen: Rust, C, C++, GO

- Binary strippen
- Merkmale in Binary finden
- Merkmale in Binarys gewichten
- Guess mit höchstem Gewicht ausgeben
