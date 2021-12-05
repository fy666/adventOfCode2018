package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func convertList(data []string) []int {
	converted := make([]int, 0, len(data))
	for _, val := range data {
		tmp, e := strconv.Atoi(val)
		if e == nil {
			converted = append(converted, tmp)
		}
	}
	return converted
}

func countItems(data map[[2]int]int) (counter int) {
	for _, j := range data {
		if j >= 2 {
			counter += 1
		}
	}
	return
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day5.txt"
	if *test {
		fileName = "day5_test.txt"
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

	used_positions := make(map[[2]int]int)
	used_positions_part2 := make(map[[2]int]int)
	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), " -> ")
		first_coord := convertList(strings.Split(txt[0], ","))
		second_coord := convertList(strings.Split(txt[1], ","))
		var first, second [2]int
		for c := 0; c <= 1; c++ {
			if first_coord[c] < second_coord[c] {
				first[c] = first_coord[c]
				second[c] = second_coord[c]
			} else {
				first[c] = second_coord[c]
				second[c] = first_coord[c]
			}
		}
		num.Linspace(first_coord[0], first_coord[1], abs(first_coord[0]-first_coord[1])+1)

		if first[0] == second[0] || first[1] == second[1] {
			fmt.Println("From", first, "to", second)
			for ix := first[0]; ix <= second[0]; ix++ {
				for iy := first[1]; iy <= second[1]; iy++ {
					var pos [2]int
					pos[0] = ix
					pos[1] = iy
					//fmt.Printf("%d,%d;", ix, iy)
					used_positions[pos] += 1
					used_positions_part2[pos] += 1
				}
			}
			//fmt.Printf("\n")

		} else {
			// Diagonal
			delta := second[0] - first[0]
			sign_first := 1
			sign_second := 1
			if second_coord[0]-first_coord[0] < 0 {
				sign_first = -1
			}
			if second_coord[1]-first_coord[1] < 0 {
				sign_second = -1
			}
			fmt.Println("From", first_coord, "to", second_coord, "delta =", delta)
			for ix := 0; ix <= delta; ix++ {
				var pos [2]int
				pos[0] = first_coord[0] + sign_first*ix
				pos[1] = first_coord[1] + sign_second*ix
				fmt.Printf("%d,%d;", pos[0], pos[1])
				used_positions_part2[pos] += 1
			}
			fmt.Printf("\n")
		}

	}

	fmt.Println("First part:", countItems(used_positions))
	fmt.Println("Second part:", countItems(used_positions_part2))
}
