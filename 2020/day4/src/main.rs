use std::fs;
use regex::Regex;
use std::collections::HashMap;
use lazy_static::lazy_static; // 1.3.0

lazy_static! {
    static ref RE_ITEM : Regex = Regex::new(r"(?P<key>[\w]{3}):(?P<value>\S*)").unwrap();
    static ref RE_HCL: Regex = Regex::new(r"#[0-9a-f]{6}").unwrap();
    static ref RE_ECL : Regex = Regex::new(r"amb|blu|brn|gry|grn|hzl|oth").unwrap();
    static ref RE_PID : Regex = Regex::new(r"\d{9}").unwrap();
}


fn puzzle1(passports: &Vec<&str>) {
    let mut count = 0;
    for p in passports{
        count += is_valid_passwd(p);
    }
    println!("{} valid passports", count);    
}

fn is_valid_passwd(pass: &str) ->i32{
    let passports : HashMap<String,String> = to_passports(&pass);
    let expected_keys = ["byr", "iyr", "eyr","hgt","hcl","ecl","pid"];
    for key in &expected_keys{
        if !passports.contains_key(key.to_owned()) {
            return 0
        }
        if !key_is_valid(&key.to_string(), passports.get(key.to_owned()).expect("dict value not found")){
            return 0
        }
    }
    return 1
}

fn key_is_valid(key: &String, value: &String) -> bool{
    //println!("is {} valid ? {}", key, value);
    if key == "byr"{
        let val : i32 = value.parse().unwrap();
        return val >= 1920 && val <= 2002;
    }
    if key == "iyr"{
        let val : i32= value.parse().unwrap();
        return val >= 2010 && val <= 2020;
    }
    if key == "eyr"{
        let val : i32= value.parse().unwrap();
        return val >= 2020 && val <= 2030;
    }
    if key == "hgt"{
        if value.len() < 3{
            return false;
        }
        let l = value.len() - 2;
        let unit = &value[l..];
        let val : i32= value[..l].parse().unwrap();
        if unit == "cm"{
            return val >= 150 && val <= 193;
        }
        else if unit == "in" {
            return val >= 59 && val <= 76;
        }
        return false;
    }
    if key == "hcl"{
        return RE_HCL.is_match(value);
    }
    if key == "ecl"{
        return RE_ECL.is_match(value);
    }
    if key == "pid"{
        return RE_PID.is_match(value) && value.len() == 9;
    }
    println!("Unparsed key = {}", key);
    false
}

fn to_passports(pass:&str) -> HashMap<String,String> {
    let mut result : HashMap<String,String> = HashMap::new();
    for cap in RE_ITEM.captures_iter(pass) {
        result.insert(cap["key"].to_owned(), cap["value"].to_owned());
    }
    result
}

fn main() {
    //let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.split("\n\n");
    let data = split.collect::<Vec<&str>>();
    println!("Imported {} passwords", data.len());
    puzzle1(&data);
}
