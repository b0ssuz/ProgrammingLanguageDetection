make:
	clang samples/sample.c -o samples/c
	g++ samples/sample.cpp -o samples/cpp
	rustc samples/sample.rs -o samples/rust
	go build -o samples/go samples/sample.go
clean:
	rm doc.pdf
	rm samples/go
	rm samples/rust
	rm samples/cpp
	rm samples/c
run:
	python main.py
test:
	pytest tests.py
pdf:
	pandoc -V geometry:margin=1in -o doc.pdf *.md
