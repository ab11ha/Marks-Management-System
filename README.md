# Marks Management System with Homomorphic Encryption

## Introduction

This project presents a secure and privacy-focused Marks Management System implemented using Homomorphic Encryption techniques in Python and Flask. The system enables professors to add marks for students, ensuring that the marks remain encrypted using the Paillier encryption scheme. Students can securely access and view their percentage marks, while the original marks are never decrypted.

## Features

- **Homomorphic Encryption:** The system leverages the Paillier encryption class to securely encrypt student marks, ensuring privacy while performing mathematical operations on the encrypted data.
- **Professor's Interface:** Professors can log in securely and add marks for their students through an intuitive and user-friendly web interface.
- **Student's Interface:** Students can access the system to view their percentage marks without compromising the privacy of the encrypted original marks.
- **Database Integration:** The system incorporates a SQL database (e.g., SQLite, MySQL, PostgreSQL) to store encrypted marks, user credentials, and other essential information.
- **Data Security:** The original marks are kept encrypted in the database at all times, ensuring that sensitive information remains confidential.
- **Scalable and Maintainable:** The codebase is designed to be scalable and maintainable, facilitating future enhancements and updates.

## Getting Started

To run the Marks Management System locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your_username/marks-management-system.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the database: The database will be set by itself once you run the code.
4.  
5. Access the system in your web browser at `http://localhost:5000`

## Dependencies

- Python 3.x
- Flask
- Flask SQLAlchemy
- Crypto
- [Database of your choice, e.g., SQLite, MySQL, PostgreSQL]

