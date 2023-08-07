from typing import List

from datagen_protocol.config import conf
from datagen_protocol.schema.attributes import Generator
from datagen_protocol.schema.base import SchemaBaseModel
from datagen_protocol.schema.hic.sequence import DataSequence
from datagen_protocol.schema.humans import HumanDatapoint


class GenerationRequest(SchemaBaseModel):
    generator: Generator
    version: str = conf["request_version"]


class DataRequest(GenerationRequest):
    generator: Generator = Generator.IDENTITIES
    datapoints: List[HumanDatapoint]
    version: str = conf["request_version"]["humans"]

    @staticmethod
    def latest_version() -> str:
        return conf["request_version"]["humans"]

    def __len__(self):
        return len(self.datapoints)


class SequenceRequest(GenerationRequest):
    generator: Generator = Generator.HIC
    sequences: List[DataSequence]
    version: str = conf["request_version"]["hic"]

    @staticmethod
    def latest_version() -> str:
        return conf["request_version"]["hic"]

    def __len__(self):
        return len(self.sequences)
