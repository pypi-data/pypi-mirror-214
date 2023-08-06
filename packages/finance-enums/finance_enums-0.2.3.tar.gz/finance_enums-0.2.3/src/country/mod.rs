#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{CountryCode, CountryCode3};

#[pyclass]
pub struct Country {
    pub code: CountryCode,
    pub code3: CountryCode3,
    pub name: &'static str,
}

#[pymethods]
impl Country {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        let code: CountryCode = CountryCode::from_str(value.as_str()).unwrap();

        Ok(
            Country {
                code,
                code3: code.codethree(),
                name: code.str(),
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.name))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Country<{}>", self.code.to_string()))
    }

    fn __richcmp__(&self, other: &Self, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Lt => Ok(self.code.to_string() < other.code.to_string()),
            CompareOp::Le => Ok(self.code.to_string() <= other.code.to_string()),
            CompareOp::Eq => Ok(self.code == other.code),
            CompareOp::Ne => Ok(self.code != other.code),
            CompareOp::Gt => Ok(self.code.to_string() > other.code.to_string()),
            CompareOp::Ge => Ok(self.code.to_string() >= other.code.to_string()),
        }
    }

    #[getter]
    fn code(&self) -> PyResult<String> {
        Ok(self.code.to_string())
    }
    
    #[getter]
    fn code3(&self) -> PyResult<String> {
        Ok(self.code3.to_string())
    }
    
    #[getter]
    fn name(&self) -> &'static str {
        self.name
    }
    
    #[getter]
    fn flag(&self) -> PyResult<String> {
        Ok(self.code.flag().to_string())
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(CountryCode::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Country> {
        CountryCode::iter().map(|item: CountryCode| Country{code: item, code3: item.codethree(), name: item.str()} ).collect()
    }

    #[classattr]
    fn AF() -> Country {
        Country {
            code: CountryCode::AF,
            code3: CountryCode::AF.codethree(),
            name: CountryCode::AF.str(),
        }
    }
    #[classattr]
    fn AX() -> Country {
        Country {
            code: CountryCode::AX,
            code3: CountryCode::AX.codethree(),
            name: CountryCode::AX.str(),
        }
    }
    #[classattr]
    fn AL() -> Country {
        Country {
            code: CountryCode::AL,
            code3: CountryCode::AL.codethree(),
            name: CountryCode::AL.str(),
        }
    }
    #[classattr]
    fn DZ() -> Country {
        Country {
            code: CountryCode::DZ,
            code3: CountryCode::DZ.codethree(),
            name: CountryCode::DZ.str(),
        }
    }
    #[classattr]
    fn AS() -> Country {
        Country {
            code: CountryCode::AS,
            code3: CountryCode::AS.codethree(),
            name: CountryCode::AS.str(),
        }
    }
    #[classattr]
    fn AD() -> Country {
        Country {
            code: CountryCode::AD,
            code3: CountryCode::AD.codethree(),
            name: CountryCode::AD.str(),
        }
    }
    #[classattr]
    fn AO() -> Country {
        Country {
            code: CountryCode::AO,
            code3: CountryCode::AO.codethree(),
            name: CountryCode::AO.str(),
        }
    }
    #[classattr]
    fn AI() -> Country {
        Country {
            code: CountryCode::AI,
            code3: CountryCode::AI.codethree(),
            name: CountryCode::AI.str(),
        }
    }
    #[classattr]
    fn AQ() -> Country {
        Country {
            code: CountryCode::AQ,
            code3: CountryCode::AQ.codethree(),
            name: CountryCode::AQ.str(),
        }
    }
    #[classattr]
    fn AG() -> Country {
        Country {
            code: CountryCode::AG,
            code3: CountryCode::AG.codethree(),
            name: CountryCode::AG.str(),
        }
    }
    #[classattr]
    fn AR() -> Country {
        Country {
            code: CountryCode::AR,
            code3: CountryCode::AR.codethree(),
            name: CountryCode::AR.str(),
        }
    }
    #[classattr]
    fn AM() -> Country {
        Country {
            code: CountryCode::AM,
            code3: CountryCode::AM.codethree(),
            name: CountryCode::AM.str(),
        }
    }
    #[classattr]
    fn AW() -> Country {
        Country {
            code: CountryCode::AW,
            code3: CountryCode::AW.codethree(),
            name: CountryCode::AW.str(),
        }
    }
    #[classattr]
    fn AU() -> Country {
        Country {
            code: CountryCode::AU,
            code3: CountryCode::AU.codethree(),
            name: CountryCode::AU.str(),
        }
    }
    #[classattr]
    fn AT() -> Country {
        Country {
            code: CountryCode::AT,
            code3: CountryCode::AT.codethree(),
            name: CountryCode::AT.str(),
        }
    }
    #[classattr]
    fn AZ() -> Country {
        Country {
            code: CountryCode::AZ,
            code3: CountryCode::AZ.codethree(),
            name: CountryCode::AZ.str(),
        }
    }
    #[classattr]
    fn BS() -> Country {
        Country {
            code: CountryCode::BS,
            code3: CountryCode::BS.codethree(),
            name: CountryCode::BS.str(),
        }
    }
    #[classattr]
    fn BH() -> Country {
        Country {
            code: CountryCode::BH,
            code3: CountryCode::BH.codethree(),
            name: CountryCode::BH.str(),
        }
    }
    #[classattr]
    fn BD() -> Country {
        Country {
            code: CountryCode::BD,
            code3: CountryCode::BD.codethree(),
            name: CountryCode::BD.str(),
        }
    }
    #[classattr]
    fn BB() -> Country {
        Country {
            code: CountryCode::BB,
            code3: CountryCode::BB.codethree(),
            name: CountryCode::BB.str(),
        }
    }
    #[classattr]
    fn BY() -> Country {
        Country {
            code: CountryCode::BY,
            code3: CountryCode::BY.codethree(),
            name: CountryCode::BY.str(),
        }
    }
    #[classattr]
    fn BE() -> Country {
        Country {
            code: CountryCode::BE,
            code3: CountryCode::BE.codethree(),
            name: CountryCode::BE.str(),
        }
    }
    #[classattr]
    fn BZ() -> Country {
        Country {
            code: CountryCode::BZ,
            code3: CountryCode::BZ.codethree(),
            name: CountryCode::BZ.str(),
        }
    }
    #[classattr]
    fn BJ() -> Country {
        Country {
            code: CountryCode::BJ,
            code3: CountryCode::BJ.codethree(),
            name: CountryCode::BJ.str(),
        }
    }
    #[classattr]
    fn BM() -> Country {
        Country {
            code: CountryCode::BM,
            code3: CountryCode::BM.codethree(),
            name: CountryCode::BM.str(),
        }
    }
    #[classattr]
    fn BT() -> Country {
        Country {
            code: CountryCode::BT,
            code3: CountryCode::BT.codethree(),
            name: CountryCode::BT.str(),
        }
    }
    #[classattr]
    fn BO() -> Country {
        Country {
            code: CountryCode::BO,
            code3: CountryCode::BO.codethree(),
            name: CountryCode::BO.str(),
        }
    }
    #[classattr]
    fn BQ() -> Country {
        Country {
            code: CountryCode::BQ,
            code3: CountryCode::BQ.codethree(),
            name: CountryCode::BQ.str(),
        }
    }
    #[classattr]
    fn BA() -> Country {
        Country {
            code: CountryCode::BA,
            code3: CountryCode::BA.codethree(),
            name: CountryCode::BA.str(),
        }
    }
    #[classattr]
    fn BW() -> Country {
        Country {
            code: CountryCode::BW,
            code3: CountryCode::BW.codethree(),
            name: CountryCode::BW.str(),
        }
    }
    #[classattr]
    fn BV() -> Country {
        Country {
            code: CountryCode::BV,
            code3: CountryCode::BV.codethree(),
            name: CountryCode::BV.str(),
        }
    }
    #[classattr]
    fn BR() -> Country {
        Country {
            code: CountryCode::BR,
            code3: CountryCode::BR.codethree(),
            name: CountryCode::BR.str(),
        }
    }
    #[classattr]
    fn IO() -> Country {
        Country {
            code: CountryCode::IO,
            code3: CountryCode::IO.codethree(),
            name: CountryCode::IO.str(),
        }
    }
    #[classattr]
    fn BN() -> Country {
        Country {
            code: CountryCode::BN,
            code3: CountryCode::BN.codethree(),
            name: CountryCode::BN.str(),
        }
    }
    #[classattr]
    fn BG() -> Country {
        Country {
            code: CountryCode::BG,
            code3: CountryCode::BG.codethree(),
            name: CountryCode::BG.str(),
        }
    }
    #[classattr]
    fn BF() -> Country {
        Country {
            code: CountryCode::BF,
            code3: CountryCode::BF.codethree(),
            name: CountryCode::BF.str(),
        }
    }
    #[classattr]
    fn BI() -> Country {
        Country {
            code: CountryCode::BI,
            code3: CountryCode::BI.codethree(),
            name: CountryCode::BI.str(),
        }
    }
    #[classattr]
    fn CV() -> Country {
        Country {
            code: CountryCode::CV,
            code3: CountryCode::CV.codethree(),
            name: CountryCode::CV.str(),
        }
    }
    #[classattr]
    fn KH() -> Country {
        Country {
            code: CountryCode::KH,
            code3: CountryCode::KH.codethree(),
            name: CountryCode::KH.str(),
        }
    }
    #[classattr]
    fn CM() -> Country {
        Country {
            code: CountryCode::CM,
            code3: CountryCode::CM.codethree(),
            name: CountryCode::CM.str(),
        }
    }
    #[classattr]
    fn CA() -> Country {
        Country {
            code: CountryCode::CA,
            code3: CountryCode::CA.codethree(),
            name: CountryCode::CA.str(),
        }
    }
    #[classattr]
    fn KY() -> Country {
        Country {
            code: CountryCode::KY,
            code3: CountryCode::KY.codethree(),
            name: CountryCode::KY.str(),
        }
    }
    #[classattr]
    fn CF() -> Country {
        Country {
            code: CountryCode::CF,
            code3: CountryCode::CF.codethree(),
            name: CountryCode::CF.str(),
        }
    }
    #[classattr]
    fn TD() -> Country {
        Country {
            code: CountryCode::TD,
            code3: CountryCode::TD.codethree(),
            name: CountryCode::TD.str(),
        }
    }
    #[classattr]
    fn CL() -> Country {
        Country {
            code: CountryCode::CL,
            code3: CountryCode::CL.codethree(),
            name: CountryCode::CL.str(),
        }
    }
    #[classattr]
    fn CN() -> Country {
        Country {
            code: CountryCode::CN,
            code3: CountryCode::CN.codethree(),
            name: CountryCode::CN.str(),
        }
    }
    #[classattr]
    fn CX() -> Country {
        Country {
            code: CountryCode::CX,
            code3: CountryCode::CX.codethree(),
            name: CountryCode::CX.str(),
        }
    }
    #[classattr]
    fn CC() -> Country {
        Country {
            code: CountryCode::CC,
            code3: CountryCode::CC.codethree(),
            name: CountryCode::CC.str(),
        }
    }
    #[classattr]
    fn CO() -> Country {
        Country {
            code: CountryCode::CO,
            code3: CountryCode::CO.codethree(),
            name: CountryCode::CO.str(),
        }
    }
    #[classattr]
    fn KM() -> Country {
        Country {
            code: CountryCode::KM,
            code3: CountryCode::KM.codethree(),
            name: CountryCode::KM.str(),
        }
    }
    #[classattr]
    fn CG() -> Country {
        Country {
            code: CountryCode::CG,
            code3: CountryCode::CG.codethree(),
            name: CountryCode::CG.str(),
        }
    }
    #[classattr]
    fn CD() -> Country {
        Country {
            code: CountryCode::CD,
            code3: CountryCode::CD.codethree(),
            name: CountryCode::CD.str(),
        }
    }
    #[classattr]
    fn CK() -> Country {
        Country {
            code: CountryCode::CK,
            code3: CountryCode::CK.codethree(),
            name: CountryCode::CK.str(),
        }
    }
    #[classattr]
    fn CR() -> Country {
        Country {
            code: CountryCode::CR,
            code3: CountryCode::CR.codethree(),
            name: CountryCode::CR.str(),
        }
    }
    #[classattr]
    fn CI() -> Country {
        Country {
            code: CountryCode::CI,
            code3: CountryCode::CI.codethree(),
            name: CountryCode::CI.str(),
        }
    }
    #[classattr]
    fn HR() -> Country {
        Country {
            code: CountryCode::HR,
            code3: CountryCode::HR.codethree(),
            name: CountryCode::HR.str(),
        }
    }
    #[classattr]
    fn CU() -> Country {
        Country {
            code: CountryCode::CU,
            code3: CountryCode::CU.codethree(),
            name: CountryCode::CU.str(),
        }
    }
    #[classattr]
    fn CW() -> Country {
        Country {
            code: CountryCode::CW,
            code3: CountryCode::CW.codethree(),
            name: CountryCode::CW.str(),
        }
    }
    #[classattr]
    fn CY() -> Country {
        Country {
            code: CountryCode::CY,
            code3: CountryCode::CY.codethree(),
            name: CountryCode::CY.str(),
        }
    }
    #[classattr]
    fn CZ() -> Country {
        Country {
            code: CountryCode::CZ,
            code3: CountryCode::CZ.codethree(),
            name: CountryCode::CZ.str(),
        }
    }
    #[classattr]
    fn DK() -> Country {
        Country {
            code: CountryCode::DK,
            code3: CountryCode::DK.codethree(),
            name: CountryCode::DK.str(),
        }
    }
    #[classattr]
    fn DJ() -> Country {
        Country {
            code: CountryCode::DJ,
            code3: CountryCode::DJ.codethree(),
            name: CountryCode::DJ.str(),
        }
    }
    #[classattr]
    fn DM() -> Country {
        Country {
            code: CountryCode::DM,
            code3: CountryCode::DM.codethree(),
            name: CountryCode::DM.str(),
        }
    }
    #[classattr]
    fn DO() -> Country {
        Country {
            code: CountryCode::DO,
            code3: CountryCode::DO.codethree(),
            name: CountryCode::DO.str(),
        }
    }
    #[classattr]
    fn EC() -> Country {
        Country {
            code: CountryCode::EC,
            code3: CountryCode::EC.codethree(),
            name: CountryCode::EC.str(),
        }
    }
    #[classattr]
    fn EG() -> Country {
        Country {
            code: CountryCode::EG,
            code3: CountryCode::EG.codethree(),
            name: CountryCode::EG.str(),
        }
    }
    #[classattr]
    fn SV() -> Country {
        Country {
            code: CountryCode::SV,
            code3: CountryCode::SV.codethree(),
            name: CountryCode::SV.str(),
        }
    }
    #[classattr]
    fn GQ() -> Country {
        Country {
            code: CountryCode::GQ,
            code3: CountryCode::GQ.codethree(),
            name: CountryCode::GQ.str(),
        }
    }
    #[classattr]
    fn ER() -> Country {
        Country {
            code: CountryCode::ER,
            code3: CountryCode::ER.codethree(),
            name: CountryCode::ER.str(),
        }
    }
    #[classattr]
    fn EE() -> Country {
        Country {
            code: CountryCode::EE,
            code3: CountryCode::EE.codethree(),
            name: CountryCode::EE.str(),
        }
    }
    #[classattr]
    fn SZ() -> Country {
        Country {
            code: CountryCode::SZ,
            code3: CountryCode::SZ.codethree(),
            name: CountryCode::SZ.str(),
        }
    }
    #[classattr]
    fn ET() -> Country {
        Country {
            code: CountryCode::ET,
            code3: CountryCode::ET.codethree(),
            name: CountryCode::ET.str(),
        }
    }
    #[classattr]
    fn FK() -> Country {
        Country {
            code: CountryCode::FK,
            code3: CountryCode::FK.codethree(),
            name: CountryCode::FK.str(),
        }
    }
    #[classattr]
    fn FO() -> Country {
        Country {
            code: CountryCode::FO,
            code3: CountryCode::FO.codethree(),
            name: CountryCode::FO.str(),
        }
    }
    #[classattr]
    fn FJ() -> Country {
        Country {
            code: CountryCode::FJ,
            code3: CountryCode::FJ.codethree(),
            name: CountryCode::FJ.str(),
        }
    }
    #[classattr]
    fn FI() -> Country {
        Country {
            code: CountryCode::FI,
            code3: CountryCode::FI.codethree(),
            name: CountryCode::FI.str(),
        }
    }
    #[classattr]
    fn FR() -> Country {
        Country {
            code: CountryCode::FR,
            code3: CountryCode::FR.codethree(),
            name: CountryCode::FR.str(),
        }
    }
    #[classattr]
    fn GF() -> Country {
        Country {
            code: CountryCode::GF,
            code3: CountryCode::GF.codethree(),
            name: CountryCode::GF.str(),
        }
    }
    #[classattr]
    fn PF() -> Country {
        Country {
            code: CountryCode::PF,
            code3: CountryCode::PF.codethree(),
            name: CountryCode::PF.str(),
        }
    }
    #[classattr]
    fn TF() -> Country {
        Country {
            code: CountryCode::TF,
            code3: CountryCode::TF.codethree(),
            name: CountryCode::TF.str(),
        }
    }
    #[classattr]
    fn GA() -> Country {
        Country {
            code: CountryCode::GA,
            code3: CountryCode::GA.codethree(),
            name: CountryCode::GA.str(),
        }
    }
    #[classattr]
    fn GM() -> Country {
        Country {
            code: CountryCode::GM,
            code3: CountryCode::GM.codethree(),
            name: CountryCode::GM.str(),
        }
    }
    #[classattr]
    fn GE() -> Country {
        Country {
            code: CountryCode::GE,
            code3: CountryCode::GE.codethree(),
            name: CountryCode::GE.str(),
        }
    }
    #[classattr]
    fn DE() -> Country {
        Country {
            code: CountryCode::DE,
            code3: CountryCode::DE.codethree(),
            name: CountryCode::DE.str(),
        }
    }
    #[classattr]
    fn GH() -> Country {
        Country {
            code: CountryCode::GH,
            code3: CountryCode::GH.codethree(),
            name: CountryCode::GH.str(),
        }
    }
    #[classattr]
    fn GI() -> Country {
        Country {
            code: CountryCode::GI,
            code3: CountryCode::GI.codethree(),
            name: CountryCode::GI.str(),
        }
    }
    #[classattr]
    fn GR() -> Country {
        Country {
            code: CountryCode::GR,
            code3: CountryCode::GR.codethree(),
            name: CountryCode::GR.str(),
        }
    }
    #[classattr]
    fn GL() -> Country {
        Country {
            code: CountryCode::GL,
            code3: CountryCode::GL.codethree(),
            name: CountryCode::GL.str(),
        }
    }
    #[classattr]
    fn GD() -> Country {
        Country {
            code: CountryCode::GD,
            code3: CountryCode::GD.codethree(),
            name: CountryCode::GD.str(),
        }
    }
    #[classattr]
    fn GP() -> Country {
        Country {
            code: CountryCode::GP,
            code3: CountryCode::GP.codethree(),
            name: CountryCode::GP.str(),
        }
    }
    #[classattr]
    fn GU() -> Country {
        Country {
            code: CountryCode::GU,
            code3: CountryCode::GU.codethree(),
            name: CountryCode::GU.str(),
        }
    }
    #[classattr]
    fn GT() -> Country {
        Country {
            code: CountryCode::GT,
            code3: CountryCode::GT.codethree(),
            name: CountryCode::GT.str(),
        }
    }
    #[classattr]
    fn GG() -> Country {
        Country {
            code: CountryCode::GG,
            code3: CountryCode::GG.codethree(),
            name: CountryCode::GG.str(),
        }
    }
    #[classattr]
    fn GN() -> Country {
        Country {
            code: CountryCode::GN,
            code3: CountryCode::GN.codethree(),
            name: CountryCode::GN.str(),
        }
    }
    #[classattr]
    fn GW() -> Country {
        Country {
            code: CountryCode::GW,
            code3: CountryCode::GW.codethree(),
            name: CountryCode::GW.str(),
        }
    }
    #[classattr]
    fn GY() -> Country {
        Country {
            code: CountryCode::GY,
            code3: CountryCode::GY.codethree(),
            name: CountryCode::GY.str(),
        }
    }
    #[classattr]
    fn HT() -> Country {
        Country {
            code: CountryCode::HT,
            code3: CountryCode::HT.codethree(),
            name: CountryCode::HT.str(),
        }
    }
    #[classattr]
    fn HM() -> Country {
        Country {
            code: CountryCode::HM,
            code3: CountryCode::HM.codethree(),
            name: CountryCode::HM.str(),
        }
    }
    #[classattr]
    fn VA() -> Country {
        Country {
            code: CountryCode::VA,
            code3: CountryCode::VA.codethree(),
            name: CountryCode::VA.str(),
        }
    }
    #[classattr]
    fn HN() -> Country {
        Country {
            code: CountryCode::HN,
            code3: CountryCode::HN.codethree(),
            name: CountryCode::HN.str(),
        }
    }
    #[classattr]
    fn HK() -> Country {
        Country {
            code: CountryCode::HK,
            code3: CountryCode::HK.codethree(),
            name: CountryCode::HK.str(),
        }
    }
    #[classattr]
    fn HU() -> Country {
        Country {
            code: CountryCode::HU,
            code3: CountryCode::HU.codethree(),
            name: CountryCode::HU.str(),
        }
    }
    #[classattr]
    fn IS() -> Country {
        Country {
            code: CountryCode::IS,
            code3: CountryCode::IS.codethree(),
            name: CountryCode::IS.str(),
        }
    }
    #[classattr]
    fn IN() -> Country {
        Country {
            code: CountryCode::IN,
            code3: CountryCode::IN.codethree(),
            name: CountryCode::IN.str(),
        }
    }
    #[classattr]
    fn ID() -> Country {
        Country {
            code: CountryCode::ID,
            code3: CountryCode::ID.codethree(),
            name: CountryCode::ID.str(),
        }
    }
    #[classattr]
    fn IR() -> Country {
        Country {
            code: CountryCode::IR,
            code3: CountryCode::IR.codethree(),
            name: CountryCode::IR.str(),
        }
    }
    #[classattr]
    fn IQ() -> Country {
        Country {
            code: CountryCode::IQ,
            code3: CountryCode::IQ.codethree(),
            name: CountryCode::IQ.str(),
        }
    }
    #[classattr]
    fn IE() -> Country {
        Country {
            code: CountryCode::IE,
            code3: CountryCode::IE.codethree(),
            name: CountryCode::IE.str(),
        }
    }
    #[classattr]
    fn IM() -> Country {
        Country {
            code: CountryCode::IM,
            code3: CountryCode::IM.codethree(),
            name: CountryCode::IM.str(),
        }
    }
    #[classattr]
    fn IL() -> Country {
        Country {
            code: CountryCode::IL,
            code3: CountryCode::IL.codethree(),
            name: CountryCode::IL.str(),
        }
    }
    #[classattr]
    fn IT() -> Country {
        Country {
            code: CountryCode::IT,
            code3: CountryCode::IT.codethree(),
            name: CountryCode::IT.str(),
        }
    }
    #[classattr]
    fn JM() -> Country {
        Country {
            code: CountryCode::JM,
            code3: CountryCode::JM.codethree(),
            name: CountryCode::JM.str(),
        }
    }
    #[classattr]
    fn JP() -> Country {
        Country {
            code: CountryCode::JP,
            code3: CountryCode::JP.codethree(),
            name: CountryCode::JP.str(),
        }
    }
    #[classattr]
    fn JE() -> Country {
        Country {
            code: CountryCode::JE,
            code3: CountryCode::JE.codethree(),
            name: CountryCode::JE.str(),
        }
    }
    #[classattr]
    fn JO() -> Country {
        Country {
            code: CountryCode::JO,
            code3: CountryCode::JO.codethree(),
            name: CountryCode::JO.str(),
        }
    }
    #[classattr]
    fn KZ() -> Country {
        Country {
            code: CountryCode::KZ,
            code3: CountryCode::KZ.codethree(),
            name: CountryCode::KZ.str(),
        }
    }
    #[classattr]
    fn KE() -> Country {
        Country {
            code: CountryCode::KE,
            code3: CountryCode::KE.codethree(),
            name: CountryCode::KE.str(),
        }
    }
    #[classattr]
    fn KI() -> Country {
        Country {
            code: CountryCode::KI,
            code3: CountryCode::KI.codethree(),
            name: CountryCode::KI.str(),
        }
    }
    #[classattr]
    fn KP() -> Country {
        Country {
            code: CountryCode::KP,
            code3: CountryCode::KP.codethree(),
            name: CountryCode::KP.str(),
        }
    }
    #[classattr]
    fn KR() -> Country {
        Country {
            code: CountryCode::KR,
            code3: CountryCode::KR.codethree(),
            name: CountryCode::KR.str(),
        }
    }
    #[classattr]
    fn KW() -> Country {
        Country {
            code: CountryCode::KW,
            code3: CountryCode::KW.codethree(),
            name: CountryCode::KW.str(),
        }
    }
    #[classattr]
    fn KG() -> Country {
        Country {
            code: CountryCode::KG,
            code3: CountryCode::KG.codethree(),
            name: CountryCode::KG.str(),
        }
    }
    #[classattr]
    fn LA() -> Country {
        Country {
            code: CountryCode::LA,
            code3: CountryCode::LA.codethree(),
            name: CountryCode::LA.str(),
        }
    }
    #[classattr]
    fn LV() -> Country {
        Country {
            code: CountryCode::LV,
            code3: CountryCode::LV.codethree(),
            name: CountryCode::LV.str(),
        }
    }
    #[classattr]
    fn LB() -> Country {
        Country {
            code: CountryCode::LB,
            code3: CountryCode::LB.codethree(),
            name: CountryCode::LB.str(),
        }
    }
    #[classattr]
    fn LS() -> Country {
        Country {
            code: CountryCode::LS,
            code3: CountryCode::LS.codethree(),
            name: CountryCode::LS.str(),
        }
    }
    #[classattr]
    fn LR() -> Country {
        Country {
            code: CountryCode::LR,
            code3: CountryCode::LR.codethree(),
            name: CountryCode::LR.str(),
        }
    }
    #[classattr]
    fn LY() -> Country {
        Country {
            code: CountryCode::LY,
            code3: CountryCode::LY.codethree(),
            name: CountryCode::LY.str(),
        }
    }
    #[classattr]
    fn LI() -> Country {
        Country {
            code: CountryCode::LI,
            code3: CountryCode::LI.codethree(),
            name: CountryCode::LI.str(),
        }
    }
    #[classattr]
    fn LT() -> Country {
        Country {
            code: CountryCode::LT,
            code3: CountryCode::LT.codethree(),
            name: CountryCode::LT.str(),
        }
    }
    #[classattr]
    fn LU() -> Country {
        Country {
            code: CountryCode::LU,
            code3: CountryCode::LU.codethree(),
            name: CountryCode::LU.str(),
        }
    }
    #[classattr]
    fn MO() -> Country {
        Country {
            code: CountryCode::MO,
            code3: CountryCode::MO.codethree(),
            name: CountryCode::MO.str(),
        }
    }
    #[classattr]
    fn MG() -> Country {
        Country {
            code: CountryCode::MG,
            code3: CountryCode::MG.codethree(),
            name: CountryCode::MG.str(),
        }
    }
    #[classattr]
    fn MW() -> Country {
        Country {
            code: CountryCode::MW,
            code3: CountryCode::MW.codethree(),
            name: CountryCode::MW.str(),
        }
    }
    #[classattr]
    fn MY() -> Country {
        Country {
            code: CountryCode::MY,
            code3: CountryCode::MY.codethree(),
            name: CountryCode::MY.str(),
        }
    }
    #[classattr]
    fn MV() -> Country {
        Country {
            code: CountryCode::MV,
            code3: CountryCode::MV.codethree(),
            name: CountryCode::MV.str(),
        }
    }
    #[classattr]
    fn ML() -> Country {
        Country {
            code: CountryCode::ML,
            code3: CountryCode::ML.codethree(),
            name: CountryCode::ML.str(),
        }
    }
    #[classattr]
    fn MT() -> Country {
        Country {
            code: CountryCode::MT,
            code3: CountryCode::MT.codethree(),
            name: CountryCode::MT.str(),
        }
    }
    #[classattr]
    fn MH() -> Country {
        Country {
            code: CountryCode::MH,
            code3: CountryCode::MH.codethree(),
            name: CountryCode::MH.str(),
        }
    }
    #[classattr]
    fn MQ() -> Country {
        Country {
            code: CountryCode::MQ,
            code3: CountryCode::MQ.codethree(),
            name: CountryCode::MQ.str(),
        }
    }
    #[classattr]
    fn MR() -> Country {
        Country {
            code: CountryCode::MR,
            code3: CountryCode::MR.codethree(),
            name: CountryCode::MR.str(),
        }
    }
    #[classattr]
    fn MU() -> Country {
        Country {
            code: CountryCode::MU,
            code3: CountryCode::MU.codethree(),
            name: CountryCode::MU.str(),
        }
    }
    #[classattr]
    fn YT() -> Country {
        Country {
            code: CountryCode::YT,
            code3: CountryCode::YT.codethree(),
            name: CountryCode::YT.str(),
        }
    }
    #[classattr]
    fn MX() -> Country {
        Country {
            code: CountryCode::MX,
            code3: CountryCode::MX.codethree(),
            name: CountryCode::MX.str(),
        }
    }
    #[classattr]
    fn FM() -> Country {
        Country {
            code: CountryCode::FM,
            code3: CountryCode::FM.codethree(),
            name: CountryCode::FM.str(),
        }
    }
    #[classattr]
    fn MD() -> Country {
        Country {
            code: CountryCode::MD,
            code3: CountryCode::MD.codethree(),
            name: CountryCode::MD.str(),
        }
    }
    #[classattr]
    fn MC() -> Country {
        Country {
            code: CountryCode::MC,
            code3: CountryCode::MC.codethree(),
            name: CountryCode::MC.str(),
        }
    }
    #[classattr]
    fn MN() -> Country {
        Country {
            code: CountryCode::MN,
            code3: CountryCode::MN.codethree(),
            name: CountryCode::MN.str(),
        }
    }
    #[classattr]
    fn ME() -> Country {
        Country {
            code: CountryCode::ME,
            code3: CountryCode::ME.codethree(),
            name: CountryCode::ME.str(),
        }
    }
    #[classattr]
    fn MS() -> Country {
        Country {
            code: CountryCode::MS,
            code3: CountryCode::MS.codethree(),
            name: CountryCode::MS.str(),
        }
    }
    #[classattr]
    fn MA() -> Country {
        Country {
            code: CountryCode::MA,
            code3: CountryCode::MA.codethree(),
            name: CountryCode::MA.str(),
        }
    }
    #[classattr]
    fn MZ() -> Country {
        Country {
            code: CountryCode::MZ,
            code3: CountryCode::MZ.codethree(),
            name: CountryCode::MZ.str(),
        }
    }
    #[classattr]
    fn MM() -> Country {
        Country {
            code: CountryCode::MM,
            code3: CountryCode::MM.codethree(),
            name: CountryCode::MM.str(),
        }
    }
    #[classattr]
    fn NA() -> Country {
        Country {
            code: CountryCode::NA,
            code3: CountryCode::NA.codethree(),
            name: CountryCode::NA.str(),
        }
    }
    #[classattr]
    fn NR() -> Country {
        Country {
            code: CountryCode::NR,
            code3: CountryCode::NR.codethree(),
            name: CountryCode::NR.str(),
        }
    }
    #[classattr]
    fn NP() -> Country {
        Country {
            code: CountryCode::NP,
            code3: CountryCode::NP.codethree(),
            name: CountryCode::NP.str(),
        }
    }
    #[classattr]
    fn NL() -> Country {
        Country {
            code: CountryCode::NL,
            code3: CountryCode::NL.codethree(),
            name: CountryCode::NL.str(),
        }
    }
    #[classattr]
    fn NC() -> Country {
        Country {
            code: CountryCode::NC,
            code3: CountryCode::NC.codethree(),
            name: CountryCode::NC.str(),
        }
    }
    #[classattr]
    fn NZ() -> Country {
        Country {
            code: CountryCode::NZ,
            code3: CountryCode::NZ.codethree(),
            name: CountryCode::NZ.str(),
        }
    }
    #[classattr]
    fn NI() -> Country {
        Country {
            code: CountryCode::NI,
            code3: CountryCode::NI.codethree(),
            name: CountryCode::NI.str(),
        }
    }
    #[classattr]
    fn NE() -> Country {
        Country {
            code: CountryCode::NE,
            code3: CountryCode::NE.codethree(),
            name: CountryCode::NE.str(),
        }
    }
    #[classattr]
    fn NG() -> Country {
        Country {
            code: CountryCode::NG,
            code3: CountryCode::NG.codethree(),
            name: CountryCode::NG.str(),
        }
    }
    #[classattr]
    fn NU() -> Country {
        Country {
            code: CountryCode::NU,
            code3: CountryCode::NU.codethree(),
            name: CountryCode::NU.str(),
        }
    }
    #[classattr]
    fn NF() -> Country {
        Country {
            code: CountryCode::NF,
            code3: CountryCode::NF.codethree(),
            name: CountryCode::NF.str(),
        }
    }
    #[classattr]
    fn MK() -> Country {
        Country {
            code: CountryCode::MK,
            code3: CountryCode::MK.codethree(),
            name: CountryCode::MK.str(),
        }
    }
    #[classattr]
    fn MP() -> Country {
        Country {
            code: CountryCode::MP,
            code3: CountryCode::MP.codethree(),
            name: CountryCode::MP.str(),
        }
    }
    #[classattr]
    fn NO() -> Country {
        Country {
            code: CountryCode::NO,
            code3: CountryCode::NO.codethree(),
            name: CountryCode::NO.str(),
        }
    }
    #[classattr]
    fn OM() -> Country {
        Country {
            code: CountryCode::OM,
            code3: CountryCode::OM.codethree(),
            name: CountryCode::OM.str(),
        }
    }
    #[classattr]
    fn PK() -> Country {
        Country {
            code: CountryCode::PK,
            code3: CountryCode::PK.codethree(),
            name: CountryCode::PK.str(),
        }
    }
    #[classattr]
    fn PW() -> Country {
        Country {
            code: CountryCode::PW,
            code3: CountryCode::PW.codethree(),
            name: CountryCode::PW.str(),
        }
    }
    #[classattr]
    fn PS() -> Country {
        Country {
            code: CountryCode::PS,
            code3: CountryCode::PS.codethree(),
            name: CountryCode::PS.str(),
        }
    }
    #[classattr]
    fn PA() -> Country {
        Country {
            code: CountryCode::PA,
            code3: CountryCode::PA.codethree(),
            name: CountryCode::PA.str(),
        }
    }
    #[classattr]
    fn PG() -> Country {
        Country {
            code: CountryCode::PG,
            code3: CountryCode::PG.codethree(),
            name: CountryCode::PG.str(),
        }
    }
    #[classattr]
    fn PY() -> Country {
        Country {
            code: CountryCode::PY,
            code3: CountryCode::PY.codethree(),
            name: CountryCode::PY.str(),
        }
    }
    #[classattr]
    fn PE() -> Country {
        Country {
            code: CountryCode::PE,
            code3: CountryCode::PE.codethree(),
            name: CountryCode::PE.str(),
        }
    }
    #[classattr]
    fn PH() -> Country {
        Country {
            code: CountryCode::PH,
            code3: CountryCode::PH.codethree(),
            name: CountryCode::PH.str(),
        }
    }
    #[classattr]
    fn PN() -> Country {
        Country {
            code: CountryCode::PN,
            code3: CountryCode::PN.codethree(),
            name: CountryCode::PN.str(),
        }
    }
    #[classattr]
    fn PL() -> Country {
        Country {
            code: CountryCode::PL,
            code3: CountryCode::PL.codethree(),
            name: CountryCode::PL.str(),
        }
    }
    #[classattr]
    fn PT() -> Country {
        Country {
            code: CountryCode::PT,
            code3: CountryCode::PT.codethree(),
            name: CountryCode::PT.str(),
        }
    }
    #[classattr]
    fn PR() -> Country {
        Country {
            code: CountryCode::PR,
            code3: CountryCode::PR.codethree(),
            name: CountryCode::PR.str(),
        }
    }
    #[classattr]
    fn QA() -> Country {
        Country {
            code: CountryCode::QA,
            code3: CountryCode::QA.codethree(),
            name: CountryCode::QA.str(),
        }
    }
    #[classattr]
    fn RE() -> Country {
        Country {
            code: CountryCode::RE,
            code3: CountryCode::RE.codethree(),
            name: CountryCode::RE.str(),
        }
    }
    #[classattr]
    fn RO() -> Country {
        Country {
            code: CountryCode::RO,
            code3: CountryCode::RO.codethree(),
            name: CountryCode::RO.str(),
        }
    }
    #[classattr]
    fn RU() -> Country {
        Country {
            code: CountryCode::RU,
            code3: CountryCode::RU.codethree(),
            name: CountryCode::RU.str(),
        }
    }
    #[classattr]
    fn RW() -> Country {
        Country {
            code: CountryCode::RW,
            code3: CountryCode::RW.codethree(),
            name: CountryCode::RW.str(),
        }
    }
    #[classattr]
    fn BL() -> Country {
        Country {
            code: CountryCode::BL,
            code3: CountryCode::BL.codethree(),
            name: CountryCode::BL.str(),
        }
    }
    #[classattr]
    fn SH() -> Country {
        Country {
            code: CountryCode::SH,
            code3: CountryCode::SH.codethree(),
            name: CountryCode::SH.str(),
        }
    }
    #[classattr]
    fn KN() -> Country {
        Country {
            code: CountryCode::KN,
            code3: CountryCode::KN.codethree(),
            name: CountryCode::KN.str(),
        }
    }
    #[classattr]
    fn LC() -> Country {
        Country {
            code: CountryCode::LC,
            code3: CountryCode::LC.codethree(),
            name: CountryCode::LC.str(),
        }
    }
    #[classattr]
    fn MF() -> Country {
        Country {
            code: CountryCode::MF,
            code3: CountryCode::MF.codethree(),
            name: CountryCode::MF.str(),
        }
    }
    #[classattr]
    fn PM() -> Country {
        Country {
            code: CountryCode::PM,
            code3: CountryCode::PM.codethree(),
            name: CountryCode::PM.str(),
        }
    }
    #[classattr]
    fn VC() -> Country {
        Country {
            code: CountryCode::VC,
            code3: CountryCode::VC.codethree(),
            name: CountryCode::VC.str(),
        }
    }
    #[classattr]
    fn WS() -> Country {
        Country {
            code: CountryCode::WS,
            code3: CountryCode::WS.codethree(),
            name: CountryCode::WS.str(),
        }
    }
    #[classattr]
    fn SM() -> Country {
        Country {
            code: CountryCode::SM,
            code3: CountryCode::SM.codethree(),
            name: CountryCode::SM.str(),
        }
    }
    #[classattr]
    fn ST() -> Country {
        Country {
            code: CountryCode::ST,
            code3: CountryCode::ST.codethree(),
            name: CountryCode::ST.str(),
        }
    }
    #[classattr]
    fn SA() -> Country {
        Country {
            code: CountryCode::SA,
            code3: CountryCode::SA.codethree(),
            name: CountryCode::SA.str(),
        }
    }
    #[classattr]
    fn SN() -> Country {
        Country {
            code: CountryCode::SN,
            code3: CountryCode::SN.codethree(),
            name: CountryCode::SN.str(),
        }
    }
    #[classattr]
    fn RS() -> Country {
        Country {
            code: CountryCode::RS,
            code3: CountryCode::RS.codethree(),
            name: CountryCode::RS.str(),
        }
    }
    #[classattr]
    fn SC() -> Country {
        Country {
            code: CountryCode::SC,
            code3: CountryCode::SC.codethree(),
            name: CountryCode::SC.str(),
        }
    }
    #[classattr]
    fn SL() -> Country {
        Country {
            code: CountryCode::SL,
            code3: CountryCode::SL.codethree(),
            name: CountryCode::SL.str(),
        }
    }
    #[classattr]
    fn SG() -> Country {
        Country {
            code: CountryCode::SG,
            code3: CountryCode::SG.codethree(),
            name: CountryCode::SG.str(),
        }
    }
    #[classattr]
    fn SX() -> Country {
        Country {
            code: CountryCode::SX,
            code3: CountryCode::SX.codethree(),
            name: CountryCode::SX.str(),
        }
    }
    #[classattr]
    fn SK() -> Country {
        Country {
            code: CountryCode::SK,
            code3: CountryCode::SK.codethree(),
            name: CountryCode::SK.str(),
        }
    }
    #[classattr]
    fn SI() -> Country {
        Country {
            code: CountryCode::SI,
            code3: CountryCode::SI.codethree(),
            name: CountryCode::SI.str(),
        }
    }
    #[classattr]
    fn SB() -> Country {
        Country {
            code: CountryCode::SB,
            code3: CountryCode::SB.codethree(),
            name: CountryCode::SB.str(),
        }
    }
    #[classattr]
    fn SO() -> Country {
        Country {
            code: CountryCode::SO,
            code3: CountryCode::SO.codethree(),
            name: CountryCode::SO.str(),
        }
    }
    #[classattr]
    fn ZA() -> Country {
        Country {
            code: CountryCode::ZA,
            code3: CountryCode::ZA.codethree(),
            name: CountryCode::ZA.str(),
        }
    }
    #[classattr]
    fn GS() -> Country {
        Country {
            code: CountryCode::GS,
            code3: CountryCode::GS.codethree(),
            name: CountryCode::GS.str(),
        }
    }
    #[classattr]
    fn SS() -> Country {
        Country {
            code: CountryCode::SS,
            code3: CountryCode::SS.codethree(),
            name: CountryCode::SS.str(),
        }
    }
    #[classattr]
    fn ES() -> Country {
        Country {
            code: CountryCode::ES,
            code3: CountryCode::ES.codethree(),
            name: CountryCode::ES.str(),
        }
    }
    #[classattr]
    fn LK() -> Country {
        Country {
            code: CountryCode::LK,
            code3: CountryCode::LK.codethree(),
            name: CountryCode::LK.str(),
        }
    }
    #[classattr]
    fn SD() -> Country {
        Country {
            code: CountryCode::SD,
            code3: CountryCode::SD.codethree(),
            name: CountryCode::SD.str(),
        }
    }
    #[classattr]
    fn SR() -> Country {
        Country {
            code: CountryCode::SR,
            code3: CountryCode::SR.codethree(),
            name: CountryCode::SR.str(),
        }
    }
    #[classattr]
    fn SJ() -> Country {
        Country {
            code: CountryCode::SJ,
            code3: CountryCode::SJ.codethree(),
            name: CountryCode::SJ.str(),
        }
    }
    #[classattr]
    fn SE() -> Country {
        Country {
            code: CountryCode::SE,
            code3: CountryCode::SE.codethree(),
            name: CountryCode::SE.str(),
        }
    }
    #[classattr]
    fn CH() -> Country {
        Country {
            code: CountryCode::CH,
            code3: CountryCode::CH.codethree(),
            name: CountryCode::CH.str(),
        }
    }
    #[classattr]
    fn SY() -> Country {
        Country {
            code: CountryCode::SY,
            code3: CountryCode::SY.codethree(),
            name: CountryCode::SY.str(),
        }
    }
    #[classattr]
    fn TW() -> Country {
        Country {
            code: CountryCode::TW,
            code3: CountryCode::TW.codethree(),
            name: CountryCode::TW.str(),
        }
    }
    #[classattr]
    fn TJ() -> Country {
        Country {
            code: CountryCode::TJ,
            code3: CountryCode::TJ.codethree(),
            name: CountryCode::TJ.str(),
        }
    }
    #[classattr]
    fn TZ() -> Country {
        Country {
            code: CountryCode::TZ,
            code3: CountryCode::TZ.codethree(),
            name: CountryCode::TZ.str(),
        }
    }
    #[classattr]
    fn TH() -> Country {
        Country {
            code: CountryCode::TH,
            code3: CountryCode::TH.codethree(),
            name: CountryCode::TH.str(),
        }
    }
    #[classattr]
    fn TL() -> Country {
        Country {
            code: CountryCode::TL,
            code3: CountryCode::TL.codethree(),
            name: CountryCode::TL.str(),
        }
    }
    #[classattr]
    fn TG() -> Country {
        Country {
            code: CountryCode::TG,
            code3: CountryCode::TG.codethree(),
            name: CountryCode::TG.str(),
        }
    }
    #[classattr]
    fn TK() -> Country {
        Country {
            code: CountryCode::TK,
            code3: CountryCode::TK.codethree(),
            name: CountryCode::TK.str(),
        }
    }
    #[classattr]
    fn TO() -> Country {
        Country {
            code: CountryCode::TO,
            code3: CountryCode::TO.codethree(),
            name: CountryCode::TO.str(),
        }
    }
    #[classattr]
    fn TT() -> Country {
        Country {
            code: CountryCode::TT,
            code3: CountryCode::TT.codethree(),
            name: CountryCode::TT.str(),
        }
    }
    #[classattr]
    fn TN() -> Country {
        Country {
            code: CountryCode::TN,
            code3: CountryCode::TN.codethree(),
            name: CountryCode::TN.str(),
        }
    }
    #[classattr]
    fn TR() -> Country {
        Country {
            code: CountryCode::TR,
            code3: CountryCode::TR.codethree(),
            name: CountryCode::TR.str(),
        }
    }
    #[classattr]
    fn TM() -> Country {
        Country {
            code: CountryCode::TM,
            code3: CountryCode::TM.codethree(),
            name: CountryCode::TM.str(),
        }
    }
    #[classattr]
    fn TC() -> Country {
        Country {
            code: CountryCode::TC,
            code3: CountryCode::TC.codethree(),
            name: CountryCode::TC.str(),
        }
    }
    #[classattr]
    fn TV() -> Country {
        Country {
            code: CountryCode::TV,
            code3: CountryCode::TV.codethree(),
            name: CountryCode::TV.str(),
        }
    }
    #[classattr]
    fn UG() -> Country {
        Country {
            code: CountryCode::UG,
            code3: CountryCode::UG.codethree(),
            name: CountryCode::UG.str(),
        }
    }
    #[classattr]
    fn UA() -> Country {
        Country {
            code: CountryCode::UA,
            code3: CountryCode::UA.codethree(),
            name: CountryCode::UA.str(),
        }
    }
    #[classattr]
    fn AE() -> Country {
        Country {
            code: CountryCode::AE,
            code3: CountryCode::AE.codethree(),
            name: CountryCode::AE.str(),
        }
    }
    #[classattr]
    fn GB() -> Country {
        Country {
            code: CountryCode::GB,
            code3: CountryCode::GB.codethree(),
            name: CountryCode::GB.str(),
        }
    }
    #[classattr]
    fn US() -> Country {
        Country {
            code: CountryCode::US,
            code3: CountryCode::US.codethree(),
            name: CountryCode::US.str(),
        }
    }
    #[classattr]
    fn UM() -> Country {
        Country {
            code: CountryCode::UM,
            code3: CountryCode::UM.codethree(),
            name: CountryCode::UM.str(),
        }
    }
    #[classattr]
    fn UY() -> Country {
        Country {
            code: CountryCode::UY,
            code3: CountryCode::UY.codethree(),
            name: CountryCode::UY.str(),
        }
    }
    #[classattr]
    fn UZ() -> Country {
        Country {
            code: CountryCode::UZ,
            code3: CountryCode::UZ.codethree(),
            name: CountryCode::UZ.str(),
        }
    }
    #[classattr]
    fn VU() -> Country {
        Country {
            code: CountryCode::VU,
            code3: CountryCode::VU.codethree(),
            name: CountryCode::VU.str(),
        }
    }
    #[classattr]
    fn VE() -> Country {
        Country {
            code: CountryCode::VE,
            code3: CountryCode::VE.codethree(),
            name: CountryCode::VE.str(),
        }
    }
    #[classattr]
    fn VN() -> Country {
        Country {
            code: CountryCode::VN,
            code3: CountryCode::VN.codethree(),
            name: CountryCode::VN.str(),
        }
    }
    #[classattr]
    fn VG() -> Country {
        Country {
            code: CountryCode::VG,
            code3: CountryCode::VG.codethree(),
            name: CountryCode::VG.str(),
        }
    }
    #[classattr]
    fn VI() -> Country {
        Country {
            code: CountryCode::VI,
            code3: CountryCode::VI.codethree(),
            name: CountryCode::VI.str(),
        }
    }
    #[classattr]
    fn WF() -> Country {
        Country {
            code: CountryCode::WF,
            code3: CountryCode::WF.codethree(),
            name: CountryCode::WF.str(),
        }
    }
    #[classattr]
    fn EH() -> Country {
        Country {
            code: CountryCode::EH,
            code3: CountryCode::EH.codethree(),
            name: CountryCode::EH.str(),
        }
    }
    #[classattr]
    fn YE() -> Country {
        Country {
            code: CountryCode::YE,
            code3: CountryCode::YE.codethree(),
            name: CountryCode::YE.str(),
        }
    }
    #[classattr]
    fn ZM() -> Country {
        Country {
            code: CountryCode::ZM,
            code3: CountryCode::ZM.codethree(),
            name: CountryCode::ZM.str(),
        }
    }
    #[classattr]
    fn ZW() -> Country {
        Country {
            code: CountryCode::ZW,
            code3: CountryCode::ZW.codethree(),
            name: CountryCode::ZW.str(),
        }
    }
}
