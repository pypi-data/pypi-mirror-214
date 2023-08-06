import abc
import enum
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import requests
from pydantic import BaseModel
from requests import Response


class WandCoreClient:
    def __init__(self, token: str, base_url: str) -> None:
        self._token = token
        self._base_url = base_url

    def request(
        self, method: str, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Response:
        resp = requests.request(
            method=method,
            url=self._base_url + path,
            headers={"Authorization": f"Bearer {self._token}"},
            json=json,
        )
        resp.raise_for_status()
        return resp


class Source(BaseModel):
    id: str


class FileSourceCreationResult(BaseModel):
    source: Source
    upload_url: str


class Sources:
    def __init__(self, core: WandCoreClient) -> None:
        self._core = core

    def create_web(
        self,
        urls: List[str],
        max_crawl_pages: int = 20,
    ) -> Source:
        res = self._core.request(
            method="post",
            path="/source/web_scraper",
            json={
                "urls": urls,
                "max_crawl_pages": max_crawl_pages,
            },
        ).json()
        return Source(id=res["source_id"])

    def create_file(self, filename: str) -> FileSourceCreationResult:
        res = self._core.request(
            method="post",
            path="/source/file",
            json={
                "filename": filename,
            },
        ).json()
        return FileSourceCreationResult(
            source=Source(id=res["source_id"]), upload_url=res["upload_signed_url"]
        )

    def create_from_filepath(self, filepath: Union[str, Path]) -> Source:
        path = Path(filepath)
        res = self.create_file(path.name)
        with path.open("rb") as file:
            requests.put(res.upload_url, data=file)
        return res.source

    def create_from_file_data(self, filename: str, data: bytes) -> Source:
        res = self.create_file(filename)
        requests.put(res.upload_url, data=data)
        return res.source


class ModelStatus(BaseModel):
    progress: int
    training_completed: bool


class Model(BaseModel):
    id: str
    source_ids: List[str]
    status: ModelStatus


class Training(BaseModel):
    id: str
    model_id: str
    status: ModelStatus


class ChatMessageAuthor(str, enum.Enum):
    AI = "ai"
    HUMAN = "human"


class ChatMessage(BaseModel):
    author: ChatMessageAuthor
    message: str


class TrainingListener(abc.ABC):
    @abc.abstractmethod
    def on_progress(self, model: Model) -> None:
        pass


class ReTrainingListener(abc.ABC):
    @abc.abstractmethod
    def on_progress(self, training: Training) -> None:
        pass


def _parse_training_payload(payload: Mapping[str, Any]) -> Training:
    return Training(
        id=payload["train_id"],
        model_id=payload["model_id"],
        status=ModelStatus(
            progress=payload["status"]["progress"],
            training_completed=payload["status"]["training_completed"],
        ),
    )


class Trainings:
    def __init__(self, core: WandCoreClient) -> None:
        self._core = core

    def get(self, training_id: str) -> Training:
        res = self._core.request(
            method="GET",
            path=f"/trainings/{training_id}",
        ).json()
        return _parse_training_payload(res)

    def list_all(self) -> List[Training]:
        res = self._core.request(
            method="GET",
            path=f"/trainings",
        ).json()
        return [_parse_training_payload(it) for it in res]


class Models:
    def __init__(self, core: WandCoreClient, trainings: Trainings) -> None:
        self._core = core
        self._trainings = trainings

    def _parse_model_payload(self, payload: Mapping[str, Any]) -> Model:
        return Model(
            id=payload["model_id"],
            source_ids=payload["source_ids"],
            status=ModelStatus(
                progress=payload["status"]["progress"],
                training_completed=payload["status"]["training_completed"],
            ),
        )

    def start_training(self, source_ids: List[str]) -> Model:
        res = self._core.request(
            method="post",
            path="/models",
            json={
                "source_ids": source_ids,
            },
        ).json()
        return self._parse_model_payload(res)

    def start_retraining(self, model_id: str) -> Training:
        res = self._core.request(
            method="POST",
            path=f"/models/{model_id}/train",
            json={},
        ).json()
        return _parse_training_payload(res)

    def get(self, model_id: str) -> Model:
        res = self._core.request(
            method="GET",
            path=f"/models/{model_id}",
        ).json()
        return self._parse_model_payload(res)

    def delete(self, model_id: str) -> None:
        self._core.request(
            method="DELETE",
            path=f"/models/{model_id}",
        ).json()

    def list_all(self) -> List[Model]:
        res = self._core.request(
            method="GET",
            path=f"/models",
        ).json()
        return [self._parse_model_payload(it) for it in res]

    def infer(
        self, model_id: str, prompt: str, chat_history: Sequence[ChatMessage]
    ) -> str:
        res = self._core.request(
            method="post",
            path=f"/models/{model_id}/infer",
            json={
                "prompt": prompt,
                "chat_history": [
                    {
                        "author": it.author,
                        "message": it.message,
                    }
                    for it in chat_history
                ],
            },
        )
        return res.text

    def train(
        self, source_ids: List[str], listener: Optional[TrainingListener] = None
    ) -> Model:
        model = self.start_training(source_ids)
        while True:
            model = self.get(model.id)
            if listener:
                listener.on_progress(model)
            if model.status.training_completed:
                return model
            time.sleep(1)

    def retrain(
        self, model_id: str, listener: Optional[ReTrainingListener] = None
    ) -> Training:
        training = self.start_retraining(model_id)
        while True:
            training = self._trainings.get(training.id)
            if listener:
                listener.on_progress(training)
            if training.status.training_completed:
                return training
            time.sleep(1)

    def start_chat(self, model_id: str) -> "ChatSession":
        return ChatSession(model_id, self)


class ChatSession:
    def __init__(self, model_id: str, client: Models) -> None:
        self._model_id = model_id
        self._client = client
        self._chat_history: List[ChatMessage] = []

    def ask(self, prompt: str) -> str:
        resp = self._client.infer(self._model_id, prompt, self._chat_history)
        self._chat_history.append(
            ChatMessage(author=ChatMessageAuthor.HUMAN, message=prompt)
        )
        self._chat_history.append(
            ChatMessage(author=ChatMessageAuthor.AI, message=resp)
        )
        return resp


class WandClient:
    def __init__(
        self,
        token: str,
        base_url: str,
    ):
        core = WandCoreClient(token=token, base_url=base_url)
        self.source = Sources(core)
        self.trainings = Trainings(core)
        self.models = Models(core, self.trainings)
