package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
)

// Return 0 if not corrupted, else corrupted score
// ): 3 points.
// ]: 57 points.
// }: 1197 points.
// >: 25137 points.
// For incomplete:
// ): 1 point.
// ]: 2 points.
// }: 3 points.
// >: 4 points.
func getCorruptedScore(data string) (string, int) {
	buffer := make([]rune, 0, 50)
	closeMap := map[rune]rune{'[': ']', '{': '}', '<': '>', '(': ')'}
	points := map[rune]int{']': 57, '}': 1197, '>': 25137, ')': 3, '[': 2, '(': 1, '{': 3, '<': 4}

	for _, val := range data {
		if val == '[' || val == '{' || val == '<' || val == '(' {
			//fmt.Printf("Openning %c\n", val)
			buffer = append(buffer, val)
		} else {
			//fmt.Printf("Found closing bracket %c, matching %c?\n", val, buffer[len(buffer)-1])
			if val == closeMap[buffer[len(buffer)-1]] {
				if len(buffer) == 0 {
					return "error", 0
				}
				buffer = buffer[:len(buffer)-1]
			} else {
				//fmt.Printf("Corrupted end of line: %c\n", val)
				return "corrupted", points[val]
			}
		}
	}
	score := 0
	for ix := len(buffer) - 1; ix >= 0; ix-- {
		score = score * 5
		score += points[buffer[ix]]
	}
	return "incomplete", score
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day10.txt"
	if *test {
		fileName = "day10_test.txt"
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

	data := make([]string, 0, 50) // create empty slice with capacity of 50+
	for scanner.Scan() {
		data = append(data, scanner.Text())
	}
	fmt.Println("Read", len(data), "lines of code")
	score := 0
	scores := make([]int, 0, len(data))
	for _, val := range data {
		fmt.Println("Processing", val)
		reason, points := getCorruptedScore(val)
		if reason == "corrupted" {
			score += points
		} else if reason == "incomplete" {
			//fmt.Println("Incomplete score = ", points)
			scores = append(scores, points)
		}
	}
	fmt.Println("Score of corrupted lines =", score)
	sort.Ints(scores)
	fmt.Println(scores)
	index := int(math.Floor(float64(len(scores)) / 2))
	fmt.Println("Middle score of incomplete lines = ", scores[index])
}
