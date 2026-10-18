errors = 0
with open("data/sample.log") as f:
    for line in f:                       # read one line at a time
        status = line.split()[-1]        # split on spaces, take the LAST field
        if status[0] in "5":            # first digit is 4 or 5 -> error
            errors += 1
print("errors:", errors)