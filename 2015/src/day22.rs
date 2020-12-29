use std::cmp::max;
//use std::cmp::min;

#[derive(Debug, Eq, PartialEq, Clone, Copy)]
enum Effect {
    MagicMissile,
    Shield,
    Drain,
    Poison,
    Recharge,
}

#[derive(Debug, Clone)]
struct Player {
    hit_points: i32,
    damage: i32,
    mana: i32,
    effects: Vec<(Effect, i32, i32)>,
    spells: Vec<Effect>,
    spent_mana: i32,
}

fn build_player(hit_points: i32, damage: i32, mana: i32) -> Player {
    Player {
        hit_points: hit_points,
        damage: damage,
        mana: mana,
        effects: Vec::new(),
        spent_mana: 0,
        spells: Vec::new(),
    }
}

impl Player {
    pub fn get_attacked(&mut self, damage: i32) {
        if damage > 0 {
            let real_damage = max(damage - self.get_armor(), 1);
            self.hit_points -= real_damage;
        }
    }

    pub fn killed(&self) -> bool {
        self.hit_points <= 0
    }

    fn get_armor(&self) -> i32 {
        if self.effects.iter().any(|&i| i.0 == Effect::Shield) {
            return 7;
        }
        0
    }

    pub fn cast(&mut self, cast: (Effect, i32, i32)) -> i32 {
        let mut damage = 0;
        self.spent_mana += cast.2;
        self.mana -= cast.2;
        self.spells.push(cast.0);
        // if self.mana < 0 {
        //     log::warn!("Player has no mana left !!");
        // }
        match cast.0 {
            Effect::MagicMissile => damage = 4,
            Effect::Shield | Effect::Poison | Effect::Recharge => self.effects.push(cast),
            Effect::Drain => {
                damage = 2;
                self.hit_points += 2
            }
        }
        return damage;
    }

    pub fn apply_effects(&mut self) -> i32 {
        let mut hit_points = 0;
        for effect in self.effects.iter_mut() {
            effect.1 -= 1;
            match effect.0 {
                Effect::Poison => hit_points += 3,
                Effect::Recharge => self.mana += 101,
                Effect::Shield => {}
                _ => log::warn!("Unmatched case !"),
            }
        }
        self.effects.retain(|&x| x.1 > 0);
        return hit_points;
    }
}

fn play_turn(
    player: &mut Player,
    boss: &mut Player,
    cast: (Effect, i32, i32),
    deadly_first_turn: bool,
) {
    log::trace!("----- Player turns ------");
    log::trace!("Player {:?}", player);
    log::trace!("Boss {:?}", boss);
    if deadly_first_turn {
        player.hit_points -= 1;
        if player.killed() {
            return;
        }
    }
    boss.get_attacked(player.apply_effects());
    if boss.killed() {
        log::trace!("Boss is dead");
        return;
    }
    boss.get_attacked(player.cast(cast));
    if boss.killed() {
        log::trace!("Boss is dead");
        return;
    }
    log::trace!("----- Boss turns ------");
    log::trace!("Player {:?}", player);
    log::trace!("Boss {:?}", boss);
    if deadly_first_turn {
        player.hit_points -= 1;
        if player.killed() {
            return;
        }
    }

    boss.get_attacked(player.apply_effects());
    if boss.killed() {
        log::trace!("Boss is dead");
        return;
    }
    player.get_attacked(boss.damage);
}

fn game_result(
    player: Player,
    boss: Player,
    spells: &Vec<(Effect, i32, i32)>,
    spent_mana: &mut Vec<i32>,
    deadly_first_turn: bool,
) {
    for spell in spells.iter() {
        if !player.effects.iter().any(|&x| x.0 == spell.0 && x.1 > 1) {
            //log::debug!("Casting {:?}", spell);
            let mut new_player = player.clone();
            let mut new_boss = boss.clone();
            play_turn(&mut new_player, &mut new_boss, *spell, deadly_first_turn);
            if new_player.mana < 0 {
                // No need to check result, go to next
                continue;
            } else if new_boss.killed() && !new_player.killed() {
                spent_mana.push(new_player.spent_mana);
                log::debug!("Player wins with {} mana", new_player.spent_mana);
                log::trace!("List of spells : {:?}", new_player.spells);
            } else if !new_player.killed()
                && (spent_mana.len() == 0
                    || player.spent_mana + spell.2 < *spent_mana.iter().min().unwrap())
            {
                // is it worth to continue?
                game_result(new_player, new_boss, &spells, spent_mana, deadly_first_turn);
            }
        }
    }
}

pub fn run(test: bool) {
    if test {
        let mut player = build_player(50, 0, 500);
        let mut boss = build_player(58, 9, 100);
        let mut spells: Vec<(Effect, i32, i32)> = Vec::new();
        spells.push((Effect::Poison, 6, 173));
        spells.push((Effect::Recharge, 5, 229));
        spells.push((Effect::Drain, 0, 73));
        spells.push((Effect::Poison, 6, 173));
        spells.push((Effect::Recharge, 5, 229));
        spells.push((Effect::Shield, 6, 113));
        spells.push((Effect::Poison, 6, 173));
        spells.push((Effect::MagicMissile, 0, 53));
        spells.push((Effect::MagicMissile, 0, 53));

        // spells.push((Effect::Recharge, 5, 229));
        // spells.push((Effect::Shield, 7, 113));
        // spells.push((Effect::Drain, 0, 73));
        // spells.push((Effect::Poison, 6, 173));
        // spells.push((Effect::MagicMissile, 0, 53));

        for spell in spells.iter() {
            play_turn(&mut player, &mut boss, *spell, false);
        }
        log::trace!("After game:\nPlayer: {:?}\nBoss: {:?}", player, boss);
    } else {
        let player = build_player(50, 0, 500);
        let boss = build_player(58, 9, 100);
        let mut spells: Vec<(Effect, i32, i32)> = Vec::new();
        spells.push((Effect::MagicMissile, 0, 53));
        spells.push((Effect::Drain, 0, 73));
        spells.push((Effect::Shield, 6, 113));
        spells.push((Effect::Poison, 6, 173));
        spells.push((Effect::Recharge, 5, 229));
        let mut spent_mana: Vec<i32> = Vec::new();
        game_result(player, boss, &spells, &mut spent_mana, false);
        let part1_min = spent_mana.iter().min().unwrap().clone();

        // Reset
        let player = build_player(50, 0, 500);
        let boss = build_player(58, 9, 100);
        spent_mana.clear();
        game_result(player, boss, &spells, &mut spent_mana, true);
        log::info!(
            "⚔️✨ min mana needed to win part 1: {}, part 2: {}",
            part1_min,
            spent_mana.iter().min().unwrap()
        );
    }
}
