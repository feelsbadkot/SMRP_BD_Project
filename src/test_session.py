import random
from datetime import datetime
from pathlib import Path

import sqlite3

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import vlc

class TestWindow(QMainWindow):
    def __init__(self, user_id, example_ids, with_music=False, parent=None):
        super().__init__(parent)

        self.user_id = user_id
        self.example_ids = example_ids
        self.with_music = with_music  # флаг на воспроизведение музыки (0 - нет музыки, 1 - есть)

        self.current_index = 0
        self.correct_answers = 0

        # подключение таймера
        self.max_test_time = 300
        self.start_time = datetime.now()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  
        self.elapsed_seconds = 0

        # размеры окна
        self.setWindowTitle("Тест с музыкой" if self.with_music else "Тест без музыки")
        self.setGeometry(200, 200, 400, 300)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # загружаем первый пример
        self.current_example = self.load_example(self.example_ids[self.current_index])
        self.example_label = QLabel(f"{self.current_example['expression']} =")
        self.example_label.setAlignment(Qt.AlignCenter)
        self.example_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.example_label)

        # поле ввода ответа
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Введите ответ")
        self.answer_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        # Привязываем сигнал returnPressed к методу next_task
        self.answer_input.returnPressed.connect(self.next_task)
        self.layout.addWidget(self.answer_input)

        # устанавливаем фокус на поле ввода при запуске
        self.answer_input.setFocus()

        # таймер
        self.timer_label = QLabel("Время: 0 сек")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 14px; color: #666;")
        self.layout.addWidget(self.timer_label)

        # кнопка перехода к следующему заданию
        self.next_button = QPushButton("Следующее задание")
        self.next_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        self.next_button.clicked.connect(self.next_task)
        self.layout.addWidget(self.next_button)

        # кнопка завершения теста
        self.finish_button = QPushButton("Завершить тест")
        self.finish_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        self.finish_button.clicked.connect(self.finish_test)
        self.layout.addWidget(self.finish_button)

        # если тест с музыкой включаем ее
        if self.with_music:
            self.setup_music()

    def setup_music(self):
        # загружаем все композиции из базы данных
        self.music_tracks = self.load_music_tracks()
        if not self.music_tracks:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить музыкальные композиции. Тест продолжится без музыки.")
            self.with_music = False
            return

        # формируем очередь из 10 композиций
        self.music_queue = random.sample(self.music_tracks, min(10, len(self.music_tracks)))
        self.current_music_index = 0

        # Инициализируем VLC
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_media_ended)

        # Начинаем воспроизведение первой композиции
        self.play_next_track()

    # функция загрузки примера из бд
    def load_example(self, example_id):
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT Expression, CorrectAnswer FROM Examples WHERE Id = ?", (example_id,))
            expression, correct_answer = cursor.fetchone()
            conn.close()
            return {"expression": expression, "correct_answer": correct_answer}
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить пример: {e}")
            return None
        
    # функция загрузки треков из БД
    def load_music_tracks(self):
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Author, Title, Duration, FilePath FROM Music")
            tracks = cursor.fetchall()
            conn.close()
            return [{"Id": t[0], "Author": t[1], "Title": t[2], "Duration": t[3], "FilePath": t[4]} for t in tracks]
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить музыку: {e}")
            return []

    # функция запуска следующего трека
    def play_next_track(self):
        # зацикливаемся если треки в очереди кончились
        if self.current_music_index >= len(self.music_queue):
            self.current_music_index = 0

        # подгружаем трек из очереди и формируем его полный путь
        track = self.music_queue[self.current_music_index]
        file_path = track["FilePath"]
        absolute_path = str(Path(file_path).resolve())
    
        # запускаем плеер
        media = self.vlc_instance.media_new(absolute_path)
        self.player.set_media(media)
        self.player.play()
        self.current_music_index += 1

    # обработка события, когда песня закончилась
    def on_media_ended(self, event):
        self.play_next_track()

    # функция обновления таймера
    def update_timer(self):
        self.elapsed_seconds += 1
        self.timer_label.setText(f"Время: {self.elapsed_seconds} сек")
        if self.elapsed_seconds >= self.max_test_time:
            self.finish_test()

    # функция смены примера
    def next_task(self):
        # проверяем ответ пользователя
        try:
            user_answer = int(self.answer_input.text())
            correct_answer = self.current_example["correct_answer"]
            if user_answer == correct_answer:
                self.correct_answers += 1
        except ValueError:
            pass  # пропускаем, если ответ не число

        # очищаем поле ввода
        self.answer_input.clear()

        # переходим к следующему примеру
        self.current_index += 1
        if self.current_index < len(self.example_ids):
            self.current_example = self.load_example(self.example_ids[self.current_index])
            self.example_label.setText(f"{self.current_example['expression']} =")
            # устанавливаем фокус на поле ввода 
            self.answer_input.setFocus()
        else:
            self.finish_test()

    # функция завершения теста
    def finish_test(self):
        # останавливаем таймер
        self.timer.stop()

        # останавливаем музыку
        if self.with_music and hasattr(self, 'player'):
            self.player.stop()
        
        # вычисляем эффективность: число секунд / число правильных ответов
        if self.correct_answers > 0:
            efficiency = self.elapsed_seconds / self.correct_answers
        else:
            efficiency = float('inf')  # Если нет правильных ответов, эффективность бесконечна

        # сохраняем результаты в таблицу Sessions
        self.save_to_db(efficiency)

        # обновляем лучший результат в базе данных
        self.update_best_result(efficiency)

        # отображаемая эффективность
        efficiency_display = f"{efficiency:.2f}" if self.correct_answers > 0 else "inf"

        # показываем результат
        QMessageBox.information(
            self,
            "Результат",
            f"Тест завершён!\n"
            f"Показанных заданий: {self.current_index}\n"
            f"Правильных ответов: {self.correct_answers}\n"
            f"Время: {self.elapsed_seconds} сек\n"
            f"Эффективность (сек/правильный ответ): {efficiency_display}"
        )

        # включаем кнопки родительского окна
        parent = self.parent()
        if parent and hasattr(parent, 'enable_buttons'):
            parent.enable_buttons()

        # закрываем окно теста
        self.close()

    def closeEvent(self, event):
        # останавливаем таймер и включаем кнопки при закрытии окна
        self.timer.stop()
        if self.with_music and hasattr(self, 'player'):
            self.player.stop()
        parent = self.parent()
        if parent and hasattr(parent, 'enable_buttons'):
            parent.enable_buttons()
        event.accept()
            
    # функций сохранения результатов в базу данных
    def save_to_db(self, efficiency):
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Sessions (UserId, SessionDate, CorrectAnswers, ElapsedSeconds, Efficiency, WithMusic)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.correct_answers, self.elapsed_seconds, efficiency, 1 if self.with_music else 0))
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить результаты сессии: {e}")

    # фукнция обновления базы данных
    def update_best_result(self, efficiency):
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            field = "EfficiencyWithMusic" if self.with_music else "EfficiencyWithoutMusic"
            cursor.execute(f"SELECT {field} FROM Investigated_Details WHERE UserId = ?", (self.user_id,))
            current_best = cursor.fetchone()[0]

            if self.correct_answers == 0:
                return
            if current_best is None or efficiency < current_best:
                cursor.execute(f"UPDATE Investigated_Details SET {field} = ? WHERE UserId = ?",
                              (efficiency, self.user_id))
                conn.commit()

            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить лучший результат: {e}")