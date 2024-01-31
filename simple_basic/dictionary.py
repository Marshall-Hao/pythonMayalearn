d= {}

d = {"red":255, "green":255, "blue":255}

print(d.get("red"))
print(d.get("yellow"))

if "red" in d:
    print(d["red"])
    
print(d.keys())
print(type(d.keys()))
d["yellow"] = 255
print(d)

print(d.items())
for item in d.items():
    print(f"{item[0]}:{item[1]}")