import string
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Condition(Enum):
    FACTORY_NEW = 0
    MINIMAL_WEAR = 1
    FIELD_TESTED = 2
    WELL_WORN = 3
    BATTLE_SCARRED = 4

    def __str__(self):
        return [
            "Factory New",
            "Minimal Wear",
            "Field-Tested",
            "Well-Worn",
            "Battle-Scarred",
        ][self.value]


@dataclass
class Skin:
    formatted_name: str
    description: Optional[str]
    image_url: str
    grade: str
    min_float: float
    max_float: float
    price: int


def remove_skin_name_formatting(skin_name: str) -> str:
    skin_name = skin_name.lower()
    skin_name = skin_name.translate(str.maketrans("", "", string.punctuation))
    for char in [" ", "™", "★"]:
        skin_name = skin_name.replace(char, "")
    return skin_name.strip()


def get_best_condition_idx(min_float: float) -> int:
    if min_float > 1.0:
        raise ValueError("min_float must be <= 1.0")
    for idx, min in reversed(list(enumerate([0.0, 0.07, 0.15, 0.38, 0.45]))):
        if min_float >= min:
            return idx
    raise ValueError(
        f"Unexpected min_float value: {min_float}. No matching condition found."
    )


def get_worst_condition_idx(max_float: float) -> int:
    if max_float == 0.0:
        return 0
    if max_float > 1.0:
        raise ValueError("max_float must be <= 1.0")
    for idx, min in reversed(list(enumerate([0.0, 0.07, 0.15, 0.38, 0.45]))):
        if max_float > min:
            return idx
    raise ValueError(
        f"Unexpected min_float value: {max_float}. No matching condition found."
    )


def get_all_conditions_for_float_range(
    min_float: float, max_float: float
) -> list[Condition]:
    if min_float >= max_float:
        raise ValueError("min_float must be < max_float")
    min_idx = get_best_condition_idx(min_float)
    max_idx = get_worst_condition_idx(max_float)
    return [Condition(i) for i in range(min_idx, max_idx + 1)]
