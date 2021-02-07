use std::fs;

fn apply_instr(reg: &mut i32, instr: &str) {
    match instr {
        "inc" => *reg = *reg + 1,
        "tpl" => *reg = *reg * 3,
        "hlf" => *reg = *reg / 2,
        _ => log::warn!("inst {} not covered", instr),
    }
}

fn puzzle(data: &Vec<&str>, mut a: i32) -> i32 {
    log::trace!("--------------------------------");
    let mut b = 0;
    let mut pc: i32 = 0;

    while pc < data.len() as i32 {
        let instr = data[pc as usize];
        log::trace!("Instr {} ({}), a={}, b={}", pc, instr, a, b);
        if instr.starts_with("jmp") {
            let j: i32 = instr[4..].parse().unwrap();
            log::trace!("Jump of {}", j);
            pc += j;
            continue;
        } else if instr.contains(",") {
            let j: i32 = instr[7..].parse().unwrap();
            let value;
            if &instr[4..5] == "a" {
                value = a;
            } else {
                value = b;
            }
            let need_jump = (instr.starts_with("jie") && value % 2 == 0)
                || (instr.starts_with("jio") && value == 1);
            if need_jump {
                pc += j;
                log::trace!("Conditionnal jump  of {}", j);
                continue;
            }
        } else {
            if &instr[4..5] == "a" {
                apply_instr(&mut a, &instr[..3]);
            } else {
                apply_instr(&mut b, &instr[..3]);
            }
        }
        pc += 1;
    }
    b
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} instructions", data.len());

    let part1 = puzzle(&data, 0);
    let part2 = puzzle(&data, 1);

    log::info!("🖥️ 💾 part 1 {}, part 2 {}", part1, part2);
}
