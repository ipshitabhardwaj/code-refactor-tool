from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

app = FastAPI(title="Python Code Refactor Tool", version="1.0.0")

# Serve static files
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class CodeRequest(BaseModel):
    code: str
    refactor_options: list[str] = []

class RefactorResponse(BaseModel):
    original_code: str
    refactored_code: str
    changes_made: list[str]
    suggestions: list[str]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        html_path = os.path.join(static_dir, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found</h1>")

@app.post("/refactor", response_model=RefactorResponse)
async def refactor_code(request: CodeRequest):
    try:
        # Import here to avoid circular imports
        from app.refactor import ast_analyzer, refactor_rules
        
        # Analyze the code
        analysis = ast_analyzer.analyze_code(request.code)
        
        # Apply refactoring based on options
        refactored_code = request.code
        changes = []
        
        if "rename_variables" in request.refactor_options:
            refactored_code, rename_changes = refactor_rules.rename_unclear_variables(refactored_code)
            changes.extend(rename_changes)
            
        if "extract_duplicate" in request.refactor_options:
            refactored_code, extracted_changes = refactor_rules.extract_duplicate_functions(refactored_code)
            changes.extend(extracted_changes)
            
        if "simplify_conditionals" in request.refactor_options:
            refactored_code, conditional_changes = refactor_rules.simplify_complex_conditionals(refactored_code)
            changes.extend(conditional_changes)
        
        # New refactoring options
        if "extract_method" in request.refactor_options:
            refactored_code, method_changes = refactor_rules.extract_method(refactored_code)
            changes.extend(method_changes)
            
        if "remove_dead_code" in request.refactor_options:
            refactored_code, dead_code_changes = refactor_rules.remove_dead_code(refactored_code)
            changes.extend(dead_code_changes)
        
        # Get suggestions
        suggestions = ast_analyzer.get_suggestions(analysis)
        
        return RefactorResponse(
            original_code=request.code,
            refactored_code=refactored_code,
            changes_made=changes,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing code: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Code Refactor Tool"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)