//use std::io;
//use std::cmp::Ordering;
use std::fs;
use regex::Regex;
//use std::convert::TryInto;

fn puzzle1(arr: &Vec<&str>) -> i32{
    let mut count = 0;
    let re = Regex::new(r"(\d*)-(\d*) (\w): (\w*)").unwrap();
    for var1 in arr {
        //println!("{}",var1);
        for cap in re.captures_iter(var1) {
            //println!("REGEX FOUND {} {} {} {}", &cap[1], &cap[2], &cap[3], &cap[4]);
            let min: i32 = cap[1].trim().parse().expect("Please type a number!");
            let max: i32 = cap[2].trim().parse().expect("Please type a number!");
            let num = count_let(&cap[4], &cap[3]);
            //println!("{} is {} times in {}", &cap[3], num, &cap[4]);
            if num >= min && num <= max{
                count = count + 1;
            }
        }
    }
    count
}

fn count_let(line: &str, i: &str) -> i32 {
    let bytes = line.as_bytes();
    let mut count = 0;
    for &item in bytes.iter() {
        if item == i.as_bytes()[0] {  
            count = count + 1;
        }
    }
    count
}

fn puzzle2(arr: &Vec<&str>) -> i32{
    let mut count = 0;
    let re = Regex::new(r"(\d*)-(\d*) (\w): (\w*)").unwrap();
    for var1 in arr {
        //println!("{}",var1);
        for cap in re.captures_iter(var1) {
            //println!("REGEX FOUND {} {} {} {}", &cap[1], &cap[2], &cap[3], &cap[4]);
            let mut min: usize = cap[1].trim().parse().expect("Please type a number!");
            min = min - 1;
            let mut max: usize = cap[2].trim().parse().expect("Please type a number!");
            max = max - 1;
            let first_pos = cap[3].chars().nth(0).unwrap() == cap[4].chars().nth(min).unwrap();
            let last_pos = cap[3].chars().nth(0).unwrap() == cap[4].chars().nth(max).unwrap();
            //println!("{} , last {}", first_pos, last_pos);
            if first_pos ^ last_pos {
                 count = count + 1;
                 //println!("Valid :)");
            }
        }
    }
    count
}

fn main() {
    let input = vec!["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"];
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let mut data : Vec<&str> = Vec::new();
    for line in text.lines(){
        data.push(line);
    }
    println!("Puzzle 1 on test");
    let res = puzzle1(&input);
    println!("Correct pwd = {}", res);

    println!("Puzzle 1 on input");
    let res =  puzzle1(&data);
    println!("Correct pwd = {}", res);

    println!("*********************");

    println!("Puzzle 2 on test");
    let res = puzzle2(&input);
    println!("Correct pwd = {}", res);
    
    println!("Puzzle 2 on input");
    let res = puzzle2(&data);
    println!("Correct pwd = {}", res);
}