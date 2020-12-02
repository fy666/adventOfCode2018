use std::fs;

fn linear_to_mat(position: usize, width: usize) -> (usize,usize){
    let line : usize = position/width; // FLOOR VALUE !
    let col = position%width;
    (line,col)
}

fn mat_to_linear(mat: (usize,usize), width:usize) -> usize{
    (mat.0*width)+mat.1
}


fn nice_print(init: &Vec<char>, width:usize){
    for (ix,seat) in init.iter().enumerate(){
        print!("{}", seat);
        if ix > 0 && ix%width == 0{
            print!("\n");
        }
    }
    print!("\n");
}

fn puzzle1(mut seats: Vec<char>, width:usize){
    let mut run = apply_rule(&seats, width, 4, true);
    let mut iter_count = 1;
    let result = loop{
        if &run[..] == &seats[..] {
            break run;
        }
        seats = run;
        run = apply_rule(&seats, width, 4, true);
        iter_count +=1;
    };
    let occupied_seats = result.iter().filter(|x| **x == '#').count();
    println!("Iter = {}, occupied seats = {}", iter_count, occupied_seats);
}

fn apply_rule(seats: &Vec<char>, width:usize, rule: i32, first: bool) -> Vec<char> {
    let mut result : Vec<char> = Vec::new();
    for (ix,seat) in seats.iter().enumerate(){
        //println!("Position {}, seat {}", ix,seat);
        if *seat == '.'{
            result.push('.');
            continue;
        }
        let mut adjacents_seats : Vec<char> = Vec::new();
        let directions = vec![(0,1),(-1,-1), (0,-1),(-1,0), (-1,1),(1,0),(1,1),(1,-1)];
        for dir in directions{
            adjacents_seats.push(first_seat_in_direction(seats, ix, width, dir, first));
        }

        let occupied_seats = adjacents_seats.iter().filter(|x| **x == '#').count();

        if occupied_seats == 0 {
            result.push('#');
        } else if occupied_seats >= rule as usize {
            result.push('L');
        }  else{
            result.push(*seat);
        }
    }
    result
}


fn puzzle2(mut seats: Vec<char>, width:usize){
    let mut run = apply_rule(&seats, width, 5, false);
    let mut iter_count = 1;
    let result = loop{
        if &run[..] == &seats[..] {//vec_equal(&run, &seats){
            break run;
        }
        seats = run;
        run = apply_rule(&seats, width, 5, false);
        iter_count +=1;
    };
    let occupied_seats = result.iter().filter(|x| **x == '#').count();
    println!("Iter = {}, occupied seats = {}", iter_count, occupied_seats);
}

fn valid_position(coord: (isize,isize), width:usize, height: usize) -> bool{
    if coord.0 < 0 || coord.1 < 0 || coord.1 >= width as isize|| coord.0 >= height as isize{
        return false
    }
    true
}

fn first_seat_in_direction(seats: &Vec<char>, position:usize, width:usize, step: (isize,isize), first: bool) -> char{
    let tmp = linear_to_mat(position, width);
    let mut mat_pos : (isize,isize) = (tmp.0 as isize, tmp.1 as isize);
    mat_pos.0 = step.0 + mat_pos.0;
    mat_pos.1 = step.1 + mat_pos.1;
    let height = seats.len() / width;
    loop{
        if !valid_position(mat_pos, width, height){
            break ' ';
        }
        let var = mat_to_linear((mat_pos.0 as usize,mat_pos.1 as usize), width);
        if seats[var] != '.' || first{
            break seats[var];
        }
        mat_pos.0 = step.0 + mat_pos.0;
        mat_pos.1 = step.1 + mat_pos.1;
    }
}

fn main() {
    //let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let mut data : Vec<char> = Vec::new();
    let width = text.lines().nth(0).unwrap().chars().count();
    let height = text.lines().count();

    for line in text.lines(){
        for c in line.chars(){
            data.push(c);
        }
    }
    println!("Imported seat plan of {} by {}", width, height);
    puzzle1(data.clone(), width);
    puzzle2(data.clone(), width);
    //nice_print(&data, width);
}