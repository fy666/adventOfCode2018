//use regex::Regex;
//use std::collections::HashMap;
//use std::collections::HashSet;
use std::collections::VecDeque;
use std::env;
use std::fs;

fn play_game1(mut player1: VecDeque<i32>, mut player2: VecDeque<i32>) {
    while player1.len() != 0 && player2.len() != 0 {
        let val1 = player1.pop_front().unwrap();
        let val2 = player2.pop_front().unwrap();
        if val1 > val2 {
            player1.push_back(val1);
            player1.push_back(val2);
        } else {
            player2.push_back(val2);
            player2.push_back(val1);
        };
    }

    let count: i32 = player1
        .iter()
        .enumerate()
        .map(|(ix, val)| *val * (player1.len() - ix) as i32)
        .sum();
    let count2: i32 = player2
        .iter()
        .enumerate()
        .map(|(ix, val)| *val * (player2.len() - ix) as i32)
        .sum();
    println!("player 1 count {}, player2 count = {}", count, count2);
}

fn recursive_play(
    mut player1: VecDeque<i32>,
    mut player2: VecDeque<i32>,
    game: i32,
) -> (bool, VecDeque<i32>) {
    println!(
        "Playing game {}, p1 ={:?}, p2= {:?}",
        game, player1, player2
    );
    let mut all_decks: Vec<VecDeque<i32>> = Vec::new();
    let mut round = 1;
    while player1.len() != 0 && player2.len() != 0 {
        if all_decks.contains(&player1) {
            return (true, player1);
        }
        all_decks.push(player1.clone());
        let val1 = player1.pop_front().unwrap();
        let val2 = player2.pop_front().unwrap();
        println!(
            "game {} round {} p1 plays {} ({}), p2 plays {} ({})",
            game,
            round,
            val1,
            player1.len(),
            val2,
            player2.len()
        );
        if val1 <= player1.len() as i32 && val2 <= player2.len() as i32 {
            let new_deck1 = VecDeque::from(Vec::from(player1.clone())[..val1 as usize].to_vec());
            let new_deck2 = VecDeque::from(Vec::from(player2.clone())[..val2 as usize].to_vec());
            let one_is_winner = recursive_play(new_deck1, new_deck2, game + 1);
            if one_is_winner.0 {
                player1.push_back(val1);
                player1.push_back(val2);
            } else {
                player2.push_back(val2);
                player2.push_back(val1);
            }
        } else {
            if val1 > val2 {
                player1.push_back(val1);
                player1.push_back(val2);
            //println!("Playing 1 wins game {} round {}", game, round);
            } else {
                player2.push_back(val2);
                player2.push_back(val1);
                //println!("Playing 2 wins game {} round {}", game, round);
            }
        }
        round += 1;
    }
    if player1.len() != 0 {
        return (true, player1);
    } else {
        return (false, player2);
    }
}

fn play_game2(mut player1: VecDeque<i32>, mut player2: VecDeque<i32>) {
    let one_is_winner = recursive_play(player1.clone(), player2.clone(), 1);
    if one_is_winner.0 {
        println!("player 1 won with deck {:?}", one_is_winner.1);
    } else {
        println!("player 2 won with deck {:?}", one_is_winner.1);
    }

    let count: i32 = one_is_winner
        .1
        .iter()
        .enumerate()
        .map(|(ix, val)| *val * (one_is_winner.1.len() - ix) as i32)
        .sum();
    println!("count {}", count);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let mut split = text.trim().split("\n\n");
    let player1: VecDeque<i32> = split
        .next()
        .unwrap()
        .split('\n')
        .skip(1)
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    let player2: VecDeque<i32> = split
        .next()
        .unwrap()
        .split('\n')
        .skip(1)
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    println!("Player 1 : {:?}", player1);
    println!("Player 2 : {:?}", player2);
    //play_game1(player1.clone(), player2.clone());
    play_game2(player1.clone(), player2.clone());
}
