import sys
import random

import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QDateEdit, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt, QDate

from test_session import TestWindow


class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registration")
        self.setGeometry(100, 100, 800, 600)  # размеры окна

        self.set_background()                 # установка фона

        # центральный виджет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # панель регистрации
        self.registration_panel = QWidget(self)
        self.registration_panel.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        self.registration_panel.setFixedSize(300, 450)

        # вертикальная панель регистрации
        self.panel_layout = QVBoxLayout(self.registration_panel)

        # запуск окна входа
        self.run_initial_form()

        # располагаем панель регистрации по центру
        self.layout.addWidget(self.registration_panel, alignment=Qt.AlignCenter)

    # функция подключения фона
    def set_background(self):
        pixmap = QPixmap("figures/background.jpg")
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def get_researchers(self):
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Full_name FROM Users WHERE Role = 'Исследователь'")
            researchers = cursor.fetchall()
            conn.close()
            return researchers
        except Exception as e:
            print(f"Ошибка при получении списка исследователей: {e}")
            return []

    # функция активация окна входа
    def run_initial_form(self):

        # приветственный лейбл
        self.title_label = QLabel("Добро пожаловать!")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        self.panel_layout.addWidget(self.title_label)

        self.who_label = QLabel("Кто Вы?")
        self.who_label.setAlignment(Qt.AlignCenter)
        self.who_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(self.who_label)

        # чекбоксы на одной строке
        self.checkbox_layout = QHBoxLayout()

        # чекбокс с исследуемым
        self.investigated_checkbox = QCheckBox("Исследуемый")
        self.investigated_checkbox.setStyleSheet("font-size: 14px; color: #333;")
        self.investigated_checkbox.setChecked(True) 
        self.investigated_checkbox.stateChanged.connect(self.investigated_checkbox_changed)
        self.checkbox_layout.addWidget(self.investigated_checkbox)

        # чекбокс с исследователем
        self.researcher_checkbox = QCheckBox("Исследователь")
        self.researcher_checkbox.setStyleSheet("font-size: 14px; color: #333;")
        self.researcher_checkbox.stateChanged.connect(self.researcher_checkbox_changed)
        self.checkbox_layout.addWidget(self.researcher_checkbox)

        self.panel_layout.addLayout(self.checkbox_layout)

        # отображение того, кто выбран на данный момент
        self.role_label = QLabel("Вы: Исследуемый")
        self.role_label.setStyleSheet("font-size: 14px; color: #666;")
        self.panel_layout.addWidget(self.role_label)

        # поле ввода логина
        self.login_label = QLabel("Логин:")
        self.login_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(self.login_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.login_input)

        # поле ввода пароля
        self.password_label = QLabel("Пароль:")
        self.password_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.password_input)

        # поле подтверждения пароля (изначально скрыто)
        self.confirm_password_label = QLabel("Подтвердите пароль:")
        self.confirm_password_label.setStyleSheet("font-size: 14px; color: #333;")
        self.confirm_password_label.setVisible(False)
        self.panel_layout.addWidget(self.confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.confirm_password_input.setVisible(False)
        self.panel_layout.addWidget(self.confirm_password_input)

        # кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        self.register_button.clicked.connect(self.show_additional_fields)
        self.panel_layout.addWidget(self.register_button)

        # кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        self.login_button.clicked.connect(self.handle_login)
        self.panel_layout.addWidget(self.login_button)

    # функция очистки окна
    def clear_layout(self):
        while self.panel_layout.count():
            item = self.panel_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                layout = item.layout()
                if layout is not None:
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.setParent(None)

    # функция смены чекбокса исследователя
    def researcher_checkbox_changed(self):
        if self.researcher_checkbox.isChecked():
            self.investigated_checkbox.setChecked(False)
            self.role_label.setText("Вы: Исследователь")
        else:
            self.investigated_checkbox.setChecked(True)
            self.role_label.setText("Вы: Исследуемый")

    # функция смены чекбокса исследуемого
    def investigated_checkbox_changed(self):
        if self.investigated_checkbox.isChecked():
            self.researcher_checkbox.setChecked(False)
            self.role_label.setText("Вы: Исследуемый")
        else:
            self.researcher_checkbox.setChecked(True)
            self.role_label.setText("Вы: Исследователь")

    # показываем поля при регистрации
    def show_additional_fields(self):
        self.clear_layout()
        if self.researcher_checkbox.isChecked():
            self.show_researcher_fields()
        else:
            self.show_investigated_fields()

    # показываем поля регистрации исследователя
    def show_researcher_fields(self):
        self.title_label = QLabel("Регистрация исследователя")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)  # Перенос текста
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        self.panel_layout.addWidget(self.title_label)

        # поле подтверждения пароля
        confirm_password_label = QLabel("Подтвердите пароль:")
        confirm_password_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(confirm_password_label)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.confirm_password_input)

        # поле для ФИО
        name_label = QLabel("ФИО:")
        name_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ФИО")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.name_input)

        # поле для даты рождения
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        self.dob_input.setMinimumWidth(150)
        self.dob_input.setStyleSheet("""
            QDateEdit {
                background-color: white; 
                color: black; 
                padding: 8px; 
                font-size: 14px; 
                border: 1px solid #ccc; 
                border-radius: 5px;
            }
            QDateEdit QCalendarWidget {
                background-color: white;  /* Белый фон для календаря */
                min-width: 300px;  /* Увеличение ширины календаря */
            }
            QDateEdit QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;  /* Белый фон для навигационной панели */
                color: black;  /* Черный текст */
                min-width: 300px;
            }
            QDateEdit QCalendarWidget QTableView {
                background-color: white;  /* Белый фон для таблицы дат */
                color: black;  /* Черный текст */
                min-width: 300px;
            }
            QDateEdit QCalendarWidget QTableView QHeaderView::section {
                background-color: white;  /* Белый фон для заголовков */
                color: black;  /* Черный текст */
            }
        """)
        self.panel_layout.addWidget(self.dob_input)

        # кнопка завершения регистрации
        complete_button = QPushButton("Завершить регистрацию")
        complete_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        complete_button.clicked.connect(self.complete_researcher_registration)
        self.panel_layout.addWidget(complete_button)

        # кнопка отмены
        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        cancel_button.clicked.connect(self.return_to_initial_form)
        self.panel_layout.addWidget(cancel_button)

    # показываем поля регистрации исследуемого
    def show_investigated_fields(self):
        self.title_label = QLabel("Регистрация исследуемого")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)  # Перенос текста
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        self.panel_layout.addWidget(self.title_label)

        # поле подтверждения пароля
        confirm_password_label = QLabel("Подтвердите пароль:")
        confirm_password_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(confirm_password_label)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.confirm_password_input)

        # поле для ФИО
        name_label = QLabel("ФИО:")
        name_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ФИО")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.name_input)

        # поле для даты рождения
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        self.dob_input.setMinimumWidth(150)
        self.dob_input.setStyleSheet("""
            QDateEdit {
                background-color: white; 
                color: black; 
                padding: 8px; 
                font-size: 14px; 
                border: 1px solid #ccc; 
                border-radius: 5px;
            }
            QDateEdit QCalendarWidget {
                background-color: white;  /* Белый фон для календаря */
                min-width: 300px;  /* Увеличение ширины календаря */
            }
            QDateEdit QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;  /* Белый фон для навигационной панели */
                color: black;  /* Черный текст */
                min-width: 300px;
            }
            QDateEdit QCalendarWidget QTableView {
                background-color: white;  /* Белый фон для таблицы дат */
                color: black;  /* Черный текст */
                min-width: 300px;
            }
            QDateEdit QCalendarWidget QTableView QHeaderView::section {
                background-color: white;  /* Белый фон для заголовков */
                color: black;  /* Черный текст */
            }
        """)
        self.panel_layout.addWidget(self.dob_input)

        researcher_label = QLabel("Мой исследователь:")
        researcher_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(researcher_label)

        self.researcher_combobox = QComboBox()
        self.researcher_combobox.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        researchers = self.get_researchers()
        self.researcher_combobox.addItem("Не выбрано", None)
        for researcher in researchers:
            self.researcher_combobox.addItem(researcher[1], researcher[0])
        self.panel_layout.addWidget(self.researcher_combobox)

        # поле для рода деятельности
        occupation_label = QLabel("Род деятельности:")
        occupation_label.setStyleSheet("font-size: 14px; color: #333;")
        self.panel_layout.addWidget(occupation_label)
        self.occupation_input = QLineEdit()
        self.occupation_input.setPlaceholderText("Введите род деятельности")
        self.occupation_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.panel_layout.addWidget(self.occupation_input)

        # кнопка завершения регистрации
        complete_button = QPushButton("Завершить регистрацию")
        complete_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        complete_button.clicked.connect(self.complete_investigated_registration)
        self.panel_layout.addWidget(complete_button)

        # кнопка отмены
        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        cancel_button.clicked.connect(self.return_to_initial_form)
        self.panel_layout.addWidget(cancel_button)

    # функция возврата к начальному состоянию
    def return_to_initial_form(self):
        self.clear_layout()
        self.run_initial_form()

    # функция регистрации исследователя
    def complete_researcher_registration(self):
        login = self.login_input.text()                               # снимаем логин
        password = self.password_input.text()                         # снимаем пароль
        confirm_password = self.confirm_password_input.text()         # снимаем подтверждение пароля
        full_name = self.name_input.text()                            # снимаем фио
        date_of_birth = self.dob_input.date().toString("yyyy-MM-dd")  # снимаем дату рождения

        # если не все поля заполнены, то просим дозаполнить
        if not all([login, password, confirm_password, full_name]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        # если пароли не совпадают, то просим чтобы совпали
        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        # подключение к БД 
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            
            # выполнение SQL-запроса по добавлению в таблицу пользователей
            cursor.execute("""
                INSERT INTO Users (Full_name, Login, Password, Role, Date_of_birth, ResearcherId)
                VALUES (?, ?, ?, 'Исследователь', ?, NULL)
            """, (full_name, login, password, date_of_birth))
            
            user_id = cursor.lastrowid  # запрашиваем последний айдишник 
            
            # выполнение SQL-запроса по добавлению в таблицу исследователей
            cursor.execute("""
                INSERT INTO Researcher_Details (UserId, Number_of_patients)
                VALUES (?, 0)
            """, (user_id,))
            
            conn.commit()
            QMessageBox.information(self, "Успех", "Исследователь успешно зарегистрирован!")
            self.return_to_initial_form()
        except sqlite3.IntegrityError as e:
            QMessageBox.warning(self, "Ошибка", "Логин или ФИО уже существуют!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
        finally:
            conn.close()

    # функция регистрации исследуемого
    def complete_investigated_registration(self):
        login = self.login_input.text()                                # снимаем логин
        password = self.password_input.text()                          # снимаем пароль
        confirm_password = self.confirm_password_input.text()          # снимаем подтверждение пароля
        full_name = self.name_input.text()                             # снимаем фио
        date_of_birth = self.dob_input.date().toString("yyyy-MM-dd")   # снимаем дату рождения
        researcher_id = self.researcher_combobox.currentData()         # снимаем выбранного исследователя
        occupation = self.occupation_input.text()                      # снимаем род деятельности

        # если не все поля заполнены, то просим дозаполнить
        if not all([login, password, confirm_password, full_name, occupation]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        # если пароли не совпадают, то просим чтобы совпали
        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        # подключение к БД 
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            
            # выполнение SQL-запроса по добавлению в таблицу пользователей
            cursor.execute("""
                INSERT INTO Users (Full_name, Login, Password, Role, Date_of_birth, ResearcherId)
                VALUES (?, ?, ?, 'Исследуемый', ?, ?)
            """, (full_name, login, password, date_of_birth, researcher_id))
            
            user_id = cursor.lastrowid
            
            # выполнение SQL-запроса по добавлению в таблицу исследованных
            cursor.execute("""
                INSERT INTO Investigated_Details (UserId, Occupation, EfficiencyWithMusic, EfficiencyWithoutMusic)
                VALUES (?, ?, NULL, NULL)
            """, (user_id, occupation))
            
            # увеличиваем число исследуемых у выбранного исследователя
            if researcher_id:
                cursor.execute("""
                    UPDATE Researcher_Details 
                    SET Number_of_patients = Number_of_patients + 1 
                    WHERE UserId = ?
                """, (researcher_id,))
            
            conn.commit()
            QMessageBox.information(self, "Успех", "Исследуемый успешно зарегистрирован!")
            self.return_to_initial_form()
        except sqlite3.IntegrityError as e:
            QMessageBox.warning(self, "Ошибка", "Логин или ФИО уже существуют!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
        finally:
            conn.close()

    # функция авторизации с проверкой по базе данных
    def handle_login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if not all([login, password]):
            QMessageBox.warning(self, "Ошибка", "Логин и пароль должны быть заполнены!")
            return

        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Password, Role FROM Users WHERE Login = ?", (login,))
            user = cursor.fetchone()
            if user and user[1] == password:
                user_id, _, role = user
                if role == 'Исследуемый' and self.investigated_checkbox.isChecked():
                    self.show_investigated_dashboard(user_id)
                elif role == 'Исследователь' and self.researcher_checkbox.isChecked():
                    self.show_researcher_dashboard(user_id)
                else:
                    QMessageBox.warning(self, "Ошибка", "Роль не соответствует выбранной!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
        finally:
            conn.close()

    # окно исследуемого после авторизации
    def show_investigated_dashboard(self, user_id):
        self.clear_layout()
        self.registration_panel.setFixedSize(300, 200)

        start_test_button = QPushButton("Начать тест")
        start_test_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        start_test_button.clicked.connect(lambda: self.start_test(user_id))
        self.panel_layout.addWidget(start_test_button)

        logout_button = QPushButton("Выйти")
        logout_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        logout_button.clicked.connect(self.return_to_initial_form)
        self.panel_layout.addWidget(logout_button)

    # окно исследователя после авторизации
    def show_researcher_dashboard(self, user_id):
        self.clear_layout()
        self.registration_panel.setFixedSize(800, 500)  # Увеличиваем размер панели

        logout_button = QPushButton("Выйти")
        logout_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        logout_button.clicked.connect(self.return_to_initial_form)
        self.panel_layout.addWidget(logout_button)

        # коннектимся к базе данных
        try:
            conn = sqlite3.connect("database/database.sqlite")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.Id, u.Full_name, u.Date_of_birth, id.Occupation, id.EfficiencyWithMusic, id.EfficiencyWithoutMusic
                FROM Users u
                LEFT JOIN Investigated_Details id ON u.Id = id.UserId
                WHERE u.Role = 'Исследуемый' AND u.ResearcherId = ?
            """, (user_id,))
            subjects = cursor.fetchall()
            conn.close()

            table = QTableWidget()
            table.setRowCount(len(subjects))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ФИО", "Дата рождения", "Род деятельности", "Эфф. с музыкой (сек/прав. отв.)", "Эфф. без музыки (сек/прав. отв.)"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # высота строк
            for row in range(len(subjects)):
                table.setRowHeight(row, 40)  # Устанавливаем высоту строки 40 пикселей

            # шрифт заголовков
            header_font = QFont()
            header_font.setPointSize(8)  # Размер шрифта для заголовков
            table.horizontalHeader().setFont(header_font)

            # заполняем таблицу
            for row, subject in enumerate(subjects):
                for col, value in enumerate(subject):
                    item = QTableWidgetItem(str(value) if value is not None else "N/A")
                    item.setTextAlignment(Qt.AlignCenter)
                    font = QFont()
                    font.setPointSize(8)  # размер шрифта для ячеек
                    item.setFont(font)
                    table.setItem(row, col, item)
            self.panel_layout.addWidget(table)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    # функция возврата к начальному состоянию
    def return_to_initial_form(self):
        self.clear_layout()
        self.registration_panel.setFixedSize(300, 450)
        self.run_initial_form()

    # старт теста
    def start_test(self, user_id):
        # формируем очередь из 10000 id примеров в случайном порядке
        total_examples = 10000  
        example_ids = random.sample(range(1, total_examples + 1), total_examples)  

        # окно теста
        self.test_window = TestWindow(user_id, example_ids, self)
        self.test_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())