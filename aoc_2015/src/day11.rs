use num::bigint::BigUint;
use onig::Regex;
use std::collections::HashSet;

fn is_valid(txt: &str) -> bool {
    if txt.contains("i") || txt.contains("o") || txt.contains("l") {
        log::trace!("{} invalid (invalid char)", txt);
        return false;
    }

    let regex_double = Regex::new(r"([a-z])\1").unwrap();

    let caps: HashSet<&str> = regex_double
        .captures_iter(txt)
        .map(|x| x.at(1).unwrap())
        .collect();
    if caps.len() < 2 {
        log::trace!("{} invalid (not enough pairs)", txt);
        return false;
    }

    let tmp: Vec<u8> = txt.chars().map(|x| x as u8).collect();
    for j in tmp.windows(3) {
        if j[1] == j[0] + 1 && j[2] == j[1] + 1 {
            log::trace!("{} valid (found increasing seq)", txt);
            return true;
        }
    }
    log::trace!("{} invalid (no increasing seq)", txt);
    false
}

fn next_pass(txt: &str) -> String {
    let mut res: String;
    let mut z = BigUint::from(u128::from_str_radix(txt, 36).unwrap());
    z = z + 1 as u32;
    res = BigUint::to_str_radix(&z, 36);
    while !res.chars().all(|x| !x.is_numeric()) {
        z = z + 1 as u32;
        res = BigUint::to_str_radix(&z, 36);
    }
    res
}

pub fn run(test_mode: bool) {
    if test_mode {
        is_valid("hijklmmn");
        is_valid("abc");
        is_valid("aaaabc");
        is_valid("aabcaa");
        is_valid("abbceffg");
        is_valid("abbcegjk");
        is_valid("abbceddgjkxyz");
        is_valid("hxbxwxba");
        let z = BigUint::from(u64::from_str_radix("abcdefgh", 36).unwrap());
        println!("z = {}, {}", z, BigUint::to_str_radix(&z, 36));
    } else {
        let input = String::from("hxbxwxba");
        let mut next_p = next_pass(&input);
        while !is_valid(&next_p) {
            next_p = next_pass(&next_p);
        }
        println!("Next valid password is {}", next_p);

        let mut next_p = next_pass(&next_p);
        while !is_valid(&next_p) {
            next_p = next_pass(&next_p);
        }
        println!("Second next valid password is {}", next_p);
    }
}
