use json;
use sysinfo::{SystemExt, ProcessorExt};

pub fn get_device_info(system: &sysinfo::System) -> json::JsonValue {
    let ret = json::object!{
        total_memory: system.get_total_memory(),
        total_swap: system.get_total_swap(),
        cpu_names: get_processor_name_list(system.get_processor_list())
    };
    ret
}

fn get_processor_name_list(cpu_list: &[sysinfo::Processor]) -> Vec<&str> {
    cpu_list.iter().map(|x| x.get_name()).collect()
}