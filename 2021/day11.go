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
		} else {
			fmt.Println("Error with ", val)
		}
	}
	return converted
}

func addOne(data *[][]int) {
	for ix := 0; ix < len(*data); ix++ {
		for iy := 0; iy < len((*data)[ix]); iy++ {
			(*data)[ix][iy] += 1
		}
	}
}

func resetFlashed(data *[][]int) {
	for ix := 0; ix < len(*data); ix++ {
		for iy := 0; iy < len((*data)[ix]); iy++ {
			if (*data)[ix][iy] > 9 {
				(*data)[ix][iy] = 0
			}
		}
	}
}

func getOctopusToFlash(data *[][]int) (octopus [][2]int) {
	for ix := 0; ix < len(*data); ix++ {
		for iy := 0; iy < len((*data)[ix]); iy++ {
			if (*data)[ix][iy] > 9 {
				octopus = append(octopus, [2]int{ix, iy})
			}
		}
	}
	return
}

func flash(data *[][]int, octopus [2]int) {
	neigh := [8][2]int{{-1, 0}, {1, 0}, {0, 1}, {0, -1}, {-1, -1}, {-1, 1}, {1, 1}, {1, -1}}
	nRow := len(*data)
	nCol := len((*data)[0])
	for _, n := range neigh {
		//fmt.Println("Neighborgh at", n[0], n[1])
		cRow := octopus[0] + n[0]
		cCol := octopus[1] + n[1]
		if cRow < nRow && cRow >= 0 && cCol < nCol && cCol >= 0 {
			(*data)[cRow][cCol] += 1
		}
	}
	return
}

func printGrid(data *[][]int) {
	fmt.Println("*************")
	for ix := 0; ix < len(*data); ix++ {
		for iy := 0; iy < len((*data)[ix]); iy++ {
			fmt.Printf("%02d ", (*data)[ix][iy])
		}
		fmt.Printf("\n")
	}
	fmt.Println("*************")
	return
}

func contain(data [][2]int, searched [2]int) bool {
	for _, d := range data {
		if d[0] == searched[0] && d[1] == searched[1] {
			return true
		}
	}
	return false
}

func doStep(data *[][]int) (flashed int) {
	addOne(data)
	octopus := getOctopusToFlash(data)
	already_flashed := make([][2]int, 0, 100)
	for len(octopus) > 0 {
		//fmt.Println(len(octopus), "Octopus to flash")
		flashed += len(octopus)
		for _, o := range octopus {
			flash(data, o)
			already_flashed = append(already_flashed, o)
			//printGrid(data)
		}
		octopus = nil
		for _, octo := range getOctopusToFlash(data) {
			if !contain(already_flashed, octo) {
				octopus = append(octopus, octo)
			}
		}
		//fmt.Println(len(octopus), "still to flash")
	}
	resetFlashed(data)

	return
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day11.txt"
	if *test {
		fileName = "day11_test.txt"
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

	data := make([][]int, 0, 50) // create empty slice with capacity of 50+
	for scanner.Scan() {
		data = append(data, convertList(strings.Split(scanner.Text(), "")))
	}
	fmt.Println("Read matrix of", len(data), "lines and", len(data[0]), "columns")
	printGrid(&data)
	count_flashed := 0
	for ix := 0; ix < 100; ix++ {
		//fmt.Println("Step", ix)
		count_flashed += doStep(&data)
		//printGrid(&data)
	}
	fmt.Println(count_flashed, "flashed after 100 steps")
	flashed := 0
	step := 100
	for flashed != 100 {
		flashed = doStep(&data)
		step += 1
	}
	fmt.Println("all flashed after", step, "steps")

	/*
		fmt.Println("Mat = ", data)
		addOne(&data)
		fmt.Println("Mat = ", data)
		octopus := getOctopusToFlash(&data)
		fmt.Println("Octopus to flash : ", octopus)
		resetFlashed(&data)
		fmt.Println("Mat = ", data)
	*/

}
