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

func countItems(data []int, valueToFind int) (counter int) {
	for _, j := range data {
		if j == valueToFind {
			counter += 1
		}
	}
	return
}

func countAllItems(fishs map[int]int) int {
	counter := 0
	for _, val := range fishs {
		counter += val
	}
	return counter
}

func find(data []int, searched int) bool {
	for _, val := range data {
		if val == searched {
			return true
		}
	}
	return false
}

func reproduce(fishs *map[int]int) {
	new_fish_to_add := (*fishs)[0]
	for ix := 0; ix <= 8; ix++ {
		(*fishs)[ix] = (*fishs)[ix+1]
	}

	(*fishs)[6] += new_fish_to_add
	(*fishs)[8] = new_fish_to_add

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
	fileName := "day6.txt"
	if *test {
		fileName = "day6_test.txt"
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

	data := make([]int, 0, 50) // create empty slice with capacity of 50+
	for scanner.Scan() {
		data = convertList(strings.Split(scanner.Text(), ","))
	}
	fmt.Println(len(data), "lanternfish found")

	lanternfish_counter := make(map[int]int)
	for ix := 0; ix <= 8; ix++ {
		lanternfish_counter[ix] = countItems(data, ix)
	}
	fmt.Println("Lanternfish first population is", lanternfish_counter)
	fmt.Println(countAllItems(lanternfish_counter), "lanternfishes")
	for ix := 0; ix < 256; ix++ {
		reproduce(&lanternfish_counter)
		if ix == 79 {
			fmt.Println("Lanternfish population after 80 days is", countAllItems(lanternfish_counter))
		}
	}
	fmt.Println("Lanternfish population after 256 days is", countAllItems(lanternfish_counter))
	//fmt.Println(countAllItems(lanternfish_counter), "lanternfishes")

}
