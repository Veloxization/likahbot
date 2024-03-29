import asyncio
import unittest
import os
from dao.time_zones_dao import TimeZonesDAO

class TestTimeZonesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.time_zones_dao = TimeZonesDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.time_zones_dao.clear_time_zones_table())

    def test_user_time_zone_is_found_correctly(self):
        asyncio.run(self.time_zones_dao.add_user_time_zone(1234, "US/Eastern"))
        row = asyncio.run(self.time_zones_dao.get_user_time_zone(1234))
        self.assertEqual(row["time_zone"], "US/Eastern")

    def test_user_time_zone_defaults_to_UTC(self):
        row = asyncio.run(self.time_zones_dao.get_user_time_zone(1234))
        self.assertEqual(row["time_zone"], "UTC")

    def test_time_zone_is_found_correctly_by_id(self):
        tz_id = asyncio.run(self.time_zones_dao.add_user_time_zone(1234, "US/Eastern"))["id"]
        row = asyncio.run(self.time_zones_dao.get_time_zone_by_id(tz_id))
        self.assertEqual(row["time_zone"], "US/Eastern")

    def test_user_time_zone_is_edited_correctly(self):
        asyncio.run(self.time_zones_dao.add_user_time_zone(1234))
        asyncio.run(self.time_zones_dao.edit_user_time_zone(1234, "US/Eastern"))
        row = asyncio.run(self.time_zones_dao.get_user_time_zone(1234))
        self.assertEqual(row["time_zone"], "US/Eastern")

    def test_user_time_zone_is_edited_correctly_by_id(self):
        tz_id = asyncio.run(self.time_zones_dao.add_user_time_zone(1234))["id"]
        asyncio.run(self.time_zones_dao.edit_time_zone_by_id(tz_id, "US/Eastern"))
        row = asyncio.run(self.time_zones_dao.get_time_zone_by_id(tz_id))
        self.assertEqual(row["time_zone"], "US/Eastern")

    def test_user_time_zone_is_deleted_correctly(self):
        asyncio.run(self.time_zones_dao.add_user_time_zone(1234, "US/Eastern"))
        asyncio.run(self.time_zones_dao.delete_user_time_zone(1234))
        row = asyncio.run(self.time_zones_dao.get_user_time_zone(1234))
        self.assertEqual(row["time_zone"], "UTC")

    def test_time_zone_is_deleted_correctly_by_id(self):
        tz_id = asyncio.run(self.time_zones_dao.add_user_time_zone(1234, "US/Eastern"))["id"]
        asyncio.run(self.time_zones_dao.delete_time_zone_by_id(tz_id))
        row = asyncio.run(self.time_zones_dao.get_time_zone_by_id(tz_id))
        self.assertIsNone(row)
