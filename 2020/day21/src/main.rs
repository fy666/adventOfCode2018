//use regex::Regex;
use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;

use std::env;
use std::fs;

fn get_food_list(input: &Vec<&str>) {
    let mut allergens: HashMap<String, HashSet<String>> = HashMap::new();
    let mut foods: HashMap<String, i32> = HashMap::new();
    for item in input.iter() {
        //let mut all = item.split("(contains ");
        let allergen = item
            .split(" (contains ")
            .nth(1)
            .unwrap()
            .replace(")", "")
            .split(", ")
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        let food_items = item
            .split(" (contains ")
            .next()
            .unwrap()
            .split(' ')
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        for all in allergen.iter() {
            if !allergens.contains_key(all) {
                allergens.insert(
                    all.to_string(),
                    food_items.clone().into_iter().collect::<HashSet<String>>(),
                );
            } else {
                let poss = allergens.get_mut(&all.to_string()).unwrap();
                let tmp = poss
                    .intersection(&food_items.clone().into_iter().collect::<HashSet<String>>())
                    .map(|x| x.to_string())
                    .collect::<HashSet<String>>();
                *poss = tmp.clone();
            }
        }

        for f in food_items {
            *foods.entry(f.to_string()).or_insert(0) += 1;
        }
    }
    //println!("Hash is {:?}", allergens);
    //tiles.push(parse_tile(&s.split('\n').collect::<Vec<&str>>()));
    let mut all_allergens: Vec<String> = Vec::new();
    for i in allergens.values() {
        for j in i {
            all_allergens.push(j.to_string());
        }
    }
    let mut count = 0;
    for (key, val) in foods {
        if !all_allergens.contains(&key) {
            count += val;
        }
    }
    println!("Part 1: non allergens found {} times", count);

    let mut unique_allergens: HashMap<String, String> = HashMap::new();
    while allergens.values().flatten().count() > 0 {
        let mut single_elem: String = String::new();
        for (key, val) in allergens.iter() {
            if val.len() == 1 {
                single_elem = val.iter().next().unwrap().to_string();
                unique_allergens.insert(key.to_string(), single_elem.to_string());
                break;
            }
        }

        for i in allergens.values_mut() {
            i.remove(&single_elem);
        }
    }

    println!("Unique allergens : {:?}", unique_allergens);

    println!(
        "Part 2:\n{}",
        unique_allergens
            .iter()
            .sorted_by_key(|x| x.0)
            .map(|x| x.1)
            .format(",")
            .to_string()
            .replace("\"", "")
    );
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split('\n');
    let data = split.collect::<Vec<&str>>();
    get_food_list(&data);
}
