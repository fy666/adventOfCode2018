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

func convertListAndLimit(data []string) []int {
	var converted []int
	for _, val := range data {
		tmp, e := strconv.Atoi(val)
		if e == nil {
			if tmp > 50 {
				tmp = 51
			} else if tmp < -50 {
				tmp = -51
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
	re := regexp.MustCompile(`(on|off) x=([\-\d]*)\.\.([\-\d]*),y=([\-\d]*)\.\.([\-\d]*),z=([\-\d]*)\.\.([\-\d]*)`)
	for scanner.Scan() {
		txt := scanner.Text()
		m := re.FindAllStringSubmatch(txt, -1)
		res := m[0]
		nums := convertListAndLimit(res[2:])
		//fmt.Println(txt, "=>", nums)
		doStep(&ligthed_positions, nums[0], nums[1], nums[2], nums[3], nums[4], nums[5], res[1] == "on")
		fmt.Println(len(ligthed_positions))
		//fmt.Println(ligthed_positions)
	}

}
