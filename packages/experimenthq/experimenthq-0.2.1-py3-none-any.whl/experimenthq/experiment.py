import time
from typing import Dict, List, Optional
import queue
import threading
import atexit


import requests

from experimenthq.notion_types import NotionTypes

API_URL = "https://www.api.experiment-hq.com/"
NOTION_BASE_URL = "https://www.notion.so/"

MAX_RETRIES = 3
RETRY_DELAY = 1


class Experiment:
    """
    Experiment class for logging parameters to Notion.

    args:
        api_key (str): API key for the ExperimentHQ API
        project (str): Name of the project to log to
        name (Optional[str]): Name of the experiment
        description (Optional[str]): Description of the experiment
        tags (Optional[List[str]]): List of tags to add to the experiment
    """

    def __init__(
        self,
        api_key: str,
        project: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        self.project = project
        self.api_key = api_key
        self.name = name
        self.description = description
        self.tags = tags
        self.session = requests.Session()

        retry_count = 0
        while True:
            try:
                self.experiment_id = self._start_experiment()
                break
            except Exception as e:
                if retry_count > MAX_RETRIES:
                    raise Exception(f"Failed to start experiment due to {e}")

                time.sleep(RETRY_DELAY)
                retry_count += 1

        self.batch_size = 10
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
        # Register the exit handler after starting the thread
        atexit.register(self._exit_handler)

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    @property
    def timeout(self) -> int:
        # Send data every 10 seconds
        return 10

    def _exit_handler(self) -> None:
        """Stops the worker thread and waits for it to finish."""
        # Put the sentinel task into the queue to tell the thread to stop
        self.queue.put(None)

        # Wait for the worker thread to finish
        self.thread.join()

    def _worker(self) -> None:
        batch_data = []
        while True:
            try:
                task = self.queue.get(timeout=self.timeout)
            except queue.Empty:
                # If the queue is empty after the timeout, send any remaining data
                if batch_data:
                    self._send_batch(batch_data)
                    batch_data = []
                continue

            if task is None:  # We use None as a sentinel to end the thread.
                # Send any remaining data in the batch before ending the thread.
                if batch_data:
                    self._send_batch(batch_data)
                break
            data = task
            batch_data.append((data))

            # If the batch has reached the desired size, send it.
            if len(batch_data) == self.batch_size:
                self._send_batch(batch_data)
                batch_data = []

    def _send_batch(self, batch_data: List) -> None:
        try:
            # Send the batch of data to the API
            # remove the retry_count from the data
            post_data = [
                {
                    "parameter_name": data["parameter_name"],
                    "parameter_value": data["parameter_value"],
                    "notion_type": data["parameter_type"],
                }
                for data in batch_data
            ]
            response = self.session.post(
                f"{API_URL}experiments/{self.experiment_id}/parameters",
                json=post_data,
                headers=self.headers,
            )

            if response.status_code not in {200, 401, 400, 404}:
                return self._requeue_failed_tasks(batch_data)
        finally:
            # Mark all tasks in the batch as done.
            for _ in range(len(batch_data)):
                self.queue.task_done()

    def _requeue_failed_tasks(self, failed_tasks: List[Dict]) -> None:
        for task in failed_tasks:
            if task["retry_count"] < MAX_RETRIES:
                task["retry_count"] += 1
                time.sleep(RETRY_DELAY)
                self.queue.put(task)
            else:
                for data in failed_tasks:
                    print(
                        f"Warning: Failed to log parameter `{data['parameter_name']}` with "
                        f"value: `{data['parameter_value']}`. Please add it manually to the "
                        f"corresponding Notion page: ",
                        "{NOTION_BASE_URL+self.experiment_id.replace('-', '')}.",
                    )

    def _start_experiment(self) -> str:
        post_data = {
            "project": self.project,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
        }
        response = self.session.post(
            f"{API_URL}experiments",
            json=post_data,
            headers=self.headers,
        )
        if response.status_code == 401:
            raise Exception("Invalid API key.")
        elif response.status_code == 403:
            raise Exception(
                "`Max experiments reached, please upgrade your plan by "
                "reaching out to us at notiontracking@gmail.com`"
            )
        elif response.status_code == 404:
            raise Exception("ExperimentHQ database not found.")
        elif response.status_code != 200:
            raise Exception("Failed to start experiment with message: " + response.text)
        elif response.status_code == 408:
            raise Exception("ExperimentHQ API timed out. Experiment not started.")
        return response.json().get("experiment_id")

    def log_parameter(
        self,
        name: str,
        value: str,
        notion_type: Optional[str] = None,
    ) -> None:
        """
        Log a parameter to Notion.

        args:
            name (str): Name of the parameter
            value (str): Value of the parameter. Depending on the type of the parameter,
                         there needs to be a specific format. Please pass several values
                         for multi_select parameters as one string separated by commas.
                         The date needs to be in ISO #8601 format and the people parameter
                         needs to be a Notion ID.
            notion_type Optional(str): Used to create a new column in the Notion database.
                                       Setting `notion_type` is optional and will be ignored
                                        if the column already exists. If the column should be
                                        created with a specific type, the following types are
                                        supported:
                                            - rich_text
                                            - number
                                            - select
                                            - multi_select
                                            - files
                                            - checkbox
                                            - url
                                            - email
                                            - phone_number
                                            - people
                                            - date
        """
        # Check if the value is valid:
        if notion_type is not None:
            NotionTypes(notion_type).validate_value(
                value=value,
                notion_type=notion_type,
            )

        data = {
            "parameter_name": name,
            "parameter_value": value,
            "parameter_type": notion_type,
            "retry_count": 0,
        }

        # Enqueue the task instead of executing it immediately
        self.queue.put(data)
