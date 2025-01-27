# Awesome FastAPI Project

A FastAPI-based web application demonstrating Python class implementation with various magic methods and RESTful API endpoints.

## Features

- FastAPI web application setup
- Python class implementation with magic methods
- RESTful API endpoints (coming soon)
- Type hints and modern Python features

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd awesome-project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
.
├── README.md
├── main.py
└── .gitignore
```

## Development

The project currently includes a `Person` class implementation with various magic methods:

- `__str__`: String representation
- `__repr__`: Detailed string representation
- `__len__`: Length calculation
- `__eq__`: Equality comparison
- `__getitem__`: Dictionary-like access
- `__setitem__`: Dictionary-like assignment

### Example Usage

```python
# Create Person instances
p1 = Person(name="John")
p2 = Person(name="Jane")

# String representation
print(p1)  # Output: Person named John

# Length
print(len(p1))  # Output: 4

# Dictionary-like access
print(p1['name'])  # Output: John
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
