import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QSpinBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt


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
        self.setWindowTitle("ITU GPA Calculator")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Add logo
        self.logo_label = QLabel(self)
        try:
            pixmap = QPixmap("images.jpeg")  # Replace with the path to your logo image
            self.logo_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load logo image: {e}")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Add author information
        self.author_label = QLabel("Author: Haseeb Ur Rehman\nRollno: Bscs22115")
        self.author_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.author_label)

        self.num_courses_label = QLabel("Enter number of courses:")
        self.num_courses_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.layout.addWidget(self.num_courses_label)

        self.num_courses_input = QSpinBox()
        self.num_courses_input.setFont(QFont("Arial", 12))
        self.num_courses_input.setMinimum(1)
        self.layout.addWidget(self.num_courses_input)

        self.next_button = QPushButton("Next")
        self.next_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.next_button.clicked.connect(self.create_course_fields)
        self.layout.addWidget(self.next_button)

        self.course_fields_layout = QVBoxLayout()
        self.layout.addLayout(self.course_fields_layout)

        self.calculate_button = QPushButton("Calculate GPA")
        self.calculate_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.calculate_button.clicked.connect(self.calculate_gpa)
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.setEnabled(False)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Set background gradient
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 lightblue, stop:1 white
                );
            }
            QLabel, QLineEdit, QSpinBox, QPushButton {
                font-size: 14px;
            }
        """)

    def create_course_fields(self):
        try:
            # Hide the number of courses input and the next button
            self.num_courses_label.hide()
            self.num_courses_input.hide()
            self.next_button.hide()

            self.course_fields_layout.setParent(None)
            self.course_fields_layout = QVBoxLayout()
            self.layout.insertLayout(4, self.course_fields_layout)

            self.course_names = []
            self.course_credits = []
            self.course_grades = []

            num_courses = self.num_courses_input.value()

            for i in range(num_courses):
                course_layout = QHBoxLayout()

                course_name_input = QLineEdit()
                course_name_input.setPlaceholderText(f"Course {i+1} Name")
                course_name_input.setFont(QFont("Arial", 12))
                course_layout.addWidget(course_name_input)
                self.course_names.append(course_name_input)

                course_credit_input = QSpinBox()
                course_credit_input.setMinimum(1)
                course_credit_input.setMaximum(5)
                course_credit_input.setPrefix("Credits: ")
                course_credit_input.setFont(QFont("Arial", 12))
                course_layout.addWidget(course_credit_input)
                self.course_credits.append(course_credit_input)

                course_grade_input = QLineEdit()
                course_grade_input.setPlaceholderText("Grade")
                course_grade_input.setFont(QFont("Arial", 12))
                course_layout.addWidget(course_grade_input)
                self.course_grades.append(course_grade_input)

                self.course_fields_layout.addLayout(course_layout)

            self.calculate_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create course fields: {e}")

    def calculate_gpa(self):
        try:
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
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate GPA: {e}")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        calculator = GPA_Calculator()
        calculator.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An unexpected error occurred: {e}")