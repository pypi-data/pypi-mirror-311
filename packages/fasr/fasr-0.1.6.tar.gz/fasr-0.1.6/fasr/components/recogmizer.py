from .base import BaseComponent
from fasr.data.audio import (
    AudioList,
    Audio,
    AudioSpanList,
    AudioSpan,
    AudioToken,
    AudioTokenList,
)
from fasr.config import registry
from funasr import AutoModel
from typing import List, Iterable
from joblib import Parallel, delayed
import re
from pathlib import Path


@registry.components.register("recognizer")
@registry.components.register("recognizer.paraformer")
class ParaformerSpeechRecognizer(BaseComponent):
    name: str = "recognizer"
    input_tags: List[str] = ["channel.segments"]
    output_tags: List[str] = ["segment.tokens"]

    model: AutoModel | None = None
    num_threads: int = 1
    batch_size_s: int = 100

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        _ = Parallel(
            n_jobs=self.num_threads, prefer="threads", pre_dispatch="1 * n_jobs"
        )(
            delayed(self.predict_step)(batch_segments)
            for batch_segments in self.batch_audio_segments(audios=audios)
        )
        return audios

    def sort_audio_segments(self, audios: AudioList[Audio]) -> List[AudioSpan]:
        all_segments = []
        for audio in audios:
            if not audio.is_bad and not audio.channels:
                for channel in audio.channels:
                    for seg in channel.segments:
                        all_segments.append(seg)
        sorted_segments = sorted(all_segments, key=lambda x: x.duration_ms)
        return sorted_segments

    def batch_audio_segments(
        self, audios: AudioList[Audio]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。
        步骤：
        - 1. 将音频片段按照时长排序。
        - 2. 将音频片段按照时长分组，每组时长不超过batch_size_s。
        """
        all_segments = []
        for audio in audios:
            if not audio.is_bad:
                for channel in audio.channels:
                    if channel.segments is None:
                        segments = [
                            AudioSpan(
                                start_ms=0,
                                end_ms=channel.duration_ms,
                                waveform=channel.waveform,
                                sample_rate=channel.sample_rate,
                                is_last=True,
                            )
                        ]
                        channel.segments = segments
                    for seg in channel.segments:
                        all_segments.append(seg)
        return self.batch_segments(all_segments)

    def predict_step(self, batch_segments: List[AudioSpan]) -> List[AudioSpan]:
        batch_waveforms = [seg.waveform for seg in batch_segments]
        fs = batch_segments[0].sample_rate  # 一个batch的音频片段采样率相同
        batch_results = self.model.generate(input=batch_waveforms, fs=fs)
        for seg, result in zip(batch_segments, batch_results):
            seg.waveform = None  # 释放内存
            tokens = []
            result_text = result["text"]
            if result_text:
                texts = result["text"].split(" ")
            else:
                texts = []
            timestamps = result["timestamp"]
            assert len(texts) == len(timestamps), f"{texts} {timestamps}"
            for token_text, timestamp in zip(texts, timestamps):
                if seg.start_ms is not None and seg.end_ms is not None:
                    start_ms = seg.start_ms + timestamp[0]
                    end_ms = seg.start_ms + timestamp[1]
                else:
                    start_ms = timestamp[0]
                    end_ms = timestamp[1]
                token = AudioToken(start_ms=start_ms, end_ms=end_ms, text=token_text)
                assert token.end_ms - token.start_ms > 0, f"{token}"
                tokens.append(token)
            seg.tokens = AudioTokenList(docs=tokens)
        return batch_segments

    def batch_segments(
        self, segments: Iterable[AudioSpan]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。"""
        self.model.kwargs["batch_size"] = self.batch_size_s * 1000
        batch_size_ms = self.batch_size_s * 1000
        segments = [seg for seg in segments]
        sorted_segments = self.sort_segments(segments)
        batch = AudioSpanList[AudioSpan]()
        for seg in sorted_segments:
            max_duration_ms = max(batch.max_duration_ms, seg.duration_ms)
            current_batch_duration_ms = max_duration_ms * len(batch)
            if current_batch_duration_ms > batch_size_ms:
                yield batch
                batch = AudioSpanList[AudioSpan]()
                batch.append(seg)
            else:
                batch.append(seg)
        if len(batch) > 0:
            yield batch

    def sort_segments(self, segments: List[AudioSpan]) -> List[AudioSpan]:
        return sorted(segments, key=lambda x: x.duration_ms)

    def from_checkpoint(
        self,
        checkpoint_dir: str = "checkpoints/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        batch_size_s: int = 100,
        num_threads: int = 1,
        **kwargs,
    ) -> "ParaformerSpeechRecognizer":
        checkpoint_dir = Path(checkpoint_dir)
        assert checkpoint_dir.exists(), f"{checkpoint_dir} not exists, please run `fasr prepare` to download the paraformer model."
        model = AutoModel(model=checkpoint_dir, disable_update=True, **kwargs)
        model.kwargs["batch_size"] = batch_size_s * 1000
        self.model = model
        self.num_threads = num_threads
        self.batch_size_s = batch_size_s
        return self

    def to_segment_stream(self, segments: AudioSpanList) -> Iterable[AudioSpan]:
        for seg in segments:
            yield from seg


@registry.components.register("recognizer.sensevoice")
class SensevoiceSpeechRecognizer(BaseComponent):
    model: AutoModel = None
    num_threads: int = 1
    batch_size_s: int = 100
    name: str = "recognizer"
    input_tags: List[str] = ["channels"]
    output_tags: List[str] = ["language", "emotion", "type", "channels.text"]

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        _ = Parallel(
            n_jobs=self.num_threads, prefer="threads", pre_dispatch="1 * n_jobs"
        )(
            delayed(self.predict_step)(batch_segments)
            for batch_segments in self.batch_audio_segments(audios=audios)
        )
        return audios

    def sort_audio_segments(self, audios: AudioList[Audio]) -> List[AudioSpan]:
        all_segments = []
        for audio in audios:
            if not audio.is_bad and not audio.channels:
                for channel in audio.channels:
                    for seg in channel.segments:
                        all_segments.append(seg)
        sorted_segments = sorted(all_segments, key=lambda x: x.duration_ms)
        return sorted_segments

    def batch_audio_segments(
        self, audios: AudioList[Audio]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。
        步骤：
        - 1. 将音频片段按照时长排序。
        - 2. 将音频片段按照时长分组，每组时长不超过batch_size_s。
        """
        all_segments = []
        for audio in audios:
            if not audio.is_bad:
                for channel in audio.channels:
                    if channel.segments is None:  # 兼容没有vad模型的情况
                        segments = [
                            AudioSpan(
                                start_ms=0,
                                end_ms=channel.duration_ms,
                                waveform=channel.waveform,
                                sample_rate=channel.sample_rate,
                                is_last=True,
                            )
                        ]
                        channel.segments = segments
                    for seg in channel.segments:
                        all_segments.append(seg)
        return self.batch_segments(all_segments)

    def predict_step(self, batch_segments: List[AudioSpan]) -> List[AudioSpan]:
        batch_waveforms = [seg.waveform for seg in batch_segments]
        fs = batch_segments[0].sample_rate  # 一个batch的音频片段采样率相同
        batch_results = self.model.generate(input=batch_waveforms, fs=fs, use_itn=True)
        for seg, result in zip(batch_segments, batch_results):
            seg.waveform = None  # 释放内存
            pattern = r"<\|(.+?)\|><\|(.+?)\|><\|(.+?)\|><\|(.+?)\|>(.+)"
            match = re.match(pattern, result["text"])
            language, emotion, audio_type, itn, text = match.groups()
            seg.language = language
            seg.emotion = emotion
            seg.type = audio_type
            seg.text = text
        return batch_segments

    def batch_segments(
        self, segments: Iterable[AudioSpan]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。"""
        self.model.kwargs["batch_size"] = self.batch_size_s * 1000
        batch_size_ms = self.batch_size_s * 1000
        segments = [seg for seg in segments]
        sorted_segments = self.sort_segments(segments)
        batch = AudioSpanList[AudioSpan]()
        for seg in sorted_segments:
            max_duration_ms = max(batch.max_duration_ms, seg.duration_ms)
            current_batch_duration_ms = max_duration_ms * len(batch)
            if current_batch_duration_ms > batch_size_ms:
                yield batch
                batch = AudioSpanList[AudioSpan]()
                batch.append(seg)
            else:
                batch.append(seg)
        if len(batch) > 0:
            yield batch

    def sort_segments(self, segments: List[AudioSpan]) -> List[AudioSpan]:
        return sorted(segments, key=lambda x: x.duration_ms)

    def from_checkpoint(
        self,
        checkpoint_dir: str = "checkpoints/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        batch_size_s: int = 100,
        num_threads: int = 1,
        **kwargs,
    ) -> "ParaformerSpeechRecognizer":
        checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(
                f"Checkpoint {checkpoint_dir} not found. if you want to use sensevoice model, please run `fasr prepare` to download the model."
            )
        model = AutoModel(model=checkpoint_dir, disable_update=True, **kwargs)
        model.kwargs["batch_size"] = batch_size_s * 1000
        self.model = model
        self.num_threads = num_threads
        self.batch_size_s = batch_size_s
        return self

    def to_segment_stream(self, segments: AudioSpanList) -> Iterable[AudioSpan]:
        for seg in segments:
            yield from seg
