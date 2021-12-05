package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Board struct {
	mat [10][5]int
}

func (board *Board) ComputeColumns() {
	for i := 0; i < 5; i++ {
		for j := 0; j < 5; j++ {
			board.mat[i+5][j] = board.mat[j][i]
		}
	}
}

func (board Board) getBoardScore(index_tirage []int) int {
	sum := 0
	for i := 0; i < 5; i++ {
		for j := 0; j < 5; j++ {
			if !find(index_tirage, board.mat[i][j]) {
				sum += board.mat[i][j]
			}
		}
	}
	return sum
}

func (board Board) getMinTirageToWin(index_tirage map[int]int) int {
	minTirages := int(len(index_tirage))
	for _, val := range board.mat {
		maxT := 0
		for _, t := range val {
			if index_tirage[t] > maxT {
				maxT = index_tirage[t]
			}
		}
		if maxT < minTirages {
			minTirages = maxT
		}
	}
	return minTirages
}

func find(data []int, searched int) bool {
	for _, val := range data {
		if val == searched {
			return true
		}
	}
	return false
}

func convertList(data []string) []int {
	converted := make([]int, 0, len(data))
	for _, val := range data {
		tmp, e := strconv.Atoi(val)
		if e == nil {
			converted = append(converted, tmp)
		}
	}
	return converted
}

func solve(boards []Board, tirage_index map[int]int, tirage []int) {
	firstWinningBoard := 0
	lastWinningBoard := 0
	minTirage := len(tirage_index)
	maxTirage := 0
	for ix, b := range boards {
		minT := b.getMinTirageToWin(tirage_index)
		if minT < minTirage {
			firstWinningBoard = ix
			minTirage = minT
		}
		if minT > maxTirage {
			lastWinningBoard = ix
			maxTirage = minT
		}
	}
	fmt.Println("First winning board:", firstWinningBoard, "at tirage", minTirage, "with number", tirage[minTirage])
	score := boards[firstWinningBoard].getBoardScore(tirage[0 : minTirage+1])
	fmt.Println("Score of the first winning board :", score*tirage[minTirage])

	fmt.Println("Last winning board:", lastWinningBoard, "at tirage", maxTirage, "with number", tirage[maxTirage])
	score = boards[lastWinningBoard].getBoardScore(tirage[0 : maxTirage+1])
	fmt.Println("Score of the last winning board :", score*tirage[maxTirage])

}

func main() {
	file, err := os.Open("day4_test.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	data := make([][]int, 0, 50) // create empty slice with capacity of 50+

	scanner.Scan()
	tirage := convertList(strings.Split(scanner.Text(), ","))
	tirage_map := make(map[int]int)
	for ix, v := range tirage {
		tirage_map[v] = ix
	}
	fmt.Println("tirage :", tirage, "indexes : ", tirage_map)
	boards := make([]Board, 0, 50)
	for scanner.Scan() {
		txt := strings.ReplaceAll(scanner.Text(), "  ", " ")
		if txt == "" {
			// create new board
			if len(data) == 5 {
				boards = append(boards, Board{})
				for i := 0; i < 5; i++ {
					for j := 0; j < 5; j++ {
						boards[len(boards)-1].mat[i][j] = data[i][j]
					}
				}
				data = data[5:]
			}
		} else {
			data = append(data, convertList(strings.Split(txt, " ")))
		}
	}
	if len(data) == 5 {
		boards = append(boards, Board{})
		for i := 0; i < 5; i++ {
			for j := 0; j < 5; j++ {
				boards[len(boards)-1].mat[i][j] = data[i][j]
			}
		}
	}

	for ix := 0; ix < len(boards); ix++ {
		boards[ix].ComputeColumns()
		//fmt.Println(b.mat)
	}
	fmt.Println("After adding columns")
	for _, b := range boards {
		fmt.Println(b.mat)
	}

	solve(boards, tirage_map, tirage)
}
