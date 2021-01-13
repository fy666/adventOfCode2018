use env_logger::Env;
use std::env;
mod day1;
mod day10;
mod day11;
mod day12;
mod day13;
mod day14;
mod day15;
mod day16;
mod day17;
mod day18;
mod day19;
mod day2;
mod day20;
mod day3;
mod day4;
mod day5;
mod day6;
mod day7;
mod day8;
mod day9;

fn get_path(test_mode: bool, day: i32) -> String {
    if test_mode {
        format!("./data/test{}.txt", day)
    } else {
        format!("./data/input{}.txt", day)
    }
}

fn main() {
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();
    let args: Vec<String> = env::args().collect();
    let day = args[1].clone();
    let file = args.get(2).unwrap_or(&String::from(" ")).clone();
    let test_mode: bool = file == "test";

    match day.as_str() {
        "1" => day1::run(&get_path(test_mode, 1)),
        "2" => day2::run(&get_path(test_mode, 2)),
        "3" => day3::run(&get_path(test_mode, 3)),
        "4" => day4::run(),
        "5" => day5::run(&get_path(test_mode, 5)),
        "6" => day6::run(&get_path(test_mode, 6)),
        "7" => day7::run(&get_path(test_mode, 7)),
        "8" => day8::run(&get_path(test_mode, 8)),
        "9" => day9::run(&get_path(test_mode, 9)),
        "10" => day10::run(test_mode),
        "11" => day11::run(test_mode),
        "12" => day12::run(&get_path(test_mode, 12)),
        "13" => day13::run(&get_path(test_mode, 13)),
        "14" => day14::run(&get_path(test_mode, 14), test_mode),
        "15" => day15::run(&get_path(test_mode, 15)),
        "16" => day16::run(&get_path(test_mode, 16)),
        "17" => day17::run(&get_path(test_mode, 17)),
        "18" => day18::run(&get_path(test_mode, 18)),
        "19" => day19::run(&get_path(test_mode, 19)),
        "20" => day20::run(&get_path(test_mode, 20)),
        "all" => {
            day1::run(&get_path(test_mode, 1));
            day2::run(&get_path(test_mode, 2));
            day3::run(&get_path(test_mode, 3));
            //day4::run(); skip day 4 because too long
            day5::run(&get_path(test_mode, 5));
            day6::run(&get_path(test_mode, 6));
            day7::run(&get_path(test_mode, 7));
            day8::run(&get_path(test_mode, 8));
            day9::run(&get_path(test_mode, 9));
            day10::run(test_mode);
            day11::run(test_mode);
            day12::run(&get_path(test_mode, 12));
            day13::run(&get_path(test_mode, 13));
            day14::run(&get_path(test_mode, 14), test_mode);
            day15::run(&get_path(test_mode, 15));
            day16::run(&get_path(test_mode, 16));
            day17::run(&get_path(test_mode, 17));
            day18::run(&get_path(test_mode, 18));
            day19::run(&get_path(test_mode, 19));
            day20::run(&get_path(test_mode, 20));
        }
        _ => log::warn!("Day {} not found", day),
    }
}
