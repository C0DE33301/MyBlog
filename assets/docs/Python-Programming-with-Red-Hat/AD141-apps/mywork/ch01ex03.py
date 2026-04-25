#!/usr/bin/env python3

original = input("Please enter a string: ")
print(original.endswith("."))
print(original.isalpha())
print("x" in original)

modified = original.replace("e", "E")
print(modified)
