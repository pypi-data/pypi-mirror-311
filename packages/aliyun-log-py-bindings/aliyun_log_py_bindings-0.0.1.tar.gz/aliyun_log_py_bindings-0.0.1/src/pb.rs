#[allow(unused)]
use prost::Message;
#[allow(unused)]
use pyo3::prelude::*;
#[allow(unused)]
use std::string::ToString;

// Include the `logs` module, which is generated from logs.proto.
pub mod logs {
    include!(concat!(env!("OUT_DIR"), "/sls.logs.rs"));
}

#[allow(unused)]
pub use logs::log::Content as ContentPb;
#[allow(unused)]
pub use logs::Log as LogPb;
#[allow(unused)]
pub use logs::LogGroup as LogGroupPb;
pub use logs::LogGroupList as LogGroupListPb;
pub use logs::LogGroupListRaw as LogGroupListRawPb;
#[allow(unused)]
pub use logs::LogGroupRaw as LogGroupRawPb;

//
// #[pyclass]
// #[derive(Debug)]
// pub(crate) struct Log {
//     internal_pb: LogPb,
// }
//
// impl Log {
//     fn get_internal_protobuf(&self) -> LogPb {
//         self.internal_pb.clone()
//     }
// }
//
// impl From<LogPb> for Log {
//     fn from(log: LogPb) -> Self {
//         Log { internal_pb: log }
//     }
// }
//
// #[pymethods]
// impl Log {
//     #[new]
//     fn new() -> Self {
//         Log {
//             internal_pb: LogPb::default(),
//         }
//     }
//
//     fn get_time(&self) -> u32 {
//         self.internal_pb.time
//     }
//
//     fn set_time(&mut self, time: i64) {
//         self.internal_pb.time = time as u32;
//     }
//
//     fn get_time_ns(&self) -> Option<u32> {
//         self.internal_pb.time_ns
//     }
//
//     #[pyo3(signature = (time_ns=None))]
//     fn set_time_ns(&mut self, time_ns: Option<i64>) {
//         match time_ns {
//             None => self.internal_pb.time_ns = None,
//             Some(v) => self.internal_pb.time_ns = Some(v as u32),
//         }
//     }
//
//     fn add_log_content(&mut self, key: String, value: String) {
//         self.internal_pb.contents.push(ContentPb { key, value });
//     }
//
//     fn clear_log_contents(&mut self) {
//         self.internal_pb.contents.clear();
//     }
//
//     fn get_log_contents(&self) -> Vec<(String, String)> {
//         self.internal_pb
//             .contents
//             .iter()
//             .map(|x| (x.key.clone(), x.value.clone()))
//             .collect()
//     }
// }
//
// #[pyclass]
// #[derive(Debug)]
// pub(crate) struct LogGroup {
//     internal_pb: LogGroupPb,
// }
//
// impl From<LogGroupPb> for LogGroup {
//     fn from(pb: LogGroupPb) -> Self {
//         LogGroup { internal_pb: pb }
//     }
// }
//
// #[pymethods]
// impl LogGroup {
//     #[new]
//     fn new() -> Self {
//         LogGroup {
//             internal_pb: LogGroupPb::default(),
//         }
//     }
//
//     fn get_topic(&self) -> Option<String> {
//         self.internal_pb.topic.clone()
//     }
//
//     fn set_topic(&mut self, topic: &str) {
//         self.internal_pb.topic = Some(topic.to_owned());
//     }
//
//     fn get_source(&self) -> Option<String> {
//         self.internal_pb.source.clone()
//     }
//
//     fn set_source(&mut self, source: &str) {
//         self.internal_pb.source = Some(source.to_owned());
//     }
//
//     fn add_log_tag(&mut self, key: &str, value: &str) {
//         self.internal_pb.log_tags.push(logs::LogTag {
//             key: key.to_string(),
//             value: value.to_string(),
//         });
//     }
//
//     fn get_log_tags(&self) -> Vec<(String, String)> {
//         self.internal_pb
//             .log_tags
//             .iter()
//             .map(|x| (x.key.clone(), x.value.clone()))
//             .collect()
//     }
//
//     fn clear_log_tags(&mut self) {
//         self.internal_pb.log_tags.clear();
//     }
//
//     fn add_log(&mut self, log: &Log) {
//         self.internal_pb.logs.push(log.get_internal_protobuf());
//     }
//
//     fn get_logs(&self) -> Vec<Log> {
//         self.internal_pb
//             .logs
//             .iter()
//             .map(|x| Log::from(x.clone()))
//             .collect()
//     }
//
//     fn clear_logs(&mut self) {
//         self.internal_pb.logs.clear();
//     }
//
//     fn serialize_to_string(&self) -> PyResult<Vec<u8>> {
//         let mut buf = Vec::new();
//         self.internal_pb.encode(&mut buf).unwrap();
//         Ok(buf)
//     }
//
//     #[staticmethod]
//     pub(crate) fn from_bytes(py: Python<'_>, bytes: Py<PyBytes>) -> PyResult<Self> {
//         Ok(LogGroupPb::decode(bytes.as_bytes(py))
//             .map_err(AliyunLogError::from)?
//             .into())
//     }
// }
//
// #[cfg(test)]
// #[pyfunction]
// #[allow(dead_code)]
// #[pyo3(signature=(bytes, raw_size, log_group_list))]
// pub(crate) fn log_group_list_pb_lz4_to_py_lgl<'py>(
//     bytes: &[u8],
//     raw_size: usize,
//     log_group_list: &Bound<'py, PyAny>,
// ) -> PyResult<()> {
//     let log_group_list_rust = crate::measure_time!("parse", {
//         let decompressed = decompress(bytes, Some(raw_size as i32))?;
//         LogGroupListPb::decode(decompressed.as_slice()).map_err(AliyunLogError::from)?
//     });
//     crate::measure_time!("setattr", {
//         Python::with_gil(|_| -> PyResult<()> {
//             modify_py_obj_by_lgl(log_group_list_rust, log_group_list)
//         })
//     })
// }
//
// #[cfg(test)]
// #[allow(dead_code)]
// /// modify py object of type pb::LogGroupList by rust call python api
// fn modify_py_obj_by_lgl(
//     log_group_list_rust: LogGroupListPb,
//     log_group_list: &Bound<PyAny>,
// ) -> PyResult<()> {
//     for log_group_rust in log_group_list_rust.log_groups {
//         let log_group = log_group_list.getattr("LogGroups")?.call_method0("add")?;
//         if let Some(topic) = log_group_rust.topic {
//             log_group.setattr("Topic", topic)?;
//         }
//         if let Some(source) = log_group_rust.source {
//             log_group.setattr("Source", source)?;
//         }
//         for log_tag_rust in log_group_rust.log_tags {
//             let log_tag = log_group.getattr("LogTags")?.call_method0("add")?;
//             log_tag.setattr("Key", log_tag_rust.key)?;
//             log_tag.setattr("Value", log_tag_rust.value)?;
//         }
//         for log_rust in log_group_rust.logs {
//             let log = log_group.getattr("Logs")?.call_method0("add")?;
//             log.setattr("Time", log_rust.time)?;
//             if let Some(t) = log_rust.time_ns {
//                 log.setattr("Time_ns", t)?;
//             }
//             for content in log_rust.contents {
//                 let c = log.getattr("Contents")?.call_method0("add")?;
//                 c.setattr("Key", content.key)?;
//                 c.setattr("Value", content.value)?;
//             }
//         }
//     }
//     Ok(())
// }
