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
	return &Tree{t1, 0, t2, nil}
}

func (t *Tree) Split() bool {
	if t == nil {
		return false
	}
	if t.Right == nil && t.Left == nil {
		//fmt.Println("Value =", t.Value)
		if t.Value >= 10 {
			//fmt.Println("Value above 10")
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

func (t *Tree) AddLeftMost(explodingTree *Tree, value int) {
	if t == nil {
		return
	}
	if t.Right == nil || t.Right == explodingTree {
		if t.Parent != nil && t.Parent.Right != t {
			if t.Parent.Right == t {
				t.Parent.AddLeftMost(t, value)
			} else {
				t.Parent.AddRightMost(t, value)
			}
		}
		return
	}
	if t.Right != nil && t.Right.Right == nil {
		//fmt.Println("LeftMost: adding", value, "to", t.Left.Value)
		t.Right.Value += value
	} else {
		t.Right.AddLeftMost(t, value)
	}
}
func (t *Tree) AddRightMost(explored *Tree, value int) {
	if t == nil {
		return
	}
	if t.Left == nil || t.Left == explored {
		if t.Parent != nil {
			if t.Parent.Right == t {
				t.Parent.AddLeftMost(t, value)
			} else {
				t.Parent.AddRightMost(t, value)
			}
		}
		return
	}
	if t.Left != nil && t.Left.Left == nil {
		//fmt.Println("RightMost: adding", value, "to", t.Right.Value)
		t.Left.Value += value
	} else {
		if t.Left != explored {
			t.Left.AddRightMost(t, value)
		}
	}
}

func (t *Tree) getHead() *Tree {
	if t.Parent != nil {
		return t.Parent.getHead()
	} else {
		return t
	}
}
func (t *Tree) Explode(level int) {
	if t == nil {
		return
	}
	//fmt.Println("Current tree = ", t.getHead().String())
	if level == 4 && t.Right != nil && t.Left != nil {
		//fmt.Println("Exploding", t.Left.Value, ",", t.Right.Value)

		left := t.Left.Value
		right := t.Right.Value
		t.Left = nil
		t.Right = nil
		t.Parent.AddLeftMost(t, left)
		t.Parent.AddRightMost(t, right)
	}
	//if t.Right != nil
	t.Left.Explode(level + 1)
	t.Right.Explode(level + 1)
	return
}

func createTree(data string, parent *Tree) (t *Tree) {
	current := &Tree{nil, 0, nil, parent}
	if data[0] == '[' {
		ix := getSplitIndex(data)
		//fmt.Println(data, ": split at", ix, " ->", data[1:ix], "and", data[ix+1:len(data)-1])
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
		t.Explode(0)
		//fmt.Println("After explode:", t)
		t.Split()
		//fmt.Println("After Split:", t)
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

	var tree *Tree
	for scanner.Scan() {
		number := scanner.Text()
		new_tree := createTree(number, nil)
		fmt.Println("to add =", new_tree)
		tree = add(tree, new_tree)
		fmt.Println("After add =", tree)
		tree.reduce()
		fmt.Println("After reduce =", tree)
		//fmt.Println("tree value", tree.getValue())
		//fmt.Println("Snail fish number =", number)
	}
	fmt.Println("Final tree =", tree)
	fmt.Println("Final tree value", tree.getValue())
	//return
	/*
		//t := createTree("[[2,[2,2]],[8,[8,1]]]", nil)
		t1 := createTree("[[[[[9,8],1],2],3],4]", nil)
		fmt.Println(t1.String(), t1.getValue())
		t2 := createTree("[10,11]", nil)
		fmt.Println(t2.String())
		t2 = add(t1, t2)
		fmt.Println(t2.String())
		t2.Split()
		fmt.Println(t2.String())
		fmt.Println(t1.String(), t1.getValue())
		t1.Explode(0)
		fmt.Println(t1.String())
		t3 := createTree("[7,[6,[5,[4,[3,2]]]]]", nil)
		t3.Explode(0)
		fmt.Println(t3)
	*/

	t4 := add(createTree("[[[[4,3],4],4],[7,[[8,4],9]]]", nil), createTree("[1,1]", nil))
	fmt.Println("Tree", t4)
	t4.reduce()
	fmt.Println("After reduce", t4, "=", t4.getValue())

	// t5 := createTree("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", nil)
	// t5.Explode(0)
	// fmt.Println("After reduce", t5)

}
