#![allow(non_snake_case)]

use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;
use pyo3::types::PyType;
use strum::IntoEnumIterator;
use std::str::FromStr;

use finance_enums::{SubIndustry as BaseSubIndustry};
use super::Industry;

#[pyclass]
pub struct SubIndustry {
    pub typ: BaseSubIndustry,
}

#[pymethods]
impl SubIndustry {
    #[new]
    fn py_new(value: String) -> PyResult<Self> {
        Ok(
            SubIndustry {
                typ: BaseSubIndustry::from_str(value.as_str()).unwrap()
            }
        )

    }

    fn __str__(&self) -> PyResult<String>   {
        Ok(format!("{}", self.typ.to_string()))
    }

    fn __repr__(&self) -> PyResult<String>   {
        Ok(format!("SubIndustry<{}>", self.typ.to_string()))
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

    fn industry(&self) -> Industry {
        Industry {
            typ: self.typ.industry()
        }
    }

    #[classmethod]
    fn __len__(_cls: &PyType) -> PyResult<usize> {
        Ok(BaseSubIndustry::iter().count())
    }

    // TODO figure out how to make a class iterator,
    // is way too complicated in pyo3 rn
    #[staticmethod]
    fn members() -> Vec<SubIndustry> {
        BaseSubIndustry::iter().map(|item: BaseSubIndustry| SubIndustry{typ: item} ).collect()
    }

    #[classattr]
    fn OilAndGasDrilling() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasDrilling
        }
    }
    #[classattr]
    fn OilAndGasEquipmentAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasEquipmentAndServices
        }
    }
    #[classattr]
    fn IntegratedOilAndGas() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IntegratedOilAndGas
        }
    }
    #[classattr]
    fn OilAndGasExplorationAndProduction() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasExplorationAndProduction
        }
    }
    #[classattr]
    fn OilAndGasRefiningAndMarketing() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasRefiningAndMarketing
        }
    }
    #[classattr]
    fn OilAndGasStorageAndTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OilAndGasStorageAndTransportation
        }
    }
    #[classattr]
    fn CoalAndConsumeableFuels() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CoalAndConsumeableFuels
        }
    }
    #[classattr]
    fn CommodityChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommodityChemicals
        }
    }
    #[classattr]
    fn DiversifiedChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedChemicals
        }
    }
    #[classattr]
    fn FertilizersAndAgriculturalChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FertilizersAndAgriculturalChemicals
        }
    }
    #[classattr]
    fn IndustrialGases() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialGases
        }
    }
    #[classattr]
    fn SpecialtyChemicals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SpecialtyChemicals
        }
    }
    #[classattr]
    fn ConstructionMaterials() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConstructionMaterials
        }
    }
    #[classattr]
    fn MetalGlassAndPlasticContainers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MetalGlassAndPlasticContainers
        }
    }
    #[classattr]
    fn PaperAndPlasticPackagingProductsAndMaterials() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PaperAndPlasticPackagingProductsAndMaterials
        }
    }
    #[classattr]
    fn Aluminum() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Aluminum
        }
    }
    #[classattr]
    fn DiversifiedMetalsAndMining() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedMetalsAndMining
        }
    }
    #[classattr]
    fn Copper() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Copper
        }
    }
    #[classattr]
    fn Gold() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Gold
        }
    }
    #[classattr]
    fn PreciousMetalsAndMinerals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PreciousMetalsAndMinerals
        }
    }
    #[classattr]
    fn Silver() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Silver
        }
    }
    #[classattr]
    fn Steel() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Steel
        }
    }
    #[classattr]
    fn ForestProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ForestProducts
        }
    }
    #[classattr]
    fn PaperProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PaperProducts
        }
    }
    #[classattr]
    fn AerospaceAndDefense() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AerospaceAndDefense
        }
    }
    #[classattr]
    fn BuildingProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::BuildingProducts
        }
    }
    #[classattr]
    fn ConstructionAndEngineering() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConstructionAndEngineering
        }
    }
    #[classattr]
    fn ElectricalComponentsAndEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectricalComponentsAndEquipment
        }
    }
    #[classattr]
    fn HeavyElectricalEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HeavyElectricalEquipment
        }
    }
    #[classattr]
    fn IndustrialConglomerates() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialConglomerates
        }
    }
    #[classattr]
    fn ConstructionMachineryAndHeavyTransportationEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConstructionMachineryAndHeavyTransportationEquipment
        }
    }
    #[classattr]
    fn AgriculturalAndFarmMachinery() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AgriculturalAndFarmMachinery
        }
    }
    #[classattr]
    fn IndustrialMachinerySuppliesAndComponents() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialMachinerySuppliesAndComponents
        }
    }
    #[classattr]
    fn TradingCompaniesAndDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TradingCompaniesAndDistributors
        }
    }
    #[classattr]
    fn CommercialPrinting() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommercialPrinting
        }
    }
    #[classattr]
    fn EnvironmentalAndFacilitiesServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::EnvironmentalAndFacilitiesServices
        }
    }
    #[classattr]
    fn OfficeServicesAndSupplies() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OfficeServicesAndSupplies
        }
    }
    #[classattr]
    fn DiviersifiedSupportServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiviersifiedSupportServices
        }
    }
    #[classattr]
    fn SecurityAndAlarmServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SecurityAndAlarmServices
        }
    }
    #[classattr]
    fn HumanResourcesAndEmploymentServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HumanResourcesAndEmploymentServices
        }
    }
    #[classattr]
    fn ResearchAndConsultingServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ResearchAndConsultingServices
        }
    }
    #[classattr]
    fn DataProcessingAndOutsourcedServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DataProcessingAndOutsourcedServices
        }
    }
    #[classattr]
    fn AirFreightAndLogistics() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AirFreightAndLogistics
        }
    }
    #[classattr]
    fn PassengerAirlines() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PassengerAirlines
        }
    }
    #[classattr]
    fn MarineTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MarineTransportation
        }
    }
    #[classattr]
    fn RailTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RailTransportation
        }
    }
    #[classattr]
    fn CargoGroundTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CargoGroundTransportation
        }
    }
    #[classattr]
    fn PassengerGroundTransportation() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PassengerGroundTransportation
        }
    }
    #[classattr]
    fn AirportServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AirportServices
        }
    }
    #[classattr]
    fn HighwaysAndRailtracks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HighwaysAndRailtracks
        }
    }
    #[classattr]
    fn MarinePortsAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MarinePortsAndServices
        }
    }
    #[classattr]
    fn AutomotivePartsAndEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AutomotivePartsAndEquipment
        }
    }
    #[classattr]
    fn TiresAndRubber() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TiresAndRubber
        }
    }
    #[classattr]
    fn AutomobileManufacturers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AutomobileManufacturers
        }
    }
    #[classattr]
    fn MotorcycleManufacturers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MotorcycleManufacturers
        }
    }
    #[classattr]
    fn ConsumerElectronics() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConsumerElectronics
        }
    }
    #[classattr]
    fn HomeFurnishings() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HomeFurnishings
        }
    }
    #[classattr]
    fn Homebuilding() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Homebuilding
        }
    }
    #[classattr]
    fn HouseholdAppliances() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HouseholdAppliances
        }
    }
    #[classattr]
    fn HousewaresAndSpecialties() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HousewaresAndSpecialties
        }
    }
    #[classattr]
    fn LeisureProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LeisureProducts
        }
    }
    #[classattr]
    fn ApparelAccessoriesAndLuxuryGoods() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ApparelAccessoriesAndLuxuryGoods
        }
    }
    #[classattr]
    fn Footwear() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Footwear
        }
    }
    #[classattr]
    fn Textiles() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Textiles
        }
    }
    #[classattr]
    fn CasinosAndGaming() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CasinosAndGaming
        }
    }
    #[classattr]
    fn HotelsResortsAndCruiseLines() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HotelsResortsAndCruiseLines
        }
    }
    #[classattr]
    fn LeisureFacilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LeisureFacilities
        }
    }
    #[classattr]
    fn Restaurants() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Restaurants
        }
    }
    #[classattr]
    fn EducationServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::EducationServices
        }
    }
    #[classattr]
    fn SpecializedConsumerServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SpecializedConsumerServices
        }
    }
    #[classattr]
    fn Distributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Distributors
        }
    }
    #[classattr]
    fn BroadlineRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::BroadlineRetail
        }
    }
    #[classattr]
    fn ApparelRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ApparelRetail
        }
    }
    #[classattr]
    fn ComputerAndElectronicsretail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ComputerAndElectronicsretail
        }
    }
    #[classattr]
    fn HomeImprovementRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HomeImprovementRetail
        }
    }
    #[classattr]
    fn OtherSpecialtyRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OtherSpecialtyRetail
        }
    }
    #[classattr]
    fn AutomotiveRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AutomotiveRetail
        }
    }
    #[classattr]
    fn HomefurnishingRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HomefurnishingRetail
        }
    }
    #[classattr]
    fn DrugRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DrugRetail
        }
    }
    #[classattr]
    fn FoodDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FoodDistributors
        }
    }
    #[classattr]
    fn FoodRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FoodRetail
        }
    }
    #[classattr]
    fn ConsumerStaplesMerchandiseRetail() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConsumerStaplesMerchandiseRetail
        }
    }
    #[classattr]
    fn Brewers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Brewers
        }
    }
    #[classattr]
    fn DistillersAndVintners() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DistillersAndVintners
        }
    }
    #[classattr]
    fn SoftDrinksAndNonAlcoholicBeverages() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SoftDrinksAndNonAlcoholicBeverages
        }
    }
    #[classattr]
    fn AgriculturalProductsAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AgriculturalProductsAndServices
        }
    }
    #[classattr]
    fn PackagedFoodsAndMeats() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PackagedFoodsAndMeats
        }
    }
    #[classattr]
    fn Tobacco() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Tobacco
        }
    }
    #[classattr]
    fn HouseholdProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HouseholdProducts
        }
    }
    #[classattr]
    fn PersonalCareProducts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PersonalCareProducts
        }
    }
    #[classattr]
    fn HealthCareEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareEquipment
        }
    }
    #[classattr]
    fn HealthCareSupplies() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareSupplies
        }
    }
    #[classattr]
    fn HealthCareDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareDistributors
        }
    }
    #[classattr]
    fn HealthCareServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareServices
        }
    }
    #[classattr]
    fn HealthCareFacilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareFacilities
        }
    }
    #[classattr]
    fn ManagedHealthCare() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ManagedHealthCare
        }
    }
    #[classattr]
    fn HealthCareTechnology() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareTechnology
        }
    }
    #[classattr]
    fn Biotechnology() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Biotechnology
        }
    }
    #[classattr]
    fn Pharmaceuticals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Pharmaceuticals
        }
    }
    #[classattr]
    fn LifeSciencesToolsAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LifeSciencesToolsAndServices
        }
    }
    #[classattr]
    fn DiversifiedBanks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedBanks
        }
    }
    #[classattr]
    fn RegionalBanks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RegionalBanks
        }
    }
    #[classattr]
    fn DiversifiedFinancialServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedFinancialServices
        }
    }
    #[classattr]
    fn MultiSectorHoldings() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultiSectorHoldings
        }
    }
    #[classattr]
    fn SpecializedFinance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SpecializedFinance
        }
    }
    #[classattr]
    fn CommercialAndResidentialMortgageFinance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommercialAndResidentialMortgageFinance
        }
    }
    #[classattr]
    fn TransactionAndPaymentProcessingServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TransactionAndPaymentProcessingServices
        }
    }
    #[classattr]
    fn ConsumerFinance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ConsumerFinance
        }
    }
    #[classattr]
    fn AssetManagementAndCustodyBanks() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AssetManagementAndCustodyBanks
        }
    }
    #[classattr]
    fn InvestmentBankingAndBrokerage() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InvestmentBankingAndBrokerage
        }
    }
    #[classattr]
    fn DiversifiedCapitalMarkets() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedCapitalMarkets
        }
    }
    #[classattr]
    fn FinancialExchangesAndData() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::FinancialExchangesAndData
        }
    }
    #[classattr]
    fn MortgageRealEstateInvestmentTrusts() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MortgageRealEstateInvestmentTrusts
        }
    }
    #[classattr]
    fn InsuranceBrokers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InsuranceBrokers
        }
    }
    #[classattr]
    fn LifeAndHealthInsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::LifeAndHealthInsurance
        }
    }
    #[classattr]
    fn MultilineInsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultilineInsurance
        }
    }
    #[classattr]
    fn PropertyAndCasualtyInsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::PropertyAndCasualtyInsurance
        }
    }
    #[classattr]
    fn Reinsurance() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Reinsurance
        }
    }
    #[classattr]
    fn ITConsultingAndOtherServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ITConsultingAndOtherServices
        }
    }
    #[classattr]
    fn InternetServicesAndInfrastructure() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InternetServicesAndInfrastructure
        }
    }
    #[classattr]
    fn ApplicationSoftware() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ApplicationSoftware
        }
    }
    #[classattr]
    fn SystemsSoftware() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SystemsSoftware
        }
    }
    #[classattr]
    fn CommunicationsEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CommunicationsEquipment
        }
    }
    #[classattr]
    fn TechnologyHardwareStorageAndPeripherals() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TechnologyHardwareStorageAndPeripherals
        }
    }
    #[classattr]
    fn ElectronicEquipmentAndInstruments() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectronicEquipmentAndInstruments
        }
    }
    #[classattr]
    fn ElectronicComponents() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectronicComponents
        }
    }
    #[classattr]
    fn ElectronicManufacturingServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectronicManufacturingServices
        }
    }
    #[classattr]
    fn TechnologyDistributors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TechnologyDistributors
        }
    }
    #[classattr]
    fn SemiconductorMaterialsAndEquipment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SemiconductorMaterialsAndEquipment
        }
    }
    #[classattr]
    fn Semiconductors() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Semiconductors
        }
    }
    #[classattr]
    fn AlternativeCarriers() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::AlternativeCarriers
        }
    }
    #[classattr]
    fn IntegratedTelecommunicationServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IntegratedTelecommunicationServices
        }
    }
    #[classattr]
    fn WirelessTelecommunicationServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::WirelessTelecommunicationServices
        }
    }
    #[classattr]
    fn Advertising() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Advertising
        }
    }
    #[classattr]
    fn Broadcasting() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Broadcasting
        }
    }
    #[classattr]
    fn CableAndSatellite() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::CableAndSatellite
        }
    }
    #[classattr]
    fn Publishing() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::Publishing
        }
    }
    #[classattr]
    fn MoviesAndEntertainment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MoviesAndEntertainment
        }
    }
    #[classattr]
    fn InteractiveHomeEntertainment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InteractiveHomeEntertainment
        }
    }
    #[classattr]
    fn InteractiveMediaAndServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::InteractiveMediaAndServices
        }
    }
    #[classattr]
    fn ElectricUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::ElectricUtilities
        }
    }
    #[classattr]
    fn GasUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::GasUtilities
        }
    }
    #[classattr]
    fn MultiUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultiUtilities
        }
    }
    #[classattr]
    fn WaterUtilities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::WaterUtilities
        }
    }
    #[classattr]
    fn IndependentPowerProducersAndEnergyTraders() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndependentPowerProducersAndEnergyTraders
        }
    }
    #[classattr]
    fn RenewableElectricity() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RenewableElectricity
        }
    }
    #[classattr]
    fn DiversifiedREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedREITs
        }
    }
    #[classattr]
    fn IndustrialREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::IndustrialREITs
        }
    }
    #[classattr]
    fn HotelAndResortREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HotelAndResortREITs
        }
    }
    #[classattr]
    fn OfficeREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OfficeREITs
        }
    }
    #[classattr]
    fn HealthCareREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::HealthCareREITs
        }
    }
    #[classattr]
    fn MultiFamilyResidentialREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::MultiFamilyResidentialREITs
        }
    }
    #[classattr]
    fn SingleFamilyResidentialREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SingleFamilyResidentialREITs
        }
    }
    #[classattr]
    fn RetailREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RetailREITs
        }
    }
    #[classattr]
    fn OtherSpecializedREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::OtherSpecializedREITs
        }
    }
    #[classattr]
    fn SelfStorageREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::SelfStorageREITs
        }
    }
    #[classattr]
    fn TelecomTowerREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TelecomTowerREITs
        }
    }
    #[classattr]
    fn TimberREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::TimberREITs
        }
    }
    #[classattr]
    fn DataCenterREITs() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DataCenterREITs
        }
    }
    #[classattr]
    fn DiversifiedRealEstateActivities() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::DiversifiedRealEstateActivities
        }
    }
    #[classattr]
    fn RealEstateOperatingCompanies() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RealEstateOperatingCompanies
        }
    }
    #[classattr]
    fn RealEstateDevelopment() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RealEstateDevelopment
        }
    }
    #[classattr]
    fn RealEstateServices() -> SubIndustry {
        SubIndustry {
            typ: BaseSubIndustry::RealEstateServices
        }
    }

}
