use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
};
use sysinfo::SystemExt;
use json;

pub mod device_info;
pub mod device_state;

fn main() {
    let listener = TcpListener::bind("0.0.0.0:5573").unwrap();
    let mut system = sysinfo::System::new();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream, &mut system);
    }
}

fn handle_connection(mut stream: TcpStream, system: &mut sysinfo::System) {
    let buf_reader = BufReader::new(&mut stream);
    let msg: String = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let msg_json = json::parse(msg.as_str()).unwrap();

    let res: json::JsonValue = match &msg_json["token"].as_str() {
            Some("state") => handle_state(&msg_json, system),
            Some(_) => handle_wrong_token(),
            None => handle_wrong_token()
    };
    stream.write_all(res.dump().as_bytes()).unwrap();
}

fn handle_state(msg: &json::JsonValue, system: &mut sysinfo::System) -> json::JsonValue {
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
        state: device_state::get_device_state(system)
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
    pass == Some("TestPassword")
}