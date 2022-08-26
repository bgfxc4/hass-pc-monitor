use json;
use sysinfo::{SystemExt, ProcessorExt};

pub fn get_device_state(system: &sysinfo::System) -> json::JsonValue {
    let ret = json::object!{
        used_memory: system.get_used_memory(),
        used_swap: system.get_used_swap(),
        cpu: {
            cores: get_json_processor_list(system.get_processor_list()),
            average: get_cpu_average(system.get_processor_list())
        }
    };
    ret
}

fn get_cpu_average(cpu_list: &[sysinfo::Processor]) -> f32 {
    let mut ret: f32 = 0.0;
    for cpu in cpu_list {
        ret += cpu.get_cpu_usage();
    }
    ret / cpu_list.len() as f32
}

fn get_json_processor_list(cpu_list: &[sysinfo::Processor]) -> json::JsonValue {
    let mut ret = json::object!{};
    for cpu in cpu_list {
        ret[cpu.get_name()] = cpu.get_cpu_usage().into();
    }
    ret
}