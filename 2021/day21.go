package main

import (
	"flag"
	"fmt"
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

type QuantumDice struct {
	value int
}

func (d *QuantumDice) getSumRoll() {
	//
}

func (d *Dice) String() string {
	return fmt.Sprintf("Dice turns = %d, val = %d", d.turns, d.value)
}

func (p *Player) String() string {
	return fmt.Sprintf("Player %d, position %d, has score %d", p.id, p.position, p.score)

}

func fakeModulo(value int, mod int) int {
	//res := value % mod
	//div := value / mod
	return (value-1)%mod + 1
	// if res == 0 {
	// 	return 1
	// }
	// return res
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
	//fmt.Println("Dice values", tmp, "sum=", sum)
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

func (p *Player) playRoll(roll int) {
	p.position += roll
	p.position = fakeModulo(p.position, 10)
	p.score += p.position
	fmt.Printf("Player %d, roll %d, goes to %d has score %d \n", p.id, roll, p.position, p.score)
	return
}

func (p *Player) wins(val int) bool {
	return p.score >= val
}

func run(player1 Player, player2 Player, seq []int) int {
	val_to_win := 21
	ix := 0
	for !player2.wins(val_to_win) && ix < len(seq) {
		player1.playRoll(seq[ix])
		ix += 1
		if player1.wins(val_to_win) || ix == len(seq) {
			break
		}
		player2.playRoll(seq[ix])
		ix += 1
	}

	if player1.wins(val_to_win) {
		return 1
	} else if player2.wins(val_to_win) {
		return 2
	} else {
		return 0
	}
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
	fmt.Println("Dice", dice)
	if player1.wins(val_to_win) {
		fmt.Println(dice.turns * player2.score)
	} else {
		fmt.Println(dice.turns * player1.score)
	}
	// Second part
	probs := map[int]int{9: 1, 3: 1, 6: 7, 7: 6, 5: 6, 8: 3, 4: 3}
	fmt.Println(probs)
	// Reset players
	player1 = &Player{0, s1, 1}
	player2 = &Player{0, s2, 2}
	fmt.Println(run(*player1, *player2, []int{9, 3}))
	fmt.Println(run(*player1, *player2, []int{9, 3, 9, 4, 9, 9, 9, 4, 4, 4, 9, 4}))

}
