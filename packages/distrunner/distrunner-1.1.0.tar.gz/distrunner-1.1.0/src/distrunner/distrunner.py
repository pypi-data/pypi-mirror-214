import json
import logging
import pathlib
import tempfile
import uuid
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Type

from claws import aws_utils


class DistRunner(AbstractContextManager):
    """
    Context manager for running distributed tasks.
    """

    def __exit__(
        self,
        __exc_type: Type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        """
        Closes the dask cluster and client
        :param __exc_type: an exception type
        :param __exc_value: an exception value
        :param __traceback: the traceback
        :return: Bool if successful or None
        """
        if self._client:
            self._client.close()

        if self._cluster:
            self._cluster.close()

        if self._config_created:
            self._config_file.unlink(missing_ok=True)

        if __exc_value:
            logging.error(__exc_value)
            logging.error(__traceback)
            raise __exc_value

        return True

    def __enter__(self) -> "DistRunner":
        """
        Enters the context manager
        :return: the DistRunner instance
        """
        if self._local:
            import dask.distributed

            self._cluster = dask.distributed.LocalCluster(
                n_workers=self._workers,
            )
        else:
            # write a config file
            self._write_config(
                account=self._coiled_account,
                token=self._api_key_secret_name,
                user=self._coiled_user,
            )

            # we don't import coiled until this point because it loads
            # the config file on import
            import coiled

            if self._requirements:
                env = coiled.create_software_environment(pip=self._requirements)

                self._cluster = coiled.Cluster(
                    name=f"distrunner-{uuid.uuid4()}",
                    n_workers=self._workers,
                    worker_memory=self._worker_memory,
                    worker_cpu=self._worker_cpus,
                    software=env,
                )
            else:
                self._cluster = coiled.Cluster(
                    name=f"distrunner-{uuid.uuid4()}",
                    n_workers=self._workers,
                    worker_memory=self._worker_memory,
                    worker_cpu=self._worker_cpus,
                )

        return self

    def _write_config(self, account, token, user):
        if self._config_file.exists():
            return

        self._config_created = True

        self._config_file.parent.mkdir(parents=True, exist_ok=True)

        aws_connector = aws_utils.AWSConnector(
            region_name=self._region, unsigned=False
        )
        token_data = json.loads(aws_connector.get_secret(token))

        config_data = (
            "coiled:\n"
            f"  account: {account}\n"
            "  server: https://cloud.coiled.io\n"
            f"  token: {token_data['coiled-api-key']}\n"
            f"  user: {user}\n"
        )

        with self._config_file.open("w") as f:
            f.write(config_data)

    def __init__(
        self,
        workers: int = 3,
        worker_memory: str = "16Gb",  # memory in MB
        worker_cpus: int = 2,
        local: bool = False,
        region: str = "eu-west-2",
        api_key_secret_name: str = "LabsAPI/coiled-api-key",
        coiled_account: str = "martin-eve",
        coiled_user: str = "martin-eve",
        requirements: list = None,
    ):
        """
        Initialize a Dask cluster with the specified number of workers.
        :param workers: the number of workers required
        :param worker_memory: the memory in MB to use for workers
        :param worker_cpus: the CPU in milli-cpu (1/1024) to use for workers
        :param local: whether to run the cluster locally
        """
        super().__init__()
        self._workers = workers
        self._worker_memory = worker_memory
        self._worker_cpus = worker_cpus
        self._local = local
        self._region = region
        self._api_key_secret_name = api_key_secret_name
        self._coiled_account = coiled_account
        self._coiled_user = coiled_user
        self._requirements = requirements

        # create the temporary storage directory
        self._temp_dir = tempfile.TemporaryDirectory()

        # internal variables
        self._config_file = pathlib.Path(
            pathlib.Path.home() / ".config" / "dask" / "coiled.yaml"
        )
        self._config_created = False
        self._cluster = None
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = self._cluster.get_client()

        return self._client
