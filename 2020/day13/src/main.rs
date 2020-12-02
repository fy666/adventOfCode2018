use std::env;
use std::fs;

fn get_closest_sup(obj: i32, x: i32) -> i32 {
    let start: i32 = obj / x;
    return (start + 1) * x;
    //println!("{}", start);
    // for i in start..start + 3 {
    //     if i * x >= obj {
    //         return i * x;
    //     }
    // }
    // println!("Error");
    // start
}

fn puzzle1(busses: &Vec<i32>, time: i32) {
    let mut repeat: Vec<i32> = Vec::new();
    let mut bus_number = busses[0];
    let mut closest_val = get_closest_sup(time, busses[0]);
    for bus in busses {
        let val = get_closest_sup(time, *bus);
        if val < closest_val {
            closest_val = val;
            bus_number = *bus;
        }
        repeat.push(val);
    }

    // for b in repeat {
    //     println!("REPEAT {}", b);
    // }
    println!(
        "Closest bus {} freq {}, answer is {}",
        bus_number,
        closest_val,
        (closest_val - time) * bus_number
    );
}

fn puzzle2_tldr(busses: &Vec<(i64, i64)>) {
    for bus in busses {
        println!("x+{} multiple of {}", bus.1, bus.0);
    }

    let mut i: i64 = 1; //99999999999708; //100000000000000;
    let res = loop {
        let mut find = true;
        let mut to_add = 1;
        for bus in busses {
            if i.rem_euclid(bus.0) != (bus.0 - bus.1).rem_euclid(bus.0) {
                find = false;
                break;
            } else {
                to_add *= bus.0;
                //println!("{}+{} divisible by {}", i, bus.1, bus.0);
            }
        }
        if find {
            break i;
        }
        i += to_add; //busses[0].0;
    };
    println!("Found {}", res);
}

fn puzzle2(busses: &Vec<(i64, i64)>) {
    let mut ppcm: i64 = 1;
    for bus in busses {
        ppcm *= bus.0;
        println!("x+{} multiple of {}", bus.1, bus.0);
    }
    println!("ppcm = {}", ppcm);
    let mut res: i64 = 0;
    for bus in busses {
        let remainder = (bus.0 - bus.1).rem_euclid(bus.0); //bus.0 - bus.1) % bus.0;
        let n_tilde = ppcm / bus.0;
        let nii = n_tilde % bus.0;
        res += n_tilde * nii * remainder;
        println!(
            "x+{} multiple of {} (r={}): ntilde={}, nii = {}, sum = {}",
            bus.1,
            bus.0,
            remainder,
            n_tilde,
            nii,
            remainder * n_tilde * nii
        );
    }
    println!("Found {}", res);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let data = text.trim().split("\n").collect::<Vec<&str>>();
    let time: i32 = data[0].parse().unwrap();
    let mut busses: Vec<i32> = Vec::new();
    let mut timed_busses: Vec<(i64, i64)> = Vec::new();
    for (ix, it) in data[1].split(",").enumerate() {
        //println!("bus {}", it);
        if it != "x" {
            busses.push(it.parse().unwrap());
            timed_busses.push((it.parse().unwrap(), ix as i64));
        }
    }
    println!("Imported time {} and {} busses", time, busses.len());
    puzzle1(&busses, time);
    //println!("MODULO {}", (19 - 91 % 19));
    //timed_busses.sort();
    //timed_busses.reverse();
    //puzzle2(&timed_busses);
    puzzle2_tldr(&timed_busses);
}
