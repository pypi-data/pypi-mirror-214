#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{BondType as BaseBondType};

#[pyclass]
pub struct BondType {
    pub typ: BaseBondType
}

#[pymethods]
impl BondType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            BondType {
                typ: BaseBondType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("BondType<{}>", self.typ.to_string()))
    }
    
    fn __richcmp__(&self, other: &Self, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Lt => Ok(self.typ.to_string() < other.typ.to_string()),
            CompareOp::Le => Ok(self.typ.to_string() <= other.typ.to_string()),
            CompareOp::Eq => Ok(self.typ == other.typ),
            CompareOp::Ne => Ok(self.typ != other.typ),
            CompareOp::Gt => Ok(self.typ.to_string() > other.typ.to_string()),
            CompareOp::Ge => Ok(self.typ.to_string() >= other.typ.to_string()),
        }
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseBondType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<BondType> {
        BaseBondType::iter().map(|item: BaseBondType| BondType{typ: item} ).collect()
    }

    #[classattr]
    fn Corporate() -> BondType {
        BondType {
            typ: BaseBondType::Corporate
        }
    }
    #[classattr]
    fn Government() -> BondType {
        BondType {
            typ: BaseBondType::Government
        }
    }
    #[classattr]
    fn Municipal() -> BondType {
        BondType {
            typ: BaseBondType::Municipal
        }
    }
}
