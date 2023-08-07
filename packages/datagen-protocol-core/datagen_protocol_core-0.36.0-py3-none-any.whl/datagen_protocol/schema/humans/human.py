from typing import List, Optional

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.attributes import Age, Ethnicity, EyesColor, FacialHairStyle, Gender, HairLength, HairStyle
from datagen_protocol.schema.base import Asset, AssetAttributes, AttributesList, SchemaBaseModel
from datagen_protocol.schema.d3 import Point, Rotation, Vector
from datagen_protocol.schema.environment import Background, Camera, Light
from datagen_protocol.schema.humans.accessories import Accessories
from datagen_protocol.schema.humans.expressions.expression import Expression
from pydantic import BaseModel, Field


class HairColor(SchemaBaseModel):
    melanin: float = fields.numeric(conf["human"]["hair"]["melanin"])
    redness: float = fields.numeric(conf["human"]["hair"]["redness"])
    whiteness: float = fields.numeric(conf["human"]["hair"]["whiteness"])
    roughness: float = fields.numeric(conf["human"]["hair"]["roughness"])
    index_of_refraction: float = fields.numeric(conf["human"]["hair"]["refraction"])


class HairModel(SchemaBaseModel):
    color_settings: HairColor = Field(default_factory=HairColor)


class HairAttributes(AssetAttributes):
    age_group_match: AttributesList[Age]
    ethnicity_match: AttributesList[Ethnicity]
    gender_match: AttributesList[Gender]
    length: HairLength
    style: AttributesList[HairStyle]


class FacialHairAttributes(AssetAttributes):
    style: FacialHairStyle


class OutfitAttributes(AssetAttributes):
    gender_match: AttributesList[Gender]


class EyebrowsAttributes(AssetAttributes):
    age_group_match: AttributesList[Age]
    ethnicity_match: AttributesList[Ethnicity]
    gender_match: AttributesList[Gender]


class Hair(HairModel, Asset[HairAttributes]):
    pass


class FacialHair(HairModel, Asset[FacialHairAttributes]):
    pass


class Eyebrows(HairModel, Asset[EyebrowsAttributes]):
    pass


class Gaze(SchemaBaseModel):
    distance: float = fields.numeric(conf["human"]["eyes"]["gaze"]["distance"])
    direction: Vector = fields.vector(conf["human"]["eyes"]["gaze"]["direction"])


class EyesAttributes(AssetAttributes):
    color: EyesColor


class Eyes(Asset[EyesAttributes]):
    target_of_gaze: Gaze = Field(default_factory=Gaze)
    iris_diameter: float = fields.numeric(conf["human"]["eyes"]["iris_diameter"])
    pupil_diameter: float = fields.numeric(conf["human"]["eyes"]["pupil_diameter"])
    sclera_seed: int = fields.numeric(conf["human"]["eyes"]["sclera_seed"])
    redness: float = fields.numeric(conf["human"]["eyes"]["redness"])


# TODO: add blemishes and make SchemaBaseModel the base class
class Head(BaseModel):
    eyes: Eyes
    hair: Optional[Hair]
    eyebrows: Optional[Eyebrows]
    facial_hair: Optional[FacialHair]
    expression: Expression = Field(default_factory=Expression)
    location: Point = fields.point(conf["human"]["head"]["location"])
    rotation: Rotation = fields.rotation(conf["human"]["head"]["rotation"])


class HumanAttributes(AssetAttributes):
    ethnicity: Ethnicity
    age: Age
    gender: Gender


class Outfit(Asset[OutfitAttributes]):
    pass


class Human(Asset[HumanAttributes]):
    head: Head
    outfit: Optional[Outfit]

    def __setattr__(self, name, value):
        # not using the pydantic validator decorator, as it is not triggered by simple value assignments.
        # and we expect the user to assign an outfit object to the human by calling human.outfit = some_outfit
        if name == "outfit" and isinstance(value, Outfit):
            if hasattr(self, "attributes") and hasattr(value, "attributes"):
                if self.attributes.gender not in value.attributes.gender_match:
                    raise ValueError('Human gender and Outfit gender must match')

        super().__setattr__(name, value)


class HumanDatapoint(SchemaBaseModel):
    human: Human
    camera: Camera
    accessories: Optional[Accessories]
    background: Optional[Background]
    lights: Optional[List[Light]]
