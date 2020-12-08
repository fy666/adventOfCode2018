
fn test() -> String{
    let ij = "Hello";
    println!("In F, {}", ij);
    ij.to_owned()
}

struct User {
    name: String,
    age: i32
}

fn build_user(name: String) -> User{
    User{
        name,
        age:4
    }
}

fn main() {
    println!("Hello, world!");
    let s = String::from("Coucou");
    // for i in s.as_bytes().iter(){
    //     println!("{}", i);
    // }
    let ii = &s[..3];
    println!("substr = {}", ii);
    let ij = test();
    println!("Outside F , {}", ij);
    let a = build_user("John".to_string());
    println!("New user: {} age {}", a.name, a.age)

                                              
}
