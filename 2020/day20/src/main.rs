//use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;

use std::env;
use std::fs;

#[derive(Debug)]
struct Tile {
    id: i32,
    edges: [[char; 10]; 4],
    data: [[char; 10]; 10],
    position: [i32; 2],
    rotation: i32,
    neighbors: Vec<i32>,
}

fn getTile() -> Tile {
    Tile {
        id: 0,
        edges: [['.'; 10]; 4],
        data: [['.'; 10]; 10],
        position: [-1, -1],
        rotation: 0,
        neighbors: Vec::new(),
    }
}

impl Tile {
    fn compute_edges(&mut self) {
        self.edges[0] = self.data[0];
        self.edges[2] = self.data[9];
        for i in 0..10 {
            self.edges[1][i] = self.data[i][0];
            self.edges[3][i] = self.data[i][9];
        }
    }
}

fn parse_tile(input: &Vec<&str>) -> Tile {
    let mut tile = getTile();
    tile.id = input[0]
        .split(" ")
        .nth(1)
        .unwrap()
        .replace(":", "")
        .parse()
        .unwrap();
    let mut ix: usize = 0;
    for line in input.iter().skip(1) {
        //println!("Tile {}, line = {}", id, line);
        for (col, data) in line.chars().enumerate() {
            tile.data[ix][col] = data;
        }
        ix += 1;
    }
    tile.compute_edges();
    //println!("tile = {:?}", tile);
    tile
}

fn puzzle1(tiles: &mut Vec<Tile>) {
    let mut all_edges: HashMap<[char; 10], (i32, Vec<i32>)> = HashMap::new();
    for t in tiles.iter() {
        for ed in 0..4 {
            let entry = all_edges.entry(t.edges[ed]).or_insert((0, Vec::new()));
            entry.0 += 1;
            entry.1.push(t.id);
            let mut tmp = t.edges[ed].clone();
            tmp.reverse();
            let entry = all_edges.entry(tmp).or_insert((0, Vec::new()));
            entry.0 += 1;
            entry.1.push(t.id);
        }
    }
    let edges_tiles = all_edges
        .iter()
        .filter(|(_edge, data)| data.0 == 1)
        .map(|(_edge, data)| data.1[0])
        .collect::<Vec<i32>>();
    let mut corners: HashMap<i32, i32> = HashMap::new();
    edges_tiles.iter().for_each(|&x| {
        *corners.entry(x).or_insert(0) += 1;
    });

    let mut res: i64 = 1;
    let mut corners_id: Vec<i32> = Vec::new();
    for (id, _val) in corners.iter().filter(|(_id, val)| **val == 4) {
        corners_id.push(*id);
        res *= *id as i64;
    }

    println!("Corners : {:?}", corners_id);

    //println!("edges tiles : {:?}", edges_tiles);

    //println!("corners : {:?}", corners);
    println!("Result = {}", res);

    let neigh = all_edges
        .values()
        .filter(|x| x.0 > 1)
        .map(|x| x.1.clone())
        .collect::<Vec<Vec<i32>>>();
    //println!("Neighbors : {:?}", neigh);

    //let mut all_neigh: HashMap<i32, Vec<i32>> = HashMap::new();
    for t in tiles.iter_mut() {
        let id = t.id;
        for n in neigh.iter().filter(|x| x.contains(&id)).flatten() {
            if *n != t.id && !t.neighbors.contains(&n) {
                t.neighbors.push(*n);
            }
        }
        println!("Tile {} : neigh : {:?}", t.id, t.neighbors);
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n\n");
    let mut tiles: Vec<Tile> = Vec::new();
    for s in split {
        tiles.push(parse_tile(&s.split('\n').collect::<Vec<&str>>()));
    }
    println!("{} tiles importes", tiles.len());
    puzzle1(&mut tiles);
}
