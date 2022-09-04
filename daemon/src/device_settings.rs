use json;

pub fn get_device_settings(conf: &json::JsonValue) -> json::JsonValue {
    let ret = json::object!{
        update_interval: conf["update_interval"].as_u16(),
        commands: conf["commands"].clone()
    };
    ret
}