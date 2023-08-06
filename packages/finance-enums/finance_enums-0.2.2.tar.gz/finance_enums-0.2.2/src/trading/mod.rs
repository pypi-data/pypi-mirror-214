#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{OrderType as BaseOrderType, Side as BaseSide, TimeInForce as BaseTimeInForce, OrderFlag as BaseOrderFlag};


#[pyclass]
pub struct OrderType {
    pub typ: BaseOrderType
}

#[pymethods]
impl OrderType {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OrderType {
                typ: BaseOrderType::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OrderType<{}>", self.typ.to_string()))
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
        Ok(BaseOrderType::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OrderType> {
        BaseOrderType::iter().map(|item: BaseOrderType| OrderType{typ: item} ).collect()
    }

    #[classattr]
    fn Market() -> OrderType {
        OrderType {
            typ: BaseOrderType::Market
        }
    }
    #[classattr]
    fn Limit() -> OrderType {
        OrderType {
            typ: BaseOrderType::Limit
        }
    }
    #[classattr]
    fn Stop() -> OrderType {
        OrderType {
            typ: BaseOrderType::Stop
        }
    }
}


#[pyclass]
pub struct Side {
    pub typ: BaseSide
}

#[pymethods]
impl Side {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Side {
                typ: BaseSide::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Side<{}>", self.typ.to_string()))
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
        Ok(BaseSide::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Side> {
        BaseSide::iter().map(|item: BaseSide| Side{typ: item} ).collect()
    }

    #[classattr]
    fn Buy() -> Side {
        Side {
            typ: BaseSide::Buy
        }
    }
    #[classattr]
    fn Sell() -> Side {
        Side {
            typ: BaseSide::Sell
        }
    }
}


#[pyclass]
pub struct TimeInForce {
    pub typ: BaseTimeInForce
}

#[pymethods]
impl TimeInForce {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            TimeInForce {
                typ: BaseTimeInForce::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("TimeInForce<{}>", self.typ.to_string()))
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
        Ok(BaseTimeInForce::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<TimeInForce> {
        BaseTimeInForce::iter().map(|item: BaseTimeInForce| TimeInForce{typ: item} ).collect()
    }

    #[classattr]
    fn Day() -> TimeInForce {
        TimeInForce {
            typ: BaseTimeInForce::Day
        }
    }
    #[classattr]
    fn GTC() -> TimeInForce {
        TimeInForce {
            typ: BaseTimeInForce::GTC
        }
    }
}



#[pyclass]
pub struct OrderFlag {
    pub typ: BaseOrderFlag
}

#[pymethods]
impl OrderFlag {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            OrderFlag {
                typ: BaseOrderFlag::from_str(value.as_str()).unwrap()
            }
        )
    }
    
    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }
    
    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("OrderFlag<{}>", self.typ.to_string()))
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
        Ok(BaseOrderFlag::iter().count())
    }
    
    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<OrderFlag> {
        BaseOrderFlag::iter().map(|item: BaseOrderFlag| OrderFlag{typ: item} ).collect()
    }


    #[classattr]
    fn None() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::None
        }
    }
    #[classattr]
    fn FillOrKill() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::FillOrKill
        }
    }
    #[classattr]
    fn ImmediateOrCancel() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::ImmediateOrCancel
        }
    }
    #[classattr]
    fn AllOrNone() -> OrderFlag {
        OrderFlag {
            typ: BaseOrderFlag::AllOrNone
        }
    }
}
