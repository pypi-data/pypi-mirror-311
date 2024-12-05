from pydantic import BaseModel, Field
from fasr.config import Config
from abc import ABC, abstractmethod
from pathlib import Path
from .prepare_model import download


class SerializableMixin(BaseModel, ABC):
    @abstractmethod
    def save(self, save_dir: str):
        raise NotImplementedError

    @abstractmethod
    def load(self, save_dir: str):
        raise NotImplementedError

    @abstractmethod
    def get_config(self) -> Config:
        raise NotImplementedError


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "fasr" / "checkpoints"  # 默认缓存目录


class ModelScopeMixin(BaseModel, ABC):
    cache_dir: str | Path = Field(default=DEFAULT_CACHE_DIR, description="默认缓存目录")
    checkpoint: str | None = Field(default=None, description="模型名称")

    @abstractmethod
    def from_checkpoint(cls, checkpoint_dir: str, **kwargs):
        raise NotImplementedError

    def download_checkpoint(self, checkpoint: str, revision: str = None):
        if not self.chekcpoint_dir:
            self.chekcpoint_dir = self.cache_dir / checkpoint
        download(model=checkpoint, revision=revision, cache_dir=self.chekcpoint_dir)
