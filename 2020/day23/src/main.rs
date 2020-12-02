fn get_previous_index(current: usize, max: usize) -> usize {
    if current == 1 {
        max - 1
    } else {
        current - 1
    }
}

fn puzzle(input_cups: Vec<usize>, turns: usize) -> Vec<usize> {
    let mut cups: Vec<usize> = vec![0; input_cups.len() + 1];
    for x in input_cups.windows(2) {
        cups[x[0]] = x[1];
    }
    cups[input_cups[input_cups.len() - 1]] = input_cups[0];

    let mut current_cup = input_cups[0];
    for _ in 0..turns {
        let mut excluded_num: Vec<usize> = Vec::new();
        excluded_num.push(cups[current_cup]);
        excluded_num.push(cups[cups[current_cup]]);
        excluded_num.push(cups[cups[cups[current_cup]]]);
        let mut where_to_insert = get_previous_index(current_cup, cups.len());
        while excluded_num.contains(&where_to_insert) {
            where_to_insert = get_previous_index(where_to_insert, cups.len());
        }
        cups[current_cup] = cups[excluded_num[2]];
        cups[excluded_num[2]] = cups[where_to_insert];
        cups[where_to_insert] = excluded_num[0]; //where_to_insert;
        current_cup = cups[current_cup];
    }
    cups
}

fn print_cups(cups: &Vec<usize>, num_to_print: usize) {
    let mut current_index = cups.iter().position(|&x| x == 1).unwrap();
    let mut printed = 0;
    print!("First part :");
    while printed < num_to_print {
        print!("{},", cups[current_index]);
        current_index = cups[current_index];
        printed += 1;
    }
    println!();
}

fn main() {
    println!("On example :");
    let data = vec![3, 8, 9, 1, 2, 5, 4, 6, 7];
    let mut long_data = data.clone();
    long_data.extend(10..1000001);
    let res = puzzle(data, 100);
    print_cups(&res, res.len() - 1);
    let res_long = puzzle(long_data, 10000000);
    println!(
        "Seond part : {} * {}  = {}",
        res_long[1],
        res_long[res_long[1]],
        res_long[1] * res_long[res_long[1]]
    );

    println!("-----------------------");
    println!("On input :");
    let data = vec![9, 1, 6, 4, 3, 8, 2, 7, 5];
    let mut long_data = data.clone();
    long_data.extend(10..1000001);
    let res = puzzle(data, 100);
    print_cups(&res, res.len() - 1);
    let res_long_input = puzzle(long_data, 10000000);
    println!(
        "Second part {} * {} = {}",
        res_long_input[1],
        res_long_input[res_long_input[1]],
        res_long_input[1] * res_long_input[res_long_input[1]]
    );
}
