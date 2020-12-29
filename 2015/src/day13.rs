use itertools::Itertools;
use onig::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

fn get_ordered_tup<'a>(a: &'a str, b: &'a str) -> (&'a str, &'a str) {
    if a > b {
        return (a, b);
    }
    (b, a)
}

fn compute_hapiness(sitting: &Vec<&str>, wishes: &HashMap<(&str, &str), i32>) -> i32 {
    let mut d = 0;
    for w in sitting.windows(2) {
        let tup = get_ordered_tup(w[0], w[1]);
        d += wishes.get(&tup).unwrap_or(&0);
    }
    let tup = get_ordered_tup(*sitting.last().unwrap(), *sitting.first().unwrap());
    d += wishes.get(&tup).unwrap_or(&0);
    d
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} guest wishes 🍽️", data.len());
    let mut whishes: HashMap<_, i32> = HashMap::new();
    let mut guests: HashSet<_> = HashSet::new();
    let regex = Regex::new(r"(.*) would (gain|lose) (.*) happiness units by sitting next to (.*).")
        .unwrap();
    for whish in data {
        let capture = regex.captures(whish).unwrap();
        let guest1 = capture.at(1).unwrap();
        let guest2 = capture.at(4).unwrap();
        let mut hapiness_unit: i32 = capture.at(3).unwrap().parse().unwrap();
        if capture.at(2).unwrap() == "lose" {
            hapiness_unit = -hapiness_unit;
        }
        let tup = get_ordered_tup(guest1, guest2);
        *whishes.entry(tup).or_insert(0) += hapiness_unit;
        guests.insert(guest1);
        guests.insert(guest2);
    }
    log::trace!("Guest wishes = {:?}", whishes);
    log::trace!("Guest list = {:?}", guests);

    let mut sitting: Vec<&str> = guests.into_iter().collect();
    let mut max_happy = 0;
    for perm in sitting.iter().copied().permutations(sitting.len()) {
        let happiness = compute_hapiness(&perm, &whishes);
        if happiness > max_happy {
            max_happy = happiness;
        }
    }
    log::info!("🍽️  max hapiness = {}", max_happy);

    max_happy = 0;
    sitting.push("Florence");
    for perm in sitting.iter().copied().permutations(sitting.len()) {
        let happiness = compute_hapiness(&perm, &whishes);
        if happiness > max_happy {
            max_happy = happiness;
        }
    }
    log::info!("🍽️  max hapiness with Florence 🥰 at table = {}", max_happy);
}
