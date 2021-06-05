SOURCES=$(wildcard [a-z]*.py)
TARGETS=$(SOURCES:%.py=%.svg)

.PHONY: default
default: build

.PHONY: build
build: $(TARGETS)

%.svg: %.py
	PYTHONPATH=.. python $< > $@

clean:
	-rm $(TARGETS)