#!/usr/bin/env python3

astring = input("Please enter some text: ")

firstchar = astring[0]
num_of_first = astring.count(firstchar)
print("First character '{0}' occurs in the text {1} times.".format(firstchar, num_of_first))

print("Last character '{0}' occurs in the text {1} times.".format(astring[-1], astring.count(astring[-1])))
