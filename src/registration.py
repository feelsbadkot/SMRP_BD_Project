import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QDateEdit
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QDate


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())