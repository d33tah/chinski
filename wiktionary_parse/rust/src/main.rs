extern crate xml;

#[macro_use]
extern crate serde_json;

use std::fs::File;
use std::io::BufReader;

use xml::reader::{EventReader, XmlEvent};

fn main() {
    let file = File::open("/dev/stdin").unwrap();
    let file = BufReader::new(file);

    let parser = EventReader::new(file);
    let mut current_title: String = "".into();
    let mut current_tag: String = "".into();
    for e in parser {
        match e {
            Ok(XmlEvent::Characters(name)) => {
                if current_tag == "title" {
                    current_title = name.clone();
                }
                if current_tag == "text" && current_title.chars().count() == 1 {
                    let val = json!([current_title, name]);
                    println!("{}", val.to_string());
                }
            }
            Ok(XmlEvent::StartElement{ name, .. }) => {
                current_tag = name.local_name;
            }
            _ => {}
        }
    }
}
