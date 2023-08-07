from enum import Enum
from pathlib import Path

EXPRESSION_PRESETS_FILE = (
    Path(__file__).parent.parent.parent.parent / "resources" / "expression_presets" / "expression_presets.json"
)


class PresetType(str, Enum):
    pass


class Happiness(PresetType):
    HAPPINESS_1 = "happiness_1"
    HAPPINESS_2 = "happiness_2"
    HAPPINESS_3 = "happiness_3"
    HAPPINESS_4 = "happiness_4"
    HAPPINESS_5 = "happiness_5"


class Anger(PresetType):
    ANGER_1 = "anger_1"
    ANGER_2 = "anger_2"
    ANGER_3 = "anger_3"
    ANGER_4 = "anger_4"
    ANGER_5 = "anger_5"


class Disgust(PresetType):
    DISGUST_1 = "disgust_1"
    DISGUST_2 = "disgust_2"
    DISGUST_3 = "disgust_3"
    DISGUST_4 = "disgust_4"
    DISGUST_5 = "disgust_5"


class Fear(PresetType):
    FEAR_1 = "fear_1"
    FEAR_2 = "fear_2"
    FEAR_3 = "fear_3"
    FEAR_4 = "fear_4"
    FEAR_5 = "fear_5"


class Surprise(PresetType):
    SURPRISE_1 = "surprise_1"
    SURPRISE_2 = "surprise_2"
    SURPRISE_3 = "surprise_3"
    SURPRISE_4 = "surprise_4"
    SURPRISE_5 = "surprise_5"


class Sadness(PresetType):
    SADNESS_1 = "sadness_1"
    SADNESS_2 = "sadness_2"
    SADNESS_3 = "sadness_3"
    SADNESS_4 = "sadness_4"
    SADNESS_5 = "sadness_5"


class Contempt(PresetType):
    CONTEMPT_1 = "contempt_1"
    CONTEMPT_2 = "contempt_2"
    CONTEMPT_3 = "contempt_3"
    CONTEMPT_4 = "contempt_4"
    CONTEMPT_5 = "contempt_5"


class MouthOpen(PresetType):
    MOUTH_OPEN_1 = "mouth_open_1"
    MOUTH_OPEN_2 = "mouth_open_2"
    MOUTH_OPEN_3 = "mouth_open_3"
    MOUTH_OPEN_4 = "mouth_open_4"
    MOUTH_OPEN_5 = "mouth_open_5"
