import unittest
from sql_handler import SqlContext
from adoption_crud import MissingInformation, InvalidTarget, CannotRemoveInfo, DuplicateInformation
from adoption_crud.species import create_species, update_species, \
    read_species, delete_species, \
    deactivate_species, activate_species


def drop_database(helper):
    helper.execute_query("DROP DATABASE IF EXISTS `adoption_agency_test`;")


def create_database(helper):
    helper.execute_query("CREATE DATABASE IF NOT EXISTS `adoption_agency_test`;")


def build_database(helper):
    with open("../sql/adoption_site_schema.sql", "r") as db_file:
        for query in db_file.read().split(";\n")[:-1]:
            helper.execute_query(query)
        helper.connector.commit()


class SpeciesCreate(unittest.TestCase):
    def setUp(self):
        # Destroy test database
        with SqlContext() as helper:
            drop_database(helper)
            create_database(helper)
        with SqlContext("adoption_agency_test") as helper:
            build_database(helper)

    @classmethod
    def tearDownClass(cls):
        with SqlContext() as helper:
            drop_database(helper)

    def test_no_name(self):
        self.assertRaises(MissingInformation, create_species, None)

    def test_name_truly_unique(self):
        name = "Test name"
        create_species(name)
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"SELECT * FROM `species` WHERE `name`=%(name)s", {"name": name})
            results = helper.fetch_all()
            self.assertEqual(len(results), 1)
            self.assertDictEqual(results[0], {
                "id": 1,
                "name": name,
                "isActive": 1
            })

    def test_name_not_unique(self):
        name = "Test name"
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 1)")
            self.assertRaises(DuplicateInformation, create_species, name)

    def test_name_unique_in_actives(self):
        name = "Test name"
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 0)")
            create_species(name)
            helper.execute_query(f"SELECT * FROM `species` WHERE `name`='{name}'")
            results = helper.fetch_all()
            self.assertEqual(len(results), 2)
            self.assertDictEqual(results[1], {
                "id": 2,
                "name": name,
                "isActive": 1
            })


class SpeciesRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destroy test database
        with SqlContext() as helper:
            drop_database(helper)
            create_database(helper)

        test_species = [
            "Test name 1",
            "Test name 2",
            "Test name 3"
        ]
        with SqlContext("adoption_agency_test") as helper:
            build_database(helper)
            for name in test_species:
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 1);")
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 0);")

    @classmethod
    def tearDownClass(cls):
        with SqlContext() as helper:
            drop_database(helper)

    def test_get_all(self):
        results = read_species()
        self.assertEqual(results, [
            {
                "id": 1,
                "name": "Test name 1",
                "isActive": 1
            },
            {
                "id": 2,
                "name": "Test name 1",
                "isActive": 0
            },
            {
                "id": 3,
                "name": "Test name 2",
                "isActive": 1
            },
            {
                "id": 4,
                "name": "Test name 2",
                "isActive": 0
            },
            {
                "id": 5,
                "name": "Test name 3",
                "isActive": 1
            },
            {
                "id": 6,
                "name": "Test name 3",
                "isActive": 0
            },
        ])

    def test_get_all_active(self):
        results = read_species(is_active=1)
        self.assertEqual(results, [
            {
                "id": 1,
                "name": "Test name 1",
                "isActive": 1
            },
            {
                "id": 3,
                "name": "Test name 2",
                "isActive": 1
            },
            {
                "id": 5,
                "name": "Test name 3",
                "isActive": 1
            },
        ])

    def test_get_all_inactive(self):
        results = read_species(is_active=0)
        self.assertEqual(results, [
            {
                "id": 2,
                "name": "Test name 1",
                "isActive": 0
            },
            {
                "id": 4,
                "name": "Test name 2",
                "isActive": 0
            },
            {
                "id": 6,
                "name": "Test name 3",
                "isActive": 0
            },
        ])

    def test_get_all_with_token_in_name(self):
        results = read_species(search_by_column={"name": "1"})
        self.assertEqual(results, [
            {
                "id": 1,
                "name": "Test name 1",
                "isActive": 1
            },
            {
                "id": 2,
                "name": "Test name 1",
                "isActive": 0
            },
        ])

    def test_get_all_active_with_token_in_name(self):
        results = read_species(search_by_column={"name": "1"}, is_active=1)
        self.assertEqual(results, [
            {
                "id": 1,
                "name": "Test name 1",
                "isActive": 1
            },
        ])

    def test_get_by_id_existing(self):
        results = read_species(_id=1)
        self.assertDictEqual(results, {
                "id": 1,
                "name": "Test name 1",
                "isActive": 1
            })

    def test_get_by_ids_existing(self):
        results = read_species(ids=[1, 3])
        self.assertEqual(results, [
            {
                "id": 1,
                "name": "Test name 1",
                "isActive": 1
            },
            {
                "id": 3,
                "name": "Test name 2",
                "isActive": 1
            },
        ])

    def test_get_by_id_missing(self):
        results = read_species(_id=10)
        self.assertIsNone(results)

    def test_get_by_ids_missing(self):
        results = read_species(ids=[10, 30])
        self.assertEqual(results, [])


class SpeciesUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destroy test database
        with SqlContext() as helper:
            drop_database(helper)
            create_database(helper)

        test_species = [
            "Test name 1",
            "Test name 2",
            "Test name 3"
        ]
        with SqlContext("adoption_agency_test") as helper:
            build_database(helper)
            for name in test_species:
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 1);")
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 0);")

    @classmethod
    def tearDownClass(cls):
        with SqlContext() as helper:
            drop_database(helper)

    def test_update_missing_id(self):
        self.assertRaises(MissingInformation, update_species, None, {})

    def test_update_nonexistent_id(self):
        self.assertRaises(InvalidTarget, update_species, 10, {})

    def test_attempt_to_remove_name(self):
        self.assertRaises(CannotRemoveInfo, update_species, 1, {"name": None})

    def test_change_name_to_unique(self):
        updated_name = "Test name 1 updated"
        update_species(1, {"name": updated_name})
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query("SELECT * FROM `species` WHERE `id`=1")
            result = helper.fetch_one()
        self.assertDictEqual(result, {
            "id": 1,
            "name": updated_name,
            "isActive": 1
        })
        
    def test_attempt_to_change_name_to_not_unique(self):
        self.assertRaises(DuplicateInformation, update_species, 1, {"name": "Test name 2"})


class SpeciesDeactivate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destroy test database
        with SqlContext() as helper:
            drop_database(helper)
            create_database(helper)

        test_species = [
            "Test name 1",
            "Test name 2",
            "Test name 3"
        ]
        with SqlContext("adoption_agency_test") as helper:
            build_database(helper)
            for name in test_species:
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 1);")
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 0);")

    @classmethod
    def tearDownClass(self):
        with SqlContext() as helper:
            drop_database(helper)

    def test_deactivate_no_id(self):
        self.assertRaises(MissingInformation, deactivate_species, None)
    
    def test_deactivate_nonexistent_id(self):
        self.assertRaises(InvalidTarget, deactivate_species, 10)
    
    def test_deactivate_inactive(self):
        target_id = 2
        deactivate_species(target_id)
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"SELECT * FROM `species` WHERE `id`={target_id}")
            result = helper.fetch_one()
            self.assertDictEqual(result, {
                "id": target_id,
                "name": "Test name 1",
                "isActive": 0
            })
    
    def test_deactivate_active(self):
        target_id = 1
        deactivate_species(target_id)
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"SELECT * FROM `species` WHERE `id`={target_id}")
            result = helper.fetch_one()
            self.assertDictEqual(result, {
                "id": target_id,
                "name": "Test name 1",
                "isActive": 0
            })


class SpeciesActivate(unittest.TestCase):
    def setUp(self):
        # Destroy test database
        with SqlContext() as helper:
            drop_database(helper)
            create_database(helper)

        self.test_species = [
            "Test name 1",
            "Test name 2",
            "Test name 3"
        ]
        with SqlContext("adoption_agency_test") as helper:
            build_database(helper)
            for name in self.test_species:
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 1);")
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 0);")
            helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('Test name 4', 0);")

    @classmethod
    def tearDownClass(cls):
        with SqlContext() as helper:
            drop_database(helper)

    def test_activate_no_id(self):
        self.assertRaises(MissingInformation, activate_species, None)
    
    def test_activate_nonexistent_id(self):
        self.assertRaises(InvalidTarget, activate_species, 10)
    
    def test_activate_inactive_would_be_unique(self):
        target_id = 7
        activate_species(target_id)
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"SELECT * FROM `species` WHERE `id`={target_id}")
            result = helper.fetch_one()
            self.assertDictEqual(result, {
                "id": target_id,
                "name": "Test name 1",
                "isActive": 1
            })

    def test_activate_inactive_would_not_be_unique(self):
        self.assertRaises(DuplicateInformation, activate_species, 2)
    
    def test_activate_active(self):
        target_id = 1
        activate_species(target_id)
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query(f"SELECT * FROM `species` WHERE `id`={target_id}")
            result = helper.fetch_one()
            self.assertDictEqual(result, {
                "id": target_id,
                "name": "Test name 1",
                "isActive": 1
            })


class SpeciesDelete(unittest.TestCase):
    def setUp(self):
        # Destroy test database
        with SqlContext() as helper:
            drop_database(helper)
            create_database(helper)

        self.test_species = [
            "Test name 1",
            "Test name 2",
            "Test name 3"
        ]
        with SqlContext("adoption_agency_test") as helper:
            build_database(helper)
            for name in self.test_species:
                helper.execute_query(f"INSERT INTO `species` (`name`, `isActive`) VALUES ('{name}', 1);")

    @classmethod
    def tearDownClass(cls):
        with SqlContext() as helper:
            drop_database(helper)

    def test_delete_no_id(self):
        self.assertRaises(MissingInformation, delete_species, None)

    def test_delete_id_nonexistent(self):
        self.assertRaises(InvalidTarget, delete_species, 10)

    def test_delete_id_exists(self):
        delete_species(1)
        with SqlContext("adoption_agency_test") as helper:
            helper.execute_query("SELECT * FROM `species`;")
            results = helper.fetch_all()
            self.assertEqual(results, [
                {
                    "id": 2,
                    "name": "Test name 2",
                    "isActive": 1
                },
                {
                    "id": 3,
                    "name": "Test name 3",
                    "isActive": 1
                }
            ])


if __name__ == '__main__':
    unittest.main()
