#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{FundType as BaseFundType, FundSubType as BaseFundSubType, MutualFundEndedness as BaseMutualFundEndedness};


#[pyclass]
pub struct FundType {
    pub typ: BaseFundType
}

#[pymethods]
impl FundType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            FundType {
                typ: BaseFundType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("FundType<{}>", self.typ.to_string()))
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
        Ok(BaseFundType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<FundType> {
        BaseFundType::iter().map(|item: BaseFundType| FundType{typ: item} ).collect()
    }

    #[classattr]
    fn ETF() -> FundType {
        FundType {
            typ: BaseFundType::ETF
        }
    }
    #[classattr]
    fn MutualFund() -> FundType {
        FundType {
            typ: BaseFundType::MutualFund
        }
    }
    #[classattr]
    fn REIT() -> FundType {
        FundType {
            typ: BaseFundType::REIT
        }
    }

}
#[pyclass]
pub struct FundSubType {
    pub typ: BaseFundSubType
}

#[pymethods]
impl FundSubType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            FundSubType {
                typ: BaseFundSubType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("FundSubType<{}>", self.typ.to_string()))
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
        Ok(BaseFundSubType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<FundSubType> {
        BaseFundSubType::iter().map(|item: BaseFundSubType| FundSubType{typ: item} ).collect()
    }

    #[classattr]
    fn Index() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Index
        }
    }
    #[classattr]
    fn Sector() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Sector
        }
    }
    #[classattr]
    fn Active() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Active
        }
    }
    #[classattr]
    fn Passive() -> FundSubType {
        FundSubType {
            typ: BaseFundSubType::Passive
        }
    }
}

#[pyclass]
pub struct MutualFundEndedness {
    pub typ: BaseMutualFundEndedness
}

#[pymethods]
impl MutualFundEndedness {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            MutualFundEndedness {
                typ: BaseMutualFundEndedness::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("MutualFundEndedness<{}>", self.typ.to_string()))
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
        Ok(BaseMutualFundEndedness::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<MutualFundEndedness> {
        BaseMutualFundEndedness::iter().map(|item: BaseMutualFundEndedness| MutualFundEndedness{typ: item} ).collect()
    }

    #[classattr]
    fn Open() -> MutualFundEndedness {
        MutualFundEndedness {
            typ: BaseMutualFundEndedness::Open
        }
    }
    #[classattr]
    fn Close() -> MutualFundEndedness {
        MutualFundEndedness {
            typ: BaseMutualFundEndedness::Close
        }
    }
}