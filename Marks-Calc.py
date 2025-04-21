import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "F": 0
}

# ---------- DARK THEME ----------
def apply_dark_theme(app):
    dark_stylesheet = """
    QWidget {
        background-color: #282c34;
        color: #ffffff;
        font-size: 18px;
    }
    QLabel {
        color: #61dafb;
        font-weight: bold;
    }
    QLineEdit, QTextEdit, QComboBox {
        background-color: #3c4049;
        color: white;
        border-radius: 6px;
        padding: 8px;
        font-size: 18px;
    }
    QPushButton {
        background-color: #61dafb;
        color: #1e1e2f;
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #4fa3d1;
    }
    QTableWidget {
        background-color: #3c4049;
        color: white;
        gridline-color: #61dafb;
        font-size: 18px;
    }
    QHeaderView::section {
        background-color: #61dafb;
        color: #1e1e2f;
        font-size: 18px;
    }
    """
    app.setStyleSheet(dark_stylesheet)

# ---------- MAIN MENU ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 Academic Toolkit")
        self.showFullScreen()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Academic Toolkit")
        title.setFont(QFont("Arial", 36, QFont.Bold))
        layout.addWidget(title)

        btn_marks = QPushButton("📘 Marks Calculator")
        btn_gpa = QPushButton("📊 GPA Calculator")

        for btn in (btn_marks, btn_gpa):
            btn.setFixedHeight(60)
            btn.setFont(QFont("Arial", 20))
            layout.addWidget(btn)

        self.setLayout(layout)

        self.stack = QStackedWidget()
        self.stack.addWidget(self)
        self.marks_calculator = MarksCalculator(self.stack)
        self.gpa_calculator = GPACalculator(self.stack)

        btn_marks.clicked.connect(lambda: self.stack.setCurrentWidget(self.marks_calculator))
        btn_gpa.clicked.connect(lambda: self.stack.setCurrentWidget(self.gpa_calculator))

# ---------- MARKS CALCULATOR ----------
class MarksCalculator(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        layout = QVBoxLayout()

        title = QLabel("📘 Marks Calculator")
        title.setFont(QFont("Arial", 32))
        layout.addWidget(title)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter internal marks (out of 60)")
        layout.addWidget(self.input)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        btn_calc = QPushButton("Calculate")
        btn_calc.clicked.connect(self.calculate)
        layout.addWidget(btn_calc)

        btn_back = QPushButton("⬅️ Back to Menu")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        self.setLayout(layout)
        self.stack.addWidget(self)

    def calculate(self):
        try:
            internal = int(self.input.text())
            if not 0 <= internal <= 60:
                raise ValueError()

            result = ""
            total_required = 50
            external_needed = total_required - internal
            marks_out_of_75 = (external_needed / 40) * 75 if external_needed > 0 else 0

            if external_needed <= 0:
                result += "✅ You already have enough marks to pass!\n\n"
            else:
                result += f"📘 You need {external_needed} out of 40 in externals\n"
                result += f"➡️ Which means {marks_out_of_75:.2f} out of 75\n\n"

            grades = {"O": 91, "A+": 81, "A": 71, "B+": 61, "B": 51}
            result += "📊 Marks required for different grades:\n"
            for grade, min_marks in grades.items():
                needed = min_marks - internal
                ext_75 = (needed / 40) * 75 if needed > 0 else 0
                if needed > 40:
                    result += f"{grade}: ❌ Not possible\n"
                elif needed <= 0:
                    result += f"{grade}: ✅ Already secured\n"
                else:
                    result += f"{grade}: Need {needed} out of 40 ({ext_75:.2f} / 75)\n"

            self.result.setText(result)
        except:
            self.result.setText("❗ Please enter a valid number between 0 and 60.")

# ---------- GPA CALCULATOR ----------
class GPACalculator(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.subjects = []

        layout = QVBoxLayout()

        title = QLabel("📊 GPA Calculator")
        title.setFont(QFont("Arial", 32))
        layout.addWidget(title)

        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Subject Name")

        self.grade_input = QComboBox()
        self.grade_input.addItems(GRADE_POINTS.keys())

        self.credit_input = QLineEdit()
        self.credit_input.setPlaceholderText("Credits")

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.grade_input)
        input_layout.addWidget(self.credit_input)

        btn_add = QPushButton("Add Subject")
        btn_add.clicked.connect(self.add_subject)
        input_layout.addWidget(btn_add)

        layout.addLayout(input_layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Subject", "Grade", "Credits"])
        layout.addWidget(self.table)

        self.gpa_label = QLabel("GPA: N/A")
        self.gpa_label.setFont(QFont("Arial", 22))
        layout.addWidget(self.gpa_label)

        btn_calc = QPushButton("Calculate GPA")
        btn_calc.clicked.connect(self.calculate_gpa)
        layout.addWidget(btn_calc)

        btn_back = QPushButton("⬅️ Back to Menu")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        self.setLayout(layout)
        self.stack.addWidget(self)

    def add_subject(self):
        name = self.name_input.text()
        grade = self.grade_input.currentText()
        try:
            credits = float(self.credit_input.text())
        except ValueError:
            return

        self.subjects.append((name, grade, credits))
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(grade))
        self.table.setItem(row, 2, QTableWidgetItem(str(credits)))

        self.name_input.clear()
        self.credit_input.clear()

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for subject in self.subjects:
            grade, credits = subject[1], subject[2]
            total_points += GRADE_POINTS.get(grade, 0) * credits
            total_credits += credits

        if total_credits == 0:
            self.gpa_label.setText("GPA: N/A")
        else:
            gpa = total_points / total_credits
            self.gpa_label.setText(f"GPA: {gpa:.2f}")

# ---------- RUN APP ----------
def run_app():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    stacked = window.stack
    stacked.showFullScreen()
    stacked.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
