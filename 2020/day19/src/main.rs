use regex::Regex;
use std::collections::HashMap;

use std::env;
use std::fs;

fn get_rules(input: &Vec<&str>) -> HashMap<usize, Vec<String>> {
    let mut rules: HashMap<usize, Vec<String>> = HashMap::new();
    let mut to_skip: Vec<usize> = Vec::new();
    let mut dummy = 0;
    while to_skip.len() != input.len() {
        for (line, i) in input.iter().enumerate() {
            if to_skip.contains(&line) {
                continue;
            }
            let num: usize = i.split(':').next().unwrap().parse().unwrap();
            let rule = i.split(": ").nth(1).unwrap();
            if rule == "\"a\"" || rule == "\"b\"" {
                rules.insert(num, vec![rule.replace("\"", "").replace(" ", "")]);
                to_skip.push(line);
            } else {
                let sub_rules: Vec<Vec<usize>> = rule
                    .split(" | ")
                    .map(|x| {
                        x.split(" ")
                            .filter(|&n| n != " ")
                            .map(|n| n.parse::<usize>().unwrap())
                            .collect()
                    })
                    .collect();
                let res = sub_rules
                    .iter()
                    .flatten()
                    .filter(|x| rules.contains_key(x))
                    .count();
                if res == sub_rules.iter().flatten().count() {
                    let mut tmp: Vec<String> = Vec::new();
                    for s in sub_rules {
                        let mut tmp_rule: Vec<String> = vec![String::from("")];
                        for n in s.iter() {
                            let mut modified_tmp_rule: Vec<String> = Vec::new();
                            for new_r in rules.get(&n).unwrap() {
                                for t in &tmp_rule {
                                    modified_tmp_rule.push(format!("{}{}", t, new_r));
                                }
                            }
                            tmp_rule = modified_tmp_rule.clone();
                        }
                        for t in tmp_rule {
                            tmp.push(t);
                        }
                    }
                    rules.insert(num, tmp);
                    to_skip.push(line);
                }
            }
        }
        dummy += 1;
    }
    println!(
        "After {} iterations, rule0 has {:?} candidates",
        dummy,
        rules.get(&0).unwrap().len()
    );
    rules
}

fn puzzle1(input: &Vec<&str>, rules: &HashMap<usize, Vec<String>>) {
    let rule_0 = rules.get(&0).unwrap();

    // Converting vector to hashmap to ease
    let mut valid: HashMap<&str, usize> = HashMap::new();
    for i in rule_0 {
        valid.insert(i, 0);
    }

    let mut count = 0;
    for i in input {
        if valid.contains_key(i) {
            count += 1
        }
    }
    println!("{} messages match rule 0", count);
}

fn puzzle2(input: &Vec<&str>, rules: &HashMap<usize, Vec<String>>) {
    // FORMING REGEX
    let rule_42 = rules.get(&42).unwrap();
    let rule_31 = rules.get(&31).unwrap();
    let mut r42_str = String::new();
    for r1 in rule_42 {
        r42_str += &format!("{}|", r1);
    }
    r42_str.pop();
    let mut r31_str = String::new();
    for r2 in rule_31 {
        r31_str += &format!("{}|", r2);
    }
    r31_str.pop();
    let new_reg: Regex = Regex::new(&format!("^({})+({})+$", r42_str, r31_str)).unwrap();

    let mut count = 0;
    for i in input {
        if new_reg.is_match(&i) {
            let g1 = new_reg.captures(&i).unwrap().get(1).unwrap().end();
            let num_g1 = g1 / rule_42[0].len();
            let num_g2 = (i.len() - g1) / rule_42[0].len();
            if num_g2 < num_g1 {
                count += 1;
            }
        }
    }
    println!("{} messages match modified rule 0", count);
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
    let rules = get_rules(&data[0].split('\n').collect::<Vec<&str>>());
    puzzle1(&data[1].split('\n').collect::<Vec<&str>>(), &rules);
    puzzle2(&data[1].split('\n').collect::<Vec<&str>>(), &rules);
}
