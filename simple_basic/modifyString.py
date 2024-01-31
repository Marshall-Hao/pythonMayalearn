s1="this is a test"
# the og string is immutable

s2 = "p" + s1[1:]

print(s2)
# replace creates a new string
print(s1.replace("t", "p"))

