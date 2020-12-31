use onig::Regex;
use std::collections::HashMap;
use std::fs;

fn apply(
    txt: &str,
    regex: &Regex,
    led_board: &mut HashMap<(i32, i32), bool>,
    led_board_intensity: &mut HashMap<(i32, i32), i32>,
) {
    let capture = regex.captures(txt).unwrap();
    let action = capture.at(1).unwrap();
    let start: (i32, i32) = (
        capture.at(2).unwrap().parse().unwrap(),
        capture.at(3).unwrap().parse().unwrap(),
    );
    let end: (i32, i32) = (
        capture.at(4).unwrap().parse().unwrap(),
        capture.at(5).unwrap().parse().unwrap(),
    );
    for i in start.0..end.0 + 1 {
        for j in start.1..end.1 + 1 {
            if action == "turn on" {
                *led_board.entry((i, j)).or_insert(false) = true;
                *led_board_intensity.entry((i, j)).or_insert(0) += 1;
            } else if action == "turn off" {
                *led_board.entry((i, j)).or_insert(false) = false;
                let val = led_board_intensity.entry((i, j)).or_insert(0);
                if *val > 0 {
                    *val -= 1;
                }
            } else if action == "toggle" {
                let val = led_board.entry((i, j)).or_insert(false);
                *val = !*val;
                *led_board_intensity.entry((i, j)).or_insert(0) += 2;
            } else {
                log::warn!("Action not handled {}", action);
            }
        }
    }
    log::debug!("Action {}, start {:?} end {:?}", action, start, end);
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} instructions", data.len());
    let mut led_board: HashMap<(i32, i32), bool> = HashMap::new();
    let mut led_board_intensity: HashMap<(i32, i32), i32> = HashMap::new();
    let regex =
        Regex::new(r"(toggle|turn on|turn off) ([0-9]*),([0-9]*) through ([0-9]*),([0-9]*)")
            .unwrap();
    for instr in data {
        apply(instr, &regex, &mut led_board, &mut led_board_intensity);
    }

    log::info!(
        "{} 💡, average intensity : {}",
        led_board.values().filter(|x| **x).count(),
        led_board_intensity.values().sum::<i32>()
    );
}
