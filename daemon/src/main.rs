use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
};
use sysinfo::SystemExt;
use json;
use sha2::{Sha512, Digest};
use std::fs::File;
use std::io::Read;

pub mod device_info;
pub mod device_state;
pub mod device_settings;

fn main() {
    let mut config = json::object!{};
    read_config(&mut config);

    let listener = TcpListener::bind(format!("0.0.0.0:{}", config["port"])).unwrap();
    let mut system = sysinfo::System::new_all();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream, &mut system, &config);
    }
}

fn read_config(out: &mut json::JsonValue) {
    let mut file = File::open("config.json").unwrap();
    let mut out_string = String::new();
    file.read_to_string(&mut out_string).unwrap();
    *out = json::parse(out_string.as_str()).unwrap();
}

fn handle_connection(mut stream: TcpStream, system: &mut sysinfo::System, config: &json::JsonValue) {
    let buf_reader = BufReader::new(&mut stream);
    let msg: String = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let msg_json = json::parse(msg.as_str()).unwrap();

    let res: json::JsonValue = match &msg_json["token"].as_str() {
            Some("state") => handle_state(&msg_json, system, config),
            Some(_) => handle_wrong_token(),
            None => handle_wrong_token()
    };
    stream.write_all(res.dump().as_bytes()).unwrap();
}

fn handle_state(msg: &json::JsonValue, system: &mut sysinfo::System, config: &json::JsonValue) -> json::JsonValue {
    let mut res = json::object!{};
    let is_auth = test_auth(msg["password"].as_str());
    if !is_auth {
        res["status"] = 401.into();
        res["msg"] = "ERROR Wrong password".into();
        return res;
    }
    res["status"] = 200.into();
    system.refresh_all();
    res["data"] = json::object!{
        info: device_info::get_device_info(system),
        state: device_state::get_device_state(system),
        settings: device_settings::get_device_settings(config)
    };
    res
}

fn handle_wrong_token() -> json::JsonValue {
    json::object!{
        status: 400,
        msg: "ERROR Wrong token"
    }
}

fn test_auth(pass: Option<&str>) -> bool {
    let hash = match pass {
        Some(p) => get_sha512(p),
        None => String::from("")
    };
    hash == get_sha512(get_sha512("TestPassword").as_str())
}

fn get_sha512(input: &str) -> String {
    let mut hasher = Sha512::new();
    hasher.update(input);
    let result = hasher.finalize();
    format!("{:x}", result)
}