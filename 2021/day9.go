package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

func isLocalMin(input [][]int, row int, col int) bool {
	nCol := len(input[0])
	nRow := len(input)
	list_pos := [][]int{{-1, 0}, {1, 0}, {0, 1}, {0, -1}}
	//fmt.Println("Pos = ", list_pos)
	for _, dir := range list_pos {
		cRow := row + dir[0]
		cCol := col + dir[1]
		if cRow < nRow && cRow >= 0 && cCol < nCol && cCol >= 0 {
			if !(input[row][col] < input[cRow][cCol]) {
				return false
			}
		}
	}
	return true
}

func findInList(input [][]int, searched []int) bool {
	for _, i := range input {
		if searched[0] == i[0] && searched[1] == i[1] {
			return true
		}
	}

	return false
}

func computeBassinSize(input [][]int, row int, col int) int {
	nCol := len(input[0])
	nRow := len(input)
	list_pos := [][]int{{-1, 0}, {1, 0}, {0, 1}, {0, -1}}
	positions_in_bassin := make([][]int, 0, 50)
	positions_in_bassin = append(positions_in_bassin, []int{row, col})
	positions_to_visit := make([][]int, 0, 50)
	positions_to_visit = append(positions_to_visit, []int{row, col})
	//fmt.Println("Pos = ", list_pos)
	for len(positions_to_visit) > 0 {
		//fmt.Println("Position to visit = ", positions_to_visit)
		//fmt.Println("Positions in bassin = ", positions_in_bassin)
		if input[positions_to_visit[0][0]][positions_to_visit[0][1]] != 9 {
			// Add position to bassin, if not already in
			if !findInList(positions_in_bassin, []int{positions_to_visit[0][0], positions_to_visit[0][1]}) {
				//fmt.Println("Adding to bassin")
				positions_in_bassin = append(positions_in_bassin, []int{positions_to_visit[0][0], positions_to_visit[0][1]})
			}
			for _, dir := range list_pos {
				cRow := positions_to_visit[0][0] + dir[0]
				cCol := positions_to_visit[0][1] + dir[1]
				if cRow < nRow && cRow >= 0 && cCol < nCol && cCol >= 0 {
					if !findInList(positions_in_bassin, []int{cRow, cCol}) {
						//fmt.Println("Adding to position list")
						positions_to_visit = append(positions_to_visit, []int{cRow, cCol})
					}
				}
			}
		}
		//fmt.Println("Position to visit = ", positions_to_visit)
		positions_to_visit = positions_to_visit[1:]
	}
	return len(positions_in_bassin)
}

func computeLowPoints(input [][]int) int {
	sum := 0
	bassin_sizes := make([]int, 0, 50)
	for ix := 0; ix < len(input); ix++ {
		for iy := 0; iy < len(input[0]); iy++ {
			//fmt.Println("At line", ix, "and column", iy, "=", input[ix][iy])
			if isLocalMin(input, ix, iy) {
				//fmt.Println("Minimum at line", ix, "and column", iy, "=", input[ix][iy])
				sum += (1 + input[ix][iy])
				bassin_sizes = append(bassin_sizes, computeBassinSize(input, ix, iy))
				fmt.Println("Bassin size", bassin_sizes[len(bassin_sizes)-1])
			}
		}
	}
	sort.Ints(bassin_sizes)
	fmt.Println("Product of 3 biggest bassins = ", bassin_sizes[len(bassin_sizes)-1]*bassin_sizes[len(bassin_sizes)-2]*bassin_sizes[len(bassin_sizes)-3])
	return sum
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
	fileName := "day9.txt"
	if *test {
		fileName = "day9_test.txt"
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
	fmt.Println("Sum of lowest points =", computeLowPoints(data))
}
