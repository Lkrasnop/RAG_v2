# RAG_v2 Project
[![CI/CD Pipeline](https://github.com/Lkrasnop/RAG_v2/actions/workflows/main.yml/badge.svg)](https://github.com/Lkrasnop/RAG_v2/actions/workflows/main.yml)

Here’s a full README file for your project based on the structure and files in the provided image:

## Overview
RAG_V2 is a modular project designed to leverage Retrieval-Augmented Generation (RAG) techniques. The project structure is organized for maintainability, scalability, and ease of use. It includes support for PDF processing, testing, and document analysis.

## Directory Structure
The project is organized as follows:

```
RAG_V2/
├── __pycache__/         # Python cache files (auto-generated)
├── .github/             # GitHub workflows and actions
├── .pytest_cache/       # Pytest cache files
├── db/                  # Database files (if any)
├── pdf/                 # PDF files for testing/processing
├── text/                # Text files for testing/processing
├── .env                 # Environment variables (not committed to Git)
├── .gitignore           # Git ignore file
├── dockerfile           # Dockerfile for building the application
├── main_test.py         # Main test suite
├── main.py              # Main application entry point
├── MakeFile             # Makefile for automating common tasks
├── Notebook_v2.ipynb    # Jupyter notebook for prototyping
├── pdf_to_text_test.py  # Unit tests for PDF processing
├── pdf_to_text.py       # PDF processing script
├── README.md            # Project documentation (this file)
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites
- Python 3.10
- Docker
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/RAG_V2.git
   cd RAG_V2
   ```

2. **Set up the Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure the environment:**
   - Copy the `.env.example` file to `.env` and fill in the required environment variables.
   - **Note:** Make sure not to commit sensitive information. The `.env` file is ignored by Git.

### Running the Application

#### Using Python directly:
   ```bash
   python main.py
   ```

#### Using Docker:
   1. **Build the Docker image:**
      ```bash
      docker build -t rag_v2_app .
      ```

   2. **Run the Docker container:**
      ```bash
      docker run -it --rm rag_v2_app
      ```

### Testing

Run the tests using pytest:
```bash
pytest
```

## Makefile Commands

The `MakeFile` includes commands for common tasks. Examples:

- **Run the application:**
  ```bash
  make run
  ```

- **Clean up temporary files:**
  ```bash
  make clean
  ```

## Contributing

Contributions are welcome! Please follow the standard GitHub pull request process.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to all contributors and open-source projects that helped shape RAG_V2.

---

Feel free to modify the content to fit your specific needs!
