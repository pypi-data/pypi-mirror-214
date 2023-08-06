#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::MIC;
use super::Country;

#[pyclass]
pub struct Exchange{
    pub mic: MIC,
}

#[pymethods]
impl Exchange {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Exchange {
                mic: MIC::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.mic.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Exchange<{}>", self.mic.to_string()))
    }

    fn __richcmp__(&self, other: &Self, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Lt => Ok(self.mic.to_string() < other.mic.to_string()),
            CompareOp::Le => Ok(self.mic.to_string() <= other.mic.to_string()),
            CompareOp::Eq => Ok(self.mic == other.mic),
            CompareOp::Ne => Ok(self.mic != other.mic),
            CompareOp::Gt => Ok(self.mic.to_string() > other.mic.to_string()),
            CompareOp::Ge => Ok(self.mic.to_string() >= other.mic.to_string()),
        }
    }    

    fn country(&self) -> Country {
        Country {
            code: self.mic.country(),
            code3: self.mic.country().codethree(),
            name: self.mic.country().str(),
        }
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(MIC::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Exchange> {
        MIC::iter().map(|item: MIC| Exchange{mic: item} ).collect()
    }

    #[classattr]
    fn XNYS() -> Exchange {
        Exchange {
            mic: MIC::XNYS
        }
    }
    #[classattr]
    fn ARCX() -> Exchange {
        Exchange {
            mic: MIC::ARCX
        }
    }
    #[classattr]
    fn XASE() -> Exchange {
        Exchange {
            mic: MIC::XASE
        }
    }
    #[classattr]
    fn XCIS() -> Exchange {
        Exchange {
            mic: MIC::XCIS
        }
    }
    #[classattr]
    fn XCHI() -> Exchange {
        Exchange {
            mic: MIC::XCHI
        }
    }
    #[classattr]
    fn XNAS() -> Exchange {
        Exchange {
            mic: MIC::XNAS
        }
    }
    #[classattr]
    fn XNGS() -> Exchange {
        Exchange {
            mic: MIC::XNGS
        }
    }
    #[classattr]
    fn XBOS() -> Exchange {
        Exchange {
            mic: MIC::XBOS
        }
    }
    #[classattr]
    fn XPHL() -> Exchange {
        Exchange {
            mic: MIC::XPHL
        }
    }
    #[classattr]
    fn XCBO() -> Exchange {
        Exchange {
            mic: MIC::XCBO
        }
    }
    #[classattr]
    fn BATS() -> Exchange {
        Exchange {
            mic: MIC::BATS
        }
    }
    #[classattr]
    fn BATY() -> Exchange {
        Exchange {
            mic: MIC::BATY
        }
    }
    #[classattr]
    fn EDGX() -> Exchange {
        Exchange {
            mic: MIC::EDGX
        }
    }
    #[classattr]
    fn EDGA() -> Exchange {
        Exchange {
            mic: MIC::EDGA
        }
    }
    #[classattr]
    fn MPRL() -> Exchange {
        Exchange {
            mic: MIC::MPRL
        }
    }
    #[classattr]
    fn MIHI() -> Exchange {
        Exchange {
            mic: MIC::MIHI
        }
    }
    #[classattr]
    fn MEMX() -> Exchange {
        Exchange {
            mic: MIC::MEMX
        }
    }
    #[classattr]
    fn IEXG() -> Exchange {
        Exchange {
            mic: MIC::IEXG
        }
    }
    #[classattr]
    fn LTSE() -> Exchange {
        Exchange {
            mic: MIC::LTSE
        }
    }
    #[classattr]
    fn XADF() -> Exchange {
        Exchange {
            mic: MIC::XADF
        }
    }
    #[classattr]
    fn FINR() -> Exchange {
        Exchange {
            mic: MIC::FINR
        }
    }
}
