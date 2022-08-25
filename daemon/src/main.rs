use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
};
use json;

fn main() {
    let listener = TcpListener::bind("0.0.0.0:5573").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let msg: String = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {:#?}", msg);
    let msg_json = json::parse(msg.as_str()).unwrap();
    
    let res: json::JsonValue = match &msg_json["token"].as_str() {
            Some("auth") => handle_auth(&msg_json),
            Some("state") => handle_state(&msg_json),
            Some(_) => handle_wrong_token(),
            None => handle_wrong_token()
    };
    println!("Answer: {:#?}", res.dump());
    stream.write_all(res.dump().as_bytes()).unwrap();
}

fn handle_auth(msg: &json::JsonValue) -> json::JsonValue {
    let mut res = json::object!{
        status: 200,
        msg: "OK"
    };
    let is_auth = test_auth(msg["password"].as_str());
    if !is_auth {
        res["status"] = 401.into();
        res["msg"] = "ERROR Wrong password".into();
        return res;
    }
    res
}

fn handle_state(msg: &json::JsonValue) -> json::JsonValue {
    let mut res = json::object!{};
    let is_auth = test_auth(msg["password"].as_str());
    if !is_auth {
        res["status"] = 401.into();
        res["msg"] = "ERROR Wrong password".into();
        return res;
    }
    res["status"] = 200.into();
    res["msg"] = json::object!{};
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