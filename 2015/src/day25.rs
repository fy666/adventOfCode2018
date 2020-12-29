fn get_number(row: i32, column: i32) -> i32 {
    let diag = column + row - 1;
    let mut start_diag: i32 = (0..diag).sum();
    start_diag += 1;
    log::debug!(
        "{},{} : diag {} starts at {}, position {}",
        row,
        column,
        diag,
        start_diag,
        start_diag + column - 1
    );
    start_diag + column - 1
}

fn op(input: u64) -> u64 {
    (input * 252533).rem_euclid(33554393)
}

pub fn run(test: bool) {
    if test {
        get_number(2, 5);
        let n = get_number(5, 3);
        let mut num: u64 = 20151125;
        for _ in 1..n {
            num = op(num);
            //log::trace!("{}", num);
        }
        log::info!("Code for 5,3 is {}", num);
    } else {
        let row = 2978;
        let column = 3083;
        let n = get_number(row, column);
        let mut num: u64 = 20151125;
        for _ in 1..n {
            num = op(num);
        }
        log::info!("❄️ Snow machine code : {}", num);
    }
}
