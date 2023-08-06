#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{OptionType as BaseOptionType, OptionExerciseType as BaseOptionExerciseType};


#[pyclass]
pub struct OptionType {
    pub typ: BaseOptionType
}

#[pymethods]
impl OptionType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OptionType {
                typ: BaseOptionType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OptionType<{}>", self.typ.to_string()))
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
        Ok(BaseOptionType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OptionType> {
        BaseOptionType::iter().map(|item: BaseOptionType| OptionType{typ: item} ).collect()
    }

    #[classattr]
    fn Call() -> OptionType {
        OptionType {
            typ: BaseOptionType::Call
        }
    }
    #[classattr]
    fn Put() -> OptionType {
        OptionType {
            typ: BaseOptionType::Put
        }
    }
}

#[pyclass]
pub struct OptionExerciseType {
    pub typ: BaseOptionExerciseType
}

#[pymethods]
impl OptionExerciseType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OptionExerciseType {
                typ: BaseOptionExerciseType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OptionExerciseType<{}>", self.typ.to_string()))
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
        Ok(BaseOptionExerciseType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OptionExerciseType> {
        BaseOptionExerciseType::iter().map(|item: BaseOptionExerciseType| OptionExerciseType{typ: item} ).collect()
    }

    #[classattr]
    fn American() -> OptionExerciseType {
        OptionExerciseType {
            typ: BaseOptionExerciseType::American
        }
    }
    #[classattr]
    fn European() -> OptionExerciseType {
        OptionExerciseType {
            typ: BaseOptionExerciseType::European
        }
    }
    #[classattr]
    fn Bermudan() -> OptionExerciseType {
        OptionExerciseType {
            typ: BaseOptionExerciseType::Bermudan
        }
    }
}
