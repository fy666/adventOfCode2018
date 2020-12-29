//use itertools::Itertools;
use onig::Regex;
use std::collections::HashMap;
//use std::collections::HashSet;
use std::cmp;
use std::fs;

fn compute_score(quantities: &Vec<i32>, ingredients: &Vec<Vec<i32>>, check_calories: bool) -> i128 {
    let mut components: Vec<i128> = vec![0; ingredients[0].len()];
    for (iq, q) in quantities.iter().enumerate() {
        let tmp = &ingredients[iq];
        for (it, t) in tmp.iter().enumerate() {
            components[it] += (q * t) as i128;
        }
    }
    if check_calories && *components.last().unwrap() != 500 {
        return 0;
    }
    if components.iter().any(|&x| x < 0) {
        return 0;
    }
    components.iter().rev().skip(1).product::<i128>()
}

fn get_perm(mut input: Vec<i32>, wanted_sum: i32, index: usize) -> Vec<Vec<i32>> {
    let mut result: Vec<Vec<_>> = Vec::new();
    if index == input.len() - 1 {
        let s: i32 = input.iter().copied().sum::<i32>();
        let end = wanted_sum - s;
        for i in 1..end + 1 {
            if i + s == wanted_sum {
                input[index] = i;
                result.push(input.clone());
            }
        }
    } else {
        let s: i32 = input.iter().copied().sum::<i32>();
        let end = wanted_sum - s;
        for i in 1..end + 1 {
            input[index] = i;
            result.extend(get_perm(input.clone(), wanted_sum, index + 1));
        }
    }
    result
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} ingredients 🍽️", data.len());
    let mut ingredients: HashMap<&str, Vec<i32>> = HashMap::new();
    let mut vec_ingredients: Vec<Vec<i32>> = Vec::new();

    let regex = Regex::new(
        r"(.*): capacity ([-\d]*), durability ([-\d]*), flavor ([-\d]*), texture ([-\d]*), calories ([-\d]*)",
    )
    .unwrap();
    for ingr in data {
        let mut tmp: Vec<i32> = Vec::new();
        let capture = regex.captures(ingr).unwrap();
        let ingr = capture.at(1).unwrap();
        for i in 2..7 {
            tmp.push(capture.at(i).unwrap().parse().unwrap());
        }
        vec_ingredients.push(tmp.clone());
        ingredients.insert(ingr, tmp);
    }
    log::trace!("Ingredient list = {:?}", ingredients);
    log::trace!("Ingredient list = {:?}", vec_ingredients);
    // Computes all combinations
    let input = vec![0; vec_ingredients.len()];
    let test = get_perm(input, 100, 0);
    log::debug!("{} combinations found", test.len());
    let mut max_score = 0;
    let mut max_score_calories = 0;
    for t in test.iter() {
        max_score = cmp::max(max_score, compute_score(&t, &vec_ingredients, false));
        max_score_calories = cmp::max(
            max_score_calories,
            compute_score(&t, &vec_ingredients, true),
        );
    }

    log::info!("🍪 max score = {}", max_score);
    log::info!(
        "🍪 with exaclty 500 calories, max score = {}",
        max_score_calories
    );
}
