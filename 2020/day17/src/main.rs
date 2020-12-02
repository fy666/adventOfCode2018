//use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs;

fn printHash(h: &HashMap<(i32, i32, i32), char>, x: (i32, i32), y: (i32, i32), z: (i32, i32)) {
    for zpos in z.0..z.1 {
        println!("z = {}", zpos);
        for ypos in y.0..y.1 {
            for xpos in x.0..x.1 {
                if h.contains_key(&(xpos, ypos, zpos)) {
                    print!("{}", h.get(&(xpos, ypos, zpos)).unwrap());
                } else {
                    print!("?");
                }
            }
            print!("\n");
        }
        //print!("\n");
    }
}

fn get_neighbors(pos: (i32, i32, i32)) -> Vec<(i32, i32, i32)> {
    let mut res: Vec<(i32, i32, i32)> = Vec::new();
    for x in pos.0 - 1..pos.0 + 2 {
        for y in pos.1 - 1..pos.1 + 2 {
            for z in pos.2 - 1..pos.2 + 2 {
                res.push((x, y, z));
            }
        }
    }
    res.retain(|&x| x != pos);
    //println!("{} neighbors {:?}", res.len(), res);
    res
}

fn iter(h: &HashMap<(i32, i32, i32), char>) -> HashMap<(i32, i32, i32), char> {
    let mut new_positions: HashMap<(i32, i32, i32), char> = HashMap::new();
    let mut keys_to_add: Vec<(i32, i32, i32)> = Vec::new();
    for (key, val) in h.iter() {
        let neigh = get_neighbors(*key);
        let mut count_active = 0;
        for n in neigh {
            if h.contains_key(&n) {
                if *h.get(&n).unwrap() == '#' {
                    count_active += 1;
                }
            } else {
                keys_to_add.push(n);
            }
        }
        if *val == '#' {
            if count_active == 2 || count_active == 3 {
                new_positions.insert(*key, '#');
            } else {
                new_positions.insert(*key, '.');
            }
        } else if *val == '.' {
            if count_active == 3 {
                new_positions.insert(*key, '#');
            } else {
                new_positions.insert(*key, '.');
            }
        }
    }

    // Insert new keys
    for new_pos in keys_to_add {
        let neigh = get_neighbors(new_pos);
        let mut count_active = 0;
        for n in neigh {
            if h.contains_key(&n) {
                if *h.get(&n).unwrap() == '#' {
                    count_active += 1;
                }
            }
        }
        if count_active == 3 {
            new_positions.insert(new_pos, '#');
        } else {
            new_positions.insert(new_pos, '.');
        }
    }

    new_positions
}

fn get_neighbors_4d(pos: (i32, i32, i32, i32)) -> Vec<(i32, i32, i32, i32)> {
    let mut res: Vec<(i32, i32, i32, i32)> = Vec::new();
    for x in pos.0 - 1..pos.0 + 2 {
        for y in pos.1 - 1..pos.1 + 2 {
            for z in pos.2 - 1..pos.2 + 2 {
                for w in pos.3 - 1..pos.3 + 2 {
                    res.push((x, y, z, w));
                }
            }
        }
    }
    res.retain(|&x| x != pos);
    //println!("{} neighbors {:?}", res.len(), res);
    res
}

fn iter_4d(h: &HashMap<(i32, i32, i32, i32), char>) -> HashMap<(i32, i32, i32, i32), char> {
    let mut new_positions: HashMap<(i32, i32, i32, i32), char> = HashMap::new();
    let mut keys_to_add: Vec<(i32, i32, i32, i32)> = Vec::new();
    for (key, val) in h.iter() {
        let neigh = get_neighbors_4d(*key);
        let mut count_active = 0;
        for n in neigh {
            if h.contains_key(&n) {
                if *h.get(&n).unwrap() == '#' {
                    count_active += 1;
                }
            } else {
                keys_to_add.push(n);
            }
        }
        if *val == '#' {
            if count_active == 2 || count_active == 3 {
                new_positions.insert(*key, '#');
            } else {
                new_positions.insert(*key, '.');
            }
        } else if *val == '.' {
            if count_active == 3 {
                new_positions.insert(*key, '#');
            } else {
                new_positions.insert(*key, '.');
            }
        }
    }

    // Insert new keys
    for new_pos in keys_to_add {
        let neigh = get_neighbors_4d(new_pos);
        let mut count_active = 0;
        for n in neigh {
            if h.contains_key(&n) {
                if *h.get(&n).unwrap() == '#' {
                    count_active += 1;
                }
            }
        }

        if count_active == 3 {
            new_positions.insert(new_pos, '#');
        } else {
            new_positions.insert(new_pos, '.');
        }
    }

    new_positions
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let mut positions: HashMap<(i32, i32, i32), char> = HashMap::new();
    let mut positions_4d: HashMap<(i32, i32, i32, i32), char> = HashMap::new();
    let mut y = 0;
    for line in text.lines() {
        let mut x = 0;
        for c in line.chars() {
            positions.insert((x, y, 0), c);
            positions_4d.insert((x, y, 0, 0), c);
            x += 1;
        }
        y += 1;
    }
    println!("Imported {} positions", positions.len());
    println!("{:?}", positions);
    println!("Entry : ");
    printHash(&positions, (-3, 6), (-3, 6), (-1, 2));
    let mut old = positions;
    for _ in 1..7 {
        let new = iter(&old);
        old = new;
        printHash(&old, (-3, 6), (-3, 6), (-2, 3));
        break;
        // println!(
        //     "After {} iteration : {} active cubes",
        //     it,
        //     old.values().filter(|&&x| x == '#').count()
        // );
    }
    println!(
        "After 6 iterations : {} active cubes",
        old.values().filter(|&&x| x == '#').count()
    );

    // println!("########################\n PUZZLE2");
    // let mut old_4d = positions_4d;
    // for _ in 1..7 {
    //     let new_4d = iter_4d(&old_4d);
    //     old_4d = new_4d;
    // }
    // println!(
    //     "After 6 iterations : {} active cubes",
    //     old_4d.values().filter(|&&x| x == '#').count()
    // );
}
