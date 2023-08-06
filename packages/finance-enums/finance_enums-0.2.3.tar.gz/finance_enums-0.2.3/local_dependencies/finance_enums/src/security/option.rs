use serde::{Deserialize, Serialize};

#[derive(
    Copy, Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize,
)]
#[strum(serialize_all = "PascalCase")]
pub enum OptionType {
    Call,
    Put,
}

#[derive(
    Copy, Clone, Debug, Deserialize, Display, EnumIter, EnumString, Eq, PartialEq, Serialize,
)]
#[strum(serialize_all = "PascalCase")]
pub enum OptionExerciseType {
    American,
    European,
    Bermudan,
}
