use std::collections::VecDeque;
use std::env;
use std::fs;

fn do_op(line: &str, add_first: bool) -> i64 {
    let mut numbers: VecDeque<i64> = VecDeque::new();
    let mut op: VecDeque<char> = VecDeque::new();
    let mut p_tmp: String = String::new();
    let mut do_skip = false;
    for i in line.chars() {
        if do_skip {
            if i == ')' && p_tmp.matches("(").count() == p_tmp.matches(")").count() {
                do_skip = false;
                numbers.push_back(do_op(&p_tmp, add_first));
                p_tmp.clear();
            } else {
                p_tmp.push(i);
            }
        } else {
            match i {
                '*' | '+' => op.push_back(i),
                '0'..='9' => numbers.push_back(i.to_digit(10).unwrap() as i64),
                '(' => do_skip = true,
                _ => println!("{} not valid", i),
            }
        }
    }
    if add_first {
        let mut number_to_mul: VecDeque<i64> = VecDeque::new();
        while numbers.len() >= 2 {
            let tmp_op = op.pop_front().unwrap();
            if tmp_op == '+' {
                let tmp_num_1 = numbers.pop_front().unwrap();
                let tmp_num_2 = numbers.pop_front().unwrap();
                numbers.push_front(tmp_num_1 + tmp_num_2);
            } else if tmp_op == '*' {
                let tmp_num_1 = numbers.pop_front().unwrap();
                number_to_mul.push_front(tmp_num_1);
            }
        }
        numbers[0] * number_to_mul.iter().product::<i64>()
    } else {
        while numbers.len() >= 2 {
            let tmp_op = op.pop_front().unwrap();
            let tmp_num_1 = numbers.pop_front().unwrap();
            let tmp_num_2 = numbers.pop_front().unwrap();
            if tmp_op == '+' {
                numbers.push_front(tmp_num_1 + tmp_num_2);
            } else if tmp_op == '*' {
                numbers.push_front(tmp_num_1 * tmp_num_2);
            }
        }
        numbers[0]
    }
}

fn puzzle(data: &Vec<&str>) {
    let mut count1 = 0;
    let mut count2 = 0;
    for operation in data {
        let tmp = do_op(&operation.replace(" ", ""), false);
        println!("{} = {}", operation, tmp);
        count1 += tmp;
        let tmp = do_op(&operation.replace(" ", ""), true);
        println!("{} = {}", operation, tmp);
        count2 += tmp;
    }
    println!("PUZZLE 1 : Sum of all operations = {}", count1);
    println!("PUZZLE 1 : Sum of all operations = {}", count2);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n");
    let data = split.collect::<Vec<&str>>();
    puzzle(&data);
}
