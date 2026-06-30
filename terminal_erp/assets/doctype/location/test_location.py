# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt
import json

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestLocation(Terminal ERPTestSuite):
	def test_location_features(self):
		locations = ["Basil Farm", "Division 1", "Field 1", "Block 1"]
		area = 0
		formatted_locations = []

		for location in locations:
			doc = terminal_framework.get_doc("Location", location)
			doc.save()
			area += doc.area
			temp = json.loads(doc.location)
			temp["features"][0]["properties"]["child_feature"] = True
			temp["features"][0]["properties"]["feature_of"] = location
			formatted_locations.extend(temp["features"])

		test_location = terminal_framework.get_doc("Location", "Test Location Area")
		test_location.save()

		test_location_features = json.loads(test_location.get("location"))["features"]
		ordered_test_location_features = sorted(
			test_location_features, key=lambda x: x["properties"]["feature_of"]
		)
		ordered_formatted_locations = sorted(formatted_locations, key=lambda x: x["properties"]["feature_of"])

		self.assertEqual(ordered_formatted_locations, ordered_test_location_features)
		self.assertEqual(area, test_location.get("area"))
