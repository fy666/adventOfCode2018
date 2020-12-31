pub fn run() {
    let data = "yzbqklnj";
    let mut puzzle1 = 1;
    let mut puzzle2 = 1;
    loop {
        let digest = md5::compute(format!("{}{}", data, puzzle1));
        let tmp: String = format!("{:?}", digest);
        if tmp.starts_with("00000") {
            break;
        }
        if tmp.starts_with("000000") {
            puzzle2 = puzzle1;
        }
        puzzle1 += 1;
    }
    loop {
        let digest = md5::compute(format!("{}{}", data, puzzle2));
        let tmp: String = format!("{:?}", digest);
        if tmp.starts_with("000000") {
            break;
        }
        puzzle2 += 1;
    }
    log::info!("Puzzle 1: 🔑 {}, Puzzle 2: 🔑 {}", puzzle1, puzzle2);
}
