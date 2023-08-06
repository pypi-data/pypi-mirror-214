use pyo3::prelude::*;

pub mod spotify;

/// This is a test function that returns the given string.
#[pyfunction]
fn echo(a: &str) -> PyResult<&str> {
    Ok(a)
}

#[pymodule]
fn cbvx(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(echo, m)?)?;

    // The iml module contains image manipulation class and functions
    let iml = PyModule::new(py.clone(), "iml")?;

    // The spotify class contains functions to generate spotify image
    iml.add_class::<spotify::Spotify>()?;

    m.add_submodule(iml)?;

    Ok(())
}
