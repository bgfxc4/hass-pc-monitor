use json;
use sysinfo::{SystemExt, CpuExt};

pub fn get_device_state(system: &sysinfo::System) -> json::JsonValue {
    let ret = json::object!{
        used_memory: system.used_memory(),
        used_swap: system.used_swap(),
        cpu: {
            cores: get_json_processor_list(system.cpus()),
            average: get_cpu_average(system.cpus())
        }
    };
    ret
}

fn get_cpu_average(cpu_list: &[sysinfo::Cpu]) -> f32 {
    let mut ret: f32 = 0.0;
    for cpu in cpu_list {
        ret += cpu.cpu_usage();
    }
    ret / cpu_list.len() as f32
}

fn get_json_processor_list(cpu_list: &[sysinfo::Cpu]) -> json::JsonValue {
    let mut ret = json::object!{};
    for cpu in cpu_list {
        ret[cpu.name()] = cpu.cpu_usage().into();
    }
    ret
}