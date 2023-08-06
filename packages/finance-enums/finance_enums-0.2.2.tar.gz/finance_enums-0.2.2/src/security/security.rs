#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{SecurityType as BaseSecurityType};

#[pyclass]
pub struct SecurityType {
    pub typ: BaseSecurityType
}

#[pymethods]
impl SecurityType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            SecurityType {
                typ: BaseSecurityType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("SecurityType<{}>", self.typ.to_string()))
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
        Ok(BaseSecurityType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<SecurityType> {
        BaseSecurityType::iter().map(|item: BaseSecurityType| SecurityType{typ: item} ).collect()
    }


    #[classattr]
    fn Equity() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Equity
        }
    }
    #[classattr]
    fn Option() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Option
        }
    }
    #[classattr]
    fn Bond() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Bond
        }
    }
    #[classattr]
    fn Forward() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Forward
        }
    }
    #[classattr]
    fn Future() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Future
        }
    }
    #[classattr]
    fn PerpetualFuture() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::PerpetualFuture
        }
    }
    #[classattr]
    fn Spread() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Spread
        }
    }
    #[classattr]
    fn Fund() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Fund
        }
    }
    #[classattr]
    fn Commodity() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Commodity
        }
    }
    #[classattr]
    fn Currency() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Currency
        }
    }
    #[classattr]
    fn Pair() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Pair
        }
    }
    #[classattr]
    fn Index() -> SecurityType {
        SecurityType {
            typ: BaseSecurityType::Index
        }
    }
}
