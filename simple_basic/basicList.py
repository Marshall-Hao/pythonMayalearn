a = []

b = [1, 2, 3, 4, 5]

c = ["a", "b", "c", "d", "e"]

d = [3.14, "asd" , [1, 2, 3]]

a.append(1)
print(a)

b.extend(c)
print(b)

b.extend("100")
print(b)

b.insert(0, "oop")
print(b)


b.remove("oop")
print(b)

b.pop(1)
print(b)