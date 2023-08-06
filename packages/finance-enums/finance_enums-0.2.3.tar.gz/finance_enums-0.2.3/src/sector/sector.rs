#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{Sector as BaseSector};
use super::IndustryGroup;

#[pyclass]
pub struct Sector {
    pub typ: BaseSector,
}

#[pymethods]
impl Sector {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Sector {
                typ: BaseSector::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Sector<{}>", self.typ.to_string()))
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

    fn industry_groups(&self) -> Vec<IndustryGroup> {
        self.typ.industry_groups().iter().map(|item| IndustryGroup{typ: item.clone()} ).collect()
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseSector::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Sector> {
        BaseSector::iter().map(|item: BaseSector| Sector{typ: item} ).collect()
    }

    // Enum values
    #[classattr]
    fn Energy() -> Sector {
        Sector {
            typ: BaseSector::Energy
        }
    }

    #[classattr]
    fn Materials() -> Sector {
        Sector {
            typ: BaseSector::Materials
        }
    }

    #[classattr]
    fn Industrials() -> Sector {
        Sector {
            typ: BaseSector::Industrials
        }
    }

    #[classattr]
    fn ConsumerDiscretionary() -> Sector {
        Sector {
            typ: BaseSector::ConsumerDiscretionary
        }
    }

    #[classattr]
    fn ConsumerStaples() -> Sector {
        Sector {
            typ: BaseSector::ConsumerStaples
        }
    }

    #[classattr]
    fn HealthCare() -> Sector {
        Sector {
            typ: BaseSector::HealthCare
        }
    }

    #[classattr]
    fn Financials() -> Sector {
        Sector {
            typ: BaseSector::Financials
        }
    }

    #[classattr]
    fn InformationTechnology() -> Sector {
        Sector {
            typ: BaseSector::InformationTechnology
        }
    }

    #[classattr]
    fn CommunicationServices() -> Sector {
        Sector {
            typ: BaseSector::CommunicationServices
        }
    }

    #[classattr]
    fn Utilities() -> Sector {
        Sector {
            typ: BaseSector::Utilities
        }
    }

    #[classattr]
    fn RealEstate() -> Sector {
        Sector {
            typ: BaseSector::RealEstate
        }
    }
}
