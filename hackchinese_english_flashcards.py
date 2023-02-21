import sys
from chinese_words import Word, get_hackchinese_translations, practice
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from pathlib import Path

import random


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HackChinese from English")
        self.words = []
        self.queue = []
        self.already_guessed = False

        widget = QWidget()
        layout = QVBoxLayout()

        # Options
        options_layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        load_vocab_button = QPushButton("Load Vocab")
        load_vocab_button.clicked.connect(self.show_dialog)
        self.word_count_text = QLabel("Words: 0")
        options_layout.addWidget(load_vocab_button)
        options_layout.addWidget(self.word_count_text)

        # Card
        card_layout = QVBoxLayout()
        self.english_label = QLabel("English:")
        self.english_label.setStyleSheet('color: #6096B4')
        self.english_word = QLabel()
        self.english_word.setWordWrap(True)
        self.chinese_label = QLabel("Chinese:")
        self.chinese_word = QLabel()
        self.chinese_label.setStyleSheet('color: #93BFCF')
        self.pinyin_label = QLabel("Pinyin:")
        self.pinyin_word = QLabel()
        self.pinyin_label.setStyleSheet('color: #BDCDD6')

        answer_layout = QVBoxLayout()
        answer_input_layout = QHBoxLayout()
        self.previous_answer = QLabel()
        self.answer_label = QLabel("Answer:")
        self.user_answer = QLineEdit()
        self.user_answer.setPlaceholderText('enter answer here...')
        self.user_answer.returnPressed.connect(self.guess_word)
        self.next_word = QPushButton('Next')
        self.next_word.clicked.connect(self.pick_next_word)
        self.user_message = QLabel()
        answer_layout.addWidget(self.previous_answer)
        answer_input_layout.addWidget(self.answer_label)
        answer_input_layout.addWidget(self.user_answer)
        answer_input_layout.addWidget(self.next_word)
        answer_layout.addLayout(answer_input_layout)
        
        card_layout.addWidget(self.english_label)
        card_layout.addWidget(self.english_word)
        card_layout.addWidget(self.chinese_label)
        card_layout.addWidget(self.chinese_word)
        card_layout.addWidget(self.pinyin_label)
        card_layout.addWidget(self.pinyin_word)
        card_layout.addLayout(answer_layout)
        card_layout.addWidget(self.user_message)

        # Stats
        stats_layout = QHBoxLayout()
        self.correct_count = QLabel("✅: 0")
        self.incorrect_count = QLabel("❌: 0")
        stats_layout.addWidget(self.correct_count)
        stats_layout.addWidget(self.incorrect_count)
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Configure layouts
        layout.addLayout(options_layout)
        layout.addLayout(card_layout)
        layout.addLayout(stats_layout)
        widget.setLayout(layout)

        # Establish primary widget
        self.setCentralWidget(widget)
    
    def get_label_count(self, label_text):
        return int(label_text.split(':')[-1].strip())

    def set_queue_to_shuffled_words(self):
        words_copy = self.words[:]
        random.shuffle(words_copy)
        self.queue = words_copy


    def pick_next_word(self):
        if not self.words:
            return

        # should only happen once...
        if len(self.queue) == 0:
            self.set_queue_to_shuffled_words()
        else:
            self.queue.pop()
            if len(self.queue) == 0:
                self.set_queue_to_shuffled_words()

        assert len(self.queue) > 0
        self.show_word(self.queue[-1])
        self.already_guessed = False
        self.user_answer.setText('')
        self.previous_answer.setText('')
        self.chinese_word.setText('')
        self.pinyin_word.setText('')
        self.user_message.setText('')


    def guess_word(self):
        if not self.words:
            return
        
        if self.already_guessed:
            self.pick_next_word()
            return

        assert len(self.queue) > 0
        word = self.queue[-1]
        guess = self.user_answer.displayText().strip()
        if guess == '':
            return

        user_answer = ''.join(guess.split()).replace('5', '').replace('ü', 'u').lower()
        correct_answer = ''.join(word.pinyin.split()).replace('ü', 'u').lower() if word.pinyin else None
        correct_answer_numerical = ''.join(
            word.pinyin_numerical.split()).replace('5', '').replace('ü', 'u').lower()

        is_correct = user_answer in [word.character, correct_answer, correct_answer_numerical]

        if not is_correct:
            count = self.get_label_count(self.incorrect_count.text()) + 1
            self.incorrect_count.setText(f"❌: {count}")
            self.user_message.setText('Wrong 😔')
            self.user_message.setStyleSheet('color: red')
        else:
            count = self.get_label_count(self.correct_count.text()) + 1
            self.correct_count.setText(f"✅: {count}")
            self.user_message.setText('Correct! 🎉')
            self.user_message.setStyleSheet('color: green')
        
        self.previous_answer.setText(f"Your answer: {user_answer}")
        self.previous_answer.setStyleSheet('color: #EEE9DA')
        self.show_word(word, show_translation=True)
        self.already_guessed = True


    def show_word(self, word: Word, show_translation: bool = False):
        english_text = ' | '.join(word.english)
        self.english_word.setText(english_text)

        if show_translation:
            if word.character:
                self.chinese_word.setText(word.character)
            if word.pinyin:
                self.pinyin_word.setText(word.pinyin)

    def load_file(self, csv_path):
        self.words = get_hackchinese_translations(csv_path)
        self.word_count_text.setText(f"Words: {len(self.words)}")

        if self.words:
            self.pick_next_word()


    def show_dialog(self):
        csv_path, _ = QFileDialog.getOpenFileName(
            self, 'Open HackChinese File', str(Path.home()), filter="*.csv")

        if csv_path:
            self.load_file(csv_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
