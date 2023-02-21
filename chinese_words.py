import pinyin as piyi
import pinyin.cedict as cedict
import pandas as pd
import random

from collections.abc import Iterable
from typing import List, Optional


class Word:
    character: str
    pinyin: str
    pinyin_numerical: str
    english: List[str]

    def __init__(self, character: str, pinyin: str = None, pinyin_numerical: str = None, english: str = None):
        self.character = character
        self.pinyin = pinyin or (piyi.get(self.character) if character else None)
        self.pinyin_numerical = pinyin_numerical or piyi.get(
            self.character, format='numerical')
        self.english = english or cedict.translate_word(self.character)

        if (self.english is not None) and isinstance(self.english, str):
            self.english = [self.english]

    def valid(self) -> bool:
        return self.english is not None

    def __repr__(self) -> str:
        return f"character: {self.character}; pinyin: {self.pinyin}; english: {' | '.join(self.english)}"


def get_hackchinese_translations(hackchinese_words_csv: str):
    chinese_characters: pd.Series = pd.read_csv(
        hackchinese_words_csv)['Simplified'].apply(lambda s: s.strip())
    return [w for w in [Word(c) for c in chinese_characters] if w.valid()]


def practice(words: List[Word], num_cards: Optional[int]=None):
    num_cards = num_cards or len(words)

    # Select N words
    random.shuffle(words)
    words = words[:num_cards]

    # Test on every word
    wrong_answers = []
    for word in words:
        print(f'English:\n{" | ".join(word.english)}\n')
        answer = input("Enter pinyin:\n")

        # Check if the user's answer matches any form of pinyin
        user_answer = ''.join(answer.split()).replace('5', '')
        correct_answer = ''.join(word.pinyin.split()) if word.pinyin else None
        correct_answer_numerical = ''.join(
            word.pinyin_numerical.split()).replace('5', '')
        if user_answer in [correct_answer, correct_answer_numerical]:
            print('Correct! ✅\n')
        else:
            print(f'Incorrect. ❌\nThe answer is: {word.pinyin or word.pinyin_numerical}\n')
            wrong_answers.append(word)

    # Print basic statistics
    num_correct = len(words) - len(wrong_answers)
    print(
        f'You answered {num_correct}/{len(words)} cards correctly!')
    if wrong_answers:
        print('You answered the following cards incorrectly:')
        for word in wrong_answers:
            print(word)
