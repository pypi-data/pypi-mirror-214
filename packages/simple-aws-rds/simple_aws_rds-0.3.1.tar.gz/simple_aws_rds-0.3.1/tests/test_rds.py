# -*- coding: utf-8 -*-

import os
import pytest
import moto
from boto_session_manager import BotoSesManager

from simple_aws_rds.rds import (
    RDSDBInstanceStatusEnum,
    RDSDBInstanceStatusGroupEnum,
    RDSDBInstance,
    StatusError,
)


class TestRDSDBInstanceStatusGroupEnum:
    def test(self):
        _ = RDSDBInstanceStatusGroupEnum.impossible_to_become_available
        _ = RDSDBInstanceStatusGroupEnum.impossible_to_become_stopped


class TestRds:
    mock_rds = None
    bsm: BotoSesManager = None

    @classmethod
    def setup_rds_resources(cls):
        cls.inst_id_1 = cls.bsm.rds_client.create_db_instance(
            DBInstanceIdentifier="db-inst-1",
            DBInstanceClass="db.t2.micro",
            Engine="mysql",
        )["DBInstance"]["DBInstanceIdentifier"]

        cls.inst_id_2 = cls.bsm.rds_client.create_db_instance(
            DBInstanceIdentifier="db-inst-2",
            DBInstanceClass="db.t2.medium",
            Engine="mysql",
            Tags=[
                dict(Key="Name", Value="my-db"),
            ],
        )["DBInstance"]["DBInstanceIdentifier"]

    @classmethod
    def setup_class(cls):
        cls.mock_rds = moto.mock_rds()
        cls.mock_rds.start()
        cls.bsm = BotoSesManager(region_name="us-east-1")
        cls.setup_rds_resources()

    @classmethod
    def teardown_class(cls):
        cls.mock_rds.stop()

    def _test(self):
        inst_id_list = [
            self.inst_id_1,
            self.inst_id_2,
        ]
        for inst_id in inst_id_list:
            db_inst = RDSDBInstance.from_id(self.bsm.rds_client, inst_id)
            assert db_inst.is_available() is True
            assert db_inst.is_stopped() is False
            assert db_inst.is_ready_to_start() is False
            assert db_inst.is_ready_to_stop() is True
            assert db_inst.id == inst_id

        db_inst_list = RDSDBInstance.query(self.bsm.rds_client).all()
        assert len(db_inst_list) == 2

        db_inst_list = RDSDBInstance.from_tag_key_value(
            self.bsm.rds_client, key="Name", value="my-db"
        ).all()
        assert len(db_inst_list) == 1
        db_inst = db_inst_list[0]
        assert db_inst.id == self.inst_id_2
        assert db_inst.tags["Name"] == "my-db"

        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        db_inst.stop_db_instance(self.bsm.rds_client)
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        assert db_inst.is_available() is False
        assert db_inst.is_stopped() is True

        db_inst.start_db_instance(self.bsm.rds_client)
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        assert db_inst.is_stopped() is False
        assert db_inst.is_available() is True

        db_inst_list = RDSDBInstance.from_tag_key_value(
            self.bsm.rds_client, key="Env", value="sandbox"
        ).all()
        assert len(db_inst_list) == 0

    def _test_wait_for_status(self):
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        assert db_inst.is_available() is True
        with pytest.raises(StatusError):
            db_inst.wait_for_stopped(
                rds_client=self.bsm.rds_client,
                verbose=False,
            )

        db_inst.stop_db_instance(self.bsm.rds_client)
        new_db_inst = db_inst.wait_for_status(
            rds_client=self.bsm.rds_client,
            stop_status=RDSDBInstanceStatusEnum.stopped,
            verbose=False,
        )
        assert new_db_inst.is_stopped() is True
        with pytest.raises(StatusError):
            db_inst.wait_for_available(
                rds_client=self.bsm.rds_client,
                verbose=False,
            )

    def test(self):
        self._test()
        self._test_wait_for_status()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
