import asyncio
import unittest
import os
from services.time_zone_service import TimeZoneService

class TestTimeZoneService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/test_schema.sql")
        self.time_zone_service = TimeZoneService(db_address)

    def tearDown(self):
        asyncio.run(self.time_zone_service.clear_time_zones())

    def test_user_time_zone_is_found_correctly(self):
        asyncio.run(self.time_zone_service.add_user_time_zone(1234, "US/Eastern"))
        tz = asyncio.run(self.time_zone_service.get_user_time_zone(1234))
        self.assertEqual(tz.time_zone, "US/Eastern")

    def test_user_time_zone_defaults_to_UTC_correctly(self):
        tz = asyncio.run(self.time_zone_service.get_user_time_zone(1234))
        self.assertEqual(tz.time_zone, "UTC")

    def test_time_zone_is_found_correctly_by_id(self):
        tz_id = asyncio.run(self.time_zone_service.add_user_time_zone(1234, "US/Eastern"))
        tz = asyncio.run(self.time_zone_service.get_time_zone_by_id(tz_id))
        self.assertEqual(tz.time_zone, "US/Eastern")

    def test_user_time_zone_is_edited_correctly(self):
        asyncio.run(self.time_zone_service.add_user_time_zone(1234))
        asyncio.run(self.time_zone_service.edit_user_time_zone(1234, "US/Eastern"))
        tz = asyncio.run(self.time_zone_service.get_user_time_zone(1234))
        self.assertEqual(tz.time_zone, "US/Eastern")

    def test_time_zone_is_edited_correctly_by_id(self):
        tz_id = asyncio.run(self.time_zone_service.add_user_time_zone(1234))
        asyncio.run(self.time_zone_service.edit_time_zone_by_id(tz_id, "US/Eastern"))
        tz = asyncio.run(self.time_zone_service.get_time_zone_by_id(tz_id))
        self.assertEqual(tz.time_zone, "US/Eastern")

    def test_user_time_zone_is_deleted_correctly(self):
        asyncio.run(self.time_zone_service.add_user_time_zone(1234, "US/Eastern"))
        asyncio.run(self.time_zone_service.delete_user_time_zone(1234))
        tz = asyncio.run(self.time_zone_service.get_user_time_zone(1234))
        self.assertEqual(tz.time_zone, "UTC")

    def test_time_zone_is_deleted_correctly_by_id(self):
        tz_id = asyncio.run(self.time_zone_service.add_user_time_zone(1234, "US/Eastern"))
        asyncio.run(self.time_zone_service.delete_time_zone_by_id(tz_id))
        tz = asyncio.run(self.time_zone_service.get_time_zone_by_id(tz_id))
        self.assertIsNone(tz)
