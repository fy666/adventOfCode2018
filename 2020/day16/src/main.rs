use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs;

fn puzzle1(nearby: &Vec<Vec<i32>>, rules: &HashMap<String, Vec<i32>>) {
    let mut count_invalid = 0;
    for ticket in nearby.iter().flatten() {
        let mut found = false;
        for value in rules.values() {
            if value.contains(ticket) {
                found = true;
                break;
            }
        }
        if !found {
            count_invalid += ticket;
        }
    }
    println!("Invalid tickets : {}", count_invalid);
}

fn is_valid(ticket: &Vec<i32>, rules: &HashMap<String, Vec<i32>>) -> bool {
    for t in ticket {
        let mut found = false;
        for value in rules.values() {
            if value.contains(t) {
                found = true;
            }
        }
        if !found {
            return false;
        }
    }
    true
}

fn reduce(keys: &mut HashMap<String, Vec<i32>>) {
    let mut already_skipped: Vec<i32> = Vec::new();
    while keys.iter().filter(|(_key, val)| val.len() == 1).count() != keys.len() {
        let num_to_skip = keys
            .values()
            .find(|val| val.len() == 1 && !already_skipped.contains(&val[0]))
            .unwrap()[0];
        already_skipped.push(num_to_skip);
        for val in keys.values_mut() {
            if val.len() > 1 && val.contains(&num_to_skip) {
                val.retain(|&x| x != num_to_skip);
            }
        }
    }
}

fn puzzle2(nearby: &Vec<Vec<i32>>, rules: &HashMap<String, Vec<i32>>, ticket: &Vec<i32>) {
    let valid_tickets: Vec<Vec<i32>> = nearby
        .iter()
        .filter(|x| is_valid(x, rules))
        .cloned()
        .collect();
    println!("Valid tickets : {}", &valid_tickets.len());
    let mut keys: HashMap<String, Vec<i32>> = HashMap::new();
    for (key, value) in rules {
        let mut result: Vec<i32> = Vec::new();
        for col in 0..valid_tickets[0].len() {
            let num = valid_tickets
                .iter()
                .filter(|x| value.contains(&x[col]))
                .count();
            //println!("{} on {} column : {} valid", key, col, num);
            if num == valid_tickets.len() {
                result.push(col as i32);
            }
        }
        keys.insert(key.to_string(), result);
    }

    println!("Fields possibilities : {:?}", keys);
    reduce(&mut keys);
    println!("After redution {:?}", keys);
    let mut count: i64 = 1;
    for (_key, value) in keys.iter().filter(|(key, _v)| key.starts_with("departure")) {
        count *= ticket[value[0] as usize] as i64;
    }
    println!("Product of departures fields = {}", count);
}

fn parse_rules(input: &Vec<&str>) -> HashMap<String, Vec<i32>> {
    let re_rule = Regex::new(r"(.*): ([0-9]*)\-([0-9]*) or ([0-9]*)\-([0-9]*)").unwrap();
    let mut result: HashMap<String, Vec<i32>> = HashMap::new();
    for i in input {
        let tmp = re_rule.captures(i).unwrap();
        let mut valid: Vec<i32> = Vec::new();
        valid.extend(tmp[2].parse::<i32>().unwrap()..tmp[3].parse::<i32>().unwrap() + 1);
        valid.extend(tmp[4].parse::<i32>().unwrap()..tmp[5].parse::<i32>().unwrap() + 1);
        result.insert(tmp[1].to_string(), valid);
    }
    println!("Found {} rules", result.len());
    result
}

fn parse_ticket(input: &Vec<&str>) -> Vec<Vec<i32>> {
    let result: Vec<Vec<i32>> = input
        .iter()
        .skip(1)
        .map(|x| x.split(',').map(|x| x.parse::<i32>().unwrap()).collect())
        .collect();
    println!("Collected {} tickets", result.len());
    result
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n\n");
    let data = split.collect::<Vec<&str>>();
    let your_ticket = parse_ticket(&data[1].split('\n').collect::<Vec<&str>>())[0].clone();
    println!("Your ticket : {:?}", your_ticket);
    let nearby_tickets = parse_ticket(&data[2].split('\n').collect::<Vec<&str>>());
    let rules = parse_rules(&data[0].split('\n').collect::<Vec<&str>>());
    puzzle1(&nearby_tickets, &rules);
    puzzle2(&nearby_tickets, &rules, &your_ticket);
}
