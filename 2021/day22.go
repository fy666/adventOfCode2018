package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func min(a int, b int) int {
	if a > b {
		return b
	}
	return a
}

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

type Cube struct {
	x1, x2, y1, y2, z1, z2 int
	val                    int
}

func (c *Cube) getCubes() int {
	return c.val * (c.x2 - c.x1 + 1) * (c.y2 - c.y1 + 1) * (c.z2 - c.z1 + 1)
}

func overlap_size(c1 *Cube, c2 *Cube) int {
	res := 1
	res *= max(min(c2.x2+1, c1.x2+1)-max(c2.x1, c1.x1), 0)
	res *= max(min(c2.y2+1, c1.y2+1)-max(c2.y1, c1.y1), 0)
	res *= max(min(c2.z2+1, c1.z2+1)-max(c2.z1, c1.z1), 0)
	return res
}

func getOverlap(c1 *Cube, c2 *Cube) *Cube {
	if overlap_size(c1, c2) == 0 {
		return nil
	}

	x2 := min(c2.x2, c1.x2)
	x1 := max(c2.x1, c1.x1)
	y2 := min(c2.y2, c1.y2)
	y1 := max(c2.y1, c1.y1)
	z2 := min(c2.z2, c1.z2)
	z1 := max(c2.z1, c1.z1)

	return &Cube{x1, x2, y1, y2, z1, z2, -c1.val}
}

func convertListAndLimit(data []string, limit bool) []int {
	var converted []int
	for _, val := range data {
		tmp, e := strconv.Atoi(val)
		if e == nil {
			if limit {
				if tmp > 50 {
					tmp = 51
				} else if tmp < -50 {
					tmp = -51
				}
			}
			converted = append(converted, tmp)
		} else {
			fmt.Println("Error with ", val)
		}
	}
	return converted
}

func doStep(data *map[[3]int]int, x1, x2, y1, y2, z1, z2 int, turn_on bool) {
	for ix := x1; ix <= x2; ix++ {
		for iy := y1; iy <= y2; iy++ {
			for iz := z1; iz <= z2; iz++ {
				//fmt.Println("adding", ix, iy, iz)
				if ix > 50 || ix < -50 || iy > 50 || iy < -50 || iz > 50 || iz < -50 {
					//fmt.Println("outside", ix, iy, iz)
					continue
				}
				if turn_on {
					(*data)[[3]int{ix, iy, iz}] = 1
				} else {
					delete((*data), [3]int{ix, iy, iz})
				}
			}
		}
	}
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day22.txt"
	if *test {
		fileName = "day22_test.txt"
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

	ligthed_positions := make(map[[3]int]int)
	cubes := make([]*Cube, 0)
	re := regexp.MustCompile(`(on|off) x=([\-\d]*)\.\.([\-\d]*),y=([\-\d]*)\.\.([\-\d]*),z=([\-\d]*)\.\.([\-\d]*)`)
	for scanner.Scan() {
		txt := scanner.Text()
		m := re.FindAllStringSubmatch(txt, -1)
		res := m[0]
		nums := convertListAndLimit(res[2:], true)
		// Part 1
		doStep(&ligthed_positions, nums[0], nums[1], nums[2], nums[3], nums[4], nums[5], res[1] == "on")
		// Part 2
		nums = convertListAndLimit(res[2:], false)
		value := 1
		if res[1] == "off" {
			value = -1
		}
		newCube := &Cube{nums[0], nums[1], nums[2], nums[3], nums[4], nums[5], value}
		cubesToAdd := make([]*Cube, 0)
		for ic := 0; ic < len(cubes); ic++ {
			overlap := getOverlap(cubes[ic], newCube)
			if overlap != nil {
				cubesToAdd = append(cubesToAdd, overlap)
			}
		}
		if newCube.val == 1 {
			cubesToAdd = append(cubesToAdd, newCube)
		}
		for ix := 0; ix < len(cubesToAdd); ix++ {
			cubes = append(cubes, cubesToAdd[ix])
		}
	}

	fmt.Println("Part 1 lighted positions =", len(ligthed_positions))
	allLigthedPositions := 0
	for ic := 0; ic < len(cubes); ic++ {
		allLigthedPositions += cubes[ic].getCubes()
	}
	fmt.Println("Part 2 lighted positions =", allLigthedPositions)

}
