
def converter(month, day):
    date_string = "%d/%d/2016" % (month, day)
    note_string = "test note for %d/%d" % (month, day)
    return(date_string, note_string)

if __name__ == "__main__":
    print("start")

    results = []

    for day in range(1, 32):
        results.append((converter(1, day)))
    for day in range(1, 30):
        results.append((converter(2, day)))
    for day in range(1, 32):
        results.append((converter(3, day)))
    for day in range(1, 31):
        results.append((converter(4, day)))
    for day in range(1, 32):
        results.append((converter(5, day)))
    for day in range(1, 31):
        results.append((converter(6, day)))
    for day in range(1, 32):
        results.append((converter(7, day)))
    for day in range(1, 32):
        results.append((converter(8, day)))
    for day in range(1, 31):
        results.append((converter(9, day)))
    for day in range(1, 32):
        results.append((converter(10, day)))
    for day in range(1, 31):
        results.append((converter(11, day)))
    for day in range(1, 32):
        results.append((converter(12, day)))

    with open('outfile.dat', 'wt') as out_file:
        for candidate in results:
            buffer = "%s %s\n" % (candidate[0], candidate[1])
            out_file.write(buffer)

print("stop")
