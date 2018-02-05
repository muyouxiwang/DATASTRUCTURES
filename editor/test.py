# -*- coding=utf-8 -*-




import unittest

import edit

class TestContent(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        
        self.file_path = "code_demo.py"
        self.content = edit.Content("code_demo.py")




    def test_get_content(self):
        with open("code_demo.py") as rf:
            t = rf.read()
        self.assertEqual(t, self.content.get_content())



    def test_search(self):
        self.assertEqual(self.content.search("whatthefuck"), set([(1, 6), (6, 0)]))

    def test_get_next_word(self):
        self.assertEqual(self.content.get_next_word(2, 5), (2, 7))
        self.assertEqual(self.content.get_next_word(3, 2), (4, 0))


    def test_get_word_end(self):
        self.assertEqual(self.content.get_word_end(3, 0), (3, 2))
        self.assertEqual(self.content.get_word_end(4, 2), (4, 5))
        self.assertEqual(self.content.get_word_end(5, 8), (5, 13))
        self.assertEqual(self.content.get_word_end(2, 6), (2, 13))

    def test_get_word_start(self):
        self.assertEqual(self.content.get_word_start(3, 2), (3, 0))

    def test_get_close_char(self):
        self.assertEqual(self.content.get_close_char(16, 4, "(", ")"), (14, 1, 18, 9))

    def test_index_to_pos(self):
        self.assertEqual(self.content.index_to_pos(27), (1, 4))

    def test_pos_to_index(self):
        self.assertEqual(self.content.pos_to_index(1, 4), 27)
        


if __name__ == "__main__":
    unittest.main()

