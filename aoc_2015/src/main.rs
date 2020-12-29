use std::env;
mod day1;

fn main() {
    let args: Vec<String> = env::args().collect();
    let day = args[1].clone();
    let mut file = args[2].clone();
    println!("Running {} on Day {}", file, day);
    if file == "test" {
        file = format!("./data/test{}.txt", day);
    } else if file == "input" {
        file = format!("./data/input{}.txt", day);
    } else {
        panic!("Please give as argument input or test");
    }
    //    if !file.ends_with(".txt") {
    //        file += &".txt".to_string();
    //   }

    match day.as_str() {
        "1" => day1::day1(&file),
        _ => println!("Day {} not found", day),
    }
}
