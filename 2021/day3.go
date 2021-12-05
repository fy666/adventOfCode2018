package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

// Iterate on a string list and count char value at given position
// If sortMostOccurences is true, it returns 1 if the more recurrent value is 1 (else 0)
// It returns the opposite if sortMostOccurences is false
func getBitCriteria(data []string, position int, sortMostOccurences bool) byte {
	var count float32 = 0.0
	var size float32 = float32(len(data))
	for _, val := range data {
		count += float32(val[position]) - 48
	}
	if count >= size/2 && sortMostOccurences || count < size/2 && !sortMostOccurences {
		return '1'
	}
	return '0'
}

func filter(data []string, f func(string) bool) []string {
	filtered := make([]string, 0, len(data))
	for _, v := range data {
		if f(v) {
			filtered = append(filtered, v)
		}
	}
	return filtered
}

func firstPart(data []string) (sum int) {
	result := ""
	neg_result := ""
	for i := 0; i < len(data[0]); i++ {
		result += string(getBitCriteria(data, i, true))
		neg_result += string(getBitCriteria(data, i, false))
	}

	gamma, _ := strconv.ParseInt(result, 2, 64)
	epsilon, _ := strconv.ParseInt(neg_result, 2, 64)
	fmt.Println("Epsilon = ", epsilon, "gamma = ", gamma)
	sum = int(epsilon * gamma)
	return
}

func getCodeThatFitsCriteria(data []string, sortMostOccurences bool) string {
	filtered_data := data
	position := 0
	for len(filtered_data) > 1 {
		criteria := getBitCriteria(filtered_data, position, sortMostOccurences)
		localSearchFunction := func(b string) bool {
			if b[position] == criteria {
				return true
			}
			return false
		}
		filtered_data = filter(filtered_data, localSearchFunction)
		//fmt.Println("Position", position, ", filtered", filtered_data)
		position += 1
	}
	return filtered_data[0]
}

func secondPart(data []string) (sum int) {
	oxygen, _ := strconv.ParseInt(getCodeThatFitsCriteria(data, true), 2, 64)
	co2, _ := strconv.ParseInt(getCodeThatFitsCriteria(data, false), 2, 64)

	sum = int(oxygen * co2)
	fmt.Println("Oxygen rating = ", oxygen, ", CO2 rating = ", co2)
	return
}

func main() {
	file, err := os.Open("day3.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	data := make([]string, 0, 50) // create empty slice with capacity of 50+

	for scanner.Scan() {
		data = append(data, scanner.Text())
	}
	first := firstPart(data)
	second := secondPart(data)
	fmt.Printf("First answer: %d, second answer: %d\n", first, second)
}
