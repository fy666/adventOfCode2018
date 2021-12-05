package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func countDecreasing(data []int) int {
	counter := 0
	previous_val := 0
	first := true
	for _, val := range data {
		if first {
			first = false
			previous_val = val
		} else {
			if previous_val < val {
				counter += 1
			}
			previous_val = val
		}
	}
	fmt.Printf("Counter = %d\n", counter)
	return counter
}

func sum(data []int) (sum int) {
	for _, val := range data {
		sum += val
	}
	return
}

func main() {
	file, err := os.Open("day1.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	data := make([]int, 0, 50) // create empty slice with capacity of 50
	fmt.Printf("Data len: %d, cap:%d\n", len(data), cap(data))

	for scanner.Scan() {
		//fmt.Println(scanner.Text())
		val, _ := strconv.Atoi(scanner.Text())
		data = append(data, val)
	}

	fmt.Printf("Data len: %d, cap:%d\n", len(data), cap(data))
	counter := countDecreasing(data)
	fmt.Printf("First star answer is %d\n", counter)

	compressed_data := make([]int, 0, 50)
	for i := 0; i < len(data); i++ {
		compressed_data = append(compressed_data, sum(data[i:i+3]))
	}
	//fmt.Println(compressed_data)
	fmt.Printf("Compressed data len: %d, cap:%d\n", len(compressed_data), cap(compressed_data))
	counter = countDecreasing(compressed_data)
	fmt.Printf("Second star answer is %d\n", counter)

}
