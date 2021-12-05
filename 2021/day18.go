package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
)

type Tree struct {
	Left   *Tree
	Value  int
	Right  *Tree
	Parent *Tree
}

func getSplitIndex(data string) int {
	counter := 0
	for ix := 0; ix < len(data); ix++ {
		switch data[ix] {
		case '[':
			counter += 1
		case ']':
			counter -= 1
		case ',':
			if counter == 1 {
				return ix
			}
		}
	}
	return 0
}

func add(t1 *Tree, t2 *Tree) (t *Tree) {
	if t1 == nil {
		return t2
	}
	new_tree := &Tree{t1, 0, t2, nil}
	t1.Parent = new_tree
	t2.Parent = new_tree
	return new_tree
}

func (t *Tree) Split() bool {
	if t == nil {
		return false
	}
	if t.Right == nil && t.Left == nil {
		if t.Value >= 10 {
			t.Right = &Tree{nil, int(math.Ceil(float64(t.Value) / 2.0)), nil, t}
			t.Left = &Tree{nil, int(math.Floor(float64(t.Value) / 2.0)), nil, t}
			// reset value
			t.Value = 0
			return true
		}
	}
	//if t.Right != nil
	if t.Left.Split() {
		return true
	}
	if t.Right.Split() {
		return true
	}
	return false
}

func AddToRight(current *Tree, explored *Tree, value int) {
	if current == nil {
		return
	}

	//fmt.Println("Adding", value, "starting with", current)
	if current.Right == explored {
		// Go up until you're on the left
		for current.Parent != nil && current.Parent.Right == current {
			current = current.Parent
		}
		if current.Parent == nil {
			return
		}
		current = current.Parent
	}

	// Go one right
	current = current.Right
	//fmt.Println("current is", current)
	// Then go down to left until a node
	for current.Left != nil {
		//fmt.Println("going down", current)
		current = current.Left
	}
	//fmt.Println("On node", current.Value)
	//fmt.Println("Add to Right", value, "to", current.Value)
	current.Value += value
}

func AddToLeft(current *Tree, explored *Tree, value int) {
	if current == nil {
		return
	}

	//fmt.Println("Adding", value, "starting with", current)
	if current.Left == explored {
		// Go up until you're on the right
		for current.Parent != nil && current.Parent.Left == current {
			current = current.Parent
			//fmt.Println("going up", current)
		}
		if current.Parent == nil {
			return
		}
		current = current.Parent
	}

	// Go one left
	current = current.Left
	//fmt.Println("current is", current)
	// Then go down to right until a node
	for current.Right != nil {
		//fmt.Println("going down", current)
		current = current.Right
	}
	//fmt.Println("On node", current.Value)
	//fmt.Println("Add to Left", value, "to", current.Value)
	current.Value += value
}

func (t *Tree) getHead() *Tree {
	if t.Parent != nil {
		return t.Parent.getHead()
	} else {
		return t
	}
}
func (t *Tree) Explode(level int) bool {
	if t == nil {
		return false
	}
	if level == 4 && t.Right != nil && t.Left != nil {
		//fmt.Println("Exploding", t.Left.Value, ",", t.Right.Value)
		left := t.Left.Value
		right := t.Right.Value
		t.Left = nil
		t.Right = nil
		AddToLeft(t.Parent, t, left)
		AddToRight(t.Parent, t, right)
		return true
	}
	if t.Left.Explode(level + 1) {
		return true
	}
	if t.Right.Explode(level + 1) {
		return true
	}
	return false
}

func createTree(data string, parent *Tree) (t *Tree) {
	current := &Tree{nil, 0, nil, parent}
	if data[0] == '[' {
		ix := getSplitIndex(data)
		current.Left = createTree(data[1:ix], current)
		current.Right = createTree(data[ix+1:len(data)-1], current)
	} else {
		val, _ := strconv.Atoi(data)
		current.Value = val
		return current
	}
	return current
}

func (t *Tree) String() string {
	if t == nil {
		return "[]"
	}
	s := ""
	if t.Left != nil {
		s += "[" + t.Left.String() + ","
	}
	if t.Left == nil && t.Right == nil {
		s += fmt.Sprint(t.Value)
	}
	if t.Right != nil {
		s += t.Right.String() + "]"
	}
	return s
}

func (t *Tree) getValue() int {
	if t == nil {
		return 0
	}
	result := 0
	if t.Left != nil {
		result += 3 * t.Left.getValue()
	}
	if t.Left == nil && t.Right == nil {
		return t.Value
	}
	if t.Right != nil {
		result += 2 * t.Right.getValue()
	}
	return result
}

func (t *Tree) reduce() {
	if t == nil {
		return
	}
	origin := ""
	for t.String() != origin {
		origin = t.String()
		for t.Explode(0) {
		}
		t.Split()
	}
	return
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day18.txt"
	if *test {
		fileName = "day18_test.txt"
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

	all_trees := make([]string, 0, 50)
	for scanner.Scan() {
		all_trees = append(all_trees, scanner.Text())
	}

	var tree *Tree
	for _, t := range all_trees {
		new_tree := createTree(t, nil)
		tree = add(tree, new_tree)
		tree.reduce()
	}
	fmt.Println("Final tree =", tree)
	fmt.Println("Final tree value", tree.getValue())

	maxSum := 0
	for t1 := 0; t1 < len(all_trees); t1++ {
		for t2 := 0; t2 < len(all_trees); t2++ {
			if t1 == t2 {
				continue
			}
			// lol
			treeSum := add(createTree(all_trees[t1], nil), createTree(all_trees[t2], nil))
			treeSum.reduce()
			val := treeSum.getValue()
			//fmt.Println("Tree", t1, "and", t2, "=", val)
			if val > maxSum {
				maxSum = val
			}
		}
	}
	fmt.Println("Maximum tree sum =", maxSum)

}
