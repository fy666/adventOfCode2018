package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
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

func printSeafloor(seafloor *[][]string) {
	for ix := 0; ix < len(*seafloor); ix++ {
		fmt.Println((*seafloor)[ix])
	}
	return
}

func sameSeafloor(seafloor *[][]string, seafloor2 *[][]string) bool {
	for ix := 0; ix < len(*seafloor); ix++ {
		for iy := 0; iy < len((*seafloor)[0]); iy++ {
			if (*seafloor)[ix][iy] != (*seafloor2)[ix][iy] {
				return false
			}
		}
	}
	return true
}

func run(seafloor [][]string) [][]string {

	new_seafloor := make([][]string, len(seafloor))
	for ix := 0; ix < len(seafloor); ix++ {
		for iy := 0; iy < len(seafloor[ix]); iy++ {
			new_seafloor[ix] = append(new_seafloor[ix], ".")
		}
	}
	//fmt.Println(new_seafloor)

	// Move Eastfacing sea cucumbers
	for ix := 0; ix < len(seafloor); ix++ {
		for iy := 0; iy < len(seafloor[ix]); iy++ {
			if seafloor[ix][iy] == ">" {
				next_pos_x := ix
				next_pos_y := (iy + 1) % len(seafloor[0])
				//fmt.Println("From", ix, iy, "going to", next_pos_x, next_pos_y)
				if seafloor[next_pos_x][next_pos_y] == "." {
					new_seafloor[next_pos_x][next_pos_y] = ">"
					//fmt.Println("Move > to", next_pos_x, next_pos_y)
				} else {
					new_seafloor[ix][iy] = ">"
				}
			} else if seafloor[ix][iy] != "." {
				new_seafloor[ix][iy] = seafloor[ix][iy]
			}
		}
	}

	seafloor = new_seafloor
	new_seafloor = make([][]string, len(seafloor))
	for ix := 0; ix < len(seafloor); ix++ {
		for iy := 0; iy < len(seafloor[ix]); iy++ {
			new_seafloor[ix] = append(new_seafloor[ix], ".")
		}
	}
	//fmt.Println("----------------------------")
	///printSeafloor(&seafloor)
	// Move South facing sea cucumbers
	for ix := 0; ix < len(seafloor); ix++ {
		for iy := 0; iy < len(seafloor[ix]); iy++ {
			if seafloor[ix][iy] == "v" {
				next_pos_x := (ix + 1) % len(seafloor)
				next_pos_y := iy
				if seafloor[next_pos_x][next_pos_y] == "." {
					new_seafloor[next_pos_x][next_pos_y] = "v"
				} else {
					new_seafloor[ix][iy] = "v"
				}
			} else if seafloor[ix][iy] != "." {
				new_seafloor[ix][iy] = seafloor[ix][iy]
			}
		}
	}

	return new_seafloor
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day25.txt"
	if *test {
		fileName = "day25_test.txt"
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

	seafloor := make([][]string, 0, 15)
	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), "")
		seafloor = append(seafloor, txt)
	}
	fmt.Println("Sea floor size", len(seafloor), "x", len(seafloor[0]))
	//printSeafloor(&seafloor)
	step := 1
	for {
		seafloor2 := run(seafloor)
		if sameSeafloor(&seafloor, &seafloor2) {
			fmt.Println("Same seafloor after", step, "steps")
			break
		}
		seafloor = seafloor2
		step += 1
	}

}
