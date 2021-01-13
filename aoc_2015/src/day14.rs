use onig::Regex;
use std::cmp::Ordering;
use std::fs;

#[derive(Debug, Eq)]
struct Reindeer {
    name: String,
    speed: i32,
    fly_time: i32,
    rest_time: i32,
    score: i32,
    position: i32,
}

impl Reindeer {
    pub fn get_distance(&self, time: i32) -> i32 {
        let full_cycles: i32 = time / (self.fly_time + self.rest_time) as i32;
        let remainder: i32 = time.rem_euclid(self.fly_time + self.rest_time);
        let mut distance = full_cycles * self.speed * self.fly_time;
        if remainder >= self.fly_time {
            distance += self.speed * self.fly_time;
        } else {
            distance += self.speed * remainder;
        }
        distance
    }

    pub fn run(&mut self, time: i32) {
        self.position = self.get_distance(time);
    }
}

impl Ord for Reindeer {
    fn cmp(&self, other: &Self) -> Ordering {
        self.position.cmp(&other.position)
    }
}

impl PartialOrd for Reindeer {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for Reindeer {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name
    }
}

pub fn run(file: &String, test: bool) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} reindeers", data.len());
    let mut runtime = 2503;
    if test {
        runtime = 2503;
    }
    let mut reindeers: Vec<_> = Vec::new();
    let regex = Regex::new(
        r"(.*) can fly (\d*) km/s for (\d*) seconds, but then must rest for (\d*) seconds.",
    )
    .unwrap();
    for deer in data {
        let capture = regex.captures(deer).unwrap();
        let name = capture.at(1).unwrap().to_string();
        let speed: i32 = capture.at(2).unwrap().parse().unwrap();
        let fly_time = capture.at(3).unwrap().parse().unwrap();
        let rest_time = capture.at(4).unwrap().parse().unwrap();
        let score = 0;
        let position = 0;
        reindeers.push(Reindeer {
            name,
            speed,
            fly_time,
            rest_time,
            score,
            position,
        });
    }
    log::trace!("🦌 reindeers = {:?}", reindeers);

    for i in 1..runtime + 1 {
        reindeers.iter_mut().for_each(|x| x.run(i));
        let best_pos = reindeers.iter_mut().max().unwrap().position;
        reindeers.iter_mut().for_each(|x| {
            if x.position == best_pos {
                x.score += 1;
            }
        });
        log::trace!(
            "At {} s, {:?} is ahead",
            i,
            reindeers.iter().max().unwrap().name
        );
    }

    let first_winner = reindeers.iter().max().unwrap();
    let second_winner = reindeers.iter().max_by_key(|x| x.score).unwrap();
    log::info!(
        "First round winner 🏆🦌 {} at {} km",
        first_winner.name,
        first_winner.position
    );
    log::info!(
        "Second round winner 🏆🦌 {} with score {}",
        second_winner.name,
        second_winner.score
    );
}
