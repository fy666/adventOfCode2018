fn get_val(a: u64, subject_num: u64) -> u64 {
    // let res = a * 7;
    (a * subject_num).rem_euclid(20201227)
}

fn get_encryption_key(val: u64, loopsize: u64) -> u64 {
    let mut tmp = 1;
    for _ in 0..loopsize {
        tmp = get_val(tmp, val);
    }
    tmp
}

fn main() {
    let door_public_key = 17_807_724;
    let card_public_key = 5764801;

    let door_public_key = 12320657;
    let card_public_key = 9659666;

    // find door loopsize
    let mut door_loopsize = 0;
    let mut value = 1;
    while value != door_public_key {
        value = get_val(value, 7);
        door_loopsize += 1;
        //println!("Loop {} val is {}", door_loopsize, value);
    }
    println!("Door loopsize = {}", door_loopsize);

    // find card loopsize
    let mut card_loopsize = 0;
    let mut value = 1;
    while value != card_public_key {
        value = get_val(value, 7);
        card_loopsize += 1;
        //println!("Loop {} val is {}", door_loopsize, value);
    }
    println!("Card loopsize = {}", card_loopsize);

    println!(
        "Encryption key {} {}",
        get_encryption_key(door_public_key, card_loopsize),
        get_encryption_key(card_public_key, door_loopsize)
    )
}
