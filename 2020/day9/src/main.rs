use std::fs;


fn is_sum_in_list(num: &[usize], wanted: usize) -> bool{
    //println!("Searching for {} in {:?}", wanted, num);
    for i in 0..num.len()-1 {
        let mut j = i+1;
        while j < num.len() {
            //println!("{},{}", i,j);
            if num[i]+num[j]== wanted{
                //println!(" = {} + {}", num[i], num[j]);
                return true
            }
            j=j+1;
        }
    }
    return false
}

fn puzzle1(numbers: &Vec<usize>, seq_len: usize)-> usize{
    let mut i : usize = seq_len;
    let res = loop{
        if !is_sum_in_list(&numbers[i-seq_len..i], numbers[i]){
            break numbers[i];
        }
        i=i+1;
    };
    println!("First invalid number is {}", res);
    res
}

fn puzzle2(numbers: &Vec<usize>, wanted: usize){
    let mut start : usize = 0;
    let mut end : usize = 1;
    let mut count;
    let res = loop{
        count = numbers[start..end].into_iter().sum::<usize>();
        if count == wanted{
            //println!("Range = {:?}", res);
            break &numbers[start..end];
        }
        else if count < wanted{
            end=end +1
        }
        else{
            start= start+1;
            end = start+1;
        }
    };
    println!("Range = {:?} sum of min and max = {}", res, res.iter().min().unwrap()+res.iter().max().unwrap());
}

fn main() {
    //let file = "test.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n").map(|x| x.parse::<usize>().unwrap());
    let data = split.collect::<Vec<usize>>();
    println!("Imported {} numbers", data.len());
    let res = puzzle1(&data, 25);
    puzzle2(&data, res);
}
