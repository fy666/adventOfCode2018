use onig::Regex;
use std::fs;

fn is_nice_p1(txt: &str) -> bool {
    let mut is_nice: bool = txt.chars().filter(|&x| "aeiou".contains(x)).count() >= 3;
    if !is_nice {
        log::trace!("{} doesnt contain at least 3 voyels", txt);
        return is_nice;
    }
    let regex_double = Regex::new(r".*([a-z])\1.*").unwrap();
    is_nice = regex_double.is_match(txt);
    if !is_nice {
        log::trace!("{} doesnt contain 2 successive letters", txt);
        return is_nice;
    }
    let regex_forbidden = Regex::new(r".*(ab|cd|pq|xy).*").unwrap();
    is_nice = !regex_forbidden.is_match(txt);
    if !is_nice {
        log::trace!("{} contains ab, cd, pq or xy", txt);
    } else {
        log::trace!("{} is nice", txt);
    }
    is_nice
}

fn is_nice_p2(txt: &str) -> bool {
    let regex_double = Regex::new(r".*([a-z]{2}).*\1.*").unwrap();
    let mut is_nice: bool = regex_double.is_match(txt);
    if !is_nice {
        log::trace!("{} doesnt contain 2 letters that repeats", txt);
        return is_nice;
    }
    let regex_forbidden = Regex::new(r".*([a-z]).\1.*").unwrap();
    is_nice = regex_forbidden.is_match(txt);
    if !is_nice {
        log::trace!("{} doesnt contains xax", txt);
    } else {
        log::trace!("{} is nice", txt);
    }
    is_nice
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} 🔑", data.len());
    let nice_p1 = data.iter().filter(|x| is_nice_p1(x)).count();
    let nice_p2 = data.iter().filter(|x| is_nice_p2(x)).count();
    log::info!("{} 🤗 strings, {} 🤗 strings", nice_p1, nice_p2);
}
