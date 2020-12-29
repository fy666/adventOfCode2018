use itertools::Itertools;
use std::cmp::min;
use std::fs;

pub fn run(file: &String, test: bool) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<i32> = text
        .trim()
        .split("\n")
        .map(|x| x.parse().unwrap())
        .collect();
    log::debug!("Imported {} cups 🥤", data.len());
    log::trace!("Cups list {:?}", data);
    let mut goal = 150;
    if test {
        goal = 25;
    }

    let mut valid_combinations = 0;
    let mut min_size = data.len();
    for num_cups in 1..data.len() {
        for combi in data.iter().copied().combinations(num_cups) {
            let loc_sum = combi.iter().sum::<i32>();
            if loc_sum == goal {
                valid_combinations += 1;
                min_size = min(min_size, combi.len());
            }
        }
    }
    log::info!(
        "{} combinations of 🥤 could hold {}L of eggnog, min number of 🥤 required = {}",
        valid_combinations,
        goal,
        min_size
    );
}
