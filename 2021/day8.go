package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func SortString(w string) string {
	s := strings.Split(w, "")
	sort.Strings(s)
	return strings.Join(s, "")
}

func SContains(input string, reference string) bool {
	for ix := 0; ix < len(reference); ix++ {
		if !strings.Contains(input, reference[ix:ix+1]) {
			return false
		}
	}
	return true
}

func decode(data []string) map[string]int {
	code := make(map[int]string)
	decoded := make(map[string]int)
	tmp_size6 := make([]string, 0, 3)
	tmp_size5 := make([]string, 0, 3)

	for _, val := range data {
		size := len(val)
		switch size {
		case 2:
			code[1] = val
		case 3:
			code[7] = val
		case 4:
			code[4] = val
		case 7:
			code[8] = val
		case 6:
			tmp_size6 = append(tmp_size6, val)
		case 5:
			tmp_size5 = append(tmp_size5, val)
		}
	}

	for _, val := range tmp_size6 {
		if !SContains(val, code[1]) {
			code[6] = val
		} else if !SContains(val, code[4]) {
			code[0] = val
		} else {
			code[9] = val
		}
	}

	for _, val := range tmp_size5 {
		if SContains(val, code[1]) {
			code[3] = val
		} else if SContains(code[9], val) {
			code[5] = val
		} else {
			code[2] = val
		}
	}

	for key, val := range code {
		decoded[SortString(val)] = key
	}
	return decoded
}

// Count number of 1,4, 7 or 8
func countSpecialDigits(data []string) int {
	count := 0
	for _, val := range data {
		size := len(val)
		if size == 2 || size == 3 || size == 4 || size == 7 {
			count += 1
		}
	}
	return count
}

func convertList(data []string) []int {
	converted := make([]int, 0, len(data))
	for _, val := range data {
		tmp, e := strconv.Atoi(val)
		if e == nil {
			converted = append(converted, tmp)
		} else {
			fmt.Println("Error with ", val)
		}
	}
	return converted
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day8.txt"
	if *test {
		fileName = "day8_test.txt"
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

	specialDigitsCounter := 0
	big_count := 0
	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), " | ")
		data := strings.Split(txt[1], " ")
		specialDigitsCounter += countSpecialDigits(data)
		this_code := decode(strings.Split(txt[0], " "))
		output := 0
		for ix, out := range data {
			//fmt.Println(out, " is ", this_code[SortString(out)], "pos = ", ix)
			output += this_code[SortString(out)] * int(math.Pow(10, float64(3-ix)))
		}
		big_count += output
	}
	fmt.Println("Special digits in output = ", specialDigitsCounter)
	fmt.Println("Sum of all outputs = ", big_count)
}
