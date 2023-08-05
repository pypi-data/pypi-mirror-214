import sys
import unittest
from unittest.mock import patch, Mock

from src.distrunner.distrunner import DistRunner


class TestDistRunner(unittest.TestCase):
    def setUp(self):
        sys.path.append("../../")
        sys.path.append("../src")

    @patch("dask.distributed.LocalCluster")
    def test_init_local(self, mock_localcluster):
        dr = DistRunner(local=True)
        with dr as dr_cm:
            self.assertEqual(dr_cm._workers, 3)
            self.assertEqual(dr_cm._worker_memory, "16Gb")
            self.assertEqual(dr_cm._worker_cpus, 2)
            self.assertEqual(dr_cm._local, True)
            self.assertEqual(dr_cm._region, "eu-west-2")
        mock_localcluster.assert_called_once_with(n_workers=3)

    @patch("coiled.Cluster")
    @patch("claws.aws_utils.AWSConnector")
    def test_init_not_local(self, mock_awsconnector, mock_coiledcluster):
        mock_awsconnector.return_value.get_secret.return_value = (
            '{"coiled-api-key": "api-key"}'
        )
        mock_cluster = Mock()
        mock_coiledcluster.return_value = mock_cluster
        dr = DistRunner(local=False)
        with dr as dr_cm:
            self.assertEqual(dr_cm._workers, 3)
            self.assertEqual(dr_cm._worker_memory, "16Gb")
            self.assertEqual(dr_cm._worker_cpus, 2)
            self.assertEqual(dr_cm._local, False)
            self.assertEqual(dr_cm._region, "eu-west-2")
        mock_coiledcluster.assert_called_once()

    @patch("dask.distributed.LocalCluster")
    def test_exit_local(self, mock_localcluster):
        dr = DistRunner(local=True)
        with dr as dr_cm:
            mock_client = Mock()
            dr_cm._client = mock_client
            mock_cluster = Mock()
            dr_cm._cluster = mock_cluster
        mock_client.close.assert_called_once()
        mock_cluster.close.assert_called_once()

    @patch("coiled.Cluster")
    @patch("claws.aws_utils.AWSConnector")
    def test_exit_not_local(self, mock_awsconnector, mock_coiledcluster):
        mock_awsconnector.return_value.get_secret.return_value = (
            '{"coiled-api-key": "api-key"}'
        )
        mock_cluster = Mock()
        mock_coiledcluster.return_value = mock_cluster
        dr = DistRunner(local=False)
        with dr as dr_cm:
            mock_client = Mock()
            dr_cm._client = mock_client
        mock_client.close.assert_called_once()
        mock_cluster.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
