package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/thoas/go-funk"
)

func containsLowerCaseDuplicate(path []string) bool {
	// Count lower case duplicates
	duplicates := make([]string, 0, 15)
	for _, p := range path {
		if strings.ToLower(p) == p {
			if funk.Contains(duplicates, p) {
				return true
			}
			duplicates = append(duplicates, p)
		}
	}
	return false
}

// node is Lower capitals
func canAddNode(path []string, node string, canVisitNodeTwice bool) (ans bool) {
	if !funk.Contains(path, node) {
		ans = true
	} else if !canVisitNodeTwice {
		ans = false
	} else {
		if node == "start" || node == "end" {
			ans = false
		} else {
			// Node already in path, can only visit one lower node twice
			ans = !containsLowerCaseDuplicate(path)
		}
	}
	//fmt.Println("Adding", node, "to", path, "canVisitNode ?", canVisitNodeTwice, " = ", ans)
	return

}
func computePaths(nodes map[string][]string, canVisitNodeTwice bool) int {

	paths := make([][]string, 0, 15)
	paths = append(paths, []string{"start"})
	final_paths := make([][]string, 0, 15)
	for len(paths) > 0 {
		current_path := paths[0]
		last_node := current_path[len(current_path)-1]
		if last_node == "end" {
			final_paths = append(final_paths, current_path)
		} else {
			for _, neigh := range nodes[last_node] {
				// If lower case, may only be used once
				if !(strings.ToLower(neigh) == neigh) || canAddNode(current_path, neigh, canVisitNodeTwice) {
					new_path := make([]string, len(paths[0]))
					copy(new_path, paths[0])
					new_path = append(new_path, neigh)
					paths = append(paths, new_path)
				}
			}
		}
		paths = paths[1:] // Pop
	}
	return len(final_paths)
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day12.txt"
	if *test {
		fileName = "day12_test.txt"
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

	nodes := make(map[string][]string, 15)
	for scanner.Scan() {
		data := strings.Split(scanner.Text(), "-")
		nodes[data[0]] = append(nodes[data[0]], data[1])
		nodes[data[1]] = append(nodes[data[1]], data[0])

	}
	//fmt.Println("Nodes", nodes)
	fmt.Println("First part,", computePaths(nodes, false), "paths")
	fmt.Println("Second part,", computePaths(nodes, true), "paths")
}
