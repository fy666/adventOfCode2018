fn look_and_say(txt: &str) -> String {
    let mut res = String::new();
    let mut curr = txt.chars().next().unwrap();
    let mut it = txt.chars();
    let mut count = 0;
    while let Some(c) = it.next() {
        if c == curr {
            count += 1;
        } else {
            res += &format!("{}{}", count, curr);
            count = 1;
            curr = c;
        }
    }
    res += &format!("{}{}", count, curr);
    log::trace!("{} -> {}", txt, res);
    res
}

pub fn run(test_mode: bool) {
    let mut input;
    if test_mode {
        input = String::from("211");
    } else {
        input = String::from("1113122113");
    }
    let mut len_after_40 = 0;
    for c in 0..50 {
        input = look_and_say(&input);
        if c == 40 {
            len_after_40 = input.len();
        }
    }
    log::info!(
        "👀 and 👄 length after 40 = {}, length after 50 = {}",
        len_after_40,
        input.len()
    );
}
