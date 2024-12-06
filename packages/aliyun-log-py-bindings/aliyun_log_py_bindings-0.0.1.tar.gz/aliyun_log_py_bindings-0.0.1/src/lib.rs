mod error;
mod json;
mod log_parser;
mod macros;
mod pb;

use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
mod aliyun_log_py_bindings {
    use super::*;

    #[pymodule]
    mod json {
        use crate::add_py_func;
        use crate::json::loads;
        use pyo3::prelude::{PyModule, PyModuleMethods};
        use pyo3::{wrap_pyfunction, Bound, PyResult};

        #[pymodule_init]
        fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
            add_py_func!(m, loads);
            Ok(())
        }
    }

    #[pymodule]
    mod log_parser {
        use crate::add_py_func;
        use crate::log_parser::{
            logs_to_flat_json_str, lz4_logs_to_flat_json, lz4_logs_to_flat_json_str,
        };
        use pyo3::prelude::{PyModule, PyModuleMethods};
        use pyo3::{wrap_pyfunction, Bound, PyResult};

        #[pymodule_init]
        fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
            add_py_func!(m, logs_to_flat_json_str);
            add_py_func!(m, lz4_logs_to_flat_json_str);
            add_py_func!(m, lz4_logs_to_flat_json);
            Ok(())
        }
    }

    // #[pymodule]
    // mod pb {
    //     use super::*;
    //     use crate::pb::*;
    //     #[pymodule_init]
    //     fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    //         m.add_class::<Log>()?;
    //         m.add_class::<LogGroup>()?;
    //         Ok(())
    //     }
    // }

    #[pymodule_init]
    fn init(_m: &Bound<'_, PyModule>) -> PyResult<()> {
        Ok(())
    }
}
