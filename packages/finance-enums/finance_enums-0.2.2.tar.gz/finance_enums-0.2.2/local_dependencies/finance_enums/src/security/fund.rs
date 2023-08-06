use serde::{Deserialize, Serialize};

#[derive(
    Copy, Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize,
)]
#[strum(serialize_all = "PascalCase")]
pub enum FundType {
    ETF,
    MutualFund,
    REIT,
}

#[derive(
    Copy, Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize,
)]
#[strum(serialize_all = "PascalCase")]
pub enum FundSubType {
    Index,
    Sector,
    Active,
    Passive,
}

#[derive(
    Copy, Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize,
)]
#[strum(serialize_all = "PascalCase")]
pub enum MutualFundEndedness {
    Open,
    Close,
}
