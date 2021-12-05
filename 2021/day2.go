package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func firstPart(data []string) (sum int) {
	var dept, hor int
	for _, val := range data {
		//fmt.Println(scanner.Text())
		command := strings.Split(val, " ")
		//fmt.Println(data[1])
		value, _ := strconv.Atoi(command[1])
		if command[0] == "forward" {
			hor += value
		} else if command[0] == "up" {
			dept -= value
		} else if command[0] == "down" {
			dept += value
		} else {
			fmt.Println("Error")
		}

		//fmt.Printf("Line: %s, dept:%d, hor:%d\n", command, dept, hor)
	}
	fmt.Printf("First star answer : %d \n", dept*hor)
	sum = dept * hor
	return
}

func secondPart(data []string) (sum int) {
	var dept, hor, aim int
	for _, val := range data {
		command := strings.Split(val, " ")
		value, _ := strconv.Atoi(command[1])
		if command[0] == "forward" {
			hor += value
			dept += value * aim
		} else if command[0] == "up" {
			aim -= value
		} else if command[0] == "down" {
			aim += value
		} else {
			fmt.Println("Error")
		}

		//fmt.Printf("Line: %s, dept:%d, hor:%d, aim:%d\n", command, dept, hor, aim)
	}
	fmt.Printf("Second star answer : %d \n", dept*hor)
	sum = dept * hor
	return
}

func main() {
	file, err := os.Open("day2.txt")
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
	first := firstPart(data)
	second := secondPart(data)
	fmt.Printf("First: %d, Second: %d\n", first, second)
}
