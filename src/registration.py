import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt


class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registration")
        self.setGeometry(100, 100, 800, 600)  # размеры окна

        self.set_background()                 # установка фона

        # центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # панель регистрации
        registration_panel = QWidget(self)
        registration_panel.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        registration_panel.setFixedSize(300, 450)

        # вертикальная панель регистрации
        panel_layout = QVBoxLayout(registration_panel)

        # приветственный лейбл
        title_label = QLabel("Добро пожаловать!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        panel_layout.addWidget(title_label)

        who_label = QLabel("Кто Вы?")
        who_label.setAlignment(Qt.AlignCenter)
        who_label.setStyleSheet("font-size: 14px; color: #333;")
        panel_layout.addWidget(who_label)

        # чекбоксы на одной строке
        checkbox_layout = QHBoxLayout()

        # чекбокс с исследуемым
        self.investigated_checkbox = QCheckBox("Исследуемый")
        self.investigated_checkbox.setStyleSheet("font-size: 14px; color: #333;")
        self.investigated_checkbox.setChecked(True) 
        self.investigated_checkbox.stateChanged.connect(self.investigated_checkbox_changed)
        checkbox_layout.addWidget(self.investigated_checkbox)

        # чекбокс с исследователем
        self.researcher_checkbox = QCheckBox("Исследователь")
        self.researcher_checkbox.setStyleSheet("font-size: 14px; color: #333;")
        self.researcher_checkbox.stateChanged.connect(self.researcher_checkbox_changed)
        checkbox_layout.addWidget(self.researcher_checkbox)

        panel_layout.addLayout(checkbox_layout)

        # отображение того, кто выбран на данный момент
        self.role_label = QLabel("Вы: Исследуемый")
        self.role_label.setStyleSheet("font-size: 14px; color: #666;")
        panel_layout.addWidget(self.role_label)

        # поле ввода логина
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("font-size: 14px; color: #333;")
        panel_layout.addWidget(login_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        panel_layout.addWidget(self.login_input)

        # поле ввода пароля
        password_label = QLabel("Пароль:")
        password_label.setStyleSheet("font-size: 14px; color: #333;")
        panel_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        panel_layout.addWidget(self.password_input)

        # поле подтверждения пароля (изначально скрыто)
        self.confirm_password_label = QLabel("Подтвердите пароль:")
        self.confirm_password_label.setStyleSheet("font-size: 14px; color: #333;")
        self.confirm_password_label.setVisible(False)
        panel_layout.addWidget(self.confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.confirm_password_input.setVisible(False)
        panel_layout.addWidget(self.confirm_password_input)

        # кнопка регистрации
        register_button = QPushButton("Зарегистрироваться")
        register_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        register_button.clicked.connect(self.show_confirm_password)
        panel_layout.addWidget(register_button)

        # кнопка входа
        login_button = QPushButton("Войти")
        login_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-size: 14px; border: none; border-radius: 5px;")
        panel_layout.addWidget(login_button)

        # располагаем панель регистрации по центру
        layout.addWidget(registration_panel, alignment=Qt.AlignCenter)

    # функция подключения фона
    def set_background(self):
        pixmap = QPixmap("figures/background.jpg")
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

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

    # показываем поле для подтверждения пароля
    def show_confirm_password(self):
        self.confirm_password_label.setVisible(True)
        self.confirm_password_input.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())