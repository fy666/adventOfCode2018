package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
)

func countLights(input map[[2]int]int) (counter int) {
	for _, val := range input {
		counter += val
	}
	return
}

func getAdjacentPoints(input [2]int) (output [][2]int) {
	square := [][2]int{{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 0}, {0, 1}, {1, -1}, {1, 0}, {1, 1}}
	for _, s := range square {
		output = append(output, [2]int{input[0] + s[0], input[1] + s[1]})
	}
	return
}

func run(input map[[2]int]int, algo string, world_off bool) map[[2]int]int {
	//decimal, _ := strconv.ParseUint(string(hex_input[ix]), 16, 64)
	output := make(map[[2]int]int)
	deflt := "1"
	if world_off == true {
		deflt = "0"
	}

	square := [][2]int{{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 0}, {0, 1}, {1, -1}, {1, 0}, {1, 1}}
	for point, _ := range input {
		//fmt.Println(float64(ix)/float64(len(input)), "%")
		adjacentPoints := getAdjacentPoints(point)
		for _, p := range adjacentPoints {
			binary_code := ""
			for _, s := range square {
				new_point := [2]int{p[0] + s[0], p[1] + s[1]}
				val, isInMap := input[new_point]
				if val == 1 {
					binary_code += "1"
				} else if !isInMap {
					binary_code += deflt
				} else {
					binary_code += "0"
				}
			}
			decimal, _ := strconv.ParseUint(binary_code, 2, 64)
			//fmt.Println("binary code", binary_code, "decimal=", decimal)
			if algo[decimal] == '#' {
				output[p] = 1
			} else {
				output[p] = 0
			}
		}
	}
	return output
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day20.txt"
	if *test {
		fileName = "day20_test.txt"
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

	dots := make([]string, 0, 15)
	algorithm := ""
	parse_map := false
	for scanner.Scan() {
		txt := scanner.Text()
		if parse_map {
			dots = append(dots, txt)
		} else {
			if txt == "" {
				parse_map = true
			} else {
				algorithm += txt
			}
		}

	}
	ligthed_positions := make(map[[2]int]int)
	fmt.Println(len(dots), "points,", len(algorithm), "algorithm conversion")
	for ix := 0; ix < len(dots); ix++ {
		for iy := 0; iy < len(dots[ix]); iy++ {
			if dots[ix][iy] == '#' {
				ligthed_positions[[2]int{ix, iy}] = 1
			} else {
				ligthed_positions[[2]int{ix, iy}] = 0
			}
		}
	}

	fmt.Println(len(ligthed_positions), "points,", countLights(ligthed_positions), "lighted positions")
	for ix := 0; ix < 25; ix++ {
		ligthed_positions = run(ligthed_positions, algorithm, true)
		ligthed_positions = run(ligthed_positions, algorithm, false)
		fmt.Println("After", 2*(ix+1), "iterations:", len(ligthed_positions), "points", countLights(ligthed_positions), "lighted positions")
	}
}
