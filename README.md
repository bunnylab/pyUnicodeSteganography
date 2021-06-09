# pyUnicodeSteganography

Experimental python package implementing several methods of unicode steganography (concealing
a message within text by sneaky use of the unicode character set).

## Build/Install

- Clone this repository

- Build: `python3 -m build`  or  `python3 setup.py build`

- Install: `python3 -m pip install .`  or  `python3 setup.py install`

## Test

`python3 setup.py test`

## Using 

```python
import pyUnicodeSteganography as usteg

text = "this is a completely normal message"
secret_msg = "attack at dawn"
encoded = usteg.encode(text, secret_msg)
decoded = usteg.decode(encoded)
```

## Steganography Methods

## Zero Width Characters

Unicode standard includes multiple non-printing or zerowidth characters such as '\u200b' zero
width space. Which are not visible when rendered by most browsers/editors and etc. These can 
be used to invisibly embed arbitrary data inside of other text. This is the default method 
this package uses for steganography.

```python
secret_text = usteg.encode("some text", "data")
secret_binary = usteg.encode("some text", b'\x00\x01', binary=True)
```

## SNOW (steganographic nature of whitespace)

[Original project site](http://darkside.com.au/snow/)

An older method which uses trailing whitespace to embed arbitrary data in text. SNOW takes
advantage of the fact that many browsers and other programs will retain but not display trailing
whitespace to embed arbitrary data. Can work even with plain ascii text and may function better 
in situations where special unicode characters are removed. 

```python
secret_text = usteg.encode("some text", "data", method="snow")
secret_binary = usteg.encode("some text", b'\x00\x01', method="snow", binary=True)
```

## Unicode Lookalikes 

Unicode includes a lot of characters which are [confusable](https://util.unicode.org/UnicodeJsps/confusables.jsp?a=a&r=None)with other characters. This can also be used to encode arbitrary data into a
string. This method strategically replaces characters in a string with lookalike characters creating a simple binary encoding. (normal char-0, lookalike-1) 

```python
secret_text = usteg.encode("some text", "a", method="lookalike")
secret_binary = usteg.encode("some text", b'\x00', method="lookalike", binary=True)
```
### Data Capacity 

Zero width and SNOW methods of steganography work by inserting new characters into a string and so 
can encode any amount of data at the cost of increasing the size of the text. Lookalike steganography replaces existing characters so the data you can encode in a string is limited by the 
number of substitutable characters in the string. The rough formula is 1 byte or 1 char / 8 substitutable chars. We also included a utility method that can calculate this for arbitrary strings.

```python
from pyUnicodeSteganography.lookalikes import capacity 
my_string = "hello I am a string I have nothing to fear because I have nothing to hide"
byte_capacity = capacity(my_string)
```

### Data Corruption 

This method has a couple of limitiations. It cannot properly handle unicode strings which contain
any of the characters it uses as lookalikes. Encoding data into strings which contain these will 
corrupt the data unpredictably. 

### Padded Output

The method also cannot determine where the 'encoded' portion of a 
string ends if you encode data into a string with more 'capacity' than you use. The returned bytes/string will instead be null padded up to the total capacity of the string you decode. Keep this 
in mind if encoding binary data. 

## Using Custom Character Sets

Package includes defaults for each method for their character set and delimiters (zerowidth and snow) or substitution table
(lookalikes). The defaults are generally reasonable but there are a lot of cases where you may want to change them. Certain 
zerowidth characters are stripped/blocked on a website, lookalikes for a different language and etc. This can be done by 
passing a list of chars to the named arguments "replacements" and "delimiter" for zerowidth/snow. Or by passing a dictionary
of chars and their lookalikes to "replacements" for lookalikes.

```python
character_set = ["\u200B", "\u200C", "\u200E", "\u0000"]
delimiter = "\u2062"
secret_text = usteg.encode("some text", "secret", replacements=character_set, delimiter=delimiter)
secret = usteg.decode(secret_text, replacements=character_set, delimiter=delimiter)
```

```python
substitution_table = {'A':'\u0391', 'B':'\u0392', 'C':'\u03F9'}
secret_text = usteg.encode("ABC ABC ABC ABC ABC ABC", "a", method="lookalike", replacements=substitution_table)
secret = usteg.decode(secret_text, method="lookalike", replacements=substitution_table)
```
### Limitations 

Currently zero width only supports a 2 bit encoding method and requires 4 char character set. You may include more but only
the first 4 will be used in encoding. Snow only supports a 1 bit encoding and requires 2 chars in its character set. For both snow and zerowidth the delimiter string must be different than the characters used in the character set. 

## Encryption

This package does not include any support for encryption but it's easy enough to send encrypted messages using 
unicode steganography. The following is a simple example of how to do so with a well supported cryptography library. 

```python
import pyUnicodeSteganography as usteg
import nacl.secret
import nacl.utils 

# create secret key and initialize secret key encryption method
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
box = nacl.secret.SecretBox(key)

# encrypt message and use unicode steganography to hide binary data in text
message = b'encrypted secret'
ciphertext = box.encrypt(message)
encoded_ciphertext = usteg.encode("hello friend", ciphertext, binary=True)

# extract encoded message and decrypt 
ciphertext = usteg.decode(encoded_ciphertext, binary=True)
plaintext = box.decrypt(ciphertext)
```