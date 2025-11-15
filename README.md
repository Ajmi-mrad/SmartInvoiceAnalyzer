# Smart Invoice Analyzer 🧾

A modern invoice management system built with FastAPI, PostgreSQL, and JWT authentication.

## 🚀 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Invoice Management**: Full CRUD operations for invoices
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Security**: Password hashing with bcrypt
- **API Documentation**: Interactive Swagger UI
- **User Isolation**: Users can only access their own invoices

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Containerization**: Docker (for PostgreSQL)

## 📋 Prerequisites

- Python 3.8+
- Docker
- PostgreSQL (via Docker)
- Git

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/SmartInvoiceAnalyzer.git
cd SmartInvoiceAnalyzer
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL with Docker
```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=invoice_db \
  -p 5432:5432 \
  -d postgres
```

### 5. Create environment file
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/invoice_db
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run the application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Invoices (Protected Routes)
- `POST /invoices/` - Create a new invoice
- `GET /invoices/` - List user's invoices
- `GET /invoices/{id}` - Get specific invoice
- `PUT /invoices/{id}` - Update invoice
- `DELETE /invoices/{id}` - Delete invoice

## 🧪 Testing with Postman

### 1. Register a user
```json
POST /auth/register
{
    "username": "testuser",
    "password": "testpassword123"
}
```

### 2. Login to get token
```json
POST /auth/login
{
    "username": "testuser",
    "password": "testpassword123"
}
```

### 3. Create an invoice (use token from step 2)
```json
POST /invoices/
Headers: Authorization: Bearer <your_token>
{
    "supplier": "Electric Company",
    "total_amount": 245.67,
    "file_path": "/uploads/invoice.pdf"
}
```

## 📁 Project Structure

```
SmartInvoiceAnalyzer/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and routes
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── auth.py          # Authentication logic
│   └── utils.py         # Utility functions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- User isolation (users can only access their own data)
- Input validation with Pydantic
- Environment variables for sensitive configuration

## 🚀 Future Enhancements

- [ ] File upload functionality for invoice PDFs
- [ ] AI-powered invoice data extraction
- [ ] Email notifications
- [ ] Invoice categorization and tagging
- [ ] Dashboard and analytics
- [ ] Export to CSV/Excel

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name** - [Your GitHub Profile](https://github.com/yourusername)

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.
