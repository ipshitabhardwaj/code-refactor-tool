"""
Code analysis and smell detection utilities
"""

def detect_code_smells(analysis: dict) -> list:
    """Detect various code smells from analysis data"""
    smells = []
    
    # Long method smell
    for func in analysis.get("long_functions", []):
        if func["lines"] > 15:
            smells.append({
                "type": "LONG_METHOD",
                "message": f"Function '{func['name']}' is too long ({func['lines']} lines)",
                "line": func["line"],
                "severity": "MEDIUM"
            })
    
    # Unclear variable names
    for var in analysis.get("unclear_variables", []):
        smells.append({
            "type": "UNCLEAR_VARIABLE",
            "message": f"Variable '{var['name']}' has unclear name",
            "line": var["line"],
            "severity": "LOW"
        })
    
    # Complex conditionals
    for conditional in analysis.get("complex_conditionals", []):
        if conditional["complexity"] > 3:
            smells.append({
                "type": "COMPLEX_CONDITIONAL",
                "message": "Overly complex conditional logic",
                "line": conditional["line"],
                "severity": "MEDIUM"
            })
    
    return smells

def get_code_metrics(code: str) -> dict:
    """Calculate basic code metrics"""
    try:
        tree = compile(code, '<string>', 'exec', ast.PyCF_ONLY_AST)
        
        metrics = {
            "lines_of_code": len(code.split('\n')),
            "function_count": 0,
            "class_count": 0,
            "average_function_length": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics["function_count"] += 1
            elif isinstance(node, ast.ClassDef):
                metrics["class_count"] += 1
        
        return metrics
    except:
        return {"error": "Could not calculate metrics"}