package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"

	"github.com/montanaflynn/stats"
)

func countItems(data []int, valueToFind int) (counter int) {
	for _, j := range data {
		if j == valueToFind {
			counter += 1
		}
	}
	return
}

func abs(input int) int {
	if input > 0 {
		return input
	}
	return -input
}

func countFuel(data []int, position int, exp bool) int {
	count := 0
	for _, val := range data {
		step := abs(val - position)
		if exp {
			count += (step * (step + 1)) / 2
		} else {
			count += step
		}
	}
	return count
}

// func Median(input Float64Data) (median float64, err error) {

// 	// Start by sorting a copy of the slice
// 	c := sortedCopy(input)

// 	// No math is needed if there are no numbers
// 	// For even numbers we add the two middle numbers
// 	// and divide by two using the mean function above
// 	// For odd numbers we just use the middle number
// 	l := len(c)
// 	if l == 0 {
// 		return math.NaN(), EmptyInputErr
// 	} else if l%2 == 0 {
// 		median, _ = Mean(c[l/2-1 : l/2+1])
// 	} else {
// 		median = c[l/2]
// 	}

// 	return median, nil
// }

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
	fileName := "day7.txt"
	if *test {
		fileName = "day7_test.txt"
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
	fmt.Println(len(data), "crabs positions found")

	fdata := stats.LoadRawData(data)
	median, _ := stats.Median(fdata)
	fmt.Println("Median is", median) // 3.65

	count := countFuel(data, int(median), false)
	fmt.Println("Fuel needed = ", count)

	m, _ := stats.Mean(fdata)
	fmt.Println("Mean =", m, ", floor =", math.Floor(m), "ceil =", math.Ceil(m))

	count = countFuel(data, int(math.Ceil(m)), true)
	fmt.Println("Second puzzle fuel needed for ceil of mean = ", count)
	count = countFuel(data, int(math.Floor(m)), true)
	fmt.Println("Second puzzle fuel needed for floor of the mean = ", count)
	minCount := count
	for ix := -100; ix < 100; ix++ {
		count = countFuel(data, int(math.Floor(m))+ix, true)
		if count < minCount {
			minCount = count
		}
		//fmt.Println("Second puzzle fuel for position", int(math.Floor(m))+ix, "needed = ", count)
	}

	fmt.Println("Second puzzle min fuel needed (around mean) =", minCount)
}
