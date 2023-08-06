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
    fn NYSD() -> Exchange {
        Exchange {
            mic: MIC::NYSD
        }
    }
    #[classattr]
    fn XCIS() -> Exchange {
        Exchange {
            mic: MIC::XCIS
        }
    }
    #[classattr]
    fn CISD() -> Exchange {
        Exchange {
            mic: MIC::CISD
        }
    }
    #[classattr]
    fn XCHI() -> Exchange {
        Exchange {
            mic: MIC::XCHI
        }
    }
    #[classattr]
    fn ARCX() -> Exchange {
        Exchange {
            mic: MIC::ARCX
        }
    }
    #[classattr]
    fn ARCD() -> Exchange {
        Exchange {
            mic: MIC::ARCD
        }
    }
    #[classattr]
    fn ARCO() -> Exchange {
        Exchange {
            mic: MIC::ARCO
        }
    }
    #[classattr]
    fn XASE() -> Exchange {
        Exchange {
            mic: MIC::XASE
        }
    }
    #[classattr]
    fn AMXO() -> Exchange {
        Exchange {
            mic: MIC::AMXO
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
    fn XNCM() -> Exchange {
        Exchange {
            mic: MIC::XNCM
        }
    }
    #[classattr]
    fn XNMS() -> Exchange {
        Exchange {
            mic: MIC::XNMS
        }
    }
    #[classattr]
    fn NASD() -> Exchange {
        Exchange {
            mic: MIC::NASD
        }
    }
    #[classattr]
    fn XNDQ() -> Exchange {
        Exchange {
            mic: MIC::XNDQ
        }
    }
    #[classattr]
    fn XBOS() -> Exchange {
        Exchange {
            mic: MIC::XBOS
        }
    }
    #[classattr]
    fn BOSD() -> Exchange {
        Exchange {
            mic: MIC::BOSD
        }
    }
    #[classattr]
    fn XBXO() -> Exchange {
        Exchange {
            mic: MIC::XBXO
        }
    }
    #[classattr]
    fn XPHL() -> Exchange {
        Exchange {
            mic: MIC::XPHL
        }
    }
    #[classattr]
    fn XPSX() -> Exchange {
        Exchange {
            mic: MIC::XPSX
        }
    }
    #[classattr]
    fn PSXD() -> Exchange {
        Exchange {
            mic: MIC::PSXD
        }
    }
    #[classattr]
    fn XPHO() -> Exchange {
        Exchange {
            mic: MIC::XPHO
        }
    }
    #[classattr]
    fn XPBT() -> Exchange {
        Exchange {
            mic: MIC::XPBT
        }
    }
    #[classattr]
    fn XPOR() -> Exchange {
        Exchange {
            mic: MIC::XPOR
        }
    }
    #[classattr]
    fn XNFI() -> Exchange {
        Exchange {
            mic: MIC::XNFI
        }
    }
    #[classattr]
    fn XISE() -> Exchange {
        Exchange {
            mic: MIC::XISE
        }
    }
    #[classattr]
    fn GMNI() -> Exchange {
        Exchange {
            mic: MIC::GMNI
        }
    }
    #[classattr]
    fn MCRY() -> Exchange {
        Exchange {
            mic: MIC::MCRY
        }
    }
    #[classattr]
    fn XCBO() -> Exchange {
        Exchange {
            mic: MIC::XCBO
        }
    }
    #[classattr]
    fn EDGA() -> Exchange {
        Exchange {
            mic: MIC::EDGA
        }
    }
    #[classattr]
    fn EDGD() -> Exchange {
        Exchange {
            mic: MIC::EDGD
        }
    }
    #[classattr]
    fn EDGX() -> Exchange {
        Exchange {
            mic: MIC::EDGX
        }
    }
    #[classattr]
    fn EDDP() -> Exchange {
        Exchange {
            mic: MIC::EDDP
        }
    }
    #[classattr]
    fn EDGO() -> Exchange {
        Exchange {
            mic: MIC::EDGO
        }
    }
    #[classattr]
    fn BATS() -> Exchange {
        Exchange {
            mic: MIC::BATS
        }
    }
    #[classattr]
    fn BZXD() -> Exchange {
        Exchange {
            mic: MIC::BZXD
        }
    }
    #[classattr]
    fn BATO() -> Exchange {
        Exchange {
            mic: MIC::BATO
        }
    }
    #[classattr]
    fn BATY() -> Exchange {
        Exchange {
            mic: MIC::BATY
        }
    }
    #[classattr]
    fn BYXD() -> Exchange {
        Exchange {
            mic: MIC::BYXD
        }
    }
    #[classattr]
    fn C2OX() -> Exchange {
        Exchange {
            mic: MIC::C2OX
        }
    }
    #[classattr]
    fn XCME() -> Exchange {
        Exchange {
            mic: MIC::XCME
        }
    }
    #[classattr]
    fn FCME() -> Exchange {
        Exchange {
            mic: MIC::FCME
        }
    }
    #[classattr]
    fn GLBX() -> Exchange {
        Exchange {
            mic: MIC::GLBX
        }
    }
    #[classattr]
    fn XCBT() -> Exchange {
        Exchange {
            mic: MIC::XCBT
        }
    }
    #[classattr]
    fn FCBT() -> Exchange {
        Exchange {
            mic: MIC::FCBT
        }
    }
    #[classattr]
    fn XKBT() -> Exchange {
        Exchange {
            mic: MIC::XKBT
        }
    }
    #[classattr]
    fn XNYM() -> Exchange {
        Exchange {
            mic: MIC::XNYM
        }
    }
    #[classattr]
    fn MIHI() -> Exchange {
        Exchange {
            mic: MIC::MIHI
        }
    }
    #[classattr]
    fn MPRL() -> Exchange {
        Exchange {
            mic: MIC::MPRL
        }
    }
    #[classattr]
    fn EPRL() -> Exchange {
        Exchange {
            mic: MIC::EPRL
        }
    }
    #[classattr]
    fn EPRD() -> Exchange {
        Exchange {
            mic: MIC::EPRD
        }
    }
    #[classattr]
    fn XMIO() -> Exchange {
        Exchange {
            mic: MIC::XMIO
        }
    }
    #[classattr]
    fn EMLD() -> Exchange {
        Exchange {
            mic: MIC::EMLD
        }
    }
    #[classattr]
    fn OTCM() -> Exchange {
        Exchange {
            mic: MIC::OTCM
        }
    }
    #[classattr]
    fn CAVE() -> Exchange {
        Exchange {
            mic: MIC::CAVE
        }
    }
    #[classattr]
    fn OTCB() -> Exchange {
        Exchange {
            mic: MIC::OTCB
        }
    }
    #[classattr]
    fn OTCQ() -> Exchange {
        Exchange {
            mic: MIC::OTCQ
        }
    }
    #[classattr]
    fn PINL() -> Exchange {
        Exchange {
            mic: MIC::PINL
        }
    }
    #[classattr]
    fn PINI() -> Exchange {
        Exchange {
            mic: MIC::PINI
        }
    }
    #[classattr]
    fn PINX() -> Exchange {
        Exchange {
            mic: MIC::PINX
        }
    }
    #[classattr]
    fn PSGM() -> Exchange {
        Exchange {
            mic: MIC::PSGM
        }
    }
    #[classattr]
    fn PINC() -> Exchange {
        Exchange {
            mic: MIC::PINC
        }
    }
    #[classattr]
    fn FINR() -> Exchange {
        Exchange {
            mic: MIC::FINR
        }
    }
    #[classattr]
    fn FINN() -> Exchange {
        Exchange {
            mic: MIC::FINN
        }
    }
    #[classattr]
    fn FINC() -> Exchange {
        Exchange {
            mic: MIC::FINC
        }
    }
    #[classattr]
    fn FINY() -> Exchange {
        Exchange {
            mic: MIC::FINY
        }
    }
    #[classattr]
    fn XADF() -> Exchange {
        Exchange {
            mic: MIC::XADF
        }
    }
    #[classattr]
    fn FINO() -> Exchange {
        Exchange {
            mic: MIC::FINO
        }
    }
    #[classattr]
    fn OOTC() -> Exchange {
        Exchange {
            mic: MIC::OOTC
        }
    }
    #[classattr]
    fn OPRA() -> Exchange {
        Exchange {
            mic: MIC::OPRA
        }
    }
    #[classattr]
    fn MEMX() -> Exchange {
        Exchange {
            mic: MIC::MEMX
        }
    }
    #[classattr]
    fn MEMD() -> Exchange {
        Exchange {
            mic: MIC::MEMD
        }
    }
    #[classattr]
    fn MXOP() -> Exchange {
        Exchange {
            mic: MIC::MXOP
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
    fn XCNQ() -> Exchange {
        Exchange {
            mic: MIC::XCNQ
        }
    }
    #[classattr]
    fn PURE() -> Exchange {
        Exchange {
            mic: MIC::PURE
        }
    }
    #[classattr]
    fn CSE2() -> Exchange {
        Exchange {
            mic: MIC::CSE2
        }
    }
    #[classattr]
    fn XTSE() -> Exchange {
        Exchange {
            mic: MIC::XTSE
        }
    }
    #[classattr]
    fn XDRK() -> Exchange {
        Exchange {
            mic: MIC::XDRK
        }
    }
    #[classattr]
    fn VDRK() -> Exchange {
        Exchange {
            mic: MIC::VDRK
        }
    }
    #[classattr]
    fn XTSX() -> Exchange {
        Exchange {
            mic: MIC::XTSX
        }
    }
    #[classattr]
    fn XTNX() -> Exchange {
        Exchange {
            mic: MIC::XTNX
        }
    }
    #[classattr]
    fn XATS() -> Exchange {
        Exchange {
            mic: MIC::XATS
        }
    }
    #[classattr]
    fn XATX() -> Exchange {
        Exchange {
            mic: MIC::XATX
        }
    }
    #[classattr]
    fn ADRK() -> Exchange {
        Exchange {
            mic: MIC::ADRK
        }
    }
    #[classattr]
    fn XMOD() -> Exchange {
        Exchange {
            mic: MIC::XMOD
        }
    }
    #[classattr]
    fn XMOC() -> Exchange {
        Exchange {
            mic: MIC::XMOC
        }
    }
    #[classattr]
    fn NEOE() -> Exchange {
        Exchange {
            mic: MIC::NEOE
        }
    }
    #[classattr]
    fn NEOD() -> Exchange {
        Exchange {
            mic: MIC::NEOD
        }
    }
    #[classattr]
    fn NEON() -> Exchange {
        Exchange {
            mic: MIC::NEON
        }
    }
    #[classattr]
    fn NEOC() -> Exchange {
        Exchange {
            mic: MIC::NEOC
        }
    }
    #[classattr]
    fn XXXX() -> Exchange {
        Exchange {
            mic: MIC::XXXX
        }
    }
    #[classattr]
    fn PYPR() -> Exchange {
        Exchange {
            mic: MIC::PYPR
        }
    }
    #[classattr]
    fn SIMU() -> Exchange {
        Exchange {
            mic: MIC::SIMU
        }
    }
}
