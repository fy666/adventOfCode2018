#!python3


count = 0
count_esc = 0
with open('./data/test8.txt', 'r') as file:
    for line in file:
        count += len(line.strip())
        count_esc += len(eval(line))
        #print("{} : {}, unescaped {}".format(line.strip(), len(line.strip()), len(eval(line))))

print("TEST : Total {}: unescaped {}, result {}".format(
    count, count_esc, count-count_esc))


count = 0
count_esc = 0
with open('./data/input8.txt', 'r') as file:
    for line in file:
        count += len(line.strip())
        count_esc += len(eval(line.strip()))
        #print("{} : {}, unescaped {}".format(line.strip(), len(line.strip()), len(eval(line))))

print("FINAL Total : unescaped {}, result {}".format(count_esc, count-count_esc))
