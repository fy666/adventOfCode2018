package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/alexcesaro/log/stdlog"
)

//var logger = stdlog.GetFromFlags()
var logger *log.Logger

func convertList(data []string) [3]int {
	var converted [3]int
	for ix, val := range data {
		tmp, e := strconv.Atoi(val)
		if e == nil {
			converted[ix] = tmp
		} else {
			fmt.Println("Error with ", val)
		}
	}
	return converted
}

type Scanner struct {
	id          int
	beacons_pos map[[3]int]int
	matched     bool
}

func countCommon(a, b *map[[3]int]int) int {
	common := 0
	for ia, _ := range *a {
		if _, contains := (*b)[ia]; contains {
			common += 1
		}
	}
	return common
}

func abs(input int) int {
	if input > 0 {
		return input
	}
	return -input
}

func createRotations() []func(*[3]int) {
	operations := make([]func(*[3]int), 0, 25)
	transfos := [][3]int{{1, 3, -2},
		{-3, 1, -2},
		{-1, -3, -2},
		{3, -1, -2},
		{3, -2, 1},
		{2, 3, 1},
		{-3, 2, 1},
		{-2, -3, 1},
		{-2, 1, 3},
		{-1, -2, 3},
		{2, -1, 3},
		{1, 2, 3},
		{-3, -1, 2},
		{1, -3, 2},
		{3, 1, 2},
		{-1, 3, 2},
		{-1, 2, -3},
		{-2, -1, -3},
		{1, -2, -3},
		{2, 1, -3},
		{2, -3, -1},
		{3, 2, -1},
		{-2, 3, -1},
		{-3, -2, -1}}
	for _, t := range transfos {
		index := [3]int{abs(t[0]) - 1, abs(t[1]) - 1, abs(t[2]) - 1}
		sign := [3]int{t[0] / abs(t[0]), t[1] / abs(t[1]), t[2] / abs(t[2])}

		operations = append(operations, func(pos *[3]int) {
			pos[0], pos[1], pos[2] = sign[0]*pos[index[0]], sign[1]*pos[index[1]], sign[2]*pos[index[2]]
		})
	}
	return operations
}

func (scan1 *Scanner) searchMatch(scan2 *Scanner, operations *[]func(*[3]int)) *[3]int {
	// try all translations to match each pair of beacons
	for _, f := range *operations {
		tmp := scan2.getBeaconsAfterRotation(f)
		for b1, _ := range scan1.beacons_pos {
			for b2, _ := range tmp {
				transla := [3]int{b1[0] - b2[0], b1[1] - b2[1], b1[2] - b2[2]}
				new := getTranslation(transla, &tmp)
				common_beacons := countCommon(&scan1.beacons_pos, &new)
				if common_beacons >= 12 {
					// append to beacon list
					for x, _ := range new {
						scan1.beacons_pos[x] = 1
					}
					//logger.Debug("Matching beacon", scan1.id, "and", scan2.id, "after translation", transla, ", com =", common_beacons)
					scan2.matched = true
					return &transla
				}
			}
		}
	}
	return nil
}

func (s *Scanner) getBeaconsAfterRotation(f func(*[3]int)) map[[3]int]int {
	res := make(map[[3]int]int)
	for pos, _ := range s.beacons_pos {
		tmp := [3]int{pos[0], pos[1], pos[2]}
		f(&tmp)
		res[tmp] = 1
	}
	return res
}

func getTranslation(t [3]int, input *map[[3]int]int) map[[3]int]int {
	res := make(map[[3]int]int)
	for pos, _ := range *input {
		res[[3]int{pos[0] + t[0], pos[1] + t[1], pos[2] + t[2]}] = 1
	}
	return res
}

func (s *Scanner) String() string {
	str := fmt.Sprintf("Scanner %d, sees %d beacons", s.id, len(s.beacons_pos))
	// for ix, val := range s.beacons_pos {
	// 	str += fmt.Sprintf("\nbeacon %d: (%d,%d,%d)", ix, val[0], val[1], val[2])
	// }
	return str
}

func allMatched(scan_list *[]*Scanner) bool {
	for _, ix := range *scan_list {
		if !ix.matched {
			return false
		}
	}
	return true
}

func getMaxDistance(pos [][3]int) int {
	dmax := 0
	for ix := 0; ix < len(pos)-1; ix++ {
		for iy := ix + 1; iy < len(pos); iy++ {
			d := 0
			for c := 0; c < 3; c++ {
				d += abs(pos[ix][c] - pos[iy][c])
			}
			if d > dmax {
				dmax = d
			}
		}
	}
	return dmax
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day19.txt"
	if *test {
		fileName = "day19_test.txt"
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

	logger = stdlog.GetFromFlags()
	scanner_list := make([]*Scanner, 0, 50)
	var scan *Scanner
	createNewScanner := false

	for scanner.Scan() {
		txt := scanner.Text()
		if txt == "" || txt[0:2] == "--" {
			createNewScanner = true
		} else {
			if createNewScanner {
				// Create new scanner
				scan = &Scanner{len(scanner_list), make(map[[3]int]int), false}
				scanner_list = append(scanner_list, scan)
				createNewScanner = false
			}
			scan.beacons_pos[convertList(strings.Split(txt, ","))] = 1
		}
	}
	logger.Info(len(scanner_list), "scanners found")
	for _, s := range scanner_list {
		logger.Debug(s)
	}

	firstScanner := scanner_list[0]
	scanner_list = scanner_list[1:]
	operations := createRotations()

	start := time.Now()
	scanner_pos := make([][3]int, 0, 25)
	for !allMatched(&scanner_list) {
		for _, scan := range scanner_list {
			if !scan.matched {
				logger.Debug("Testing with scanner", scan.id)
				d := firstScanner.searchMatch(scan, &operations)
				if d != nil {
					scanner_pos = append(scanner_pos, *d)
				}
			}
		}
	}
	logger.Info("Unique beacons =", len(firstScanner.beacons_pos))
	logger.Info("Max scanner distance = ", getMaxDistance(scanner_pos))
	elapsed := time.Since(start)
	logger.Info("Day 19 took", elapsed)
}
