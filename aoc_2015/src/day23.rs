//use itertools::Itertools;
use onig::Regex;
use std::collections::HashMap;
use std::fs;

fn get_mfcsam() -> HashMap<String, i32> {
    let mut message = HashMap::new();
    message.insert("children".to_string(), 3);
    message.insert("cats".to_string(), 7);
    message.insert("samoyeds".to_string(), 2);
    message.insert("pomeranians".to_string(), 3);
    message.insert("akitas".to_string(), 0);
    message.insert("vizslas".to_string(), 0);
    message.insert("goldfish".to_string(), 5);
    message.insert("trees".to_string(), 3);
    message.insert("cars".to_string(), 2);
    message.insert("perfumes".to_string(), 1);
    message
}

fn compare_data(mfcsam: &HashMap<String, i32>, aunt: &HashMap<&str, i32>) -> bool {
    for (key, value) in mfcsam.iter() {
        if aunt.contains_key(key.as_str()) {
            if value != aunt.get(key.as_str()).unwrap() {
                return false;
            }
        }
    }
    true
}

fn compare_data_real(mfcsam: &HashMap<String, i32>, aunt: &HashMap<&str, i32>) -> bool {
    for (key, value) in mfcsam.iter() {
        if aunt.contains_key(key.as_str()) {
            let aunt_value = aunt.get(key.as_str()).unwrap();
            let ok = match key.as_str() {
                "cats" | "trees" => aunt_value > value,
                "pomeranians" | "goldfish" => aunt_value < value,
                _ => aunt_value == value,
            };
            if !ok {
                return false;
            }
        }
    }
    true
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} aunts Sue", data.len());

    let mfcsam = get_mfcsam();
    log::trace!("MFCSAM {:?}", mfcsam);

    let regex = Regex::new(r" ([a-z]*): (\d*)").unwrap();
    let mut num_aunt = 1;
    for aunt in data {
        let mut items: HashMap<_, i32> = HashMap::new();
        for caps in regex.captures_iter(aunt) {
            items.insert(caps.at(1).unwrap(), caps.at(2).unwrap().parse().unwrap());
        }
        if compare_data(&mfcsam, &items) {
            log::info!("Aunt Sue 👵 {} has given the MFCSAM 🕵️", num_aunt);
            log::trace!("Aunt Sue {} is {:?}", num_aunt, items);
        }
        if compare_data_real(&mfcsam, &items) {
            log::info!("‍Real Aunt Sue 🤦 {} has given the MFCSAM 🕵️", num_aunt);
            log::trace!("Aunt Sue {} is {:?}", num_aunt, items);
        }
        num_aunt += 1;
    }
}
