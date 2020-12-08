use std::fs;

fn get_last_index(input: &Vec<(String, i32)>, line_to_switch : i32) -> (bool, i32) {
    let mut index : i32 = 0;
    let mut acc : i32 = 0;
    let mut already_went : Vec<i32> = Vec::new();

    let last_index = loop {
        if already_went.contains(&index) || index >= input.len() as i32 {
            break index
        }
        already_went.push(index);
        
        let mut instr = input[index as usize].0.clone();
        if index == line_to_switch{
            if instr=="jmp"{
                instr = String::from("nop");
            }
            else if instr == "nop" {
                instr = String::from("jmp");
            }
        }

        if instr =="jmp"{
            index += input[index as usize].1;
            continue;
        }
        if instr =="acc"{
            acc+=input[index as usize].1;
        }
        index += 1;
    };
    //println!("Changing line {} : {}", line_to_switch, last_index == input.len() as i32);
    (last_index == input.len() as i32, acc)
}

fn puzzle2(input: &Vec<(String, i32)>){
    let mut line_to_change=0;
    for instr in input {
        if instr.0 == "jmp" || instr.0 == "nop"{
            let res = get_last_index(&input, line_to_change);
            if res.0 {
                println!("Second puzzle, changed line {}, acc = {}", line_to_change, res.1);
                break;
            }
        }
        line_to_change+=1;
    } 
}

fn puzzle1(input: &Vec<(String, i32)>){
    let mut index : i32 = 0;
    let mut acc : i32 = 0;
    let mut already_went : Vec<i32> = Vec::new();
    loop {
        if already_went.contains(&index){
            break;
        }
        already_went.push(index);
        if input[index as usize].0 =="jmp"{
            index += input[index as usize].1;
            continue;
        }
        if input[index as usize].0 =="acc"{
            acc+=input[index as usize].1
        }
        index += 1;
    }
    println!("First puzzle, acc = {}", acc);
}


fn convert_lines_to_instr(input: Vec<&str>) -> Vec<(String, i32)>{
    let mut res : Vec<(String, i32)> = Vec::new();
    for l in input{
        let tmp = l.split(" ").collect::<Vec<&str>>();
        res.push((tmp[0].to_string(), tmp[1].parse().unwrap()));
    }
    res
}

fn main() {
    //let file = "test.txt";
    //let file = "test2.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n");
    let data = split.collect::<Vec<&str>>();
    let data = convert_lines_to_instr(data);
    println!("Imported {} instructions", data.len());
    puzzle1(&data);
    puzzle2(&data);
}