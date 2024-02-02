
import regex as re
import numpy as np

# 12 red cubes, 13 green cubes, and 14 blue cubes
num_reg = re.compile("(\d+)")
regex_str = [re.compile(f"(\d+) {x}") for x in ["red", "green", "blue"]]
rules = [12,13,14]

def valid_record(record, rules=[]):
    for reg, rule in zip(regex_str, rules):
        a=reg.search(record)
        if a and int(a.group(1)) > rule:
            return False
        # elif rule > 0:
        #     return False
    return True

def get_rgb(record):
    res = []
    for reg, rule in zip(regex_str, rules):
        a=reg.search(record)
        val = int(a.group(1)) if a else 0
        res.append(val)
    return res
            

def main():
  
    #"(\d)+ red", "(\d)+ blue"]
    result = 0
    part2=0
    with open("./src/files/day2.txt", "r") as f:
        for line in f.readlines():
            #print(line.strip())
            game = line.strip().split(":")[0]
            #print(game)
            num_game = int(num_reg.search(game).group(1))
           
            if np.all([valid_record(record, rules= rules) for record in line.strip().split(":")[1].split(";")]):
                result += num_game
                print(f" {line.strip()} -> valid")
            
            rs=[]
            gs = []
            bs = []
            for record in line.strip().split(":")[1].split(";"):
                r = get_rgb(record)
                #print(r, record)
                rs.append(r[0])
                gs.append(r[1])
                bs.append(r[2])
            #print(max(rs),max(bs),max(gs))
            cube_power = max(rs) * max(bs) * max(gs)
            #print(cube_power)
            part2+=cube_power
            # min_b = max(bs)
            # min_g = max(gs)
            # for record in line.strip().split(":")[1].split(";"):
            #     if valid_record(record, rules= rules):
            #         print(f"  {record} -> valid")
                    
              

    print(f"Part 1 res = {result}")
    print(f"Part 2 res = {part2}")


if __name__ == "__main__":
    main()
