//use regex::Regex;
//use std::collections::HashMap;
//use std::collections::HashSet;
//use std::collections::VecDeque;
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let mut split = text.trim().split("\n\n");
}
