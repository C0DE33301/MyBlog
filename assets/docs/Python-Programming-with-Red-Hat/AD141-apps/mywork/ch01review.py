#!/usr/bin/env python3

visitor = input("What is your name? ").capitalize()

print(f"Hello, {visitor}!")

age = int(input(f"What is your age, {visitor}? "))

roundyears = 10 - (age % 10)

print("So in {0} years you will b {1}!".format(roundyears, age + roundyears))

print("(friendly hint: {0} in hexadecimal is {1})".format(age + roundyears, hex(age + roundyears)))
