package main

import (
	"bufio"
	"container/heap"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/thoas/go-funk"
)

func abs(input int) int {
	if input > 0 {
		return input
	}
	return -input
}

// An Item is something we manage in a priority queue.
type CrabStatus struct {
	crabs    map[[2]int]string
	priority int // The priority of the item in the queue.
	steps    int
	state    string
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*CrabStatus

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
	item := x.(*CrabStatus)
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
func (pq *PriorityQueue) update(item *CrabStatus, value map[[2]int]string, priority int) {
	item.crabs = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

func isFreeSpot(input string) bool {
	return input == "." || input == "X"
}

func isForbidden(input string) bool {
	return input == "X"
}

func isCrab(input string) bool {
	return input == "A" || input == "B" || input == "C" || input == "D"
}

func isChamberEmptyOrFilledWithCorrectCrab(room string, rooms *map[[2]int]string, crabs *map[[2]int]string) bool {
	for pos, c := range *rooms {
		if c != room {
			continue
		}
		// Found room with correct name, should be filled with crabs of same name or empy
		if val, contains := (*crabs)[pos]; contains {
			if val != room {
				return false
			}
		}
	}
	return true
}

func filterPotentialPositions(crab [2]int, crabs *map[[2]int]string, rooms *map[[2]int]string, ppuzzle *[][]string, potential_positions *[][2]int) [][2]int {
	result := make([][2]int, 0, 50)
	puzzle := *ppuzzle
	shouldGoToHallway := false
	if _, contains := (*rooms)[crab]; contains {
		//fmt.Println("Crab is in chamber", chamber)
		shouldGoToHallway = true
	}

	for _, pos := range *potential_positions {
		if isForbidden(puzzle[pos[0]][pos[1]]) {
			continue
		}
		_, isChamber := (*rooms)[pos]
		if shouldGoToHallway && isChamber {
			continue
		}
		if !shouldGoToHallway {
			// Check if room is correct
			if (*crabs)[crab] != (*rooms)[pos] {
				continue
			}
			// Room should be empty or filled with same crabs
			if !isChamberEmptyOrFilledWithCorrectCrab((*crabs)[crab], rooms, crabs) {
				continue
			}
		}
		result = append(result, pos)
	}
	return result
}

func getPotentialPositions(crab [2]int, crabs *map[[2]int]string, rooms *map[[2]int]string, ppuzzle *[][]string) [][2]int {
	row := crab[0]
	col := crab[1]
	puzzle := *ppuzzle
	nCol := len(puzzle[0])
	nRow := len(puzzle)
	list_pos := [][]int{{-1, 0}, {1, 0}, {0, 1}, {0, -1}}
	potential_positions := make([][2]int, 0, 50)
	positions_to_visit := make([][2]int, 0, 50)
	positions_to_visit = append(positions_to_visit, [2]int{row, col})
	//fmt.Println("Pos = ", list_pos)
	//fmt.Println("Treating crab", crabs[crab], "on pos", crab)
	for len(positions_to_visit) > 0 {
		for _, dir := range list_pos {
			cRow := positions_to_visit[0][0] + dir[0]
			cCol := positions_to_visit[0][1] + dir[1]
			if cRow < nRow && cRow >= 0 && cCol < nCol && cCol >= 0 {
				//fmt.Println("Test ", cRow, ",", cCol)
				_, contains := (*crabs)[[2]int{cRow, cCol}]
				if isFreeSpot(puzzle[cRow][cCol]) && !contains && !funk.Contains(potential_positions, [2]int{cRow, cCol}) {
					//fmt.Println("Adding to position list")
					positions_to_visit = append(positions_to_visit, [2]int{cRow, cCol})
					potential_positions = append(potential_positions, [2]int{cRow, cCol})
				}
			}
		}
		// Pop
		positions_to_visit = positions_to_visit[1:]
	}
	potential_positions = filterPotentialPositions(crab, crabs, rooms, &puzzle, &potential_positions)
	//fmt.Println("Positions accessible to crab", crab, "=", potential_positions)
	return potential_positions
}

func isFinished(crabs *map[[2]int]string, rooms *map[[2]int]string) bool {
	for pos, crabType := range *crabs {
		if (*rooms)[pos] != crabType {
			return false
		}
	}
	return true
}

func getStateString(crabs *map[[2]int]string, positions *[][2]int) string {
	result := ""
	for _, pos := range *positions {
		if val, contains := (*crabs)[pos]; contains {
			result += val
		} else {
			result += "."
		}
	}
	return result
}

func displayState(state string) {
	fmt.Println(state[0:2] + "X" + state[2:3] + "X" + state[3:4] + "X" + state[4:5] + "X" + state[5:7])
	fmt.Println(".." + state[7:8] + "." + state[8:9] + "." + state[9:10] + "." + state[10:11] + ".")
	fmt.Println(".." + state[11:12] + "." + state[12:13] + "." + state[13:14] + "." + state[14:15] + ".")
	return
}

func heuristic(crabs *map[[2]int]string, rooms *map[[2]int]string) int {
	distance := 0
	displacement_cost := map[string]int{"A": 1, "B": 10, "C": 100, "D": 1000}
	col_rooms := map[string]int{"A": 3, "B": 5, "C": 7, "D": 9}
	hallway_line := 1
	for posC, crabType := range *crabs {
		local_dist := 0
		// The crab is in one room
		if val, contains := (*rooms)[posC]; contains {
			if val != crabType {
				local_dist += abs(posC[1] - col_rooms[crabType])
				local_dist += posC[0] - hallway_line
			} else {
				local_dist = 0
			}
		} else {
			local_dist += abs(posC[1] - col_rooms[crabType])
		}
		distance += local_dist * displacement_cost[crabType]
	}
	return distance
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	var part2 = flag.Bool("part2", false, "Use test input")
	flag.Parse()
	fileName := "day23.txt"
	if *test {
		fileName = "day23_test.txt"
	} else if *part2 {
		fileName = "day23_part2.txt"
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

	puzzle := make([][]string, 0, 15)

	for scanner.Scan() {
		txt := strings.Split(scanner.Text(), "")
		puzzle = append(puzzle, txt)
	}

	fmt.Println("puzzle size", len(puzzle), "x", len(puzzle[0]))

	// Construct crab position list and rooms
	crab_positions := make(map[[2]int]string)
	rooms := make(map[[2]int]string)
	state_positions := make([][2]int, 0, 10)
	//rooms_positions := make([][2]int, 0, 10)
	map_rooms := map[int]string{3: "A", 5: "B", 7: "C", 9: "D"}
	for ix := 0; ix < len(puzzle); ix++ {
		for iy := 0; iy < len(puzzle[ix]); iy++ {
			if isCrab(puzzle[ix][iy]) {
				crab_positions[[2]int{ix, iy}] = puzzle[ix][iy]
				rooms[[2]int{ix, iy}] = map_rooms[iy]
				state_positions = append(state_positions, [2]int{ix, iy})
				puzzle[ix][iy] = "."
			} else if puzzle[ix][iy] == "." {
				state_positions = append(state_positions, [2]int{ix, iy})
			}
		}
	}

	start := time.Now()
	pq := make(PriorityQueue, 0)
	heap.Init(&pq)

	firstItem := &CrabStatus{
		crabs:    crab_positions,
		state:    getStateString(&crab_positions, &state_positions),
		steps:    0,
		priority: 0,
	}
	heap.Push(&pq, firstItem)

	displacement_cost := map[string]int{"A": 1, "B": 10, "C": 100, "D": 1000}
	cost_matrix := make(map[string]int)
	iteration := 0

	for pq.Len() > 0 {
		current_crabs := heap.Pop(&pq).(*CrabStatus)
		if isFinished(&current_crabs.crabs, &rooms) {
			fmt.Println("After", iteration, "iterations, found goal with cost =", current_crabs.priority, "steps =", current_crabs.steps)
			break
		}
		for pos, crabType := range current_crabs.crabs {
			// Crab already in its final position
			if rooms[pos] == crabType && isChamberEmptyOrFilledWithCorrectCrab(crabType, &current_crabs.crabs, &rooms) {
				continue
			}
			pot := getPotentialPositions(pos, &current_crabs.crabs, &rooms, &puzzle)
			for _, new_pos := range pot {
				new_crabs := make(map[[2]int]string)
				for key, val := range current_crabs.crabs {
					if key != pos {
						new_crabs[key] = val
					}
				}
				new_crabs[new_pos] = crabType
				dist := abs(pos[0]-new_pos[0]) + abs(pos[1]-new_pos[1])
				cost := displacement_cost[crabType] * dist
				cost += cost_matrix[current_crabs.state]
				new_state := getStateString(&new_crabs, &state_positions)
				h := heuristic(&new_crabs, &rooms)
				if val, contains := cost_matrix[new_state]; !contains || cost < val {
					new_item := &CrabStatus{
						crabs:    new_crabs,
						priority: h + cost,
						steps:    current_crabs.steps + 1,
						state:    new_state,
					}
					cost_matrix[new_state] = cost
					heap.Push(&pq, new_item)
				}
			}
		}
		iteration++
	}
	fmt.Println("Exit after", iteration, "iterations")
	elapsed := time.Since(start)
	fmt.Printf("Algorithm took %s \n", elapsed)
}
