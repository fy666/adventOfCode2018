use std::fs;
use std::collections::HashSet;

fn count_different_answers(answer: &str) -> i32{
    let mut set: HashSet<char> = HashSet::new();
    for letter in answer.chars(){
        if letter == '\n'{
            continue;
        }
        set.insert(letter);
    }
    println!("Subset {} = {}", answer, set.len());
    set.len() as i32
}

fn count_same_answers(answer: &str) -> i32{
    let mut count = 0;
    let mut set: HashSet<char> = HashSet::new();
    let people_in_group = answer.lines().count();
    for letter in (b'a' ..= b'z').map(char::from){
       let c = answer.matches(letter).count();
       
       if c == people_in_group{
           count +=1
       }
    }
    //println!("Subset {} = {}", answer, count);
   count
}

fn puzzle(answers: &Vec<&str>) {
    let mut count1 = 0;
    let mut count2 = 0;
    for answer in answers{
        count1 += count_different_answers(&answer);
        count2 += count_same_answers(&answer);
    }
    println!("Total different answers is {}", count1);
    println!("Total same answers is {}", count2);
}

fn main() {
    //let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.split("\n\n");
    let data = split.collect::<Vec<&str>>();
    println!("Imported {} groups", data.len());
    puzzle(&data);
}