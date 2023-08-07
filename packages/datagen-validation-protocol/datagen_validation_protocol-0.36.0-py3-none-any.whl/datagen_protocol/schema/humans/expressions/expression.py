import json

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.base import SchemaBaseModel
from datagen_protocol.schema.humans.expressions.presets import EXPRESSION_PRESETS_FILE, PresetType


class Expression(SchemaBaseModel):
    brow_inner_up: float = fields.numeric(conf["human"]["expression"]["brow_inner_up"])
    brow_down_left: float = fields.numeric(conf["human"]["expression"]["brow_down"]["left"])
    brow_down_right: float = fields.numeric(conf["human"]["expression"]["brow_down"]["right"])
    brow_outer_up_left: float = fields.numeric(conf["human"]["expression"]["brow_outer_up"]["left"])
    brow_outer_up_right: float = fields.numeric(conf["human"]["expression"]["brow_outer_up"]["right"])
    cheek_puff: float = fields.numeric(conf["human"]["expression"]["cheek_puff"])
    cheek_squint_left: float = fields.numeric(conf["human"]["expression"]["cheek_squint"]["left"])
    cheek_squint_right: float = fields.numeric(conf["human"]["expression"]["cheek_squint"]["right"])
    eye_blink_left: float = fields.numeric(conf["human"]["expression"]["eye_blink"]["left"])
    eye_blink_right: float = fields.numeric(conf["human"]["expression"]["eye_blink"]["right"])
    eye_squint_left: float = fields.numeric(conf["human"]["expression"]["eye_squint"]["left"])
    eye_squint_right: float = fields.numeric(conf["human"]["expression"]["eye_squint"]["right"])
    eye_wide_left: float = fields.numeric(conf["human"]["expression"]["eye_wide"]["left"])
    eye_wide_right: float = fields.numeric(conf["human"]["expression"]["eye_wide"]["right"])
    jaw_open: float = fields.numeric(conf["human"]["expression"]["jaw_open"])
    jaw_forward: float = fields.numeric(conf["human"]["expression"]["jaw_forward"])
    jaw_left: float = fields.numeric(conf["human"]["expression"]["jaw"]["left"])
    jaw_right: float = fields.numeric(conf["human"]["expression"]["jaw"]["right"])
    mouth_funnel: float = fields.numeric(conf["human"]["expression"]["mouth_funnel"])
    mouth_pucker: float = fields.numeric(conf["human"]["expression"]["mouth_pucker"])
    mouth_left: float = fields.numeric(conf["human"]["expression"]["mouth"]["left"])
    mouth_right: float = fields.numeric(conf["human"]["expression"]["mouth"]["right"])
    mouth_roll_upper: float = fields.numeric(conf["human"]["expression"]["mouth_roll"]["upper"])
    mouth_roll_lower: float = fields.numeric(conf["human"]["expression"]["mouth_roll"]["lower"])
    mouth_shrug_upper: float = fields.numeric(conf["human"]["expression"]["mouth_shrug"]["upper"])
    mouth_shrug_lower: float = fields.numeric(conf["human"]["expression"]["mouth_shrug"]["lower"])
    mouth_close: float = fields.numeric(conf["human"]["expression"]["mouth_close"])
    mouth_smile_left: float = fields.numeric(conf["human"]["expression"]["mouth_smile"]["left"])
    mouth_smile_right: float = fields.numeric(conf["human"]["expression"]["mouth_smile"]["right"])
    mouth_frown_left: float = fields.numeric(conf["human"]["expression"]["mouth_frown"]["left"])
    mouth_frown_right: float = fields.numeric(conf["human"]["expression"]["mouth_frown"]["right"])
    mouth_dimple_left: float = fields.numeric(conf["human"]["expression"]["mouth_dimple"]["left"])
    mouth_dimple_right: float = fields.numeric(conf["human"]["expression"]["mouth_dimple"]["right"])
    mouth_upper_up_left: float = fields.numeric(conf["human"]["expression"]["mouth_upper_up"]["left"])
    mouth_upper_up_right: float = fields.numeric(conf["human"]["expression"]["mouth_upper_up"]["right"])
    mouth_lower_down_left: float = fields.numeric(conf["human"]["expression"]["mouth_lower_down"]["left"])
    mouth_lower_down_right: float = fields.numeric(conf["human"]["expression"]["mouth_lower_down"]["right"])
    mouth_press_left: float = fields.numeric(conf["human"]["expression"]["mouth_press"]["left"])
    mouth_press_right: float = fields.numeric(conf["human"]["expression"]["mouth_press"]["right"])
    mouth_stretch_left: float = fields.numeric(conf["human"]["expression"]["mouth_stretch"]["left"])
    mouth_stretch_right: float = fields.numeric(conf["human"]["expression"]["mouth_stretch"]["right"])
    nose_sneer_left: float = fields.numeric(conf["human"]["expression"]["nose_sneer"]["left"])
    nose_sneer_right: float = fields.numeric(conf["human"]["expression"]["nose_sneer"]["right"])
    nostril_up_left: float = fields.numeric(conf["human"]["expression"]["nostril_up"]["left"])
    nostril_up_right: float = fields.numeric(conf["human"]["expression"]["nostril_up"]["right"])

    @classmethod
    def from_facs(cls, facs_action_units: dict) -> "Expression":
        return cls(
            **{
                "brow_inner_up": facs_action_units.get("AU1", 0.0),
                "brow_down_left": max(facs_action_units.get("AU4", 0.0), facs_action_units.get("AU9", 0.0) * 0.3),
                "brow_down_right": max(facs_action_units.get("AU4", 0.0), facs_action_units.get("AU9", 0.0) * 0.3),
                "brow_outer_up_left": facs_action_units.get("AU2", 0.0),
                "brow_outer_up_right": facs_action_units.get("AU2", 0.0),
                "eye_blink_left": max(
                    facs_action_units.get("AU41", 0.0),
                    facs_action_units.get("AU42", 0.0) * 0.4,
                    facs_action_units.get("AU43", 0.0),
                    facs_action_units.get("AU44", 0.0) * 0.3,
                    facs_action_units.get("AU45", 0.0),
                ),
                "eye_blink_right": max(
                    facs_action_units.get("AU41", 0.0),
                    facs_action_units.get("AU42", 0.0) * 0.4,
                    facs_action_units.get("AU43", 0.0),
                    facs_action_units.get("AU44", 0.0) * 0.3,
                    facs_action_units.get("AU45", 0.0),
                ),
                "eye_squint_left": facs_action_units.get("AU7", 0.0),
                "eye_squint_right": facs_action_units.get("AU7", 0.0),
                "eye_wide_left": facs_action_units.get("AU5", 0.0),
                "eye_wide_right": facs_action_units.get("AU5", 0.0),
                "cheek_puff": facs_action_units.get("AU34", 0.0),
                "cheek_squint_left": max(facs_action_units.get("AU6"), facs_action_units.get("AU44")),
                "cheek_squint_right": max(facs_action_units.get("AU6"), facs_action_units.get("AU44")),
                "nose_sneer_left": facs_action_units.get("AU9"),
                "nose_sneer_right": facs_action_units.get("AU9"),
                "jaw_open": max(
                    facs_action_units.get("AU25", 0.0) * 0.05,
                    facs_action_units.get("AU26", 0.0) * 0.35,
                    facs_action_units.get("AU27", 0.0),
                    facs_action_units.get("AU28", 0.0) * 0.3,
                ),
                "jaw_forward": facs_action_units.get("AU29"),
                "jaw_left": facs_action_units.get("AU30"),
                "jaw_right": facs_action_units.get("AU30"),
                "mouth_funnel": max(
                    facs_action_units.get("AU18") * 0.5,
                    facs_action_units.get("AU22", 0.0),
                    facs_action_units.get("AU23", 0.0) * 0.3,
                ),
                "mouth_pucker": max(
                    facs_action_units.get("AU18") * 0.5,
                    facs_action_units.get("AU22", 0.0) * 0.3,
                    facs_action_units.get("AU23", 0.0),
                ),
                "mouth_left": facs_action_units.get("AU13", 0.0) * 0.7,
                "mouth_right": facs_action_units.get("AU13", 0.0) * 0.7,
                "mouth_roll_upper": facs_action_units.get("AU28", 0.0),
                "mouth_roll_lower": max(facs_action_units.get("AU28", 0.0), facs_action_units.get("AU23") * 0.13),
                "mouth_shrug_lower": facs_action_units.get("AU17", 0.0),
                "mouth_shrug_upper": facs_action_units.get("AU10", 0.0),
                "mouth_close": facs_action_units.get("AU23", 0.0) * 0.07,
                "mouth_smile_left": max(facs_action_units.get("AU12", 0.0), facs_action_units.get("AU13", 0.0) * 0.3),
                "mouth_smile_right": max(facs_action_units.get("AU12", 0.0), facs_action_units.get("AU13", 0.0) * 0.3),
                "mouth_frown_left": facs_action_units.get("AU15", 0.0),
                "mouth_frown_right": facs_action_units.get("AU15", 0.0),
                "mouth_dimple_left": facs_action_units.get("AU14", 0.0),
                "mouth_dimple_right": facs_action_units.get("AU14", 0.0),
                "mouth_upper_up_left": max(facs_action_units.get("AU10", 0.0), facs_action_units.get("AU9", 0.0) * 0.3),
                "mouth_upper_up_right": max(
                    facs_action_units.get("AU10", 0.0), facs_action_units.get("AU9", 0.0) * 0.3
                ),
                "mouth_lower_down_left": facs_action_units.get("AU16", 0.0),
                "mouth_lower_down_right": facs_action_units.get("AU16", 0.0),
                "mouth_press_left": max(
                    facs_action_units.get("AU13"),
                    facs_action_units.get("AU22", 0.0),
                    facs_action_units.get("AU23", 0.0),
                ),
                "mouth_press_right": max(
                    facs_action_units.get("AU13"),
                    facs_action_units.get("AU22", 0.0),
                    facs_action_units.get("AU23", 0.0),
                ),
                "mouth_stretch_left": max(facs_action_units.get("AU13", 0.0) * 0.5, facs_action_units.get("AU20", 0.0)),
                "mouth_stretch_right": max(
                    facs_action_units.get("AU13", 0.0) * 0.5, facs_action_units.get("AU20", 0.0)
                ),
                "nostril_up_left": 0.0,
                "nostril_up_right": 0.0,
            }
        )

    @classmethod
    def from_preset(cls, preset_type: PresetType) -> "Expression":
        with open(EXPRESSION_PRESETS_FILE, "r") as f:
            data = json.load(f)
            return cls(**data[preset_type])
