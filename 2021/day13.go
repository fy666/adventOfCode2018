package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/thoas/go-funk"
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

func foldAlong(input [][]int, xDir bool, s int) (output [][]int) {
	for _, point := range input {
		curr := point[1]
		if xDir {
			curr = point[0]
		}
		new_point := point
		if curr > s {
			new_point = []int{point[0], 2*s - curr}
			if xDir {
				new_point = []int{2*s - curr, point[1]}
			}
		}
		if !funk.Contains(output, new_point) {
			output = append(output, new_point)
		}
	}
	return output
}

func displayPoints(input [][]int) {
	xMax := 0
	yMax := 0
	for _, point := range input {
		if point[0] > xMax {
			xMax = point[0]
		}
		if point[1] > yMax {
			yMax = point[1]
		}
	}
	for iy := 0; iy <= yMax; iy++ {
		for ix := 0; ix <= xMax; ix++ {
			if funk.Contains(input, []int{ix, iy}) {
				fmt.Printf("#")
			} else {
				fmt.Printf(".")
			}
		}
		fmt.Printf("\n")
	}
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day13.txt"
	if *test {
		fileName = "day13_test.txt"
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

	dots := make([][]int, 0, 15)
	fold_operations := make([][]string, 0, 15)
	parse_folds := false
	for scanner.Scan() {
		txt := scanner.Text()
		if parse_folds {
			fold_operations = append(fold_operations, strings.Split(txt, "="))
		} else {
			if txt == "" {
				parse_folds = true
			} else {
				dots = append(dots, convertList(strings.Split(txt, ",")))
			}
		}

	}
	fmt.Println(len(dots), "points,", len(fold_operations), "operations")

	for ix, op := range fold_operations {
		s, _ := strconv.Atoi(op[1])
		dots = foldAlong(dots, 'x' == op[0][len(op[0])-1], s)
		fmt.Println("After", ix+1, "folding operations:", len(dots)) //new_dots)
	}
	displayPoints(dots)

}
