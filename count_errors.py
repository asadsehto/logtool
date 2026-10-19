errors = 0
with open("data/sample.log") as f:
    for line in f:                       # read one line at a time
        field = line.split()
        status = field[-1]               # split on spaces, take the LAST field
        if status[0] in "45":            # first digit is 4 or 5 -> error
            errors += 1
            print(f"IP: {field[1]}, Code: {status}")
print(f"Total errors: {errors}")

print("Numbers from 0 to 4:")
for i in range(5):
    print(i)