package main

import (
	"flag"
	"fmt"
)

func max(data []int) (res int) {
	res = data[0]
	for _, v := range data {
		if v > res {
			res = v
		}
	}
	return
}

type Trajectory struct {
	x, y        int
	vx, vy      int
	y_positions []int
}

func (t *Trajectory) step() {
	t.x += t.vx
	t.y += t.vy
	if t.vx > 0 {
		t.vx -= 1
	} else if t.vx < 0 {
		t.vx += 1
	}
	t.vy -= 1
	t.y_positions = append(t.y_positions, t.y)
}

func (t *Trajectory) run(area [4]int) (int, bool) {
	for t.x < area[1] && t.y > area[2] {
		t.step()
		if t.x >= area[0] && t.x <= area[1] && t.y >= area[2] && t.y <= area[3] {
			return max(t.y_positions), true
		}
	}
	return 0, false
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()

	area := [4]int{287, 309, -76, -48}
	if *test {
		area = [4]int{20, 30, -10, -5}
	}
	fmt.Println("Target area:", area)
	if true {
		best_height := 0
		best_vx := 0
		best_vy := 0
		valid_shoot := 0
		for vx := 0; vx < 500; vx++ {
			for vy := -500; vy < 500; vy++ {
				traj := Trajectory{x: 0, y: 0, y_positions: make([]int, 0, 50), vx: vx, vy: vy}
				maxh, isValid := traj.run(area)
				if isValid {
					valid_shoot += 1
				}
				if maxh > best_height {
					best_vx = vx
					best_vy = vy
					best_height = maxh
				}
			}
		}
		fmt.Println("Best height at", best_height, "starting with", best_vx, ",", best_vy)
		fmt.Println(valid_shoot, "valid shoots")
	}
}
