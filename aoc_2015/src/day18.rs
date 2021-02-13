use ndarray::{s, Array2};
use std::cmp;
use std::fs;

fn iter_once(arr: &Array2<i32>, broken_leds: bool) -> Array2<i32> {
    let mut res = arr.clone();
    let x_n = arr.shape()[0];
    let y_n = arr.shape()[1];
    for ((x, y), val) in arr.indexed_iter() {
        let slice = arr.slice(s![
            cmp::max(x.saturating_sub(1), 0)..cmp::min(x + 2, x_n),
            cmp::max(y.saturating_sub(1), 0)..cmp::min(y + 2, y_n)
        ]);
        let neighbors = slice.sum() - val;
        log::trace!("{:?} {:?}: val {}", x, y, val);
        log::trace!("slice\n{:?}\n = {}", slice, neighbors);
        if *val == 1 && (neighbors < 2 || neighbors > 3) {
            res[[x, y]] = 0;
        }
        if *val == 0 && neighbors == 3 {
            res[[x, y]] = 1;
        }
    }
    if broken_leds {
        turn_on_corners(&mut res);
    }
    res
}

fn turn_on_corners(arr: &mut Array2<i32>) {
    let x_n = arr.shape()[0] - 1;
    let y_n = arr.shape()[1] - 1;
    arr[[0, 0]] = 1;
    arr[[x_n, 0]] = 1;
    arr[[0, y_n]] = 1;
    arr[[x_n, y_n]] = 1;
}

fn char_to_led(input: &char) -> i32 {
    if *input == '#' {
        return 1;
    } else {
        return 0;
    }
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<i32> = text
        .lines()
        .flat_map(|l| l.chars().map(|x| char_to_led(&x)))
        .collect();
    let grid = (data.len() as f32).sqrt() as usize;

    log::debug!("Imported grid of {}", grid);
    let mut steps = 101;
    if grid == 6 {
        steps = 5; // if test mode
    }
    let arr = Array2::from_shape_vec((grid, grid), data).unwrap();

    let mut res = arr.clone();
    for step in 1..steps {
        res = iter_once(&res, false);
        log::debug!("After {} step:\n{:?}", step, res);
    }

    let mut res2 = arr.clone();
    turn_on_corners(&mut res2);
    log::debug!("First:\n{:?}", res2);
    for step in 1..steps {
        res2 = iter_once(&res2, true);
        log::debug!("After {} step:\n{:?}", step, res2);
    }
    log::info!("Part 1: {} 💡, part 2: {} 💡", res.sum(), res2.sum());
}
