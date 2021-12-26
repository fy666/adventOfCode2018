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
	beacons_pos [][3]int
}

func (s *Scanner) String() string {
	str := fmt.Sprintf("Scanner %d, sees %d beacons", s.id, len(s.beacons_pos))
	// for ix, val := range s.beacons_pos {
	// 	str += fmt.Sprintf("\nbeacon %d: (%d,%d,%d)", ix, val[0], val[1], val[2])
	// }
	return str
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

	scanner_list := make([]*Scanner, 0, 50)
	var data [][3]int
	var scan *Scanner
	createNewScanner := false
	for scanner.Scan() {
		txt := scanner.Text()
		if txt == "" || txt[0:2] == "--" {
			createNewScanner = true
		} else {
			if createNewScanner {
				// Create new scanner
				data = make([][3]int, 0, 50)
				scan = &Scanner{len(scanner_list), data}
				scanner_list = append(scanner_list, scan)
				createNewScanner = false
			}
			scan.beacons_pos = append(scan.beacons_pos, convertList(strings.Split(txt, ",")))
		}
	}
	fmt.Println(len(scanner_list), "scanners found")
	for _, s := range scanner_list {
		fmt.Println(s)
	}
}
