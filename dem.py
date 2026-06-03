import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# Глобальная переменная для роли
current_role = ""

# --- ОКНО ВХОДА С ВЫБОРОМ РОЛИ ---
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор роли")
        self.setGeometry(300, 300, 300, 200)
        
        layout = QVBoxLayout()
        
        label = QLabel("Выберите вашу роль:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Кнопки для выбора роли
        self.admin_btn = QPushButton("Администратор")
        self.manager_btn = QPushButton("Менеджер")
        self.user_btn = QPushButton("Пользователь")
        
        self.admin_btn.clicked.connect(lambda: self.set_role("Администратор"))
        self.manager_btn.clicked.connect(lambda: self.set_role("Менеджер"))
        self.user_btn.clicked.connect(lambda: self.set_role("Пользователь"))
        
        layout.addWidget(self.admin_btn)
        layout.addWidget(self.manager_btn)
        layout.addWidget(self.user_btn)
        
        self.setLayout(layout)
    
    def set_role(self, role):
        global current_role
        current_role = role
        self.open_table_window()
    
    def open_table_window(self):
        self.table_window = TableWindow()
        self.table_window.show()
        self.close()

# --- ОКНО ДЛЯ ОТОБРАЖЕНИЯ ТАБЛИЦ ---
class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Просмотр таблиц - Роль: {current_role}")
        self.setGeometry(200, 200, 800, 500)
        
        layout = QVBoxLayout()
        
        # Информация о роли
        role_label = QLabel(f"Вы вошли как: {current_role}")
        role_label.setStyleSheet("font-weight: bold; padding: 10px; background-color: lightgray;")
        layout.addWidget(role_label)
        
        # Кнопки для выбора таблицы
        btn_layout = QHBoxLayout()
        
        self.tovar_btn = QPushButton("Таблица Товары")
        self.order_btn = QPushButton("Таблица Заказы")
        self.user_btn = QPushButton("Таблица Пользователи")
        
        self.tovar_btn.clicked.connect(lambda: self.load_table("tovar"))
        self.order_btn.clicked.connect(lambda: self.load_table("orders"))
        self.user_btn.clicked.connect(lambda: self.load_table("user"))
        
        btn_layout.addWidget(self.tovar_btn)
        btn_layout.addWidget(self.order_btn)
        btn_layout.addWidget(self.user_btn)
        
        layout.addLayout(btn_layout)
        
        # Таблица для отображения данных
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # Кнопка выхода
        exit_btn = QPushButton("Выйти")
        exit_btn.clicked.connect(self.exit_app)
        layout.addWidget(exit_btn)
        
        self.setLayout(layout)
        
        # Подключаемся к БД
        self.connect_to_db()
    
    def connect_to_db(self):
        try:
            self.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='demo2026'
            )
            self.cursor = self.db.cursor()
            QMessageBox.information(self, "Успех", "Подключение к БД установлено!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к БД:\n{str(e)}")
    
    def load_table(self, table_name):
        """Загружает и отображает данные из указанной таблицы"""
        try:
            # Получаем данные
            self.cursor.execute(f"SELECT * FROM {table_name}")
            data = self.cursor.fetchall()
            
            # Получаем названия колонок
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [col[0] for col in self.cursor.fetchall()]
            
            # Настраиваем таблицу
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            
            # Заполняем данными
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            
            # Растягиваем колонки
            self.table.resizeColumnsToContents()
            
            QMessageBox.information(self, "Успех", f"Загружено {len(data)} записей из таблицы '{table_name}'")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить таблицу:\n{str(e)}")
    
    def exit_app(self):
        self.close()
        # Возвращаемся к окну входа
        self.login_window = LoginWindow()
        self.login_window.show()

# --- ЗАПУСК ПРИЛОЖЕНИЯ ---
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec_())