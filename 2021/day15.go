package main

import (
	"bufio"
	"container/heap"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// An Item is something we manage in a priority queue.
type Item struct {
	node     [2]int
	path     [][2]int // The value of the item; arbitrary.
	priority int      // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) update(item *Item, value [2]int, priority int) {
	item.node = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

func findPath(input [][]int, expand int) {
	nCol := expand * len(input[0])
	nRow := expand * len(input)
	goal := [2]int{expand*(len(input)) - 1, expand*len(input[0]) - 1}
	list_pos := [][]int{{-1, 0}, {1, 0}, {0, 1}, {0, -1}}
	pq := make(PriorityQueue, 0)
	heap.Init(&pq)

	firstItem := &Item{
		node:     [2]int{0, 0},
		path:     make([][2]int, 0, 15),
		priority: 0,
	}
	heap.Push(&pq, firstItem)
	cost_matrix := make(map[[2]int]int)
	cost_matrix[firstItem.node] = firstItem.priority
	iteration := 0

	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*Item)
		//fmt.Println("Current node", item.node, "cost =", item.priority) // "path =", item.path)
		if item.node[0] == goal[0] && item.node[1] == goal[1] {
			fmt.Println("After", iteration, "iterations, found goal at", item.node, "cost =", item.priority)
			break
		}
		for _, dir := range list_pos {
			cRow := item.node[0] + dir[0]
			cCol := item.node[1] + dir[1]
			if cRow < nRow && cRow >= 0 && cCol < nCol && cCol >= 0 {
				costCol := cCol % (nCol / expand)
				costRow := cRow % (nCol / expand)
				to_add := cCol/(nCol/expand) + cRow/(nCol/expand)
				cost := (input[costRow][costCol] + to_add) % 9
				if cost == 0 {
					cost = 9
				}
				cost += cost_matrix[item.node]
				h := goal[0] - cRow + goal[1] - cCol
				new_item := &Item{
					node:     [2]int{cRow, cCol},
					path:     make([][2]int, len(item.path)),
					priority: h + cost,
				}
				if cost_matrix[new_item.node] == 0 || cost < cost_matrix[new_item.node] {
					cost_matrix[new_item.node] = cost
					copy(new_item.path, item.path)
					new_item.path = append(new_item.path, [2]int{cRow, cCol})
					heap.Push(&pq, new_item)
				}
			}
		}
		iteration++
	}
	return
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
	fileName := "day15.txt"
	if *test {
		fileName = "day15_test.txt"
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
	findPath(data, 1)
	findPath(data, 5)
}
