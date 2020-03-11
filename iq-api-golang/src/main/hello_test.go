package main

import "testing"

func HelloPuppy() string {
	return "Hello, Cute puppy :)"
}

func TestHelloPuppy(t *testing.T) {
	expected := "Hello, Cute puppy :)"
	if actual := HelloPuppy(); actual != expected {
		t.Errorf("Expect - %v, but got - %v", expected, actual)
	}
}
