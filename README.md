# code-refactor-tool
# 🐍 Python Code Refactor Tool
A web-based tool that automatically analyzes and refactors Python code using AST parsing and intelligent algorithms. Perfect for improving code quality and learning best practices.

## 🌐 Live Demo

**Try it now:** [https://code-refactor-tool-production.up.railway.app](https://code-refactor-tool-production.up.railway.app) 

**Or:** [https://code-refactor-tool.onrender.com](https://code-refactor-tool.onrender.com)

## ✨ Features

- **🔍 AST-Based Analysis** - Deep code analysis using Python's Abstract Syntax Trees
- **🔤 Smart Variable Renaming** - Automatically renames unclear single-letter variables
- **🔄 Conditional Simplification** - Extracts complex conditionals into readable variables
- **📝 Duplicate Code Detection** - Identifies and highlights repeated code patterns
- **🎨 Beautiful Web Interface** - Modern, responsive UI with syntax highlighting
- **⚡ Real-time Processing** - Instant refactoring results
- **📊 Code Quality Suggestions** - Actionable improvement recommendations

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, AST parsing
- **Frontend:** HTML5, CSS3, JavaScript, Prism.js
- **Deployment:** Railway, Uvicorn
- **Analysis:** AST, astor, custom refactoring algorithms

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/code-refactor-tool.git
   cd code-refactor-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Open your browser**
   Navigate to http://localhost:8000

### Using Docker
```bash
# Build and run with Docker
docker build -t code-refactor-tool .
docker run -p 8000:8000 code-refactor-tool
```
## 📖 Usage
### Web Interface
Paste your Python code in the left editor
Select refactoring options:
✅ Rename Unclear Variables
✅ Extract Duplicate Code
✅ Simplify Complex Conditionals
✅ Extract Methods
✅ Remove Dead Code

Click "Refactor Code" or press Ctrl+Enter
View results in the refactored code panel
Check suggestions for further improvements

## Keyboard Shortcuts
Ctrl+Enter - Refactor code
Ctrl+/ - Focus code editor
Esc - Clear code editor

## Sample Codes
The tool includes several sample codes to test:
Complex Function - Long functions with multiple responsibilities
Nested Conditionals - Deeply nested if-else statements
Duplicate Code - Repeated logic across functions
Messy Variables - Poorly named single-letter variables
