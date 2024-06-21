#!/usr/bin/python3

import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QFormLayout, QTextEdit
from PyQt6.QtCore import Qt

class KeyEnrollApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Key Enrollment with mokutil")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Create, enroll, or unenroll a signing key")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.warning_text = QTextEdit()
        self.warning_text.setReadOnly(True)
        self.warning_text.setText(
            "Warning: Enrolling a self-signed key for Secure Boot carries certain risks.\n\n"
            "1. If the key is compromised, it could allow malicious software to bypass Secure Boot protections.\n"
            "2. Ensure the key is stored securely and only enroll keys from trusted sources.\n"
            "3. If you're not familiar with the implications of using a self-signed key, seek advice from a knowledgeable source.\n\n"
            "Password Requirements: Use only upper case letters, lower case letters, and numbers. Do not use symbols or special characters."
        )
        layout.addWidget(self.warning_text)

        form_layout = QFormLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)

        layout.addLayout(form_layout)

        self.button_create_key = QPushButton("Create and Enroll Signing Key")
        self.button_create_key.clicked.connect(self.create_and_enroll_signing_key)
        layout.addWidget(self.button_create_key)

        self.button_unenroll_key = QPushButton("Unenroll Signing Key")
        self.button_unenroll_key.clicked.connect(self.unenroll_signing_key)
        layout.addWidget(self.button_unenroll_key)

        self.setLayout(layout)
        self.certs_directory = "/etc/pki/akmods/certs/"

    def check_secure_boot(self):
        try:
            sb_state = subprocess.run(['mokutil', '--sb-state'], check=True, capture_output=True, text=True)
            if "SecureBoot enabled" not in sb_state.stdout:
                self.label.setText("Secure Boot is not enabled.")
                QMessageBox.warning(self, "Warning", "Secure Boot is not enabled. Exiting.")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            self.label.setText(f"Error checking Secure Boot state: {e.stderr}")
            QMessageBox.critical(self, "Error", f"Error checking Secure Boot state: {e.stderr}")
            sys.exit(1)

    def create_and_enroll_signing_key(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            self.label.setText("Passwords do not match.")
            QMessageBox.warning(self, "Warning", "Passwords do not match.")
            return

        if not password:
            self.label.setText("Password cannot be empty.")
            QMessageBox.warning(self, "Warning", "Password cannot be empty.")
            return

        if not password.isalnum():
            self.label.setText("Password must only contain upper case letters, lower case letters, and numbers.")
            QMessageBox.warning(self, "Warning", "Password must only contain upper case letters, lower case letters, and numbers.")
            return

        try:
            # Create the signing key
            create_key_result = subprocess.run(['/usr/sbin/kmodgenca', '-a'], check=True, capture_output=True, text=True)
            self.label.setText("Signing key created at /etc/pki/akmods/certs/public_key.der")
            QMessageBox.information(self, "Success", "Signing key created successfully.")
            
            # Enroll the signing key
            enroll_key_result = subprocess.run(['mokutil', '--import', os.path.join(self.certs_directory, 'public_key.der')], input=f"{password}\n{password}\n", text=True, check=True, capture_output=True)
            self.label.setText("Key successfully enrolled. Reboot to complete.")
            QMessageBox.information(self, "Success", "Key successfully enrolled. Reboot to complete.")
        
        except subprocess.CalledProcessError as e:
            self.label.setText(f"Error: {e.stderr}")
            QMessageBox.critical(self, "Error", f"Error: {e.stderr}")

    def unenroll_signing_key(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            self.label.setText("Passwords do not match.")
            QMessageBox.warning(self, "Warning", "Passwords do not match.")
            return

        if not password:
            self.label.setText("Password cannot be empty.")
            QMessageBox.warning(self, "Warning", "Password cannot be empty.")
            return

        if not password.isalnum():
            self.label.setText("Password must only contain upper case letters, lower case letters, and numbers.")
            QMessageBox.warning(self, "Warning", "Password must only contain upper case letters, lower case letters, and numbers.")
            return

        try:
            # Unenroll the signing key
            unenroll_key_result = subprocess.run(['mokutil', '--delete', os.path.join(self.certs_directory, 'public_key.der')], input=f"{password}\n{password}\n", text=True, check=True, capture_output=True)
            if unenroll_key_result.returncode == 0:
                self.label.setText("Key successfully unenrolled. Reboot to complete.")
                QMessageBox.information(self, "Success", "Key successfully unenrolled. Reboot to complete.")

                # Remove all files in /etc/pki/akmods/certs/
                try:
                    for filename in os.listdir(self.certs_directory):
                        file_path = os.path.join(self.certs_directory, filename)
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            os.rmdir(file_path)
                    self.label.setText("All key files removed from /etc/pki/akmods/certs/")
                    QMessageBox.information(self, "Success", "All key files removed from /etc/pki/akmods/certs/")
                except Exception as e:
                    self.label.setText(f"Failed to delete files. Reason: {str(e)}")
                    QMessageBox.critical(self, "Error", f"Failed to delete files. Reason: {str(e)}")

        except subprocess.CalledProcessError as e:
            self.label.setText(f"Error: {e.stderr}")
            QMessageBox.critical(self, "Error", f"Error: {e.stderr}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyEnrollApp()
    window.check_secure_boot()
    window.show()
    sys.exit(app.exec())

