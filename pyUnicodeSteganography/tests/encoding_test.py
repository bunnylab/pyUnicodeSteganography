from unittest import TestCase

import pyUnicodeSteganography as stego

class TestStringEncoding(TestCase):
    def setUp(self):
        self.test_strings = ["hello my darling", "aa", "a", "this string is longer than the other ones lalalala"]
        self.messages = ["secret", "longer secret", "q248098e7rq908wr", "a"]
    
    def test_zw(self):
        for test in self.test_strings:
            for msg in self.messages:
                try:
                    encoded = stego.encode(test, msg)
                    self.assertTrue(stego.decode(encoded) == msg)
                except ValueError:
                    pass
       
    def test_snow(self):
        for test in self.test_strings:
            for msg in self.messages:
                encoded = stego.encode(test, msg, method="snow")
                self.assertTrue(stego.decode(encoded, method="snow") == msg)

    def test_lookalikes(self):
        for test in self.test_strings:
            for msg in self.messages:
                # lookalike encode calls will correctly fail with a value error with insufficient
                # subsitutable chars for message, returned message is always padded with null chars
                try:
                    encoded = stego.encode(test, msg, method="lookalike")
                    self.assertTrue(stego.decode(encoded, method="lookalike")[:len(msg)] == msg)
                except ValueError:
                    pass
      

class TestBinaryEncoding(TestCase):
    def setUp(self):
        self.test_strings = ["hello my darling", "aa", "a", "this string is longer than the other ones lalalala"]
        self.messages = [b'\x00\x00\x00\x00\x00', b'\xf9\xf7']
    
    def test_zw(self):
        for test in self.test_strings:
            for msg in self.messages:
                try:
                    encoded = stego.encode(test, msg, binary=True)
                    self.assertTrue(stego.decode(encoded, binary=True) == msg)
                except ValueError:
                    pass
       
    def test_snow(self):
        for test in self.test_strings:
            for msg in self.messages:
                encoded = stego.encode(test, msg, method="snow", binary=True)
                self.assertTrue(stego.decode(encoded, method="snow", binary=True) == msg)

    def test_lookalikes(self):
        for test in self.test_strings:
            for msg in self.messages:
                # lookalike encode calls will correctly fail with a value error with insufficient
                # subsitutable chars for message, returned message is always padded with null chars
                try:
                    encoded = stego.encode(test, msg, method="lookalike", binary=True)
                    self.assertTrue(stego.decode(encoded, method="lookalike", binary=True)[:len(msg)] == msg)
                except ValueError:
                    pass
       
