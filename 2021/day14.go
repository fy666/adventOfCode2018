package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

func countPoints(polymer string) (res int) {
	max := 0
	min := len(polymer)
	for _, p := range polymer {
		occ := strings.Count(polymer, string(p))
		if occ > max {
			max = occ
		}
		if occ < min {
			min = occ
		}
	}
	//fmt.Println(": most occuring = ", max, "least occuring = ", min)
	return max - min
}

func expand(polymer string, rules map[string]string) string {
	var b bytes.Buffer
	for ix := 0; ix < len(polymer)-1; ix++ {
		b.WriteString(string(polymer[ix]))
		if val, ok := rules[polymer[ix:ix+2]]; ok {
			b.WriteString(val)
			//do something here
		}
	}
	b.WriteString(string(polymer[len(polymer)-1]))
	return b.String()
}

func concatenate(s []string) (res string) {
	for ix := 0; ix < len(s); ix++ {
		if ix == len(s)-1 {
			res += s[ix]
		} else {
			res += s[ix][:len(s[ix])-1]
		}
	}
	return
}

func createPairs(polymer string) map[string]int {
	result := make(map[string]int)
	for ix := 0; ix < len(polymer)-1; ix++ {
		result[polymer[ix:ix+2]] += 1
	}
	return result
}

func expandSmarter(polymer string, rules *map[string]string, keys *[]string) string {
	output := make([]string, 0, 3)
	//debug_output := make([]string, 0, 3)
	//fmt.Println("Treating", polymer, ",", len(*keys), "keys")
	for ix := len(*keys) - 1; ix >= 0; ix-- {
		pos := strings.Index(polymer, (*keys)[ix])
		if pos != -1 {
			if polymer == (*keys)[ix] {
				//fmt.Println("Exact match, input = ", polymer, "output=", (*rules)[(*keys)[ix]])
				return (*rules)[(*keys)[ix]]
			}
			if pos != 0 {
				output = append(output, expandSmarter(polymer[:pos+1], rules, keys))
			}
			output = append(output, (*rules)[(*keys)[ix]])
			if pos+len((*keys)[ix]) != len(polymer) {
				output = append(output, expandSmarter(polymer[pos+len((*keys)[ix])-1:], rules, keys))
			}
			result := concatenate(output)
			(*keys) = append((*keys), polymer)
			(*rules)[polymer] = result
			//fmt.Println("Concatenating input = ", polymer, "output=", result, "vec=", output)
			return result
		}
	}
	return polymer
}

func expandGenius(polymer map[string]int, rules map[string]string) map[string]int {
	result := make(map[string]int)
	for key, val := range polymer {
		if rule, ok := rules[key]; ok {
			result[key[:1]+rule] += val
			result[rule+key[1:2]] += val
		} else {
			result[key] += val
		}
	}
	return result
}

func getLength(polymer map[string]int) int {
	total := 0
	for _, val := range polymer {
		total += val
	}
	total += 1
	return total
}

func countPointsWithPairs(polymer map[string]int, original string) (res int) {
	max := 0
	min := getLength(polymer)
	accumulate := make(map[string]int)
	for key, val := range polymer {
		accumulate[key[:1]] += val
		accumulate[key[1:2]] += val
	}

	accumulate[original[:1]] += 1                            // First char was not counted twice
	accumulate[original[len(original)-1:len(original)]] += 1 // First char was not counted twice
	for _, val := range accumulate {
		if val < min {
			min = val
		} else if val > max {
			max = val
		}
	}
	return (max - min) / 2
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day14.txt"
	if *test {
		fileName = "day14_test.txt"
	}
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	rules_old := make(map[string]string)
	rules := make(map[string]string)
	keys := make([]string, 0, 50)
	scanner.Scan()
	polymer := scanner.Text()
	scanner.Scan()
	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), " -> ")
		rules_old[txt[0]] = txt[1]
		rules[txt[0]] = txt[0][0:1] + txt[1] + txt[0][1:]
		keys = append(keys, txt[0])
	}

	firstPolymer := polymer
	for step := 0; step < 10; step++ {
		firstPolymer = expandSmarter(firstPolymer, &rules, &keys)
		sort.Slice(keys, func(i, j int) bool {
			return len(keys[i]) < len(keys[j])
		})
		//fmt.Println("For step", step+1, "size =", len(polymer),"points =", countPoints(polymer)
	}
	fmt.Println("For 10th step: size =", len(firstPolymer), " points =", countPoints(firstPolymer))

	fmt.Println("******* GENIUS ************")
	polymer_pairs := createPairs(polymer)
	for step := 0; step < 40; step++ {
		polymer_pairs = expandGenius(polymer_pairs, rules_old)
		if step == 9 {
			fmt.Println("For 10th step: size =", getLength(polymer_pairs), "points = ", countPointsWithPairs(polymer_pairs, polymer))
		}
		//fmt.Println("For step", step+1, "size =", getLength(polymer_pairs), "points = ", countPointsWithPairs(polymer_pairs, polymer))
	}
	fmt.Println("For 40th step: size =", getLength(polymer_pairs), "points = ", countPointsWithPairs(polymer_pairs, polymer))
}
