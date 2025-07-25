# Contributing to FedRAMP Analysis Hub

Thank you for your interest in contributing to the FedRAMP Analysis Hub! This document provides guidelines for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How to Contribute

### Reporting Issues

- Check if the issue already exists in the [Issues](https://github.com/yourusername/fedramp-analysis-hub/issues) section
- Provide a clear and descriptive title
- Include steps to reproduce the issue
- Specify your environment (OS, Python version, etc.)

### Suggesting Enhancements

- Open an issue with the `enhancement` label
- Clearly describe the enhancement and its benefits
- Provide examples of how it would work

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure the app works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/yourusername/fedramp-analysis-hub.git
cd fedramp-analysis-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
```

### Coding Standards

- Follow PEP 8 for Python code
- Add docstrings to functions and classes
- Keep functions focused and small
- Write descriptive variable names
- Add comments for complex logic

### Testing

- Test your changes locally before submitting
- Ensure all pages load without errors
- Verify search functionality works
- Check that exports function correctly

### Documentation

- Update README.md if needed
- Add docstrings to new functions
- Include comments for complex logic
- Update requirements.txt for new dependencies

## Questions?

Feel free to open an issue for any questions about contributing.