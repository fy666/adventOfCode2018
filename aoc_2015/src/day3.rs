use std::collections::HashMap;
use std::fs;

pub fn get_pos(mov: char, pos: &(i32, i32)) -> (i32, i32) {
    match mov {
        '>' => return (pos.0 + 1, pos.1),
        '<' => return (pos.0 - 1, pos.1),
        '^' => return (pos.0, pos.1 + 1),
        'v' => return (pos.0, pos.1 - 1),
        _ => log::warn!("! {} not a valid move", mov),
    };
    *pos
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let mut all_positions_puzzle1: HashMap<(i32, i32), i32> = HashMap::new();
    let mut all_positions_puzzle2: HashMap<(i32, i32), i32> = HashMap::new();
    log::debug!("Imported {} moves", text.len());

    let mut position = (0, 0); // starting point
    let mut santa_position = (0, 0); // starting point for santa
    let mut robot_position = (0, 0); // starting point for robot
    *all_positions_puzzle1.entry(position).or_insert(0) += 1;
    *all_positions_puzzle2.entry(position).or_insert(0) += 1;
    for (ix, c) in text.trim().chars().enumerate() {
        if ix % 2 == 0 {
            santa_position = get_pos(c, &santa_position);
            *all_positions_puzzle2.entry(santa_position).or_insert(0) += 1;
        } else {
            robot_position = get_pos(c, &robot_position);
            *all_positions_puzzle2.entry(robot_position).or_insert(0) += 1;
        }
        position = get_pos(c, &position);
        *all_positions_puzzle1.entry(position).or_insert(0) += 1;
    }
    log::info!(
        "🎅 alone visited {} 🏡, 🎅 and 🤖 visited {} 🏡",
        all_positions_puzzle1.len(),
        all_positions_puzzle2.len()
    );
}
