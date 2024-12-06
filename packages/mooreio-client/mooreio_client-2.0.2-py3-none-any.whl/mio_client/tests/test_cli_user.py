# Copyright 2020-2024 Datum Technology Corporation
# All rights reserved.
#######################################################################################################################
import os
from pathlib import Path
from unittest import SkipTest

import pytest

import mio_client.cli
from .common import OutputCapture, TestBase


class TestCliUser(TestBase):

    @pytest.mark.single_process
    @pytest.mark.integration
    def test_cli_login_logout(self, capsys):
        result = self.login(capsys, 'admin', 'admin')
        assert result.return_code == 0
        assert "Logged in successfully" in result.text
        assert mio_client.cli.root_manager.user.authenticated == True
        result = self.logout(capsys)
        assert result.return_code == 0
        assert "Logged out successfully" in result.text
        assert mio_client.cli.root_manager.user.authenticated == False


