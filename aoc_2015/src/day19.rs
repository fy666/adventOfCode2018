//use itertools::Itertools;
//use onig::Regex;
//use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

fn get_best_match(input: &str, replacements: &Vec<Vec<&str>>) -> usize {
    let mut best_rep = -1;
    let mut best_index = 0; //nput.len();
                            //let mut best_score = -1;
    for (ix, rep) in replacements.iter().enumerate() {
        for (index, _m) in input.match_indices(rep[1]) {
            //log::trace!("potential rep {:?}", rep);
            // let tmp_score = (rep[1].len() - rep[0].len()) as i32;
            // if tmp_score > best_score {
            //     best_score = tmp_score;
            //     best_rep = ix as i32;
            // }
            if index > best_index {
                best_rep = ix as i32;
                best_index = index;
            }
        }
    }
    if best_rep == -1 {
        panic!("No match found in {:?}", input)
    }
    best_rep as usize
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n\n").collect();
    let raw_replacements: Vec<Vec<&str>> = data[0]
        .trim()
        .split("\n")
        .map(|x| x.split(" => ").collect())
        .collect();
    log::debug!(
        "Imported {} replacements : {:?}",
        raw_replacements.len(),
        raw_replacements
    );
    let molecule = data[1];
    log::debug!("Molecule to find: {}", molecule);
    let mut molecules: HashSet<String> = HashSet::new();
    for rep in raw_replacements.iter() {
        for (index, _m) in molecule.match_indices(rep[0]) {
            let mut new_s = molecule.to_string();
            new_s.replace_range(index..index + rep[0].len(), rep[1]);
            molecules.insert(new_s);
        }
    }
    log::info!("{} distinct molecules", molecules.len());
    //log::trace!(" {:?}", molecules);

    let mut medicine = data[1].to_string();
    let mut operations = 0;
    while medicine != "e" {
        // find closer longer match
        let i = get_best_match(&medicine, &raw_replacements);
        let (index, _m) = medicine
            .match_indices(raw_replacements[i][1])
            .max_by_key(|x| x.0)
            .unwrap();
        medicine.replace_range(
            index..index + raw_replacements[i][1].len(),
            raw_replacements[i][0],
        );

        //medicine = medicine.replacen(raw_replacements[i][1], raw_replacements[i][0], 1);
        log::trace!(
            "{} replacing {:?} -> {:?}",
            operations,
            raw_replacements[i],
            medicine
        );
        // replace
        operations += 1;
    }
    log::info!("After {:?} operations -> {:?}", operations, medicine);
}
