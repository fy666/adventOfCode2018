#[allow(unused)]
pub use log::{debug, error, info, trace, warn};
use std::fs;

fn safe_level(report: &Vec<i32>) -> bool {
    let increasing: bool = report[0] < report[1];
    for level in report.windows(2) {
        trace!("{} and {}", level[0], level[1]);
        if increasing && level[0] >= level[1] {
            return false;
        }
        if !increasing && level[0] <= level[1] {
            return false;
        }
        if (level[0] - level[1]).abs() > 3 {
            return false;
        }
    }
    return true;
}

fn safe_level_ignore_one(report: &Vec<i32>) -> bool {
    let l = report.len();
    if safe_level(&report) {
        return true;
    }
    for n in 0..l {
        let mut sub_report = report.clone();
        sub_report.remove(n);
        trace!("Sub report = {:?}", sub_report);
        if safe_level(&sub_report) {
            return true;
        }
    }
    return false;
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");

    let reports: Vec<Vec<i32>> = text
        .lines()
        .map(|x| x.split(" ").map(|y| y.parse::<i32>().unwrap()).collect())
        .collect();
    let count_a: i32 = reports.iter().map(|x| safe_level(x) as i32).sum();
    info!("Number of valid reports = {:?}", count_a);
    let count_b: i32 = reports
        .iter()
        .map(|x| safe_level_ignore_one(x) as i32)
        .sum();
    info!("Number of valid reports with one ignore = {:?}", count_b);
}
