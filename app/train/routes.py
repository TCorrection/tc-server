from app.train import bp
import re
from collections import Counter

from app.extensions import db
from app.models.centuryXVIIWords import centuryXVIIWords
from app.models.centuryXVIIIWords import centuryXVIIIWords

@bp.route('/train/xvii')
def xvii():
    
    def words(text):
      return re.findall(r'[a-zA-ZăĂâÂîÎșȘțȚ&]+', text.lower())

    WORDS = Counter(words(open('data/train/sec7/train.txt', encoding="utf-8").read()))

    for key, value in WORDS.items():

      newWord = centuryXVIIWords(word = key, counter = value)
      db.session.add(newWord)
      db.session.commit()

    return 'Dictionarul de cuvinte a fost generat!'

@bp.route('/train/xviii')
def xviii():
    
    def words(text):
      return re.findall(r'[a-zA-ZăĂâÂîÎșȘțȚ&]+', text.lower())

    WORDS = Counter(words(open('data/train/sec8/train.txt', encoding="utf-8").read()))

    for key, value in WORDS.items():

      newWord = centuryXVIIIWords(word = key, counter = value)
      db.session.add(newWord)
      db.session.commit()

    return 'Dictionarul de cuvinte a fost generat!'


__letters__ = {
    "english": "abcdefghijklmnopqrstuvwxyz",
    "romanian": "abcdefghijklmnopqrstuvwxyzăîșț",
}