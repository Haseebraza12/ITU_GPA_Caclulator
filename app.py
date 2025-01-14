import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QSpinBox
)


class GPA_Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.grade_to_gpa = {
            "A+": 4.0, "A": 4.0, "A-": 3.67,
            "B+": 3.33, "B": 3.0, "B-": 2.67,
            "C+": 2.33, "C": 2.0, "C-": 1.67,
            "D+": 1.33, "D": 1.0, "F": 0.0,
        }

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GPA Calculator")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.num_courses_label = QLabel("Enter number of courses:")
        self.layout.addWidget(self.num_courses_label)

        self.num_courses_input = QSpinBox()
        self.num_courses_input.setMinimum(1)
        self.layout.addWidget(self.num_courses_input)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.create_course_fields)
        self.layout.addWidget(self.next_button)

        self.course_fields_layout = QVBoxLayout()
        self.layout.addLayout(self.course_fields_layout)

        self.calculate_button = QPushButton("Calculate GPA")
        self.calculate_button.clicked.connect(self.calculate_gpa)
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.setEnabled(False)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def create_course_fields(self):
        self.course_fields_layout.setParent(None)
        self.course_fields_layout = QVBoxLayout()
        self.layout.insertLayout(3, self.course_fields_layout)

        self.course_names = []
        self.course_credits = []
        self.course_grades = []

        num_courses = self.num_courses_input.value()

        for i in range(num_courses):
            course_layout = QHBoxLayout()

            course_name_input = QLineEdit()
            course_name_input.setPlaceholderText(f"Course {i+1} Name")
            course_layout.addWidget(course_name_input)
            self.course_names.append(course_name_input)

            course_credit_input = QSpinBox()
            course_credit_input.setMinimum(1)
            course_credit_input.setMaximum(5)
            course_credit_input.setPrefix("Credits: ")
            course_layout.addWidget(course_credit_input)
            self.course_credits.append(course_credit_input)

            course_grade_input = QLineEdit()
            course_grade_input.setPlaceholderText("Grade")
            course_layout.addWidget(course_grade_input)
            self.course_grades.append(course_grade_input)

            self.course_fields_layout.addLayout(course_layout)

        self.calculate_button.setEnabled(True)

    def calculate_gpa(self):
        total_credits = 0
        total_gpa = 0

        for i in range(len(self.course_names)):
            course_name = self.course_names[i].text().strip()
            course_credits = self.course_credits[i].value()
            course_grade = self.course_grades[i].text().strip().upper()

            if course_grade not in self.grade_to_gpa:
                QMessageBox.warning(self, "Invalid Grade", f"Invalid grade entered for {course_name}")
                return

            gpa = self.grade_to_gpa[course_grade]
            total_credits += course_credits
            total_gpa += gpa * course_credits

        if total_credits == 0:
            QMessageBox.warning(self, "No Credits", "Total credits cannot be zero.")
            return

        gpa_result = total_gpa / total_credits
        QMessageBox.information(self, "GPA Result", f"Your GPA is {gpa_result:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = GPA_Calculator()
    calculator.show()
    sys.exit(app.exec())