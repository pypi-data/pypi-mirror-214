from enum import Enum, auto
from typing import Dict, NamedTuple, List

import torch


class Pooling(Enum):
    NONE = auto()
    MEAN = auto()
    HAMMING = auto()

## ITEM FILE MODELS
class ItemData(NamedTuple):
    onset: float
    offset: float
    context_id: int
    phone_id: int
    speaker_id: int


class ItemFile(NamedTuple):
    # key: fileid, value: list of items in the file
    files_data: Dict[str, List[ItemData]]
    # Encodings (e.g. phone_match might be A: 3, N: 2)
    context_match: Dict[str, int]
    phone_match: Dict[str, int]
    speaker_match: Dict[str, int]


## ABXFeatureDataset models
# The order of the elements in ManifestFeatureItem is important.
# It is a dependency for the iterator classes which assume
# the order given here.
class ManifestFeatureItem(NamedTuple):
    start_i: int
    loc_size: int
    context_id: int
    phone_id: int
    speaker_id: int


class ABXFeaturesDataItem(NamedTuple):
    data: torch.Tensor
    out_size: int
    context_id: int
    phone_id: int
    speaker_id: int

class ContextType(Enum):
    WITHIN = auto()
    ANY = auto()
