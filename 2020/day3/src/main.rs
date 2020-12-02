//use std::io;
//use std::cmp::Ordering;
use std::fs;
//use std::convert::TryInto;

fn puzzle1(arr: &Vec<char>, width: usize, height: usize, x_step : usize, y_step : usize) -> i64{
    let mut x = 0;
    let mut y = 0;
    // let y_step = 1;
    // let x_step = 3;
    let mut count = 0;
    while y < height {
        if(arr[(y*width)+x%width] == '#'){
            count += 1;
        }
        y += y_step;
        x += x_step;
    }
    println!("You hit {} trees", count);
    count
}

fn print_vec(arr: &Vec<char>){
    for i in arr{
        print!("{}", i);
    }
    println!("");
}

fn main() {
    let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    //let mut data : Vec<&str> = Vec::new();
    let mut data : Vec<char> = Vec::new();
    let width = text.lines().nth(0).unwrap().chars().count();
    let height = text.lines().count();

    for line in text.lines(){
        for c in line.chars(){
            data.push(c);
        }
    }
    println!("Imported forest of {} by {}", width, height);
    //print_vec(&data);
    let mut mul = 1;
    mul *= puzzle1(&data, width, height, 3 ,1);
    
    mul *= puzzle1(&data, width, height, 1 ,1);
    mul *= puzzle1(&data, width, height, 5 ,1);
    mul *= puzzle1(&data, width, height, 7 ,1);
    mul *= puzzle1(&data, width, height, 1 , 2);
    println!("Total is {}", mul);
}