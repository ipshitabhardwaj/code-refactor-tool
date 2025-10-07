import ast
from typing import Dict, List, Any

def analyze_code(code: str) -> Dict[str, Any]:
    """Analyze Python code and return insights"""
    try:
        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return analyzer.get_analysis()
    except SyntaxError as e:
        return {"error": f"Syntax error: {e}", "long_functions": [], "unclear_variables": [], "complex_conditionals": []}
    except Exception as e:
        return {"error": f"Analysis error: {e}", "long_functions": [], "unclear_variables": [], "complex_conditionals": []}

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.analysis = {
            "long_functions": [],
            "duplicate_code": [],
            "unclear_variables": [],
            "complex_conditionals": [],
            "code_smells": []
        }
        self.current_function = None
        
    def visit_FunctionDef(self, node):
        # Track current function
        old_function = self.current_function
        self.current_function = node.name
        
        # Check function length
        function_lines = node.end_lineno - node.lineno if node.end_lineno else 0
        if function_lines > 15:
            self.analysis["long_functions"].append({
                "name": node.name,
                "lines": function_lines,
                "line": node.lineno
            })
        
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_Assign(self, node):
        # Check for unclear variable names
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                if len(var_name) == 1 and var_name not in ['i', 'j', 'k', 'x', 'y', 'z']:
                    self.analysis["unclear_variables"].append({
                        "name": var_name,
                        "line": node.lineno,
                        "context": self.current_function or "global"
                    })
        self.generic_visit(node)
    
    def visit_If(self, node):
        # Check complex conditionals
        complexity = self._check_conditional_complexity(node.test)
        if complexity > 2:
            self.analysis["complex_conditionals"].append({
                "line": node.lineno,
                "complexity": complexity
            })
        self.generic_visit(node)
    
    def _check_conditional_complexity(self, node) -> int:
        """Calculate complexity of a conditional expression"""
        if isinstance(node, (ast.BoolOp, ast.Compare)):
            count = 1
            for child in ast.iter_child_nodes(node):
                count += self._check_conditional_complexity(child)
            return count
        return 0
    
    def get_analysis(self):
        return self.analysis

def get_suggestions(analysis: Dict[str, Any]) -> List[str]:
    """Generate human-readable suggestions from analysis"""
    suggestions = []
    
    if "error" in analysis:
        return [f"❌ {analysis['error']}"]
    
    for long_func in analysis.get("long_functions", []):
        suggestions.append(
            f"📏 Function '{long_func['name']}' is {long_func['lines']} lines long. Consider breaking it into smaller functions."
        )
    
    for var in analysis.get("unclear_variables", []):
        suggestions.append(
            f"🔤 Variable '{var['name']}' has an unclear name. Use more descriptive names."
        )
    
    for conditional in analysis.get("complex_conditionals", []):
        suggestions.append(
            f"🔀 Complex conditional on line {conditional['line']}. Consider extracting to a well-named function or variable."
        )
    
    if not suggestions:
        suggestions.append("✅ Code looks good! No major issues found.")
    
    return suggestions