use std::fs;
use regex::Regex;
use std::collections::HashMap;
use std::collections::VecDeque;
use lazy_static::lazy_static; // 1.3.0

fn rec(childs: &HashMap<String, Vec<(String, i32)>>, current_node: &(String,i32)) -> i32 {
    let mut count = current_node.1;
    println!("On node {:?}", current_node);
    if !childs.contains_key(&current_node.0){
        //println!("not in list, return own value {}", current_node.1);
        return current_node.1;
    }
    for i in childs.get(&current_node.0).unwrap().iter(){
        //println!("go on node {:?}", i);
        count += rec(&childs, i) * current_node.1;
        println!("Count on {:?} = {}", current_node, count);
    }
    count
}


fn get_all_parents(parents: &HashMap<String, Vec<String>>){
    let mut wanted : VecDeque<String> = VecDeque::new();
    wanted.push_back(String::from("shiny gold"));
    let mut ancestors : Vec<String> = Vec::new();
    while wanted.len() > 0 {
        let key = wanted.pop_front().unwrap();
        for i in parents.get(&key).unwrap().iter(){
            if !ancestors.contains(i){
                ancestors.push(i.to_string());
                if parents.contains_key(i){
                    wanted.push_back(i.to_string());
                }
            }
        }
    }
    println!("Shiny bag found in {} bags", ancestors.len());
}

fn puzzle1(rules: &Vec<&str>) {
    let mut parents : HashMap<String, Vec<(String, i32)>> = HashMap::new();
    let mut childs : HashMap<String, Vec<String>> = HashMap::new();
    for p in rules{
       //all_bags.push(to_rule(p));
        add_entry(p, &mut parents, &mut childs);
    }
    for (parent, child)  in &parents{
        println!("{} has childs: {:?}", parent, child);
    }
    let shiny = (String::from("shiny gold"), 1);
    let result = rec(&parents, &shiny);
    println!("Shiny gold contains {} bags", result-1);
}

fn add_entry(line:&str, parents: &mut HashMap<String, Vec<(String, i32)>>, childs: &mut HashMap<String, Vec<String>>) {
    lazy_static! {
        static ref RE : Regex = Regex::new(r"^(\w* \w*) bags contain").unwrap();
        static ref RE_LAST : Regex= Regex::new(r"^(\w* \w*) bags contain no other bags").unwrap();
        static ref RE_BAGS :Regex = Regex::new(r"(\d) (\w* \w*) bag").unwrap();
    }
    if RE_LAST.is_match(line){
        // Last bag, nothing to do
        return        
    }
    else{
        let first = RE.captures(line).unwrap().get(1).unwrap().as_str();
        let mut child_list : Vec<(String,i32)> = Vec::new();
        for cap in RE_BAGS.captures_iter(line) {
            child_list.push((cap[2].to_string(), cap[1].parse().unwrap()));
            childs.entry((&cap[2]).to_string()).or_insert_with(Vec::new).push(first.to_string());
        }
        parents.insert(first.to_string(), child_list);
    }
}

fn main() {
    //let file = "test.txt";
    //let file = "test2.txt";
    let file = "puzzle.txt";
    let text = fs::read_to_string(file).expect("File not found");
    let split = text.trim().split("\n");
    let data = split.collect::<Vec<&str>>();
    println!("Imported {} luggages descriptions", data.len());
    puzzle1(&data);
}