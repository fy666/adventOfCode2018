use std::cmp::max;
use std::cmp::min;

#[derive(Debug, Clone, Copy)]
struct Player {
    hit_points: i32,
    damage: i32,
    armor: i32,
    cost: i32,
}

#[derive(Debug)]
struct Gear {
    cost: i32,
    damage: i32,
    armor: i32,
    name: String,
}

impl Player {
    pub fn get_attacked(&mut self, damage: i32) {
        let real_damage = max(damage - self.armor, 1);
        self.hit_points -= real_damage;
    }
    pub fn equip(&mut self, gear: &Gear) {
        self.damage += gear.damage;
        self.armor += gear.armor;
        self.cost += gear.cost;
    }
    pub fn unequip(&mut self, gear: &Gear) {
        self.damage -= gear.damage;
        self.armor -= gear.armor;
        self.cost -= gear.cost;
    }
}

fn game_result(mut player: Player, mut boss: Player) -> bool {
    loop {
        boss.get_attacked(player.damage);
        if boss.hit_points <= 0 {
            break true;
        }
        player.get_attacked(boss.damage);
        if player.hit_points <= 0 {
            break false;
        }
    }
}

pub fn run(test: bool) {
    let mut weapons: Vec<Gear> = Vec::new();
    weapons.push(Gear {
        name: "Dagger".to_string(),
        cost: 8,
        damage: 4,
        armor: 0,
    });
    weapons.push(Gear {
        name: "Shortsword".to_string(),
        cost: 10,
        damage: 5,
        armor: 0,
    });
    weapons.push(Gear {
        name: "Warhammer".to_string(),
        cost: 25,
        damage: 6,
        armor: 0,
    });
    weapons.push(Gear {
        name: "Longsword".to_string(),
        cost: 40,
        damage: 7,
        armor: 0,
    });
    weapons.push(Gear {
        name: "Gretaxe".to_string(),
        cost: 74,
        damage: 8,
        armor: 0,
    });
    let mut armors: Vec<Gear> = Vec::new();
    armors.push(Gear {
        name: "Leather".to_string(),
        cost: 13,
        damage: 0,
        armor: 1,
    });
    armors.push(Gear {
        name: "Chainmail".to_string(),
        cost: 31,
        damage: 0,
        armor: 2,
    });
    armors.push(Gear {
        name: "Splintmail".to_string(),
        cost: 53,
        damage: 0,
        armor: 3,
    });
    armors.push(Gear {
        name: "Bandedmail".to_string(),
        cost: 75,
        damage: 0,
        armor: 4,
    });
    armors.push(Gear {
        name: "Platemail".to_string(),
        cost: 102,
        damage: 0,
        armor: 5,
    });
    armors.push(Gear {
        name: "No arm".to_string(),
        cost: 0,
        damage: 0,
        armor: 0,
    });
    let mut rings: Vec<Gear> = Vec::new();
    rings.push(Gear {
        name: "No ring".to_string(),
        cost: 0,
        damage: 0,
        armor: 0,
    });
    rings.push(Gear {
        name: "Damage +1".to_string(),
        cost: 25,
        damage: 1,
        armor: 0,
    });
    rings.push(Gear {
        name: "Damage +2".to_string(),
        cost: 50,
        damage: 2,
        armor: 0,
    });
    rings.push(Gear {
        name: "Damage +3".to_string(),
        cost: 100,
        damage: 3,
        armor: 0,
    });
    rings.push(Gear {
        name: "Defense +1".to_string(),
        cost: 20,
        damage: 0,
        armor: 1,
    });
    rings.push(Gear {
        name: "Defense +2".to_string(),
        cost: 40,
        damage: 0,
        armor: 2,
    });
    rings.push(Gear {
        name: "Defense +3".to_string(),
        cost: 80,
        damage: 0,
        armor: 3,
    });

    if test {
        let mut player = Player {
            hit_points: 8,
            damage: 0,
            armor: 0,
            cost: 0,
        };
        let boss = Player {
            hit_points: 12,
            damage: 7,
            armor: 2,
            cost: 0,
        };
        println!("Equipment cost: {}", player.cost);
        println!("{}", game_result(player.clone(), boss.clone()));

        let mut min_gear_cost = 1000;
        for weap in weapons.iter() {
            player.equip(weap);
            let tmp = player.cost;
            if game_result(player.clone(), boss.clone()) {
                min_gear_cost = min(tmp, min_gear_cost);
            }
        }
        println!("Min weapon cost: {}", min_gear_cost);
    } else {
        let mut player = Player {
            hit_points: 100,
            damage: 0,
            armor: 0,
            cost: 0,
        };
        let boss = Player {
            hit_points: 109,
            damage: 8,
            armor: 2,
            cost: 0,
        };
        let mut min_gear_cost_to_win = 1000;
        let mut max_gear_cost_to_loose = 0;
        for weap in weapons.iter() {
            player.equip(weap);
            for arm in armors.iter() {
                player.equip(arm);
                for ring1 in rings.iter() {
                    player.equip(ring1);
                    for ring2 in rings.iter() {
                        if ring1.name == ring2.name && ring2.name != "No ring" {
                            continue;
                        }
                        player.equip(ring2);
                        log::trace!(
                            "Player {:?} equipped with {},{},{} and {}",
                            player,
                            weap.name,
                            arm.name,
                            ring1.name,
                            ring2.name
                        );
                        if game_result(player.clone(), boss.clone()) {
                            min_gear_cost_to_win = min(player.cost, min_gear_cost_to_win);
                        } else {
                            max_gear_cost_to_loose = max(player.cost, max_gear_cost_to_loose);
                        }
                        player.unequip(ring2);
                    }
                    player.unequip(ring1);
                }
                player.unequip(arm);
            }
            player.unequip(weap);
        }
        log::info!("⚔️  min 💰 needed to win: {}", min_gear_cost_to_win);
        log::info!(
            "⚔️  most 💰 needed to still loose: {}",
            max_gear_cost_to_loose
        );
    }
}
