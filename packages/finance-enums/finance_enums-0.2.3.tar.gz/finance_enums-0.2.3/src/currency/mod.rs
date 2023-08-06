#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{Currency as BaseCurrency};

#[pyclass]
pub struct Currency {
    pub code: BaseCurrency,
}

#[pymethods]
impl Currency {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        let value_as_str = value.as_str();
        let base_currency = match value_as_str {
            "EUr" => BaseCurrency::EUX,
            "GBp" => BaseCurrency::GBX,
            "USd" => BaseCurrency::USX,
            _ => BaseCurrency::from_str(value_as_str).unwrap()
        };
        Ok(
            Currency {
                code: base_currency
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.code.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Currency<{}>", self.code.to_string()))
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
    fn name(&self) -> &'static str {
        self.code.name()
    }
    
    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseCurrency::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Currency> {
        BaseCurrency::iter().map(|item: BaseCurrency| Currency{code: item} ).collect()
    }

    #[classattr]
    fn AED() -> Currency {
        Currency {
            code: BaseCurrency::AED
        }
    }
    #[classattr]
    fn AFN() -> Currency {
        Currency {
            code: BaseCurrency::AFN
        }
    }
    #[classattr]
    fn ALL() -> Currency {
        Currency {
            code: BaseCurrency::ALL
        }
    }
    #[classattr]
    fn AMD() -> Currency {
        Currency {
            code: BaseCurrency::AMD
        }
    }
    #[classattr]
    fn ANG() -> Currency {
        Currency {
            code: BaseCurrency::ANG
        }
    }
    #[classattr]
    fn AOA() -> Currency {
        Currency {
            code: BaseCurrency::AOA
        }
    }
    #[classattr]
    fn ARS() -> Currency {
        Currency {
            code: BaseCurrency::ARS
        }
    }
    #[classattr]
    fn AUD() -> Currency {
        Currency {
            code: BaseCurrency::AUD
        }
    }
    #[classattr]
    fn AWG() -> Currency {
        Currency {
            code: BaseCurrency::AWG
        }
    }
    #[classattr]
    fn AZN() -> Currency {
        Currency {
            code: BaseCurrency::AZN
        }
    }
    #[classattr]
    fn BAM() -> Currency {
        Currency {
            code: BaseCurrency::BAM
        }
    }
    #[classattr]
    fn BBD() -> Currency {
        Currency {
            code: BaseCurrency::BBD
        }
    }
    #[classattr]
    fn BDT() -> Currency {
        Currency {
            code: BaseCurrency::BDT
        }
    }
    #[classattr]
    fn BGN() -> Currency {
        Currency {
            code: BaseCurrency::BGN
        }
    }
    #[classattr]
    fn BHD() -> Currency {
        Currency {
            code: BaseCurrency::BHD
        }
    }
    #[classattr]
    fn BIF() -> Currency {
        Currency {
            code: BaseCurrency::BIF
        }
    }
    #[classattr]
    fn BMD() -> Currency {
        Currency {
            code: BaseCurrency::BMD
        }
    }
    #[classattr]
    fn BND() -> Currency {
        Currency {
            code: BaseCurrency::BND
        }
    }
    #[classattr]
    fn BOB() -> Currency {
        Currency {
            code: BaseCurrency::BOB
        }
    }
    #[classattr]
    fn BOV() -> Currency {
        Currency {
            code: BaseCurrency::BOV
        }
    }
    #[classattr]
    fn BRL() -> Currency {
        Currency {
            code: BaseCurrency::BRL
        }
    }
    #[classattr]
    fn BSD() -> Currency {
        Currency {
            code: BaseCurrency::BSD
        }
    }
    #[classattr]
    fn BTN() -> Currency {
        Currency {
            code: BaseCurrency::BTN
        }
    }
    #[classattr]
    fn BWP() -> Currency {
        Currency {
            code: BaseCurrency::BWP
        }
    }
    #[classattr]
    fn BYN() -> Currency {
        Currency {
            code: BaseCurrency::BYN
        }
    }
    #[classattr]
    fn BZD() -> Currency {
        Currency {
            code: BaseCurrency::BZD
        }
    }
    #[classattr]
    fn CAD() -> Currency {
        Currency {
            code: BaseCurrency::CAD
        }
    }
    #[classattr]
    fn CDF() -> Currency {
        Currency {
            code: BaseCurrency::CDF
        }
    }
    #[classattr]
    fn CHE() -> Currency {
        Currency {
            code: BaseCurrency::CHE
        }
    }
    #[classattr]
    fn CHF() -> Currency {
        Currency {
            code: BaseCurrency::CHF
        }
    }
    #[classattr]
    fn CHW() -> Currency {
        Currency {
            code: BaseCurrency::CHW
        }
    }
    #[classattr]
    fn CLF() -> Currency {
        Currency {
            code: BaseCurrency::CLF
        }
    }
    #[classattr]
    fn CLP() -> Currency {
        Currency {
            code: BaseCurrency::CLP
        }
    }
    #[classattr]
    fn COP() -> Currency {
        Currency {
            code: BaseCurrency::COP
        }
    }
    #[classattr]
    fn COU() -> Currency {
        Currency {
            code: BaseCurrency::COU
        }
    }
    #[classattr]
    fn CRC() -> Currency {
        Currency {
            code: BaseCurrency::CRC
        }
    }
    #[classattr]
    fn CUC() -> Currency {
        Currency {
            code: BaseCurrency::CUC
        }
    }
    #[classattr]
    fn CUP() -> Currency {
        Currency {
            code: BaseCurrency::CUP
        }
    }
    #[classattr]
    fn CVE() -> Currency {
        Currency {
            code: BaseCurrency::CVE
        }
    }
    #[classattr]
    fn CZK() -> Currency {
        Currency {
            code: BaseCurrency::CZK
        }
    }
    #[classattr]
    fn DJF() -> Currency {
        Currency {
            code: BaseCurrency::DJF
        }
    }
    #[classattr]
    fn DKK() -> Currency {
        Currency {
            code: BaseCurrency::DKK
        }
    }
    #[classattr]
    fn DOP() -> Currency {
        Currency {
            code: BaseCurrency::DOP
        }
    }
    #[classattr]
    fn DZD() -> Currency {
        Currency {
            code: BaseCurrency::DZD
        }
    }
    #[classattr]
    fn EGP() -> Currency {
        Currency {
            code: BaseCurrency::EGP
        }
    }
    #[classattr]
    fn ERN() -> Currency {
        Currency {
            code: BaseCurrency::ERN
        }
    }
    #[classattr]
    fn ETB() -> Currency {
        Currency {
            code: BaseCurrency::ETB
        }
    }
    #[classattr]
    fn EUR() -> Currency {
        Currency {
            code: BaseCurrency::EUR
        }
    }
    #[classattr]
    fn EUX() -> Currency {
        Currency {
            code: BaseCurrency::EUX
        }
    }
    #[classattr]
    fn FJD() -> Currency {
        Currency {
            code: BaseCurrency::FJD
        }
    }
    #[classattr]
    fn FKP() -> Currency {
        Currency {
            code: BaseCurrency::FKP
        }
    }
    #[classattr]
    fn GBP() -> Currency {
        Currency {
            code: BaseCurrency::GBP
        }
    }
    #[classattr]
    fn GBX() -> Currency {
        Currency {
            code: BaseCurrency::GBX
        }
    }
    #[classattr]
    fn GEL() -> Currency {
        Currency {
            code: BaseCurrency::GEL
        }
    }
    #[classattr]
    fn GHS() -> Currency {
        Currency {
            code: BaseCurrency::GHS
        }
    }
    #[classattr]
    fn GIP() -> Currency {
        Currency {
            code: BaseCurrency::GIP
        }
    }
    #[classattr]
    fn GMD() -> Currency {
        Currency {
            code: BaseCurrency::GMD
        }
    }
    #[classattr]
    fn GNF() -> Currency {
        Currency {
            code: BaseCurrency::GNF
        }
    }
    #[classattr]
    fn GTQ() -> Currency {
        Currency {
            code: BaseCurrency::GTQ
        }
    }
    #[classattr]
    fn GYD() -> Currency {
        Currency {
            code: BaseCurrency::GYD
        }
    }
    #[classattr]
    fn HKD() -> Currency {
        Currency {
            code: BaseCurrency::HKD
        }
    }
    #[classattr]
    fn HNL() -> Currency {
        Currency {
            code: BaseCurrency::HNL
        }
    }
    #[classattr]
    fn HTG() -> Currency {
        Currency {
            code: BaseCurrency::HTG
        }
    }
    #[classattr]
    fn HUF() -> Currency {
        Currency {
            code: BaseCurrency::HUF
        }
    }
    #[classattr]
    fn IDR() -> Currency {
        Currency {
            code: BaseCurrency::IDR
        }
    }
    #[classattr]
    fn ILS() -> Currency {
        Currency {
            code: BaseCurrency::ILS
        }
    }
    #[classattr]
    fn INR() -> Currency {
        Currency {
            code: BaseCurrency::INR
        }
    }
    #[classattr]
    fn IQD() -> Currency {
        Currency {
            code: BaseCurrency::IQD
        }
    }
    #[classattr]
    fn IRR() -> Currency {
        Currency {
            code: BaseCurrency::IRR
        }
    }
    #[classattr]
    fn ISK() -> Currency {
        Currency {
            code: BaseCurrency::ISK
        }
    }
    #[classattr]
    fn JMD() -> Currency {
        Currency {
            code: BaseCurrency::JMD
        }
    }
    #[classattr]
    fn JOD() -> Currency {
        Currency {
            code: BaseCurrency::JOD
        }
    }
    #[classattr]
    fn JPY() -> Currency {
        Currency {
            code: BaseCurrency::JPY
        }
    }
    #[classattr]
    fn KES() -> Currency {
        Currency {
            code: BaseCurrency::KES
        }
    }
    #[classattr]
    fn KGS() -> Currency {
        Currency {
            code: BaseCurrency::KGS
        }
    }
    #[classattr]
    fn KHR() -> Currency {
        Currency {
            code: BaseCurrency::KHR
        }
    }
    #[classattr]
    fn KMF() -> Currency {
        Currency {
            code: BaseCurrency::KMF
        }
    }
    #[classattr]
    fn KPW() -> Currency {
        Currency {
            code: BaseCurrency::KPW
        }
    }
    #[classattr]
    fn KRW() -> Currency {
        Currency {
            code: BaseCurrency::KRW
        }
    }
    #[classattr]
    fn KWD() -> Currency {
        Currency {
            code: BaseCurrency::KWD
        }
    }
    #[classattr]
    fn KYD() -> Currency {
        Currency {
            code: BaseCurrency::KYD
        }
    }
    #[classattr]
    fn KZT() -> Currency {
        Currency {
            code: BaseCurrency::KZT
        }
    }
    #[classattr]
    fn LAK() -> Currency {
        Currency {
            code: BaseCurrency::LAK
        }
    }
    #[classattr]
    fn LBP() -> Currency {
        Currency {
            code: BaseCurrency::LBP
        }
    }
    #[classattr]
    fn LKR() -> Currency {
        Currency {
            code: BaseCurrency::LKR
        }
    }
    #[classattr]
    fn LRD() -> Currency {
        Currency {
            code: BaseCurrency::LRD
        }
    }
    #[classattr]
    fn LSL() -> Currency {
        Currency {
            code: BaseCurrency::LSL
        }
    }
    #[classattr]
    fn LYD() -> Currency {
        Currency {
            code: BaseCurrency::LYD
        }
    }
    #[classattr]
    fn MAD() -> Currency {
        Currency {
            code: BaseCurrency::MAD
        }
    }
    #[classattr]
    fn MDL() -> Currency {
        Currency {
            code: BaseCurrency::MDL
        }
    }
    #[classattr]
    fn MGA() -> Currency {
        Currency {
            code: BaseCurrency::MGA
        }
    }
    #[classattr]
    fn MKD() -> Currency {
        Currency {
            code: BaseCurrency::MKD
        }
    }
    #[classattr]
    fn MMK() -> Currency {
        Currency {
            code: BaseCurrency::MMK
        }
    }
    #[classattr]
    fn MNT() -> Currency {
        Currency {
            code: BaseCurrency::MNT
        }
    }
    #[classattr]
    fn MOP() -> Currency {
        Currency {
            code: BaseCurrency::MOP
        }
    }
    #[classattr]
    fn MRU() -> Currency {
        Currency {
            code: BaseCurrency::MRU
        }
    }
    #[classattr]
    fn MUR() -> Currency {
        Currency {
            code: BaseCurrency::MUR
        }
    }
    #[classattr]
    fn MVR() -> Currency {
        Currency {
            code: BaseCurrency::MVR
        }
    }
    #[classattr]
    fn MWK() -> Currency {
        Currency {
            code: BaseCurrency::MWK
        }
    }
    #[classattr]
    fn MXN() -> Currency {
        Currency {
            code: BaseCurrency::MXN
        }
    }
    #[classattr]
    fn MXV() -> Currency {
        Currency {
            code: BaseCurrency::MXV
        }
    }
    #[classattr]
    fn MYR() -> Currency {
        Currency {
            code: BaseCurrency::MYR
        }
    }
    #[classattr]
    fn MZN() -> Currency {
        Currency {
            code: BaseCurrency::MZN
        }
    }
    #[classattr]
    fn NAD() -> Currency {
        Currency {
            code: BaseCurrency::NAD
        }
    }
    #[classattr]
    fn NGN() -> Currency {
        Currency {
            code: BaseCurrency::NGN
        }
    }
    #[classattr]
    fn NIO() -> Currency {
        Currency {
            code: BaseCurrency::NIO
        }
    }
    #[classattr]
    fn NOK() -> Currency {
        Currency {
            code: BaseCurrency::NOK
        }
    }
    #[classattr]
    fn NPR() -> Currency {
        Currency {
            code: BaseCurrency::NPR
        }
    }
    #[classattr]
    fn NZD() -> Currency {
        Currency {
            code: BaseCurrency::NZD
        }
    }
    #[classattr]
    fn OMR() -> Currency {
        Currency {
            code: BaseCurrency::OMR
        }
    }
    #[classattr]
    fn PAB() -> Currency {
        Currency {
            code: BaseCurrency::PAB
        }
    }
    #[classattr]
    fn PEN() -> Currency {
        Currency {
            code: BaseCurrency::PEN
        }
    }
    #[classattr]
    fn PGK() -> Currency {
        Currency {
            code: BaseCurrency::PGK
        }
    }
    #[classattr]
    fn PHP() -> Currency {
        Currency {
            code: BaseCurrency::PHP
        }
    }
    #[classattr]
    fn PKR() -> Currency {
        Currency {
            code: BaseCurrency::PKR
        }
    }
    #[classattr]
    fn PLN() -> Currency {
        Currency {
            code: BaseCurrency::PLN
        }
    }
    #[classattr]
    fn PYG() -> Currency {
        Currency {
            code: BaseCurrency::PYG
        }
    }
    #[classattr]
    fn QAR() -> Currency {
        Currency {
            code: BaseCurrency::QAR
        }
    }
    #[classattr]
    fn RON() -> Currency {
        Currency {
            code: BaseCurrency::RON
        }
    }
    #[classattr]
    fn RSD() -> Currency {
        Currency {
            code: BaseCurrency::RSD
        }
    }
    #[classattr]
    fn CNY() -> Currency {
        Currency {
            code: BaseCurrency::CNY
        }
    }
    #[classattr]
    fn RUB() -> Currency {
        Currency {
            code: BaseCurrency::RUB
        }
    }
    #[classattr]
    fn RWF() -> Currency {
        Currency {
            code: BaseCurrency::RWF
        }
    }
    #[classattr]
    fn SAR() -> Currency {
        Currency {
            code: BaseCurrency::SAR
        }
    }
    #[classattr]
    fn SBD() -> Currency {
        Currency {
            code: BaseCurrency::SBD
        }
    }
    #[classattr]
    fn SCR() -> Currency {
        Currency {
            code: BaseCurrency::SCR
        }
    }
    #[classattr]
    fn SDG() -> Currency {
        Currency {
            code: BaseCurrency::SDG
        }
    }
    #[classattr]
    fn SEK() -> Currency {
        Currency {
            code: BaseCurrency::SEK
        }
    }
    #[classattr]
    fn SGD() -> Currency {
        Currency {
            code: BaseCurrency::SGD
        }
    }
    #[classattr]
    fn SHP() -> Currency {
        Currency {
            code: BaseCurrency::SHP
        }
    }
    #[classattr]
    fn SLE() -> Currency {
        Currency {
            code: BaseCurrency::SLE
        }
    }
    #[classattr]
    fn SLL() -> Currency {
        Currency {
            code: BaseCurrency::SLL
        }
    }
    #[classattr]
    fn SOS() -> Currency {
        Currency {
            code: BaseCurrency::SOS
        }
    }
    #[classattr]
    fn SRD() -> Currency {
        Currency {
            code: BaseCurrency::SRD
        }
    }
    #[classattr]
    fn SSP() -> Currency {
        Currency {
            code: BaseCurrency::SSP
        }
    }
    #[classattr]
    fn STN() -> Currency {
        Currency {
            code: BaseCurrency::STN
        }
    }
    #[classattr]
    fn SVC() -> Currency {
        Currency {
            code: BaseCurrency::SVC
        }
    }
    #[classattr]
    fn SYP() -> Currency {
        Currency {
            code: BaseCurrency::SYP
        }
    }
    #[classattr]
    fn SZL() -> Currency {
        Currency {
            code: BaseCurrency::SZL
        }
    }
    #[classattr]
    fn THB() -> Currency {
        Currency {
            code: BaseCurrency::THB
        }
    }
    #[classattr]
    fn TJS() -> Currency {
        Currency {
            code: BaseCurrency::TJS
        }
    }
    #[classattr]
    fn TMT() -> Currency {
        Currency {
            code: BaseCurrency::TMT
        }
    }
    #[classattr]
    fn TND() -> Currency {
        Currency {
            code: BaseCurrency::TND
        }
    }
    #[classattr]
    fn TOP() -> Currency {
        Currency {
            code: BaseCurrency::TOP
        }
    }
    #[classattr]
    fn TRY() -> Currency {
        Currency {
            code: BaseCurrency::TRY
        }
    }
    #[classattr]
    fn TTD() -> Currency {
        Currency {
            code: BaseCurrency::TTD
        }
    }
    #[classattr]
    fn TWD() -> Currency {
        Currency {
            code: BaseCurrency::TWD
        }
    }
    #[classattr]
    fn TZS() -> Currency {
        Currency {
            code: BaseCurrency::TZS
        }
    }
    #[classattr]
    fn UAH() -> Currency {
        Currency {
            code: BaseCurrency::UAH
        }
    }
    #[classattr]
    fn UGX() -> Currency {
        Currency {
            code: BaseCurrency::UGX
        }
    }
    #[classattr]
    fn USD() -> Currency {
        Currency {
            code: BaseCurrency::USD
        }
    }
    #[classattr]
    fn USX() -> Currency {
        Currency {
            code: BaseCurrency::USX
        }
    }
    #[classattr]
    fn USN() -> Currency {
        Currency {
            code: BaseCurrency::USN
        }
    }
    #[classattr]
    fn UYI() -> Currency {
        Currency {
            code: BaseCurrency::UYI
        }
    }
    #[classattr]
    fn UYU() -> Currency {
        Currency {
            code: BaseCurrency::UYU
        }
    }
    #[classattr]
    fn UYW() -> Currency {
        Currency {
            code: BaseCurrency::UYW
        }
    }
    #[classattr]
    fn UZS() -> Currency {
        Currency {
            code: BaseCurrency::UZS
        }
    }
    #[classattr]
    fn VED() -> Currency {
        Currency {
            code: BaseCurrency::VED
        }
    }
    #[classattr]
    fn VES() -> Currency {
        Currency {
            code: BaseCurrency::VES
        }
    }
    #[classattr]
    fn VND() -> Currency {
        Currency {
            code: BaseCurrency::VND
        }
    }
    #[classattr]
    fn VUV() -> Currency {
        Currency {
            code: BaseCurrency::VUV
        }
    }
    #[classattr]
    fn WST() -> Currency {
        Currency {
            code: BaseCurrency::WST
        }
    }
    #[classattr]
    fn XAF() -> Currency {
        Currency {
            code: BaseCurrency::XAF
        }
    }
    #[classattr]
    fn XAG() -> Currency {
        Currency {
            code: BaseCurrency::XAG
        }
    }
    #[classattr]
    fn XAU() -> Currency {
        Currency {
            code: BaseCurrency::XAU
        }
    }
    #[classattr]
    fn XBA() -> Currency {
        Currency {
            code: BaseCurrency::XBA
        }
    }
    #[classattr]
    fn XBB() -> Currency {
        Currency {
            code: BaseCurrency::XBB
        }
    }
    #[classattr]
    fn XBC() -> Currency {
        Currency {
            code: BaseCurrency::XBC
        }
    }
    #[classattr]
    fn XBD() -> Currency {
        Currency {
            code: BaseCurrency::XBD
        }
    }
    #[classattr]
    fn XCD() -> Currency {
        Currency {
            code: BaseCurrency::XCD
        }
    }
    #[classattr]
    fn XDR() -> Currency {
        Currency {
            code: BaseCurrency::XDR
        }
    }
    #[classattr]
    fn XOF() -> Currency {
        Currency {
            code: BaseCurrency::XOF
        }
    }
    #[classattr]
    fn XPD() -> Currency {
        Currency {
            code: BaseCurrency::XPD
        }
    }
    #[classattr]
    fn XPF() -> Currency {
        Currency {
            code: BaseCurrency::XPF
        }
    }
    #[classattr]
    fn XPT() -> Currency {
        Currency {
            code: BaseCurrency::XPT
        }
    }
    #[classattr]
    fn XSU() -> Currency {
        Currency {
            code: BaseCurrency::XSU
        }
    }
    #[classattr]
    fn XTS() -> Currency {
        Currency {
            code: BaseCurrency::XTS
        }
    }
    #[classattr]
    fn XUA() -> Currency {
        Currency {
            code: BaseCurrency::XUA
        }
    }
    #[classattr]
    fn XXX() -> Currency {
        Currency {
            code: BaseCurrency::XXX
        }
    }
    #[classattr]
    fn YER() -> Currency {
        Currency {
            code: BaseCurrency::YER
        }
    }
    #[classattr]
    fn ZAR() -> Currency {
        Currency {
            code: BaseCurrency::ZAR
        }
    }
    #[classattr]
    fn ZMW() -> Currency {
        Currency {
            code: BaseCurrency::ZMW
        }
    }
    #[classattr]
    fn ZWL() -> Currency {
        Currency {
            code: BaseCurrency::ZWL
        }
    }
}
