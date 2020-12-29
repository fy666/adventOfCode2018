use std::fs;

fn count_unescaped(txt: &str) -> usize {
    let tmp = txt.replace("\\\\", "a").replace("\\\"", "b");
    let unicode = tmp.matches("\\x").count();
    log::trace!(
        "unesc {} -> {} len = {}",
        txt,
        tmp,
        tmp.len() - 2 - 3 * unicode
    );
    tmp.len() - 2 - 3 * unicode
}

fn count_new_encode(txt: &str) -> usize {
    let tmp = txt.replace("\"", "88").replace("\\", "99");
    log::trace!("new {} -> {} len = {}", txt, tmp, tmp.len() + 2);
    tmp.len() + 2
}

pub fn run(file: &String) {
    let text = fs::read_to_string(file).expect("File not found");
    let data: Vec<&str> = text.trim().split("\n").collect();
    log::debug!("Imported {} strings", data.len());

    let mut count_all = 0;
    let mut count_unesc = 0;
    let mut count_enc = 0;
    for l in data {
        count_all += l.len();
        let cu = count_unescaped(l);
        count_unesc += cu;
        let ce = count_new_encode(l);
        count_enc += ce;
        log::debug!(
            "Line {}, len {}, escaped len {}, new enc len {}",
            l,
            l.len(),
            cu,
            ce
        );
    }
    log::info!(
        "📜 size after escaped {} , size after new encoding {}",
        count_all - count_unesc,
        count_enc - count_all
    );
}
