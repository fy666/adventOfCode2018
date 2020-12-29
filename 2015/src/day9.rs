use itertools::Itertools;
use onig::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

fn total_distance(trip: &Vec<&String>, map: &HashMap<(String, String), i32>) -> i32 {
    let mut d = 0;
    for w in trip.windows(2) {
        let tup = (w[0].to_string(), w[1].to_string());
        d += map.get(&tup).unwrap();
    }
    d
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} distances", data.len());
    let mut city_map: HashMap<(String, String), i32> = HashMap::new();
    let mut all_cities: HashSet<String> = HashSet::new();
    let regex = Regex::new(r"(.*) to (.*) = (.*)").unwrap();
    for trip in data {
        let capture = regex.captures(trip).unwrap();
        let city1: String = capture.at(1).unwrap().parse().unwrap();
        let city2: String = capture.at(2).unwrap().parse().unwrap();
        let d: i32 = capture.at(3).unwrap().parse().unwrap();
        city_map.insert((city1.clone(), city2.clone()), d);
        city_map.insert((city2.clone(), city1.clone()), d);
        all_cities.insert(city1);
        all_cities.insert(city2);
    }
    log::trace!("City map = {:?}", city_map);
    log::trace!("All cities = {:?}", all_cities);
    let trip: Vec<String> = all_cities.into_iter().collect();

    let mut min_d: i32 = city_map.values().sum();
    let mut max_d = 0;
    for perm in trip.iter().permutations(trip.len()).unique() {
        let d_loc = total_distance(&perm, &city_map);
        if d_loc < min_d {
            min_d = d_loc;
        }
        if d_loc > max_d {
            max_d = d_loc;
        }
    }
    log::info!(
        "🎅 min trip distance = {}, max trip distance = {}",
        min_d,
        max_d,
    );
}
