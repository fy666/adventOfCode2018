fn get_presents(input: i32) -> i32 {
    let mut presents = 0;
    let sqrt = (input as f64).sqrt() as i32;
    for i in 1..sqrt + 1 {
        if input.rem_euclid(i) == 0 {
            presents += i * 10;
            if (input / i) != i {
                presents += (input / i) * 10;
            }
        }
    }
    presents
}

fn get_lazy_presents(input: i32) -> i32 {
    let mut presents = 0;
    let sqrt = (input as f64).sqrt() as i32;
    for i in 1..sqrt + 1 {
        if input.rem_euclid(i) == 0 {
            let div = input / i;
            if div <= 50 {
                presents += i * 11;
            }
            if div != i && i <= 50 {
                presents += div * 11;
            }
        }
    }
    presents
}

pub fn run(test: bool) {
    if test {
        for h in 1..10 {
            log::debug!("House {} got {} presents", h, get_presents(h));
        }
        for h in 1..10 {
            log::debug!(
                "House {} got {} presents (lazy elves)",
                h,
                get_lazy_presents(h)
            );
        }
    } else {
        let lowest_gifts = 29000000;
        let mut lowest_house = 10;
        let mut gifts = get_presents(lowest_house);
        while gifts < lowest_gifts {
            lowest_house += 1;
            gifts = get_presents(lowest_house);
        }
        log::info!(
            "After 🧝 distribution, 🏠 {} has {} 🎁",
            lowest_house,
            get_presents(lowest_house)
        );
        // Part 2
        lowest_house = 10;
        gifts = get_lazy_presents(lowest_house);
        while gifts < lowest_gifts {
            lowest_house += 1;
            gifts = get_lazy_presents(lowest_house);
        }
        log::info!(
            "After lazy 🧝 distribution, 🏠 {} has {} 🎁",
            lowest_house,
            get_presents(lowest_house)
        );
    }
}
