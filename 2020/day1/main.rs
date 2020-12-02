//use std::io;
//use std::cmp::Ordering;
use std::fs;

fn puzzle1(arr: &Vec<i32>){
    'outer: for var1 in arr {
        for var2 in arr {
            if var1+var2 == 2020 {
                println!("{} * {} = {}", var1, var2, var1*var2);
                break 'outer
            }
        }
    }
}

fn puzzle2(arr: &Vec<i32>){
    'outer: for var1 in arr {
        for var2 in arr {
            for var3 in arr {
                if var1+var2+var3 == 2020 {
                    println!("{} * {} * {} = {}", var1, var2, var3, var1*var2*var3);
                    break 'outer
                }
            }
        }
    }
}

fn main() {
    let input = vec![1721, 979,366,299,675,1456];
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let mut data : Vec<i32> = Vec::new();
    for line in text.lines(){
        data.push(line.parse().expect("Line is not a int"));
    }
    println!("Puzzle 1 on test");
    puzzle1(&input);
    println!("Puzzle 1 on input");
    puzzle1(&data);

    println!("Puzzle 2 on test");
    puzzle2(&input);
    println!("Puzzle 2 on input");
    puzzle2(&data);

    //println!("Guess the number!");


   /*  let secret_number = 101; //rand::thread_rng().gen_range(1, 101);

    println!("The secret number is: {}", secret_number);

    loop {
        println!("Please input your guess.");

        let mut guess = String::new();

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        println!("You guessed: {}", guess);

        let guess: i32 = guess.trim().parse().expect("Please type a number!");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    } */
}