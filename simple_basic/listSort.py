a = [43, 26, 3, 5]

b=  ["dog", "cat", "DOG", "CAT"]

# a.sort()

# sorted will create a new list
print(sorted(a))

a.sort(reverse=True)
print(a)
# case insensitive 
print(sorted(b, key=str.lower))

b.sort(key=str.lower,reverse=True)
print(b)