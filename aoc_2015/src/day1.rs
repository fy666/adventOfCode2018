use std::fs;

pub fn day1(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    println!("Imported {} chars", text.len());
    let mut floor: i32 = 0;
    let mut first_pos: i32 = -1;
    for (ix, c) in text.chars().enumerate() {
        match c {
            '(' => floor = floor + 1,
            ')' => floor = floor - 1,
            '\n' => (),
            _ => println!("Untreated char : {}", c),
        }
        if floor == -1 && first_pos == -1 {
            first_pos = ix as i32;
            first_pos += 1;
        }
    }
    println!(
        "🏡 Final floor {}, first position to basement {}",
        floor, first_pos
    );
}
