import io
import json
import os
from dataclasses import dataclass
from typing import Any, List

from huggingface_hub import HfApi, create_repo

from autotrain import logger


@dataclass
class DreamboothPreprocessor:
    """
    DreamboothPreprocessor is a class responsible for preparing concept images and prompts data for DreamBooth Task.

    Attributes:
        concept_images (List[Any]): A list of concept images to be processed.
        concept_name (str): The name of the concept.
        username (str): The username of the person creating the project.
        project_name (str): The name of the project.
        token (str): The authentication token for accessing the repository.
        local (bool): A flag indicating whether the processing is local or remote.

    Methods:
        __post_init__(): Initializes the repository name and creates a remote repository if not local.
        _upload_concept_images(file, api): Uploads a concept image to the remote repository.
        _upload_concept_prompts(api): Uploads the concept prompts to the remote repository.
        _save_concept_images(file): Saves a concept image locally.
        _save_concept_prompts(): Saves the concept prompts locally.
        prepare(): Prepares the concept images and prompts by either saving them locally or uploading them to a remote repository.
    """

    concept_images: List[Any]
    concept_name: str
    username: str
    project_name: str
    token: str
    local: bool

    def __post_init__(self):
        self.repo_name = f"{self.username}/autotrain-data-{self.project_name}"
        if not self.local:
            try:
                create_repo(
                    repo_id=self.repo_name,
                    repo_type="dataset",
                    token=self.token,
                    private=True,
                    exist_ok=False,
                )
            except Exception:
                logger.error("Error creating repo")
                raise ValueError("Error creating repo")

    def _upload_concept_images(self, file, api):
        logger.info(f"Uploading {file} to concept1")
        if isinstance(file, str):
            path_in_repo = f"concept1/{file.split('/')[-1]}"
        else:
            path_in_repo = f"concept1/{file.filename.split('/')[-1]}"

        api.upload_file(
            path_or_fileobj=file if isinstance(file, str) else file.file.read(),
            path_in_repo=path_in_repo,
            repo_id=self.repo_name,
            repo_type="dataset",
            token=self.token,
        )

    def _upload_concept_prompts(self, api):
        _prompts = {}
        _prompts["concept1"] = self.concept_name

        prompts = json.dumps(_prompts)
        prompts = prompts.encode("utf-8")
        prompts = io.BytesIO(prompts)
        api.upload_file(
            path_or_fileobj=prompts,
            path_in_repo="prompts.json",
            repo_id=self.repo_name,
            repo_type="dataset",
            token=self.token,
        )

    def _save_concept_images(self, file):
        logger.info("Saving concept images")
        logger.info(file)
        if isinstance(file, str):
            _file = file
            path = f"{self.project_name}/autotrain-data/concept1/{_file.split('/')[-1]}"

        else:
            _file = file.file.read()
            path = f"{self.project_name}/autotrain-data/concept1/{file.filename.split('/')[-1]}"

        os.makedirs(os.path.dirname(path), exist_ok=True)
        # if file is a string, copy the file to the new location
        if isinstance(file, str):
            with open(_file, "rb") as f:
                with open(path, "wb") as f2:
                    f2.write(f.read())
        else:
            with open(path, "wb") as f:
                f.write(_file)

    def _save_concept_prompts(self):
        _prompts = {}
        _prompts["concept1"] = self.concept_name
        path = f"{self.project_name}/autotrain-data/prompts.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(_prompts, f)

    def prepare(self):
        api = HfApi(token=self.token)
        for _file in self.concept_images:
            if self.local:
                self._save_concept_images(_file)
            else:
                self._upload_concept_images(_file, api)

        if self.local:
            self._save_concept_prompts()
        else:
            self._upload_concept_prompts(api)

        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"
