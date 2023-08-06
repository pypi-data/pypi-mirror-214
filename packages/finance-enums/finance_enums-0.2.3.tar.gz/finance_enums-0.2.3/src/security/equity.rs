#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{EquityType as BaseEquityType};


#[pyclass]
pub struct EquityType {
    pub typ: BaseEquityType
}

#[pymethods]
impl EquityType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            EquityType {
                typ: BaseEquityType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("EquityType<{}>", self.typ.to_string()))
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
        Ok(BaseEquityType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<EquityType> {
        BaseEquityType::iter().map(|item: BaseEquityType| EquityType{typ: item} ).collect()
    }

    #[classattr]
    fn Shares() -> EquityType {
        EquityType {
            typ: BaseEquityType::Shares
        }
    }
    #[classattr]
    fn PreferredShares() -> EquityType {
        EquityType {
            typ: BaseEquityType::PreferredShares
        }
    }
    #[classattr]
    fn ConvertibleShares() -> EquityType {
        EquityType {
            typ: BaseEquityType::ConvertibleShares
        }
    }
    #[classattr]
    fn PreferredConvertibleShares() -> EquityType {
        EquityType {
            typ: BaseEquityType::PreferredConvertibleShares
        }
    }
    #[classattr]
    fn DepositoryReceipt() -> EquityType {
        EquityType {
            typ: BaseEquityType::DepositoryReceipt
        }
    }
}
