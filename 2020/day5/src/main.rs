use std::fs;


fn dico_search(range: [i32;2], up: bool) -> [i32;2]{
    let mid = (range[1]-range[0])/2;
    //println!("Input range {},{} mid = {}", range[0], range[1], mid);
    if up{
        return [range[0], range[0]+mid];
    }
    else{
        return [range[0]+mid+1, range[1]];
    }
}

fn find_position(seat : &str, first_range: [i32;2], crit: char)->i32{
    let mut range=first_range;
    for i in seat.chars(){
        range = dico_search(range, i==crit);
    }
    if range[0]==range[1]{
        return range[0];
    }
    else{
        println!("Range not unique !!!");
        return 0;
    }
}

fn find_seat(seat: &String) -> [i32;2]{
    let mut res=[0,0];
    res[0]=find_position(&seat[..7], [0,127], 'F'); // row
    res[1]=find_position(&seat[7..], [0,7], 'L'); // col
    res
}

fn get_seat_id(seat: &String) ->i32{
    let seat_num = find_seat(&seat);
    return seat_num[0]*8 + seat_num[1];
}

// fn puzzle1(seats: &Vec<&str>) {
//     let mut max_id = get_seat_id(&seats[0].to_string());
//     for seat in seats{
//         let id = get_seat_id(&seat.to_string());
//         if id > max_id{
//             max_id = id;
//         }
//     }
//     println!("Max id = {}", max_id);    
// }

fn puzzle(seats: &Vec<&str>) {
    let mut all_seats = [0;789];
    for (ix,seat) in seats.iter().enumerate(){
        all_seats[ix] = get_seat_id(&seat.to_string());
    }
    let max_id = all_seats.iter().max().unwrap();
    println!("Max seat ID = {}", max_id);

    for n in 0..*max_id{
        if !all_seats.contains(&n) && all_seats.contains(&(&n-1)) && all_seats.contains(&(&n+1)) {
            println!("{} not in list", n);
        }
    }
}

fn main() {
    //let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.split("\n");
    let data = split.collect::<Vec<&str>>();
    println!("Imported {} seats", data.len());
    puzzle(&data);
}