#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{Industry as BaseIndustry};
use super::{IndustryGroup, SubIndustry};

#[pyclass]
pub struct Industry {
    pub typ: BaseIndustry,
}

#[pymethods]
impl Industry {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            Industry {
                typ: BaseIndustry::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("Industry<{}>", self.typ.to_string()))
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

    fn industry_group(&self) -> IndustryGroup {
        IndustryGroup {
            typ: self.typ.industry_group()
        }
    }

    fn subindustries(&self) -> Vec<SubIndustry> {
        self.typ.subindustries().iter().map(|item| SubIndustry{typ: item.clone()} ).collect()
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseIndustry::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<Industry> {
        BaseIndustry::iter().map(|item: BaseIndustry| Industry{typ: item} ).collect()
    }

    #[classattr]
    fn EnergyEquipmentAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::EnergyEquipmentAndServices
        }
    }
    #[classattr]
    fn OilGasAndConsumeableFules() -> Industry {
        Industry {
            typ: BaseIndustry::OilGasAndConsumeableFules
        }
    }
    #[classattr]
    fn Chemicals() -> Industry {
        Industry {
            typ: BaseIndustry::Chemicals
        }
    }
    #[classattr]
    fn ConstructionMaterials() -> Industry {
        Industry {
            typ: BaseIndustry::ConstructionMaterials
        }
    }
    #[classattr]
    fn ContainersAndPackaging() -> Industry {
        Industry {
            typ: BaseIndustry::ContainersAndPackaging
        }
    }
    #[classattr]
    fn MetalsAndMining() -> Industry {
        Industry {
            typ: BaseIndustry::MetalsAndMining
        }
    }
    #[classattr]
    fn PaperAndForestProducts() -> Industry {
        Industry {
            typ: BaseIndustry::PaperAndForestProducts
        }
    }
    #[classattr]
    fn AerospaceAndDefense() -> Industry {
        Industry {
            typ: BaseIndustry::AerospaceAndDefense
        }
    }
    #[classattr]
    fn BuildingProducts() -> Industry {
        Industry {
            typ: BaseIndustry::BuildingProducts
        }
    }
    #[classattr]
    fn ConstructionAndEngineering() -> Industry {
        Industry {
            typ: BaseIndustry::ConstructionAndEngineering
        }
    }
    #[classattr]
    fn ElectricalEquipment() -> Industry {
        Industry {
            typ: BaseIndustry::ElectricalEquipment
        }
    }
    #[classattr]
    fn IndustrialConglomerates() -> Industry {
        Industry {
            typ: BaseIndustry::IndustrialConglomerates
        }
    }
    #[classattr]
    fn Machinery() -> Industry {
        Industry {
            typ: BaseIndustry::Machinery
        }
    }
    #[classattr]
    fn TradingCompaniesAndDistributors() -> Industry {
        Industry {
            typ: BaseIndustry::TradingCompaniesAndDistributors
        }
    }
    #[classattr]
    fn CommercialServicesAndSupplies() -> Industry {
        Industry {
            typ: BaseIndustry::CommercialServicesAndSupplies
        }
    }
    #[classattr]
    fn ProfessionalServices() -> Industry {
        Industry {
            typ: BaseIndustry::ProfessionalServices
        }
    }
    #[classattr]
    fn AirFreightAndLogistics() -> Industry {
        Industry {
            typ: BaseIndustry::AirFreightAndLogistics
        }
    }
    #[classattr]
    fn PassengerAirlines() -> Industry {
        Industry {
            typ: BaseIndustry::PassengerAirlines
        }
    }
    #[classattr]
    fn MarineTransportation() -> Industry {
        Industry {
            typ: BaseIndustry::MarineTransportation
        }
    }
    #[classattr]
    fn GroundTransportation() -> Industry {
        Industry {
            typ: BaseIndustry::GroundTransportation
        }
    }
    #[classattr]
    fn TransportationInfrastructure() -> Industry {
        Industry {
            typ: BaseIndustry::TransportationInfrastructure
        }
    }
    #[classattr]
    fn AutomobileComponents() -> Industry {
        Industry {
            typ: BaseIndustry::AutomobileComponents
        }
    }
    #[classattr]
    fn Automobiles() -> Industry {
        Industry {
            typ: BaseIndustry::Automobiles
        }
    }
    #[classattr]
    fn HouseholdDurables() -> Industry {
        Industry {
            typ: BaseIndustry::HouseholdDurables
        }
    }
    #[classattr]
    fn LeisureProducts() -> Industry {
        Industry {
            typ: BaseIndustry::LeisureProducts
        }
    }
    #[classattr]
    fn TextilesApparelAndLuxuryGoods() -> Industry {
        Industry {
            typ: BaseIndustry::TextilesApparelAndLuxuryGoods
        }
    }
    #[classattr]
    fn HotelsRestaurantsAndLeisure() -> Industry {
        Industry {
            typ: BaseIndustry::HotelsRestaurantsAndLeisure
        }
    }
    #[classattr]
    fn DiversifiedConsumerServices() -> Industry {
        Industry {
            typ: BaseIndustry::DiversifiedConsumerServices
        }
    }
    #[classattr]
    fn Distributors() -> Industry {
        Industry {
            typ: BaseIndustry::Distributors
        }
    }
    #[classattr]
    fn BroadlineRetail() -> Industry {
        Industry {
            typ: BaseIndustry::BroadlineRetail
        }
    }
    #[classattr]
    fn SpecialtyRetail() -> Industry {
        Industry {
            typ: BaseIndustry::SpecialtyRetail
        }
    }
    #[classattr]
    fn ConsumerStaplesDistributionAndRetail() -> Industry {
        Industry {
            typ: BaseIndustry::ConsumerStaplesDistributionAndRetail
        }
    }
    #[classattr]
    fn Beverages() -> Industry {
        Industry {
            typ: BaseIndustry::Beverages
        }
    }
    #[classattr]
    fn FoodProducts() -> Industry {
        Industry {
            typ: BaseIndustry::FoodProducts
        }
    }
    #[classattr]
    fn Tobacco() -> Industry {
        Industry {
            typ: BaseIndustry::Tobacco
        }
    }
    #[classattr]
    fn HouseholdProducts() -> Industry {
        Industry {
            typ: BaseIndustry::HouseholdProducts
        }
    }
    #[classattr]
    fn PersonalCareProducts() -> Industry {
        Industry {
            typ: BaseIndustry::PersonalCareProducts
        }
    }
    #[classattr]
    fn HealthCareEquipmentAndSupplies() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareEquipmentAndSupplies
        }
    }
    #[classattr]
    fn HealthCareProvidersAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareProvidersAndServices
        }
    }
    #[classattr]
    fn HealthCareTechnology() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareTechnology
        }
    }
    #[classattr]
    fn Biotechnology() -> Industry {
        Industry {
            typ: BaseIndustry::Biotechnology
        }
    }
    #[classattr]
    fn Pharmaceuticals() -> Industry {
        Industry {
            typ: BaseIndustry::Pharmaceuticals
        }
    }
    #[classattr]
    fn LifeSciencesToolsAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::LifeSciencesToolsAndServices
        }
    }
    #[classattr]
    fn Banks() -> Industry {
        Industry {
            typ: BaseIndustry::Banks
        }
    }
    #[classattr]
    fn FinancialServices() -> Industry {
        Industry {
            typ: BaseIndustry::FinancialServices
        }
    }
    #[classattr]
    fn ConsumerFinance() -> Industry {
        Industry {
            typ: BaseIndustry::ConsumerFinance
        }
    }
    #[classattr]
    fn CapitalMarkets() -> Industry {
        Industry {
            typ: BaseIndustry::CapitalMarkets
        }
    }
    #[classattr]
    fn MortgageRealEstateInvestmentTrusts() -> Industry {
        Industry {
            typ: BaseIndustry::MortgageRealEstateInvestmentTrusts
        }
    }
    #[classattr]
    fn Insurance() -> Industry {
        Industry {
            typ: BaseIndustry::Insurance
        }
    }
    #[classattr]
    fn ITServices() -> Industry {
        Industry {
            typ: BaseIndustry::ITServices
        }
    }
    #[classattr]
    fn Software() -> Industry {
        Industry {
            typ: BaseIndustry::Software
        }
    }
    #[classattr]
    fn CommunicationsEquipment() -> Industry {
        Industry {
            typ: BaseIndustry::CommunicationsEquipment
        }
    }
    #[classattr]
    fn TechnologyHardwareStorageAndPeripherals() -> Industry {
        Industry {
            typ: BaseIndustry::TechnologyHardwareStorageAndPeripherals
        }
    }
    #[classattr]
    fn ElectronicEquipmentInstrumentsAndComponents() -> Industry {
        Industry {
            typ: BaseIndustry::ElectronicEquipmentInstrumentsAndComponents
        }
    }
    #[classattr]
    fn SemiconductorsAndSemiconductorEquipment() -> Industry {
        Industry {
            typ: BaseIndustry::SemiconductorsAndSemiconductorEquipment
        }
    }
    #[classattr]
    fn DiversifiedTelecommunicationServices() -> Industry {
        Industry {
            typ: BaseIndustry::DiversifiedTelecommunicationServices
        }
    }
    #[classattr]
    fn WirelessTelecommunicationServices() -> Industry {
        Industry {
            typ: BaseIndustry::WirelessTelecommunicationServices
        }
    }
    #[classattr]
    fn Media() -> Industry {
        Industry {
            typ: BaseIndustry::Media
        }
    }
    #[classattr]
    fn Entertainment() -> Industry {
        Industry {
            typ: BaseIndustry::Entertainment
        }
    }
    #[classattr]
    fn InteractiveMediaAndServices() -> Industry {
        Industry {
            typ: BaseIndustry::InteractiveMediaAndServices
        }
    }
    #[classattr]
    fn ElectricUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::ElectricUtilities
        }
    }
    #[classattr]
    fn GasUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::GasUtilities
        }
    }
    #[classattr]
    fn MultiUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::MultiUtilities
        }
    }
    #[classattr]
    fn WaterUtilities() -> Industry {
        Industry {
            typ: BaseIndustry::WaterUtilities
        }
    }
    #[classattr]
    fn IndependentPowerAndRenewableElectricityProducers() -> Industry {
        Industry {
            typ: BaseIndustry::IndependentPowerAndRenewableElectricityProducers
        }
    }
    #[classattr]
    fn DiversifiedREITs() -> Industry {
        Industry {
            typ: BaseIndustry::DiversifiedREITs
        }
    }
    #[classattr]
    fn IndustrialREITs() -> Industry {
        Industry {
            typ: BaseIndustry::IndustrialREITs
        }
    }
    #[classattr]
    fn HotelAndResortREITs() -> Industry {
        Industry {
            typ: BaseIndustry::HotelAndResortREITs
        }
    }
    #[classattr]
    fn OfficeREITs() -> Industry {
        Industry {
            typ: BaseIndustry::OfficeREITs
        }
    }
    #[classattr]
    fn HealthCareREITs() -> Industry {
        Industry {
            typ: BaseIndustry::HealthCareREITs
        }
    }
    #[classattr]
    fn ResidentialREITs() -> Industry {
        Industry {
            typ: BaseIndustry::ResidentialREITs
        }
    }
    #[classattr]
    fn RetailREITs() -> Industry {
        Industry {
            typ: BaseIndustry::RetailREITs
        }
    }
    #[classattr]
    fn SpecializedREITs() -> Industry {
        Industry {
            typ: BaseIndustry::SpecializedREITs
        }
    }
    #[classattr]
    fn RealEstateManagementAndDevelopment() -> Industry {
        Industry {
            typ: BaseIndustry::RealEstateManagementAndDevelopment
        }
    }
}
