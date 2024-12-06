import json
import os
import unittest
from mydict import MyDict
from unittest.mock import patch, MagicMock
from src.cisco import CiscoSSHDevice

current_dir = os.path.dirname(__file__)

test_file_path = os.path.join(current_dir, 'mock_data_cisco.json')

with open(test_file_path, "r") as f:
    netbox_data = json.load(f)
    mock_interfaces = [MyDict(x) for x in netbox_data["interfaces"]]
    mock_serial = netbox_data["version_serial"]


class TestCiscoSSHDevice(unittest.TestCase):
    @patch('src.cisco.ConnectHandler')  # Mock the ConnectHandler class
    def test_get_interface_details(self, mock_connect_handler):
        # Set up the mock connection's behavior
        mock_connection = MagicMock()
        mock_connection.send_command.return_value = mock_interfaces
        mock_connect_handler.return_value = mock_connection

        # Create an instance of CiscoSSHDevice
        device = CiscoSSHDevice(hostname='192.168.1.1', username='user', password='pass')

        # Call the method under test
        result = device.get_interface_details()

        # Assert the result is as expected
        self.assertEqual(len(result), len(mock_interfaces))
        for idx, interface in enumerate(mock_interfaces):
            self.assertEqual(result[idx].interface, interface['interface'])
            self.assertEqual(result[idx].link_status, interface['link_status'])
            self.assertEqual(result[idx].protocol_status, interface['protocol_status'])
            self.assertEqual(result[idx].description, interface['description'])

        # Ensure send_command was called with the correct command
        mock_connection.send_command.assert_called_once_with('show interface', use_textfsm=True)

    @patch('src.cisco.ConnectHandler')  # Mock the ConnectHandler class
    def test_get_device_serial(self, mock_connect_handler):
        # Set up the mock connection's behavior
        mock_connection = MagicMock()
        mock_connection.send_command.return_value = mock_serial
        mock_connect_handler.return_value = mock_connection

        # Create an instance of CiscoSSHDevice
        device = CiscoSSHDevice(hostname='192.168.1.1', username='user', password='pass')

        # Call the method under test
        serial_number = device.get_device_serial()

        # Assert the result is as expected
        self.assertEqual(serial_number, "FOX3986YDP3")

        # Ensure send_command was called with the correct command
        mock_connection.send_command.assert_called_once_with('show version | include Processor')
