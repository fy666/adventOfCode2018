use std::fs;

#[derive(Debug)]
struct Gift {
    l: i32,
    w: i32,
    h: i32,
    all_num: Vec<i32>,
}

impl Gift {
    fn new(line: &str) -> Self {
        let mut tmp: Vec<i32> = line.split('x').map(|x| x.parse().unwrap()).collect();
        tmp.sort();
        Gift {
            l: tmp[0],
            w: tmp[1],
            h: tmp[2],
            all_num: tmp,
        }
    }

    fn get_area(&self) -> i32 {
        2 * self.l * self.w
            + 2 * self.w * self.h
            + 2 * self.h * self.l
            + self.all_num[0] * self.all_num[1]
    }

    fn get_ribbon(&self) -> i32 {
        2 * self.all_num[0] + 2 * self.all_num[1] + self.w * self.h * self.l
    }
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    println!("Imported {} 🎁", data.len());
    let mut needed_area = 0;
    let mut needed_ribbon = 0;
    for gift in data {
        let g = Gift::new(gift);
        // println!("{:?} area = {}", g, g.get_area());
        needed_area += g.get_area();
        needed_ribbon += g.get_ribbon();
    }
    println!("Needed paper {}, needed 🎀 {} ", needed_area, needed_ribbon);
}
