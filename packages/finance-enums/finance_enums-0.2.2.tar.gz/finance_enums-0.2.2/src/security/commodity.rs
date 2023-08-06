#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{CommodityType as BaseCommodityType};

#[pyclass]
pub struct CommodityType {
    pub typ: BaseCommodityType
}

#[pymethods]
impl CommodityType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            CommodityType {
                typ: BaseCommodityType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("CommodityType<{}>", self.typ.to_string()))
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
        Ok(BaseCommodityType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<CommodityType> {
        BaseCommodityType::iter().map(|item: BaseCommodityType| CommodityType{typ: item} ).collect()
    }

    #[classattr]
    fn Energy() -> CommodityType {
        CommodityType {
            typ: BaseCommodityType::Energy
        }
    }
    #[classattr]
    fn Metals() -> CommodityType {
        CommodityType {
            typ: BaseCommodityType::Metals
        }
    }
    #[classattr]
    fn Agriculture() -> CommodityType {
        CommodityType {
            typ: BaseCommodityType::Agriculture
        }
    }
}
