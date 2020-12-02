use std::fs;

fn count_consec(data: &Vec<usize>){
    let mut c : Vec<usize> = Vec::new();
    let mut count = 0;
    //let num_1 = 
    for i in data {
        if (*i as i32) == 3{
            c.push(count);
            count = 0
        }
        else{
            count += 1;
        }
    }
    let mmax = c.iter().max().unwrap() + 1;
    //println!("max ={}", mmax);
    for i in 1..mmax{
        let number = c.iter().filter(|&n| *n == i).count();
        println!("{} groups of {} consecutive 1", number, i);
    }
    println!("Res = {:?}", c);
}



fn main() {
    //let file = "small.txt";
    //let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n").map(|x| x.parse::<usize>().unwrap());
    let mut data = split.collect::<Vec<usize>>();
    println!("Imported {} numbers", data.len());
    println!("Vector first {:?}", data);
    data.push(0);
    data.push(data.iter().max().unwrap()+3);
    data.sort();
    //println!("{:?}",data.windows(2).map(|w| w[1] - w[0]));
    println!("Vector sorted {:?}", data);
    let result = &data.windows(2).map(|w| w[1] - w[0]).collect::<Vec<_>>();
    println!("{:?}, len = {}", result, result.len()); // [2, 2, 4, 4, 1]
    let num_1 = result.iter().filter(|&n| *n == 1).count();
    let num_3 = result.iter().filter(|&n| *n == 3).count();
    println!("{} 1, {} 3, res = {}", num_1, num_3, num_1*num_3);

    count_consec(&result);
    //result2.push_front();
    // let result2 = &data.windows(3).map(|w| ((w[1] as i32) -(w[0] as i32)).abs() + ((w[2] as i32) -(w[1] as i32)).abs()).collect::<Vec<_>>();
    // let skippable = result2.iter().filter(|&n| *n < 3).count();
    // println!("{:?}, len = {}", result2, result2.len()); // [2, 2, 4, 4, 1]
    // println!("Skipable : {}", skippable);
    //let res = puzzle1(&data, 25);
    //puzzle2(&data, res);
}
