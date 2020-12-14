use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs;

fn puzzle1(input: &Vec<&str>) {
    let re_mask = Regex::new(r"mask = ([0X1]*)").unwrap();
    let re_mem = Regex::new(r"mem\[([0-9]*)\] = ([0-9]*)").unwrap();
    let mut memory: HashMap<u64, u64> = HashMap::new();
    let mut mask_and: u64 = 0;
    let mut mask_or: u64 = 0;
    for l in input {
        if re_mask.is_match(l) {
            let tmp = re_mask.captures(l).unwrap().get(1).unwrap().as_str();
            mask_and = u64::from_str_radix(&tmp.replace("X", "1"), 2).unwrap();
            mask_or = u64::from_str_radix(&tmp.replace("X", "0"), 2).unwrap();
            println!("Mask {} AND {} OR {}", tmp, mask_and, mask_or);
        } else if re_mem.is_match(l) {
            //let cap =
            let mem_index: u64 = re_mem
                .captures(l)
                .unwrap()
                .get(1)
                .unwrap()
                .as_str()
                .parse()
                .unwrap();
            let mem_data: u64 = re_mem
                .captures(l)
                .unwrap()
                .get(2)
                .unwrap()
                .as_str()
                .parse()
                .unwrap();
            let value = (mem_data & mask_and) | mask_or;
            println!("Mem {} value {} (read {})", mem_index, value, mem_data);
            memory.insert(mem_index, value);
        }
    }
    let mut sum = 0;
    for (_key, value) in memory {
        sum += value;
    }
    println!("PUZZLE 1 : sum of memory {}", sum);
}

fn gen_all_addresses(mask: &str, address: u64) -> Vec<u64> {
    let mut res: Vec<u64> = Vec::new();
    let x_index = mask
        .chars()
        .enumerate()
        .filter(|(_ix, c)| *c == 'X')
        .map(|(ix, _c)| ix)
        .collect::<Vec<usize>>();
    let no_x_mask = u64::from_str_radix(&mask.replace("X", "1"), 2).unwrap();
    let only_x_mask = u64::from_str_radix(&mask.replace("0", "1").replace("X", "0"), 2).unwrap();
    let first_address = no_x_mask | address;
    for i in 0..(1 << x_index.len()) {
        let mut local_mask = only_x_mask;
        for (ix, p) in x_index.iter().enumerate() {
            // if i as u64 & (1 << ix) > 0 {
            //     local_mask += 1 << (mask.len() - 1 - p);
            // }
            if i >> ix & 1 == 1 {
                local_mask += 1 << (mask.len() - 1 - p);
            }
        }
        //println!("Localmask = {:b}", local_mask);
        res.push(local_mask & first_address);
    }
    res
}

fn puzzle2(input: &Vec<&str>) {
    let re_mask = Regex::new(r"mask = ([0X1]*)").unwrap();
    let re_mem = Regex::new(r"mem\[([0-9]*)\] = ([0-9]*)").unwrap();
    let mut memory: HashMap<u64, u64> = HashMap::new();
    let mut mask = "";
    for l in input {
        if re_mask.is_match(l) {
            mask = re_mask.captures(l).unwrap().get(1).unwrap().as_str();
        } else if re_mem.is_match(l) {
            //let cap =
            let mem_index: u64 = re_mem
                .captures(l)
                .unwrap()
                .get(1)
                .unwrap()
                .as_str()
                .parse()
                .unwrap();
            let mem_data: u64 = re_mem
                .captures(l)
                .unwrap()
                .get(2)
                .unwrap()
                .as_str()
                .parse()
                .unwrap();
            for add in gen_all_addresses(&mask, mem_index) {
                //println!("Mem {} value {}", add, mem_data);
                memory.insert(add, mem_data);
            }
        }
    }
    let mut sum = 0;
    for (_key, value) in memory {
        sum += value;
    }
    println!("PUZZLE 2 : sum of memory {}", sum);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n");
    let data = split.collect::<Vec<&str>>();
    puzzle2(&data);
}
