use serde_json::Value;
use std::fs;

fn get_sum(input: &Value, filter: bool) -> i64 {
    log::trace!("input = {:?}", input);
    match input {
        Value::Number(i) => i.as_i64().unwrap(),
        Value::Array(i) => i.iter().map(|x| get_sum(x, filter)).sum(),
        Value::Object(i) => {
            let mut res = 0;
            if !filter || !i.values().any(|x| *x == Value::String("red".to_string())) {
                res = i.values().map(|x| get_sum(x, filter)).sum();
            }
            res
        }
        _ => 0,
    }
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: serde_json::Value = serde_json::from_str(&text).unwrap();
    log::trace!("json : {:?}", data);
    log::info!("➕  {}", get_sum(&data, false));
    log::info!("✖️    {}", get_sum(&data, true));
}
