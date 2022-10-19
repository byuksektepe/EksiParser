from insert.db import Database
import unittest

db = Database()
# -> SE442 TEST # SE442 TEST # SE442 TEST # SE442 TEST # SE442 TEST ->

class InsertDBTests(unittest.TestCase):

    def test_set_and_create_insert_database(self):
        x = db.set()
        self.assertEqual(x, True, "-> ! -> Ekşi Insert Otomasyonu için db oluşturma başarısız.")
        pass

    def test_get_data_from_insert_database(self):
        x = db.get()
        self.assertEqual(x[1], True, "-> ! -> Ekşi Insert Otomasyonu için veri alma başarısız.")
        print(x[0])
        pass
