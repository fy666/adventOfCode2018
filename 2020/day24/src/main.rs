//use regex::Regex;
use std::collections::HashMap;
//use std::collections::HashSet;
//use std::collections::VecDeque;
use std::env;
use std::fs;

fn get_moves(data: &Vec<&str>) -> Vec<[i32; 2]> {
    let mut all_tiles: HashMap<[i32; 2], i32> = HashMap::new();
    for line in data.iter() {
        let mut keep_next = false;
        let mut last: char = ' ';
        let mut tile: [i32; 2] = [0, 0];
        for c in line.chars() {
            if keep_next {
                if last == 'n' {
                    if c == 'e' {
                        // println!("Going north est");
                        tile = [tile[0] + 1, tile[1] + 1];
                    } else if c == 'w' {
                        //println!("Going north west");
                        tile = [tile[0] - 1, tile[1] + 1];
                        // tile = (tile.0 - 0.5, tile.1 + 0.5);
                    }
                } else if last == 's' {
                    if c == 'e' {
                        //println!("Going sud est");
                        //tile = (tile.0 - 0.5, tile.1 + 0.5);
                        tile = [tile[0] + 1, tile[1] - 1];
                    } else if c == 'w' {
                        //println!("Going sud west");
                        // tile = (tile.0 - 0.5, tile.1 - 0.5);
                        tile = [tile[0] - 1, tile[1] - 1];
                    }
                }
                keep_next = false;
                continue;
            }
            match c {
                'e' => {
                    // println!("Going east");
                    //tile = (tile.0 + 1.0, tile.1);
                    tile = [tile[0] + 2, tile[1]];
                }
                'w' => {
                    //println!("Goind west");
                    //tile = (tile.0 - 1.0, tile.1);
                    tile = [tile[0] - 2, tile[1]];
                }
                'n' | 's' => {
                    last = c;
                    keep_next = true
                }
                _ => println!("{} not found", c),
            };
        }
        //println!("End tile to flip at {:?}", tile);
        *all_tiles.entry(tile).or_insert(0) += 1;
    }
    //println!("All end tiles = {:?}", all_tiles);
    println!(
        "{} black tiles",
        all_tiles.values().filter(|&x| x % 2 == 1).count()
    );
    all_tiles
        .iter()
        .filter(|&x| x.1 % 2 == 1)
        .map(|x| *x.0)
        .collect::<Vec<[i32; 2]>>()
}

fn is_neighboor(a: &[i32; 2], b: &[i32; 2]) -> bool {
    if (a[0] - b[0]).abs() == 2 && a[1] == b[1] {
        return true;
    } else if (a[0] - b[0]).abs() == 1 && (a[1] - b[1]).abs() == 1 {
        return true;
    }
    false
}

fn get_neighboors(a: &[i32; 2]) -> Vec<[i32; 2]> {
    let mut output: Vec<[i32; 2]> = Vec::new();
    output.push([a[0] - 2, a[1]]);
    output.push([a[0] + 2, a[1]]);

    output.push([a[0] - 1, a[1] - 1]);
    output.push([a[0] - 1, a[1] + 1]);
    output.push([a[0] + 1, a[1] - 1]);
    output.push([a[0] + 1, a[1] + 1]);

    output
}

fn flip_day(input: &Vec<[i32; 2]>) -> Vec<[i32; 2]> {
    let mut output: Vec<[i32; 2]> = Vec::new();
    // handle tiles that are already black
    for tile in input.iter() {
        let black_neigh = input
            .iter()
            .filter(|&x| x != tile && is_neighboor(x, tile))
            .count();
        if black_neigh == 1 || black_neigh == 2 {
            output.push(tile.clone());
        }
    }

    // search for tiles that could became black
    let mut neighs: HashMap<[i32; 2], i32> = HashMap::new();
    for tile in input.iter() {
        for n in get_neighboors(&tile) {
            if !input.contains(&n) {
                *neighs.entry(n).or_insert(0) += 1;
            }
        }
    }

    for (key, val) in neighs {
        if val == 2 {
            output.push(key);
        }
    }

    output
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    println!("Imported {} paths", data.len());
    let mut black_tiles = get_moves(&data);
    println!("{} black tiles", black_tiles.len());
    for t in 0..100 {
        black_tiles = flip_day(&black_tiles);
        println!("day {} : black tiles {}", t, black_tiles.len());
    }
    //println!("{} black tiles", black_tiles.len()); //black_tiles);
}
