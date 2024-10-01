from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

import random
import re

app = QApplication([])

from words import *

class Hangman(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.word = random.choice(words_list)
        self.guesses = ['_' for _ in self.word]
        self.used_letters = set()
        self.attempts_left = 8
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Віселиця")
        self.resize(300, 200)
        label_word = QLabel(" ".join(self.guesses), self)
        self.label_word = label_word
        result_label = QLabel("", self)
        self.result_label = result_label
        used_letters_label = QLabel("Використані літери: ", self)
        self.used_letters_label = used_letters_label
        label_image = QLabel(self)
        self.label_image = label_image
        self.hangman_images = [QPixmap(f'man{i}.jpg') for i in range(1, 10)]
        self.label_image.setPixmap(self.hangman_images[0])
        input_box = QLineEdit(self)
        input_box.setMaxLength(1)
        self.input_box = input_box
        guess_btn = QPushButton("Вгадати", self)
        guess_btn.clicked.connect(self.check_guess)
        self.guess_btn = guess_btn
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input_box)
        h_layout.addWidget(self.guess_btn)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_word)
        v_layout.addWidget(self.result_label)
        v_layout.addWidget(self.used_letters_label)
        v_layout.addWidget(self.label_image)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

    def check_guess(self):
        guess = self.input_box.text().lower()
        self.input_box.clear()

        if not re.match(r'^[а-яА-Я\'ієї]{1}$', guess) or guess in self.used_letters:
            self.result_label.setText('Помилка: Введіть одну нову кириличну літеру або апостроф.')
            QTimer.singleShot(3000, lambda: self.result_label.clear())
            return True

        self.used_letters.add(guess)
        self.used_letters_label.setText(f'Використані літери: {', '.join(self.used_letters)}')

        if guess in self.word:
            for index, letter in enumerate(self.word):
                if letter == guess:
                    self.guesses[index] = guess
            self.label_word.setText(' '.join(self.guesses))
        else:
            self.attempts_left -= 1
            self.label_image.setPixmap(self.hangman_images[8 - self.attempts_left])

        self.check_game_over()

    def check_game_over(self):
        if '_' not in self.guesses:
            self.result_label.setText('Вітаємо! Ви виграли!')
            self.guess_btn.setText('Грати знову')
            self.guess_btn.clicked.disconnect()
            self.guess_btn.clicked.connect(self.play_again)
        elif self.attempts_left == 0:
            self.result_label.setText(f'Гру програно! Слово було: {self.word}')
            self.guess_btn.setText('Грати знову')
            self.guess_btn.clicked.disconnect()
            self.guess_btn.clicked.connect(self.play_again)

    def play_again(self):
        self.word = random.choice(words_list)
        self.guesses = ['_' for _ in self.word]
        self.used_letters = set()
        self.attempts_left = 8
        self.label_word.setText(' '.join(self.guesses))
        self.result_label.clear()
        self.used_letters_label.setText('Використані літери: ')
        self.label_image.setPixmap(self.hangman_images[0])
        self.guess_btn.setText('Вгадати')
        self.guess_btn.clicked.disconnect()
        self.guess_btn.clicked.connect(self.check_guess)

game = Hangman()
game.show()

app.exec()
