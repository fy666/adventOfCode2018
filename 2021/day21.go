package main

import (
	"flag"
	"fmt"
	"math"
)

type Player struct {
	score    int
	position int
	id       int
}

type Dice struct {
	value int
	turns int
}

func (d *Dice) String() string {
	return fmt.Sprintf("Dice turns = %d, val = %d", d.turns, d.value)
}

func (p *Player) String() string {
	return fmt.Sprintf("Player %d, position %d, has score %d", p.id, p.position, p.score)

}

func fakeModulo(value int, mod int) int {
	return (value-1)%mod + 1
}

func (d *Dice) roll3() int {
	sum := d.value
	var tmp [3]int
	tmp[0] = sum
	d.value = fakeModulo(d.value+1, 100)
	sum += d.value
	tmp[1] = d.value
	d.value = fakeModulo(d.value+1, 100)
	sum += d.value
	tmp[2] = d.value
	d.value = fakeModulo(d.value+1, 100)
	d.turns += 3
	return sum
}

func (p *Player) play(d *Dice) {
	turn := d.roll3()
	p.position += turn
	p.position = fakeModulo(p.position, 10)
	p.score += p.position
	//fmt.Printf("Player %d, roll %d, goes to %d has score %d \n", p.id, turn, p.position, p.score)
	return
}

func (p *Player) wins(val int) bool {
	return p.score >= val
}

func coutWins(state [5]int, probs *map[int]int, stateCounts *map[[5]int][2]int64) [2]int64 { // Second part
	if val, found := (*stateCounts)[state]; found {
		return val
	}
	var result [2]int64
	for roll, proba := range *probs {
		new_state := state
		turn := new_state[4]
		new_state[turn+2] = fakeModulo(new_state[turn+2]+roll, 10)
		new_state[turn] += new_state[turn+2]
		new_state[4] = (new_state[4] + 1) % 2
		//fmt.Println("Rolling", roll, "on state", state, "new = ", new_state)
		if new_state[0] >= 21 {
			result[0] += int64(proba)
		} else if new_state[1] >= 21 {
			result[1] += int64(proba)
		} else {
			sub_result := coutWins(new_state, probs, stateCounts)
			result[0] += sub_result[0] * int64(proba)
			result[1] += sub_result[1] * int64(proba)
		}
	}
	(*stateCounts)[state] = result
	return result
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()

	s1 := 8
	s2 := 3
	if *test {
		s1 = 4
		s2 = 8
	}

	player1 := &Player{0, s1, 1}
	player2 := &Player{0, s2, 2}
	dice := &Dice{1, 0}
	val_to_win := 1000

	for !player2.wins(val_to_win) {
		player1.play(dice)
		if player1.wins(val_to_win) {
			break
		}
		player2.play(dice)
	}

	fmt.Println("Player 1", player1)
	fmt.Println("Player 2", player2)
	fmt.Println(dice)
	if player1.wins(val_to_win) {
		fmt.Println("Part 1 result =", dice.turns*player2.score)
	} else {
		fmt.Println("Part 1 result =", dice.turns*player1.score)
	}
	// Second part
	probs := map[int]int{9: 1, 3: 1, 6: 7, 7: 6, 5: 6, 8: 3, 4: 3}
	state := [5]int{0, 0, s1, s2, 0}
	stateCounts := make(map[[5]int][2]int64)
	res := coutWins(state, &probs, &stateCounts)
	fmt.Println("Count wins =", res)
	fmt.Printf("Max number of wins = %.f \n", math.Max(float64(res[0]), float64(res[1])))
	fmt.Println("Number of states =", len(stateCounts))
}
