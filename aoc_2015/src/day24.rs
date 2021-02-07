use itertools::Itertools;
//use std::collections::HashMap;
use std::fs;

fn puzzle(data: &Vec<u64>, parts: u64) -> u64 {
    let s: u64 = data.iter().sum();
    let target = s / parts;
    let mut prod = u64::MAX;
    log::debug!("For {} parts, target = {}", parts, target);
    for i in 1..data.len() {
        let mut found = false;
        for c in data.iter().copied().combinations(i) {
            let tmp: u64 = c.iter().copied().sum();
            if tmp == target {
                found = true;
                let tmp_prod: u64 = c.iter().copied().product();
                if tmp_prod < prod {
                    prod = tmp_prod;
                    log::trace!("{:?} : product = {}", c, tmp_prod);
                }
            }
        }
        if found {
            break;
        }
    }
    prod
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let mut data: Vec<u64> = text.lines().map(|x| x.parse().unwrap()).collect();
    let s: u64 = data.iter().sum();
    log::debug!("Imported {} numbers, sum = {}", data.len(), s);
    data.reverse();
    let part1 = puzzle(&data, 3);
    let part2 = puzzle(&data, 4);

    log::info!("🎁 ⚖️  for 3: {}, for 4: {}", part1, part2);
}
