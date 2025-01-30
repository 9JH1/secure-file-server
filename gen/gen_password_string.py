
from random import choice as rpick
from random import shuffle 
from hashlib import sha256 as hash256
from uuid import uuid4 as uuid
from cryptography.fernet import Fernet
from subprocess import run
from random import randint as random
from re import sub


word_cull = 0
end_randomize = False
word = 2# 0 = nothing, 1 = sha256, 2 = uuid, 3 = fernet // fernet takes 5 seconds
word_list = "thats what you get".split(" "); # can of course be an actual list array dont worry :D
word_word = str(rpick(word_list));
phrase_randomize = False
excluded_types = [] # number symbol letter letter_upper letter_lower
case = 2  # 0 = none, 1 = random, 2 = upper, 3 = lower 
#           having everything in lower means easy input same with using caps lock for upper

replace = {'-':'','i':'!'}
char = "!@#$%^&*()_+{}[]S$^:>'"
char_sprinkle = 6

if phrase_randomize:
    shuffle(word_list);

if word==1 and word_word != "":
    word = hash256(word_word.encode()).hexdigest()
elif word == 2:
    word = str(uuid())
elif word == 3 and word_word != "":
    _fernet = str(run(['./gen_new_method', '--password',f'{word_word}'], capture_output=True, text=True).stdout)
    _fernet = "".join(_fernet.splitlines())
    _fernet = Fernet(_fernet.encode())
    word = _fernet.encrypt(word_word.encode())
    word = word.decode()
_word = ""
if isinstance(word, str):
    for n in range(round(len(word_list))):
        for nn in range(round(len(word) / len(word_list))-word_cull):
            _word = _word + word[nn+n]
        _word = _word + word_list[n]
    word = _word
elif isinstance(word,int):
    for n in range(len(word_list)):
        _word = _word + word_list[n]
    word = _word
for i in replace:
    word = word.replace(i,replace[i]);
if case == 1:
    word = ''.join(map(rpick, zip(word.lower(), word.upper())))
elif case == 2:
    word = word.upper()
elif case == 3:
    word = word.lower()

if "symbol" in excluded_types:
    word = sub(r'[^\w]', ' ', word)
if "number" in excluded_types:
    word = sub(r'[0-9]+', '', word)
if "letter_upper" in excluded_types:
    word = sub(r'[A-Z]', '', word)
if "letter_lower" in excluded_types:
    word = sub(r'[a-z]', '', word)
if "letter" in excluded_types:
    word = sub(r'[a-z]', '', word)
    word = sub(r'[A-Z]', '', word)

for n in range(char_sprinkle):
    _word = list(word)
    _random = random(0,len(_word)-1)
    _word.insert(_random,rpick(list(char)))
    word = ""
    for i in _word:
        word = word + i
if end_randomize:
    _word = list(word)
    shuffle(_word)
    word = ""
    for i in _word:
        word = word + i
print(word)
