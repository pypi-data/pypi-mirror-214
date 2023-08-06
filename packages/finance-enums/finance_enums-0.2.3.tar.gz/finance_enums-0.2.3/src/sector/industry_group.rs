#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{IndustryGroup as BaseIndustryGroup};
use super::{Sector, Industry};

#[pyclass]
pub struct IndustryGroup {
    pub typ: BaseIndustryGroup,
}

#[pymethods]
impl IndustryGroup {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            IndustryGroup {
                typ: BaseIndustryGroup::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("IndustryGroup<{}>", self.typ.to_string()))
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

    fn sector(&self) -> Sector {
        Sector {
            typ: self.typ.sector()
        }
    }

    fn industries(&self) -> Vec<Industry> {
        self.typ.industries().iter().map(|item| Industry{typ: item.clone()} ).collect()
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseIndustryGroup::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<IndustryGroup> {
        BaseIndustryGroup::iter().map(|item: BaseIndustryGroup| IndustryGroup{typ: item} ).collect()
    }

    // Energy
    #[classattr]
    fn Energy() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Energy
        }
    }

    // Materials
    #[classattr]
    fn Materials() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Materials
        }
    }

    // Industrials
    #[classattr]
    fn CapitalGoods() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::CapitalGoods
        }
    }

    #[classattr]
    fn CommercialAndProfessionalServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::CommercialAndProfessionalServices
        }
    }

    #[classattr]
    fn Transportation() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Transportation
        }
    }
    
    // Consumer Discretionary
    #[classattr]
    fn AutomobilesAndComponents() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::AutomobilesAndComponents
        }
    }
    #[classattr]
    fn ConsumerDurablesAndApparel() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerDurablesAndApparel
        }
    }
    #[classattr]
    fn ConsumerServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerServices
        }
    }
    #[classattr]
    fn ConsumerDiscretionaryDistributionAndRetail() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerDiscretionaryDistributionAndRetail
        }
    }
    // Consumer Staples
    #[classattr]
    fn ConsumerStaplesDistributionAndRetail() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::ConsumerStaplesDistributionAndRetail
        }
    }
    #[classattr]
    fn FoodBeverageAndTobacco() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::FoodBeverageAndTobacco
        }
    }
    #[classattr]
    fn HouseholdAndPersonalProducts() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::HouseholdAndPersonalProducts
        }
    }
    // Health Care
    #[classattr]
    fn HealthCareEquipmentAndServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::HealthCareEquipmentAndServices
        }
    }
    #[classattr]
    fn PharmaceuticalsBiotechnologyAndLifeSciences() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::PharmaceuticalsBiotechnologyAndLifeSciences
        }
    }
    // Financials
    #[classattr]
    fn Banks() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Banks
        }
    }
    #[classattr]
    fn FinancialServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::FinancialServices
        }
    }
    #[classattr]
    fn Insurance() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Insurance
        }
    }
    // Information Technology
    #[classattr]
    fn SoftwareAndServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::SoftwareAndServices
        }
    }
    #[classattr]
    fn TechnologyHardwareAndEquipment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::TechnologyHardwareAndEquipment
        }
    }
    #[classattr]
    fn SemiconductorsAndSemiconductorEquipment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::SemiconductorsAndSemiconductorEquipment
        }
    }
    // Communication Services
    #[classattr]
    fn TelecommunicationServices() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::TelecommunicationServices
        }
    }
    #[classattr]
    fn MediaAndEntertainment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::MediaAndEntertainment
        }
    }
    // Utilities
    #[classattr]
    fn Utilities() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::Utilities
        }
    }
    // Real Estate
    #[classattr]
    fn EquityRealEstateInvestmentTrusts() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::EquityRealEstateInvestmentTrusts
        }
    }
    #[classattr]
    fn RealEstateManagementAndDevelopment() -> IndustryGroup {
        IndustryGroup {
            typ: BaseIndustryGroup::RealEstateManagementAndDevelopment
        }
    }
}
