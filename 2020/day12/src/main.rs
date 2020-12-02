use std::env;
use std::fs;

static DIRECTIONS: [(i32, i32); 4] = [(1, 0), (0, 1), (-1, 0), (0, -1)];

struct Ship {
    x: i32,
    y: i32,
    waypoint: (i32, i32),
    dir_x: i32,
    dir_y: i32,
}

impl Ship {
    fn move_ship(&mut self, cmd: (char, i32)) {
        match cmd.0 {
            'N' => self.y += cmd.1,
            'E' => self.x += cmd.1,
            'W' => self.x -= cmd.1,
            'S' => self.y -= cmd.1,
            'F' => {
                self.y += self.dir_y * cmd.1;
                self.x += self.dir_x * cmd.1;
            }
            'R' | 'L' => {
                if cmd.1 == 180 {
                    self.dir_y = -self.dir_y;
                    self.dir_x = -self.dir_x;
                } else {
                    let mut index: isize = DIRECTIONS
                        .iter()
                        .position(|&r| r.0 == self.dir_x && r.1 == self.dir_y)
                        .unwrap() as isize;
                    if (cmd.0 == 'R' && cmd.1 == 90) || (cmd.0 == 'L' && cmd.1 == 270) {
                        index = (index - 1).rem_euclid(DIRECTIONS.len() as isize);
                    } else if (cmd.0 == 'R' && cmd.1 == 270) || (cmd.0 == 'L' && cmd.1 == 90) {
                        index = (index + 1).rem_euclid(DIRECTIONS.len() as isize);
                    }
                    self.dir_x = DIRECTIONS[index as usize].0;
                    self.dir_y = DIRECTIONS[index as usize].1;
                }
            }
            _ => println!("Command {} not matched", cmd.0),
        }
    }

    fn get_manathan(&self) -> i32 {
        self.x.abs() + self.y.abs()
    }

    fn move_waypoint(&mut self, cmd: (char, i32)) {
        match cmd.0 {
            'N' => self.waypoint.1 += cmd.1,
            'E' => self.waypoint.0 += cmd.1,
            'W' => self.waypoint.0 -= cmd.1,
            'S' => self.waypoint.1 -= cmd.1,
            'F' => {
                self.y += self.waypoint.1 * cmd.1;
                self.x += self.waypoint.0 * cmd.1;
            }
            'R' | 'L' => {
                if cmd.1 == 180 {
                    self.waypoint = (-self.waypoint.0, -self.waypoint.1);
                } else if (cmd.0 == 'R' && cmd.1 == 90) || (cmd.0 == 'L' && cmd.1 == 270) {
                    self.waypoint = (self.waypoint.1, -self.waypoint.0);
                } else if (cmd.0 == 'R' && cmd.1 == 270) || (cmd.0 == 'L' && cmd.1 == 90) {
                    self.waypoint = (-self.waypoint.1, self.waypoint.0);
                }
            }
            _ => println!("Command {} not matched", cmd.0),
        }
    }

    fn print_pos(&self) {
        println!(
            "Position ship ({},{}), direction : ({},{}), position waypoint ({:?})",
            self.x, self.y, self.dir_x, self.dir_y, self.waypoint
        );
    }
}

fn puzzle1(moves: &Vec<(char, i32)>) {
    let mut ship = Ship {
        x: 0,
        y: 0,
        dir_x: 1,
        dir_y: 0,
        waypoint: (10, 1),
    };
    for m in moves {
        //println!("Appliying {:?}",m);
        ship.move_ship(*m);
        //ship.print_pos();
    }
    ship.print_pos();
    println!("Distance to final position = {}", ship.get_manathan());
}

fn puzzle2(moves: &Vec<(char, i32)>) {
    let mut ship = Ship {
        x: 0,
        y: 0,
        dir_x: 1,
        dir_y: 0,
        waypoint: (10, 1),
    };
    for m in moves {
        //println!("Appliying {:?}",m);
        ship.move_waypoint(*m);
        //ship.print_pos();
    }
    ship.print_pos();
    println!("Distance to final position = {}", ship.get_manathan());
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut file = args[1].clone();
    if !file.ends_with(".txt") {
        file += &".txt".to_string();
    }
    println!("Reading = {}", file);
    let text = fs::read_to_string(file).expect("File not found");
    let data = text
        .trim()
        .split("\n")
        .map(|x| ((&x[..1]).chars().next().unwrap(), x[1..].parse().unwrap()))
        .collect::<Vec<(char, i32)>>();
    println!("Imported {} instructions", data.len());
    puzzle1(&data);
    puzzle2(&data);
}
