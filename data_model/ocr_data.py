import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class OCRDataPair:
    image_path: Path
    image_transcripts_path: Path

    def to_json(self) -> Dict:
        return {
            "image_path": str(self.image_path),
            "image_transcripts_path": str(self.image_transcripts_path),
        }

    @classmethod
    def from_json(cls, data: Dict):
        return cls(Path(data["image_path"]), Path(data["image_transcripts_path"]))


@dataclass
class OCRDataList:
    pairs: List[OCRDataPair]

    def save(self, path: Path) -> None:
        with path.open("w") as file:
            for data_pair in self.pairs:
                line = json.dumps(data_pair.to_json(), ensure_ascii=False)
                file.write(line + "\n")

    @classmethod
    def load(cls, path: Path):
        data_pairs = []
        with path.open() as file:
            for line in file:
                line_data = json.loads(line)
                data_pair = OCRDataPair.from_json(line_data)
                data_pairs.append(data_pair)
        return cls(data_pairs)
