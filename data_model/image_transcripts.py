import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Vertex:
    x: int
    y: int

    def to_json(self) -> Dict:
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_json(cls, data: Dict):
        return cls(data["x"], data["y"])


@dataclass
class BoundingPolygon:
    vertices: List[Vertex]

    def to_json(self) -> Dict:
        return {"vertices": [vertex.to_json() for vertex in self.vertices]}

    @classmethod
    def from_json(cls, data: Dict):
        return cls([Vertex.from_json(vertex) for vertex in data["vertices"]])


@dataclass
class ImageTranscript:
    text: Optional[str]
    bounding_polygon: Optional[BoundingPolygon]
    confidence: Optional[float]
    language: Optional[str]

    def to_json(self) -> Dict:
        return {
            "text": self.text,
            "bounding_polygon": self.bounding_polygon.to_json()
            if self.bounding_polygon
            else None,
            "confidence": self.confidence,
            "language": self.language,
        }

    @classmethod
    def from_json(cls, data: Dict):
        if data["bounding_polygon"]:
            bounding_polygon = BoundingPolygon.from_json(data["bounding_polygon"])
        else:
            bounding_polygon = None
        return cls(data["text"], bounding_polygon, data["confidence"], data["language"])


class ImageTranscriptsVersion(Enum):
    v01 = "v0.1"


@dataclass
class ImageTranscripts:
    transcripts: List[ImageTranscript]

    def save(
        self, path: Path, version: ImageTranscriptsVersion = ImageTranscriptsVersion.v01
    ) -> None:
        data = self.to_json(version)
        with path.open("w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, path: Path):
        with path.open() as file:
            data = json.load(file)
        return ImageTranscripts.from_json(data)

    def to_json(
        self, version: ImageTranscriptsVersion = ImageTranscriptsVersion.v01
    ) -> Dict:
        if version == ImageTranscriptsVersion.v01:
            data = {
                "version": ImageTranscriptsVersion.v01.value,
                "transcripts": [
                    transcript.to_json() for transcript in self.transcripts
                ],
            }
        else:
            raise NotImplementedError
        return data

    @classmethod
    def from_json(cls, data: Dict):
        version = data["version"]
        if version == ImageTranscriptsVersion.v01.value:
            instance = cls(
                [
                    ImageTranscript.from_json(transcript)
                    for transcript in data["transcripts"]
                ]
            )
        else:
            raise NotImplementedError
        return instance
