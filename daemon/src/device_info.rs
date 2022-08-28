use json;
use sysinfo::{SystemExt, CpuExt};

pub fn get_device_info(system: &sysinfo::System) -> json::JsonValue {
    let ret = json::object!{
        total_memory: system.total_memory(),
        total_swap: system.total_swap(),
        cpu_names: get_processor_name_list(system.cpus()),
        system_name: system.name(),
        kernel_version: system.kernel_version(),
        os_version: system.os_version(),
        host_name: system.host_name()
    };
    ret
}

fn get_processor_name_list(cpu_list: &[sysinfo::Cpu]) -> Vec<&str> {
    cpu_list.iter().map(|x| x.name()).collect()
}