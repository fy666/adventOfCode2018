use std::collections::HashMap;
// use std::env;
// use std::fs;

fn get_last_repeats(input: &Vec<i32>, to_find: i32) -> (i32, i32) {
    let mut i1: i32 = -1;
    let mut i2: i32 = -1;
    let mut cloned_input = input.clone();
    cloned_input.reverse();
    for (ix, num) in cloned_input.iter().enumerate() {
        if *num == to_find {
            if i1 == -1 {
                i1 = (input.len() - ix - 1) as i32;
            } else {
                i2 = (input.len() - ix - 1) as i32;
                break;
            }
        }
    }
    (i1, i2)
}

fn puzzle1(input: &Vec<i32>) {
    let mut index = input.len();
    let mut all_num: Vec<i32> = input.clone();
    let mut last_number = input[input.len() - 1];

    while index < 30000000 {
        let tmp = get_last_repeats(&all_num, last_number);
        //println!("Last num = {}, repeats = {:?}", last_number, tmp);
        if tmp.1 == -1 {
            all_num.push(0);
            last_number = 0;
        } else if tmp.0 != -1 && tmp.1 != -1 {
            let diff = tmp.0 - tmp.1;
            all_num.push(diff);
            last_number = diff;
        } else {
            println!("Error");
        }
        //println!("{}", last_number);
        index += 1;
    }
    println!("{:?}", all_num[2019]);
}

fn puzzle2(input: &Vec<i32>, rule: usize) {
    let mut index = input.len();
    let mut last_number = input[input.len() - 1];
    let mut all_numbers: HashMap<i32, (i32, i32)> = HashMap::new();
    for (ix, num) in input.iter().enumerate() {
        all_numbers.insert(*num as i32, (ix as i32, -1));
    }
    //println!("{:?}", all_numbers);
    while index < rule {
        let tmp = all_numbers.get(&last_number).unwrap();
        //println!("TMP = {:?}", tmp);
        if tmp.1 == -1 {
            last_number = 0;
            let tmp = all_numbers.get(&last_number).unwrap();
            all_numbers.insert(0, (index as i32, tmp.0));
        } else if tmp.0 != -1 && tmp.1 != -1 {
            let diff = tmp.0 - tmp.1;
            last_number = diff;
            if (all_numbers.contains_key(&last_number)) {
                let tmp = all_numbers.get(&last_number).unwrap();
                all_numbers.insert(last_number, (index as i32, tmp.0));
            } else {
                all_numbers.insert(last_number, (index as i32, -1));
            }
        } else {
            println!("Error");
        }
        //println!("Turn {} : saying {}", index + 1, last_number);
        //println!("{:?}", all_numbers);
        index += 1;
    }
    println!("Last num = {}", last_number);
}

fn main() {
    //let data = vec![0, 3, 6];
    //let data = vec![1, 2, 3];
    let data = vec![0, 13, 1, 16, 6, 17];

    puzzle2(&data, 30000000);
}
