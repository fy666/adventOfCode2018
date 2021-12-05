package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

type Result struct {
	state [2]int
	value int64
}

func runPartNomad(input int, commands []string, input_variables [2]int, value int64, c chan Result, onExit func()) {
	defer onExit()
	variables := [4]int{0, 0, 0, 0}
	copy(variables[1:], input_variables[:])
	mapping := map[string]int{"x": 0, "y": 1, "z": 2, "w": 3}
	for _, command := range commands {
		txt := strings.Split(command, " ")
		if len(txt) < 3 {
			variables[mapping[txt[1]]] = input
			continue
		}
		f := func(x int, y int) int { return x + y }
		switch txt[0] {
		case "add":
			f = func(x int, y int) int { return x + y }
		case "mod":
			f = func(x int, y int) int { return x % y }
		case "div":
			f = func(x int, y int) int { return x / y }
		case "mul":
			f = func(x int, y int) int { return x * y }
		case "eql":
			f = func(x int, y int) int {
				if x == y {
					return 1
				}
				return 0
			}
		}
		val, err := strconv.Atoi(txt[2])
		if err != nil {
			val = variables[mapping[txt[2]]]
		}
		variables[mapping[txt[1]]] = f(variables[mapping[txt[1]]], val)
	}
	copy(input_variables[:], variables[1:3])
	c <- Result{input_variables, value}
	return
}

func findSubmarineModel(code *[][]string, ix int, states *map[[2]int]int64, keepMax bool) map[[2]int]int64 {
	new_states := make(map[[2]int]int64)
	fmt.Println("Iterating on number", ix, len(*states), "states")
	c := make(chan Result, len(*states)*9)
	var wg sync.WaitGroup

	for key, val := range *states {
		var digit int64
		for digit = 1; digit <= 9; digit += 1 {
			new_value := val*10 + digit
			wg.Add(1)
			go runPartNomad(int(digit), (*code)[ix], key, new_value, c, func() { wg.Done() })
		}
	}
	go func() {
		defer close(c)
		wg.Wait()
	}()

	for res := range c {
		if same_val, contains := new_states[res.state]; contains {
			if (keepMax && res.value > same_val) || (!keepMax && res.value < same_val) {
				new_states[res.state] = res.value
			}
		} else {
			new_states[res.state] = res.value
		}
	}
	ix += 1
	if ix < 14 {
		new_states = findSubmarineModel(code, ix, &new_states, keepMax)
	}
	return new_states
}

func findExtremumValid(data map[[2]int]int64) (int64, int64) {
	var maxv int64 = 0
	var minv int64 = 99999999999999
	for key, val := range data {
		if key[1] == 0 {
			if val > maxv {
				maxv = val
			}
			if val < minv {
				minv = val
			}
		}
	}
	fmt.Println("Max value = ", maxv, ", min value =", minv)
	return minv, maxv
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day24.txt"
	if *test {
		fileName = "day24_test.txt"
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

	//variables := make(map[string]int)
	monad_code := make([][]string, 0, 50)
	append_ix := -1
	//re := regexp.MustCompile(`(on|off) x=([\-\d]*)\.\.([\-\d]*),y=([\-\d]*)\.\.([\-\d]*),z=([\-\d]*)\.\.([\-\d]*)`)
	for scanner.Scan() {
		txt := scanner.Text()
		if strings.HasPrefix(txt, "inp") {
			new_monad_code := make([]string, 0, 50)
			monad_code = append(monad_code, new_monad_code)
			append_ix += 1
		}
		monad_code[append_ix] = append(monad_code[append_ix], txt)
	}

	fmt.Println("Importing nomad code of", len(monad_code))
	states := make(map[[2]int]int64)
	states[[2]int{0, 0}] = 0
	start := time.Now()
	result := findSubmarineModel(&monad_code, 0, &states, true)
	findExtremumValid(result)
	elapsed := time.Since(start)
	fmt.Printf("Algorithm took %s \n", elapsed)

	/*
		start = time.Now()
		result = findSubmarineModel(&monad_code, 0, &states, false)
		findExtremumValid(result)
		elapsed = time.Since(start)
		fmt.Printf("Algorithm took %s \n", elapsed)
	*/
	return
}
