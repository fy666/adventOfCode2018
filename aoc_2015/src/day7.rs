use std::collections::HashMap;
use std::fs;

fn get_wire_value<'a>(
    w: &str,
    wires_instr: &'a HashMap<String, String>,
    cache: &'a mut HashMap<String, u16>,
) -> u16 {
    if let Ok(i) = wires_instr.get(w).unwrap().parse::<u16>() {
        return i;
    }
    let instr = wires_instr.get(w).unwrap();
    if let Some(i) = cache.get(instr) {
        return *i;
    }

    let result;
    if instr.starts_with("NOT") {
        let val = &instr[4..]
            .parse::<u16>()
            .unwrap_or_else(|_| get_wire_value(&instr[4..], &wires_instr, cache));
        result = !val;
    } else {
        let tmp = instr.split(" ").collect::<Vec<_>>();
        if tmp.len() < 3 {
            result = get_wire_value(instr, &wires_instr, cache);
        } else {
            let val1 = tmp[0]
                .parse::<u16>()
                .unwrap_or_else(|_| get_wire_value(tmp[0], &wires_instr, cache));
            let val2 = tmp[2]
                .parse::<u16>()
                .unwrap_or_else(|_| get_wire_value(tmp[2], &wires_instr, cache));
            result = match tmp[1] {
                "AND" => val1 & val2,
                "OR" => val1 | val2,
                "LSHIFT" => val1 << val2,
                "RSHIFT" => val1 >> val2,
                _ => panic!("No valid instr found {}", instr),
            }
        }
    }

    cache.insert(instr.to_string(), result);
    return result;
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} wires instructions", data.len());

    let mut wires: HashMap<String, String> = HashMap::new();
    let mut cache: HashMap<String, u16> = HashMap::new();
    for d in data {
        let tmp: Vec<&str> = d.split(" -> ").collect();
        if tmp.len() == 2 {
            wires.insert(String::from(tmp[1]), String::from(tmp[0]));
        } else {
            log::warn!("Invalid instruction on line {}", d);
        }
    }

    log::info!("Wiring instructions : {:?}", wires);
    let result = get_wire_value("a", &wires, &mut cache);
    log::info!("value of a is {}", result);
    wires.insert("b".to_string(), format!("{}", result).to_string());
    cache.clear();
    let result = get_wire_value("a", &wires, &mut cache);
    log::info!("After updating b, value of a is {}", result);
}
