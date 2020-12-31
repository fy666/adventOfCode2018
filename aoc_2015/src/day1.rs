use std::fs;

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    log::debug!("Imported {} chars", text.len());
    let mut floor: i32 = 0;
    let mut first_pos: i32 = -1;
    for (ix, c) in text.chars().enumerate() {
        match c {
            '(' => floor = floor + 1,
            ')' => floor = floor - 1,
            '\n' => (),
            _ => log::trace!("Untreated char : {}", c),
        }
        if floor == -1 && first_pos == -1 {
            first_pos = ix as i32;
            first_pos += 1;
        }
    }
    log::info!(
        "🏡 Final floor {}, first position to basement {}",
        floor,
        first_pos
    );
}
