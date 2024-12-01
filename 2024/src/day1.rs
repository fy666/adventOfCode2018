use itertools::Itertools;
#[allow(unused)]
pub use log::{debug, error, info, trace, warn};
use std::collections::HashMap;
use std::fs;

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    debug!("Imported {} numbers", data.len());

    let (mut left, mut right): (Vec<i32>, Vec<i32>) = text
        .lines()
        .map(|x| {
            x.split("   ")
                .map(|y| y.parse::<i32>().unwrap())
                .collect_tuple()
                .unwrap()
        })
        .unzip();
    trace!("Vec 1 = {:?}, vec 2 = {:?}", left, right);

    left.sort();
    right.sort();

    let merged: i32 = left
        .iter()
        .zip(right.iter())
        .map(|(x, y)| (x - y).abs())
        .sum();
    info!("Total distance between lists = {}", merged);

    let res2: usize = left
        .iter()
        .map(|x| right.iter().filter(|&n| n == x).count() * (*x as usize))
        .sum();
    info!("Similarity score = {}", res2);

    // Hashmap impl
    let mut right_hash = HashMap::new();
    right.iter().for_each(|num| {
        right_hash.entry(num).and_modify(|x| *x += 1).or_insert(1);
    });
    trace!("Hash map = {:?}", right_hash);

    let res2hash: usize = left
        .iter()
        .map(|x| right_hash.get(&x).unwrap_or(&0) * (*x as usize))
        .sum();
    info!("Similarity score using hash map = {}", res2hash);
}
