# -*- coding: utf-8 -*-

import pytest


def test():
    from simple_aws_rds import api

    _ = api.RDSDBInstanceStatusEnum
    _ = api.RDSDBInstance
    _ = api.RDSDBInstanceIterProxy


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
