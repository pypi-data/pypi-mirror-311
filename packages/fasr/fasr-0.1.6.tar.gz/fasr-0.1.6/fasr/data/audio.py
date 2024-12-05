from docarray import BaseDoc, DocList
from docarray.typing import NdArray, ID
from docarray.utils.filter import filter_docs
from typing import Optional, List, Iterable, Union, Dict, ByteString
import requests
from io import BytesIO
import librosa
from joblib import Parallel, delayed
import os
from functools import lru_cache
from pydantic import ConfigDict, Field
from loguru import logger
from pathlib import Path
from torch import Tensor
from torchaudio.functional import resample as torchaudio_resample
from queue import Queue
import numpy as np


class AudioToken(BaseDoc):
    """Audio token object that represents a token of an audio file.

    Args:
        start_ms (int): Start ms of the token.
        end_ms (int): End ms of the token.
        text (str): Text of the token.
        waveform (NdArray): Waveform of the token.
        follow (str): Follow char. Defaults to "".
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ID = None
    start_ms: int = Field(..., title="Start time of the token.")
    end_ms: int = Field(..., title="End time of the token.")
    text: str = Field(..., title="Text of the token.")
    waveform: NdArray | Tensor | None = Field(None, title="Waveform of the token.")
    follow: Optional[str] = Field(" ", title="Follow char.")

    @property
    def duration_ms(self):
        """Get the duration of the token in milliseconds."""
        return self.end_ms - self.start_ms


class AudioTokenList(DocList):
    @property
    def duration_ms(self):
        """Get the total duration of all the tokens in milliseconds."""
        return sum([token.duration_ms for token in self])

    @property
    def duration(self):
        """Get the total duration of all the tokens in seconds."""
        return self.duration_ms / 1000

    @property
    def text(self):
        """Get the text of all the tokens."""
        text = ""
        for t in self:
            text += t.text
            text += t.follow
        return text


class AudioSpan(BaseDoc):
    """Audio span object that represents a segment of an audio file.

    Args:
        start_ms (int): Start ms of the segment.
        end_ms (int): End ms of the segment.
        waveform (NdArray): Waveform of the segment.
        feats (NdArray): Features of the segment.
        tokens (AudioTokenList): Tokens of the segment.
        sample_rate (int): Sample rate of the segment.
        is_last (bool): Whether the segment is the last segment. Defaults to False.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="ignore")

    id: ID = None
    start_ms: Optional[float] = Field(None, title="Start time of the segment.")
    end_ms: Optional[float] = Field(None, title="End time of the segment.")
    waveform: NdArray | Tensor | None = None
    feats: NdArray | Tensor | None = None
    scores: NdArray | Tensor | None = None
    tokens: Optional[AudioTokenList[AudioToken]] = None
    sample_rate: Optional[int] = None
    language: Optional[str] = None
    emotion: Optional[str] = None
    type: Optional[str] = None
    is_last: bool = False
    is_bad: bool = False
    bad_reason: Optional[str] = None
    bad_component: Optional[str] = None

    @property
    def duration_ms(self):
        """Get the duration of the segment in milliseconds."""
        return self.end_ms - self.start_ms

    @property
    def duration(self):
        """Get the duration of the segment in seconds."""
        return self.duration_ms / 1000

    @property
    def text(self):
        """Get the text of all the tokens."""
        if hasattr(self, "_text"):
            return self._text
        text = ""
        if self.tokens is None:
            return text
        for t in self.tokens:
            text += t.text
            text += t.follow
        return text

    @text.setter
    def text(self, text: str):
        self._text = text

    def __lt__(self, other: "AudioSpan") -> bool:
        """Compare the duration of the segment with another segment. like `self < other`.

        Args:
            other (AudioSpan): Another segment.

        Returns:
            bool: Whether the duration of the segment is less than the duration of the other segment.
        """
        return self.duration_ms < other.duration_ms

    def __gt__(self, other: "AudioSpan") -> bool:
        """Compare the duration of the segment with another segment. like `self > other`.

        Args:
            other (AudioSpan): Another segment.

        Returns:
            bool: Whether the duration of the segment is greater than the duration of the other segment.
        """
        return self.duration_ms > other.duration_ms

    def __getitem__(self, index: int) -> Optional[AudioToken]:
        """Get the token at the index.

        Args:
            index (int): Index of the token.

        Returns:
            AudioToken: Token at the index.
        """
        if self.tokens is None:
            return None
        return self.tokens[index]

    def __len__(self) -> int:
        """Get the number of tokens in the segment.

        Returns:
            int: Number of tokens in the segment.
        """
        if self.tokens is None:
            return 0
        return len(self.tokens)


class AudioSpanList(DocList):
    @property
    def duration_ms(self):
        """Get the total duration of all the spans in milliseconds."""
        return sum([span.duration_ms for span in self])

    @property
    def duration(self):
        """Get the total duration of all the spans in seconds."""
        return self.duration_ms / 1000

    @property
    def padded_duration_ms(self):
        """Get the padded duration of all the spans in milliseconds."""
        all_durations = [span.duration_ms for span in self]
        if len(all_durations) == 0:
            return 0
        duration = max(all_durations) * len(all_durations)
        return duration

    @property
    def max_duration_ms(self):
        """Get the maximum duration of all the spans in milliseconds."""
        all_durations = [span.duration_ms for span in self]
        if len(all_durations) == 0:
            return 0
        return max(all_durations)

    @property
    def text(self):
        """Get the text of all the spans."""
        _text = ""
        for span in self:
            _text += span.text
        return _text


class AudioChannel(BaseDoc):
    """Audio channel object that represents a channel of an audio file.

    Args:
        channel (Literal["left", "right", "mono"]): Channel of the audio file.
        waveform (NdArray): Waveform of the audio file.
        sample_rate (int): Sample rate of the audio file.
        feats (NdArray): Features of the audio file.
        segments (AudioSpanList): Segments of the audio file.
        sents (AudioSpanList): Sentences of the audio file.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="ignore")

    id: ID = None
    waveform: Tensor | NdArray = Field(..., title="Waveform of the audio file.")
    sample_rate: int = Field(..., title="Sample rate of the audio file.")
    feats: NdArray | Tensor | None = Field(
        None, title="Features of the audio file provided by the frontend."
    )
    steps: Optional[AudioSpanList[AudioSpan]] = Field(
        None, title="Steps of the audio file provided by the detector."
    )
    segments: Optional[AudioSpanList[AudioSpan]] = Field(
        None, title="Segments of the audio file provided by the detector."
    )
    sents: Optional[AudioSpanList[AudioSpan]] = Field(
        None, title="Sentences of the audio file provided by the sentencizer."
    )
    is_last: Optional[bool] = Field(False, title="Whether the channel is the last.")
    is_bad: Optional[bool] = Field(False, title="Whether the channel is bad.")
    bad_reason: Optional[Union[str, Exception]] = Field(
        None, title="Reason why the audio file is bad."
    )

    @property
    def duration(self):
        """Get the duration of the audio file in seconds."""
        return librosa.get_duration(y=self.waveform, sr=self.sample_rate)

    @property
    def duration_ms(self):
        return self.duration * 1000

    @property
    def text(self):
        """Get the text of all the spans."""
        if hasattr(self, "_text"):
            return self._text
        if self.sents:
            text = ""
            for sent in self.sents:
                text += sent.text
            return text
        elif self.segments:
            text = ""
            for seg in self.segments:
                text += seg.text
            return text
        else:
            return ""

    @text.setter
    def text(self, text: str):
        self._text = text

    def resample(self, sample_rate: int) -> "AudioChannel":
        """Resample the audio channel waveform to the target sample rate.

        Args:
            sample_rate (int): Target sample rate.
        """
        self.waveform = librosa.resample(
            self.waveform, orig_sr=self.sample_rate, target_sr=sample_rate
        )
        self.sample_rate = sample_rate
        return self

    def resample_torch(self, sample_rate: int) -> "AudioChannel":
        """Resample the audio channel waveform to the target sample rate.

        Args:
            sample_rate (int): Target sample rate.
        """
        self.waveform = torchaudio_resample(
            self.waveform,
            self.sample_rate,
            sample_rate,
            lowpass_filter_width=16,
            rolloff=0.85,
            resampling_method="sinc_interp_kaiser",
            beta=8.555504641634386,
        )
        self.sample_rate = sample_rate
        return self

    def align_bad(self) -> bool:
        """Check if the audio channel is bad."""
        for span in self.segments:  # recognizer报错
            if span.is_bad:
                self.is_bad = True
                self.bad_reason = span.bad_reason
                return True
        for span in self.sents:  # sentencizer报错
            if span.is_bad:
                return True
        for span in self.steps:  # detector报错
            if span.is_bad:
                return True
        return False

    def is_recognized(self) -> bool:
        """Check if the audio channel is recognized."""
        if not self.segments:
            return False
        for span in self.segments:
            span: AudioSpan
            if span.tokens is None:
                return False
        return True

    def __getitem__(self, index) -> Optional[AudioSpan]:
        if not self.segments:
            return None
        return self.segments[index]

    def __len__(self) -> int:
        if not self.segments:
            return 0
        return len(self.segments)


class AudioChannelList(DocList):
    @property
    def text(self):
        """Get the text of all the spans."""
        if not self.sents:
            return ""
        else:
            all_sents = [sent for channel in self for sent in channel.sents]
            sorted_sents = sorted(all_sents, key=lambda x: x.start_ms)
            text = ""
            for sent in sorted_sents:
                text += sent.text
            return text


class Audio(BaseDoc):
    """Audio object that represents an audio file.

    Args:
        url (HttpUrl): URL of the audio file.
        sample_rate (Optional[int], optional): Sample rate of the audio file. Defaults to None.
        waveform (Optional[NdArray], optional): Waveform of the audio file. Defaults to None.
        mono (Optional[bool], optional): Whether the audio file is mono. Defaults to None.
        feats (Optional[NdArray], optional): Features of the audio file. Defaults to None.
        duration (Optional[float], optional): Duration of the audio file. Defaults to None.
        segments (Union[Iterable[List], List], optional): Segments of the audio file. Defaults to None.
        pipeline (List[str], optional): List of processing steps. Defaults to [].
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="ignore"
    )

    url: Optional[Union[str, Path]] = Field(None, title="URL of the audio file.")
    sample_rate: Optional[int] = Field(None, title="Sample rate of the audio file.")
    waveform: NdArray | Tensor | None = Field(None, title="Waveform of the audio file.")
    channels: Optional[AudioChannelList[AudioChannel]] = Field(
        None, title="Channels of the audio file."
    )
    mono: Optional[bool] = Field(None, title="Whether the audio file is mono.")
    duration: Optional[float] = Field(None, title="Duration of the audio file.")
    pipeline: Optional[List[str]] = Field(None, title="List of processing steps.")
    language: Optional[str] = Field(None, title="Language of the audio file.")
    emotion: Optional[str] = Field(None, title="Emotion of the audio file.")
    type: Optional[str] = Field(None, title="Type of the audio file.")
    is_bad: Optional[bool] = Field(False, title="Whether the audio file is bad.")
    is_last: Optional[bool] = Field(False, title="Whether the audio file is the last.")
    bad_reason: Optional[Union[str, Exception]] = Field(
        None, title="Reason why the audio file is bad."
    )
    bad_component: Optional[str] = Field(
        None, title="Component that marked the audio bad."
    )
    spent_time: Dict[str, float] = Field(
        None, title="Time spent on processing the audio."
    )

    def load(self, mono: bool = False) -> "Audio":
        """Load the audio file from the URL."""
        try:
            if Path(self.url).exists():
                self.waveform, self.sample_rate = librosa.load(
                    self.url, sr=self.sample_rate, mono=mono
                )
            else:
                bytes_ = requests.get(self.url).content
                self.waveform, self.sample_rate = librosa.load(
                    BytesIO(bytes_), sr=self.sample_rate, mono=mono
                )
            self.duration = librosa.get_duration(y=self.waveform, sr=self.sample_rate)
        except Exception:
            raise ValueError(f"Failed to load audio from {self.url}.")
        if len(self.waveform.shape) == 1:
            self.mono = True
            self.channels = AudioChannelList[AudioChannel](
                [
                    AudioChannel(
                        id=self.id,
                        waveform=self.waveform,
                        sample_rate=self.sample_rate,
                        segments=[
                            AudioSpan(
                                start_ms=0,
                                end_ms=self.duration_ms,
                                waveform=self.waveform,
                                sample_rate=self.sample_rate,
                                is_last=True,
                            )
                        ],
                    )
                ]
            )

        else:
            self.mono = False
            self.channels = AudioChannelList[AudioChannel](
                [
                    AudioChannel(
                        id=self.id,
                        waveform=channel_waveform,
                        sample_rate=self.sample_rate,
                        segments=[
                            AudioSpan(
                                start_ms=0,
                                end_ms=self.duration_ms,
                                waveform=channel_waveform,
                                sample_rate=self.sample_rate,
                                is_last=True,
                            )
                        ],
                    )
                    for channel_waveform in self.waveform
                ]
            )
        return self

    def from_bytes(self, data: ByteString) -> "Audio":
        """Load the audio file from bytes.

        Args:
            data (ByteString): Bytes of the audio file.

        Returns:
            Audio: Audio object.
        """
        arr, sr = librosa.load(BytesIO(data), sr=self.sample_rate, mono=self.mono)
        self.waveform = arr
        self.sample_rate = sr
        if len(arr.shape) == 1:
            self.mono = True
            self.channels = AudioChannelList[AudioChannel](
                [
                    AudioChannel(
                        id=self.id,
                        waveform=self.waveform,
                        sample_rate=self.sample_rate,
                        segments=[
                            AudioSpan(
                                start_ms=0,
                                end_ms=self.duration_ms,
                                waveform=self.waveform,
                                sample_rate=self.sample_rate,
                                is_last=True,
                            )
                        ],
                    )
                ]
            )
        else:
            self.mono = False
            self.channels = AudioChannelList[AudioChannel](
                [
                    AudioChannel(
                        id=self.id,
                        waveform=channel_waveform,
                        sample_rate=self.sample_rate,
                        segments=[
                            AudioSpan(
                                start_ms=0,
                                end_ms=self.duration_ms,
                                waveform=channel_waveform,
                                sample_rate=self.sample_rate,
                                is_last=True,
                            )
                        ],
                    )
                    for channel_waveform in self.waveform
                ]
            )

        self.duration = librosa.get_duration(y=self.waveform, sr=self.sample_rate)
        return self

    def resample(self, sample_rate: int) -> "Audio":
        """Resample the audio file to the target sample rate.

        Args:
            sample_rate (int): Target sample rate.
        """
        self.sample_rate = sample_rate
        if self.waveform is not None:
            self.waveform = librosa.resample(
                self.waveform, orig_sr=self.sample_rate, target_sr=sample_rate
            )
        if self.channels is not None:
            self.resample_channel(sample_rate)
        return self

    def resample_channel(self, sample_rate: int) -> "Audio":
        """Resample the audio channel waveform to the target sample rate.

        Args:
            sample_rate (int): Target sample rate.
        """
        if self.waveform is None:
            logger.warning(
                f"Audio {self.id} resample failed because it has no waveform."
            )
            return self
        for channel in self.channels:
            channel.waveform = librosa.resample(
                channel.waveform, orig_sr=self.sample_rate, target_sr=sample_rate
            )
            channel.sample_rate = sample_rate
        return self

    def append_channel(self, waveform: NdArray, sample_rate: int) -> "Audio":
        """Append a channel to the audio file.

        Args:
            waveform (NdArray): Waveform of the channel.
            sample_rate (int): Sample rate of the channel.
        """
        if self.channels is None:
            self.channels = AudioChannelList[AudioChannel]()
        self.channels.append(
            AudioChannel(
                id=self.id,
                waveform=waveform,
                sample_rate=sample_rate,
                segments=[
                    AudioSpan(
                        start_ms=0,
                        end_ms=self.duration_ms,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        is_last=True,
                    )
                ],
            )
        )
        return self

    def align_channel_bad(self):
        """Align the bad status of the audio file with its channels."""
        if self.channels is None:
            return
        for channel in self.channels:
            if channel.is_bad:
                self.is_bad = True
                self.bad_reason = channel.bad_reason
                self.bad_component = channel.bad_component
                break

    def align_segment_bad(self):
        """Align the bad status of the audio file with its channels."""
        if self.channels is None:
            return
        for channel in self.channels:
            for span in channel.segments:
                if span.is_bad:
                    self.is_bad = True
                    self.bad_reason = span.bad_reason
                    self.bad_component = span.bad_component
                    break

    def clear(self):
        self.waveform = None
        if self.channels is None:
            return
        for channel in self.channels:
            channel.waveform = None
            channel.feats = None
            channel.steps = None
            if channel.segments:
                for span in channel.segments:
                    span.waveform = None
                    span.feats = None
                    span.scores = None

    def chunk(self, chunk_size_ms: int) -> "AudioList['Audio']":
        """Chunk the audio file into smaller chunks.
        Args:
            chunk_size_ms (int): Size of the chunk in milliseconds.
        Returns:
            AudioList: Chunked audio list.
        """
        chunked_audios = AudioList()
        chunk_stride = self.sample_rate / 1000 * chunk_size_ms
        num_chunks = num_chunks = int(np.ceil(self.duration_ms / chunk_size_ms))
        if self.duration_ms > chunk_size_ms:
            for i in range(num_chunks):
                start = int(i * chunk_stride)
                end = int((i + 1) * chunk_stride)
                if end > len(self.waveform):
                    end = len(self.waveform)
                chunk_waveform = self.waveform[start:end]
                chunk_audio = Audio(
                    id=self.id,
                    url=self.url,
                    sample_rate=self.sample_rate,
                    waveform=chunk_waveform,
                    duration=librosa.get_duration(
                        y=chunk_waveform, sr=self.sample_rate
                    ),
                )
                chunked_audios.append(chunk_audio)
        else:
            chunked_audios.append(self)
        return chunked_audios

    def display(self, channel_idx: int = 0):
        """Display the audio file."""
        from IPython.display import Audio as IPAudio

        return IPAudio(
            self.channels[channel_idx].waveform,
            rate=self.channels[channel_idx].sample_rate,
        )

    @property
    def is_loaded(self):
        if self.url is None:
            return False
        if self.waveform is None:
            return False
        if self.sample_rate is None:
            return False
        if self.channels is None:
            return False
        for channel in self.channels:
            if channel.waveform is None:
                return False
        return True

    @property
    def duration_ms(self):
        """Get the duration of the audio file in milliseconds."""
        if self.duration is None:
            return None
        return self.duration * 1000

    def __getitem__(self, key) -> Optional[AudioChannel]:
        if self.channels is None:
            return None
        return self.channels[key]

    def __len__(self) -> int:
        if self.channels is None:
            return 0
        return len(self.channels)


class AudioList(DocList):
    def load_stream(self, num_workers: int = 2) -> Iterable[Audio]:
        """Load all the audio files in parallel.

        Args:
            num_workers (int, optional): Number of workers to use. Defaults to -1. If -1, use all available cores.
        """
        if len(self) == 0:
            return
        if num_workers == -1:
            num_workers = get_cpu_cores()
        batch_size = max(len(self) // num_workers, 1)
        res = Parallel(
            n_jobs=num_workers,
            prefer="threads",
            batch_size=batch_size,
            return_as="generator_unordered",
            pre_dispatch="4 * n_jobs",
        )(delayed(doc.load)() for doc in self)
        return res

    def load(self, num_workers: int = 2):
        """Load all the audio files in parallel.

        Args:
            num_workers (int, optional): Number of workers to use. Defaults to -1. If -1, use all available cores.
        """
        if len(self) == 0:
            return
        if num_workers == -1:
            num_workers = get_cpu_cores()
        batch_size = max(len(self) // num_workers, 1)
        _ = Parallel(n_jobs=num_workers, prefer="threads", batch_size=batch_size)(
            delayed(doc.load)() for doc in self
        )
        return self

    @classmethod
    def from_urls(
        cls, urls: Union[str, List[str]], load: bool = False, num_workers: int = 2
    ):
        """Create an AudioList from a list of URLs.

        Args:
            urls (List[str]): List of URLs.
            load (bool, optional): Whether to load the audio files. Defaults to False.
            num_workers (int, optional): Number of workers to use. Defaults to -1. If -1, use all available cores.

        Returns:
            AudioList: List of Audio objects.
        """
        if isinstance(urls, str):
            urls = [urls]
        audios = cls([Audio(url=url) for url in urls])
        if load:
            audios = audios.load(num_workers=num_workers)
        return audios

    def resample_channel(self, sample_rate: int, num_workers: int = 2):
        """Resample all the audio files in parallel.

        Args:
            sample_rate (int): Target sample rate.
            num_workers (int, optional): Number of workers to use. Defaults to -1. If -1, use all available cores.
        """
        if num_workers == -1:
            num_workers = get_cpu_cores()
        batch_size = max(len(self) // num_workers, 1)
        _ = Parallel(n_jobs=num_workers, prefer="threads", batch_size=batch_size)(
            delayed(doc.resample_channel)(sample_rate) for doc in self
        )
        return self

    def filter_audio_id(self, ids: List[str], op: str = "$in") -> Optional["AudioList"]:
        """Filter the audio files by their IDs.
        Args:
            ids (List[str]): List of audio IDs.
            op (str, optional): Operator to use. Defaults to "$in". Can be "$in", "$nin"

        Returns:
            Optional[AudioList]: Filtered audio files.
        """
        query = {"id": {op: ids}}
        audios: AudioList[Audio] = AudioList[Audio](filter_docs(self, query=query))
        return audios

    def filter_urls(self, urls: List[str], op: str = "$in") -> Optional["AudioList"]:
        """Filter the audio files by their URLs.
        Args:
            urls (List[str]): List of audio URLs.
            op (str, optional): Operator to use. Defaults to "$in". Can be "$in", "$nin"

        Returns:
            Optional[AudioList]: Filtered audio files.
        """
        query = {"url": {op: urls}}
        audios: AudioList = filter_docs(self, query=query)
        if len(audios) == 0:
            return None
        return audios

    def analysis_timer(self):
        """Print the time spent on processing the audio files."""
        component_spent = {}
        for audio in self:
            for component, spent in audio.spent_time.items():
                if component not in component_spent:
                    component_spent[component] = 0
                component_spent[component] += spent
        total_spent = sum(component_spent.values())
        print("Total spent time: ", round(total_spent, 2))
        for component, spent in component_spent.items():
            print(f"{component}: {spent:.2f}s, {spent / total_spent:.2%}")

    def clear(self) -> None:
        """Clear the waveform, features, and scores of all the audio files. should be called after processing. this method is used to save memory."""
        for audio in self:
            audio.clear()

    def has_bad_audio(self) -> bool:
        """Check if there is bad audio in the list"""
        ids = [audio.id for audio in self if audio.is_bad]
        return len(ids) > 0

    @property
    def duration_s(self):
        """Get the total duration of all the audio files in seconds."""
        durations = []
        for i in range(len(self)):
            audio: Audio = self[i]
            if audio.duration is not None:
                durations.append(audio.duration)
        return round(sum(durations), 2)

    @property
    def duration_ms(self):
        """Get the total duration of all the audio files in milliseconds."""
        durations = []
        for audio in self:
            if audio.duration_ms is not None:
                durations.append(audio.duration_ms)
        return round(sum(durations), 2)

    @property
    def channels(self):
        """Get all the channels of the audio files."""
        channels = []
        for audio in self:
            if audio.channels is not None:
                channels.extend(audio.channels)
        return channels

    @property
    def bad_audios(self) -> "AudioList":
        """Get the bad audios in the list"""
        return AudioList([audio for audio in self if audio.is_bad])

    @property
    def good_audios(self) -> "AudioList":
        """Get the good audios in the list"""
        return AudioList([audio for audio in self if not audio.is_bad])

    def __sub__(self, other: "AudioList") -> "AudioList":
        """Get the difference between two AudioList objects."""
        other_ids = [audio.id for audio in other]
        return self.filter_audio_id(other_ids, op="$nin")

    def __str__(self) -> str:
        num_bad_audios = sum([audio.is_bad for audio in self])
        return f"AudioList with {len(self)} audios, {num_bad_audios} bad audios."

    def __repr__(self) -> str:
        return self.__str__()


class AudioQueue(Queue):
    """Create a queue object with a given audio duration limit.

    item in the queue is a tuple of (Audio, Queue).
    """

    def _qsize(self) -> int | bool:
        if len(self.queue) == 0:
            return False  # line 139 Queue._get: while self._qsize() >= self.maxsize: this will be False
        durations = []
        for item in self.queue:
            audio, queue = item
            audio: Audio
            if audio.duration is not None:
                durations.append(audio.duration)
        qsize = round(sum(durations), 2)
        if qsize == 0:
            qsize = 1  # though the audio duration is 0, the queue is not empty, if the queue is empty, will raise Empty
        return qsize


@lru_cache
def get_cpu_cores():
    return os.cpu_count()
