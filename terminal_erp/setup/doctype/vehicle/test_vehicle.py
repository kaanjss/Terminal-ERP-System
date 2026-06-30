# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework
from terminal_framework.utils import random_string

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestVehicle(Terminal ERPTestSuite):
	def test_make_vehicle(self):
		vehicle = terminal_framework.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": random_string(10).upper(),
				"make": "Maruti",
				"model": "PCM",
				"last_odometer": 5000,
				"acquisition_date": terminal_framework.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234ABCD",
				"uom": "Litre",
				"vehicle_value": terminal_framework.utils.flt(500000),
			}
		)
		vehicle.insert()

	def test_renaming_vehicle(self):
		license_plate = random_string(10).upper()

		vehicle = terminal_framework.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": license_plate,
				"make": "Skoda",
				"model": "Slavia",
				"last_odometer": 5000,
				"acquisition_date": terminal_framework.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234EFGH",
				"uom": "Litre",
				"vehicle_value": terminal_framework.utils.flt(500000),
			}
		)
		vehicle.insert()

		new_license_plate = random_string(10).upper()
		terminal_framework.rename_doc("Vehicle", license_plate, new_license_plate)

		self.assertEqual(
			new_license_plate, terminal_framework.db.get_value("Vehicle", new_license_plate, "license_plate")
		)
