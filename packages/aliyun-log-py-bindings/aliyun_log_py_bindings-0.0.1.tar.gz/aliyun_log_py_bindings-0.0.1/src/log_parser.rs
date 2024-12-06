use crate::error::AliyunLogError;
use crate::pb;
use lz4::block::decompress;
use prost::Message;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyString};
use pyo3::{pyfunction, Bound, IntoPyObject, PyObject, PyResult, Python};
use serde_json::{Map, Value};

#[pyfunction]
pub(crate) fn logs_to_flat_json_str(py: Python, bytes: &[u8]) -> PyResult<String> {
    py.allow_threads(|| {
        let log_group_list = pb::LogGroupListPb::decode(bytes).map_err(AliyunLogError::from)?;
        Ok(pb_to_flat_json_str(log_group_list))
    })
}

#[pyfunction]
pub(crate) fn lz4_logs_to_flat_json_str(
    py: Python,
    compressed: &[u8],
    raw_size: usize,
) -> PyResult<String> {
    py.allow_threads(|| {
        let bytes = decompress(compressed, Some(raw_size as i32)).unwrap();
        let log_group_list =
            pb::LogGroupListPb::decode(bytes.as_slice()).map_err(AliyunLogError::from)?;
        Ok(pb_to_flat_json_str(log_group_list))
    })
}

#[pyfunction]
pub(crate) fn lz4_logs_to_flat_json(
    py: Python,
    bytes: &[u8],
    raw_size: usize,
    time_as_str: bool,
    decode_utf8: bool,
) -> PyResult<PyObject> {
    let log_group_list = py
        .allow_threads(|| {
            let decompressed = decompress(bytes, Some(raw_size as i32)).unwrap();
            pb::LogGroupListRawPb::decode(decompressed.as_slice())
        })
        .map_err(AliyunLogError::from)?;
    log_group_list_to_flat_json_py(py, log_group_list, time_as_str, decode_utf8)
}

fn logs_to_flat_json_value(log_group_list: pb::LogGroupListPb) -> Value {
    let mut logs = vec![];
    for log_group in log_group_list.log_groups {
        let tag_kvs: Vec<(String, &str)> = log_group
            .log_tags
            .iter()
            .map(|log_tag| {
                (
                    format!("__tag__:{}", log_tag.key).to_string(),
                    log_tag.value.as_str(),
                )
            })
            .collect();
        let topic = log_group.topic;
        let source = log_group.source;
        for log in log_group.logs {
            let mut m = Map::new();
            for content in log.contents {
                m.insert(content.key, Value::from(content.value));
            }
            m.insert("__time__".to_string(), Value::from(log.time));
            if let Some(ref t) = topic {
                m.insert("__topic__".to_string(), Value::from(t.clone()));
            }
            if let Some(ref s) = source {
                m.insert("__source__".to_string(), Value::from(s.clone()));
            }
            if let Some(ns) = log.time_ns {
                m.insert("__time_ns__".to_string(), Value::from(ns));
            }
            for (k, v) in &tag_kvs {
                m.insert(k.to_string(), Value::from(*v));
            }
            logs.push(Value::Object(m));
        }
    }
    Value::Array(logs)
}
fn pb_to_flat_json_str(log_group_list: pb::LogGroupListPb) -> String {
    logs_to_flat_json_value(log_group_list).to_string()
}

fn log_group_list_to_flat_json_py(
    py: Python,
    log_group_list: pb::LogGroupListRawPb,
    time_as_str: bool,
    decode_utf8: bool,
) -> PyResult<PyObject> {
    let py_list = PyList::empty(py);
    for log_group in log_group_list.log_groups {
        let tag_kvs: Vec<(String, &String)> = log_group
            .log_tags
            .iter()
            .map(|log_tag| {
                (
                    format!("__tag__:{}", log_tag.key).to_string(),
                    &log_tag.value,
                )
            })
            .collect();
        let topic = log_group.topic;
        let source = log_group.source;
        let py_dict = PyDict::new(py);
        for log in log_group.logs {
            py_dict.set_item("__time__", get_time_py_object(py, log.time, time_as_str)?)?;
            if let Some(ns) = log.time_ns {
                py_dict.set_item("__time_ns__", get_time_py_object(py, ns, time_as_str)?)?;
            }
            for content in log.contents {
                set_py_dict(&py_dict, &content.key, &content.value, decode_utf8)?;
            }
            if let Some(ref t) = topic {
                py_dict.set_item("__topic__", t)?;
            }
            if let Some(ref s) = source {
                py_dict.set_item("__source__", s)?;
            }
            for (k, v) in &tag_kvs {
                py_dict.set_item(k.as_str(), v.as_str())?;
            }
        }
        py_list.append(py_dict)?;
    }
    Ok(py_list.into())
}

fn get_time_py_object(py: Python, value: u32, time_as_str: bool) -> PyResult<PyObject> {
    if time_as_str {
        Ok(PyString::new(py, &value.to_string()).into_any().into())
    } else {
        Ok(value.into_pyobject(py)?.into_any().into())
    }
}

fn set_py_dict(
    py_dict: &Bound<PyDict>,
    key: &str,
    value: &[u8],
    decode_utf8: bool,
) -> PyResult<()> {
    if decode_utf8 {
        py_dict.set_item(key, std::str::from_utf8(value)?)?;
    } else {
        py_dict.set_item(key, value)?;
    }
    Ok(())
}
