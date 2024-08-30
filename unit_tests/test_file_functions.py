import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import functions

read_file = getattr(functions, "read_file")
write_file = getattr(functions, "write_file")
insert_into_file = getattr(functions, "insert_into_file")
append_file = getattr(functions, "append_file")
modify_file = getattr(functions, "modify_file")
list_files_and_dir = getattr(functions, "list_files_and_dir")
delete_file_or_dir = getattr(functions, "delete_file_or_dir")
read_pdf_to_text = getattr(functions, "read_pdf_to_text")


class TestFileFunctions(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_file.txt'
        with open(self.test_file, 'w') as f:
            f.write('Line 1\nLine 2\nLine 3\n')

    def tearDown(self):
        # Clean up the test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_read_file(self):
        content = read_file(self.test_file)
        self.assertEqual(content, '1: Line 1\n2: Line 2\n3: Line 3\n')

    def test_write_file(self):
        write_file(self.test_file, 'New content\n')
        content = read_file(self.test_file)
        self.assertEqual(content, '1: New content\n')

    def test_insert_into_file(self):
        insert_into_file(self.test_file, 2, 'Inserted line')
        insert_into_file(self.test_file, 2, 'Inserted line')
        content = read_file(self.test_file)
        self.assertEqual(content, '1: Line 1\n2: Inserted line\n3: Inserted line\n4: Line 2\n5: Line 3\n')

    def test_append_file(self):
        append_file(self.test_file, 'Appended line\n')
        content = read_file(self.test_file)
        self.assertEqual(content, '1: Line 1\n2: Line 2\n3: Line 3\n4: Appended line\n')

    def test_modify_file(self):
        modify_file(self.test_file, 2, 2, 'Modified line')
        content = read_file(self.test_file)
        self.assertEqual(content, '1: Line 1\n2: Modified line\n3: Line 3\n')

    def test_list_files_and_dir(self):
        modify_file(self.test_file, 2, 2, 'Modified line')
        result = list_files_and_dir('.', recursive=True)
        self.assertEqual("test_file.txt" in result, True)

    def test_delete_file_or_dir(self):
        delete_file_or_dir(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))

    def test_read_pdf_to_text(self):
        # Skipping for now as it requires external file, also easily inconsistent
        pass

if __name__ == '__main__':
    unittest.main()