from __future__ import annotations

from typing import Optional, List, TypeVar, Generic

from chzzk.model import DefaultModel
from chzzk.model.channel import PartialChannel, Channel
from chzzk.model.live import Live
from chzzk.model.video import VideoMetadata


T = TypeVar("T", bound="SearchRecord")


class Offset(DefaultModel):
    offset: int


class Page(DefaultModel):
    next: Offset


class SearchCursor(DefaultModel, Generic[T]):
    size: int
    page: Optional[Page] = None
    data: List[T]

    def __getitem__(self, item):
        return self.data[item]

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)


class SearchRecord(DefaultModel):
    pass


class VideoSearchRecord(SearchRecord):
    video: VideoMetadata
    channel: PartialChannel


class LiveSearchRecord(SearchRecord):
    live: Live
    channel: PartialChannel


class ChannelSearchRecord(SearchRecord):
    channel: Channel
