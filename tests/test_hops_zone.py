"""Test the TadoZone object."""

import json
import unittest
from unittest import mock

from . import common

from PyTado.http import Http
from PyTado.interface.api import TadoX


class TadoZoneTestCase(unittest.TestCase):
    """Test cases for zone class"""

    def setUp(self) -> None:
        super().setUp()
        login_patch = mock.patch(
            "PyTado.http.Http._login", return_value=(1, "foo")
        )
        is_x_line_patch = mock.patch(
            "PyTado.http.Http._check_x_line_generation", return_value=True
        )
        get_me_patch = mock.patch("PyTado.interface.api.Tado.get_me")
        login_patch.start()
        is_x_line_patch.start()
        get_me_patch.start()
        self.addCleanup(login_patch.stop)
        self.addCleanup(is_x_line_patch.stop)
        self.addCleanup(get_me_patch.stop)

        self.http = Http("my@username.com", "mypassword")
        self.tado_client = TadoX(self.http)

    def set_fixture(self, filename: str) -> None:
        get_state_patch = mock.patch(
            "PyTado.interface.api.TadoX.get_state",
            return_value=json.loads(common.load_fixture(filename)),
        )
        get_state_patch.start()
        self.addCleanup(get_state_patch.stop)

    def test_get_zone_state(self):
        """Test general homes response."""

        self.set_fixture("tadox/homes_response.json")
        mode = self.tado_client.get_zone_state(14)

        assert mode.preparation is False
        assert mode.zone_id == 14
