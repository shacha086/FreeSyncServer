import sqlalchemy.orm
from database import Session
from db_helper import DBHelper
import unittest


class MyTestCase(unittest.TestCase):
    helper = DBHelper(Session)

    def test_add(self):
        kw = "Test"
        self.helper.set(kw, "114514")
        self.assertEqual(self.helper.get(kw), "114514")

    def test_query(self):
        test_hash = self.helper.get("Test")
        self.assertEqual(test_hash, '114514')  # add assertion here

    def test_exist(self):
        self.assertTrue(self.helper.is_exist("Test"))

    def test_delete(self):
        kw = "Test1"
        if not self.helper.is_exist(kw):
            self.test_add()
        self.helper.delete(kw)
        self.assertEqual(self.helper.is_exist(kw), False)

    def test_modify(self):
        kw = "Test2"
        self.helper.set(kw, "1")
        self.assertEqual(self.helper.get(kw), "1")
        self.helper.set(kw, "2")
        self.assertEqual(self.helper.get(kw), "2")

    def test_context(self):
        with Session() as sess:
            sess: sqlalchemy.orm.Session
            kw = ["", "Test1", "Test2", "Test3"]
            self.helper.set(kw[3], "aw", session=sess)
            self.assertEqual(self.helper.get(kw[3], session=sess), "aw")
            all_file = self.helper.get_all(session=sess)
            slice_ = (0, 2)
            slice_file = self.helper.get_slice(slice_, session=sess)
            self.assertEqual(all_file[slice_[0]:slice_[1]], slice_file, "Slice test failed.")

            for it in all_file:
                if str(it.path) in kw:
                    self.helper.delete(it.path, session=sess)

            self.helper.commit(session=sess)
            after = self.helper.get_all(session=sess)
            all_file = [it for it in all_file if it.path != "Test"]
            self.assertFalse([True for it in after if it in all_file])


if __name__ == '__main__':
    unittest.main()
