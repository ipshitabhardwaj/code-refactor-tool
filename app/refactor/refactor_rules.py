import ast
import astor
from typing import Tuple, List

def extract_duplicate_functions(code: str) -> Tuple[str, List[str]]:
    """Find and extract duplicate code patterns into functions"""
    changes = []
    
    try:
        # Simple duplicate detection by line
        lines = code.split('\n')
        seen_lines = {}
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip empty lines, comments, and very short lines
            if stripped and not stripped.startswith('#') and len(stripped) > 5:
                if stripped in seen_lines:
                    changes.append(f"Found duplicate code on line {i+1}: '{stripped[:40]}...'")
                else:
                    seen_lines[stripped] = i
        
        return code, changes
        
    except Exception as e:
        return code, [f"Could not analyze duplicates: {str(e)}"]

def rename_unclear_variables(code: str) -> Tuple[str, List[str]]:
    """Rename single-letter variables to more descriptive names"""
    changes = []
    
    try:
        tree = ast.parse(code)
        renamer = VariableRenamer()
        renamer.visit(tree)
        
        changes.extend(renamer.changes_made)
        refactored_code = astor.to_source(tree)
        
        return refactored_code, changes
        
    except Exception as e:
        return code, [f"Could not rename variables: {str(e)}"]

class VariableRenamer(ast.NodeVisitor):
    def __init__(self):
        self.changes_made = []
        self.renamed_vars = {}  # Track renames to update references
        
    def visit_FunctionDef(self, node):
        # Reset for each function to avoid cross-function renaming
        self.current_function_vars = {}
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                old_name = target.id
                # Only rename single-letter variables that aren't common loop counters
                if len(old_name) == 1 and old_name not in ['i', 'j', 'k', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'm', 'n']:
                    new_name = f"value_{old_name}"
                    target.id = new_name
                    self.renamed_vars[old_name] = new_name
                    self.changes_made.append(f"Renamed variable '{old_name}' to '{new_name}'")
        
        self.generic_visit(node)
    
    def visit_Name(self, node):
        # Update variable references
        if node.id in self.renamed_vars and isinstance(node.ctx, ast.Load):
            node.id = self.renamed_vars[node.id]
        self.generic_visit(node)

def simplify_complex_conditionals(code: str) -> Tuple[str, List[str]]:
    """Simplify complex if conditions"""
    changes = []
    
    try:
        tree = ast.parse(code)
        simplifier = ConditionalSimplifier()
        modified_tree = simplifier.visit(tree)
        
        changes.extend(simplifier.changes_made)
        refactored_code = astor.to_source(modified_tree)
        
        return refactored_code, changes
        
    except Exception as e:
        return code, [f"Could not simplify conditionals: {str(e)}"]

class ConditionalSimplifier(ast.NodeVisitor):
    def __init__(self):
        self.changes_made = []
        self.conditional_count = 0
        self.new_assignments = []
        
    def visit_Module(self, node):
        self.generic_visit(node)
        # Add new assignments at the beginning of functions
        return node
    
    def visit_FunctionDef(self, node):
        # Store original body
        original_body = node.body.copy()
        
        # Visit all nodes in the function
        self.generic_visit(node)
        
        # Insert new assignments after the function definition but before its body
        if self.new_assignments:
            node.body = self.new_assignments + original_body
            self.new_assignments = []
            
        return node
        
    def visit_If(self, node):
        # Check if this is a complex conditional
        if isinstance(node.test, ast.BoolOp) and len(node.test.values) > 2:
            self.conditional_count += 1
            var_name = f"should_execute_{self.conditional_count}"
            
            # Create a new assignment for the complex condition
            new_assign = ast.Assign(
                targets=[ast.Name(id=var_name, ctx=ast.Store())],
                value=node.test,
                lineno=node.lineno
            )
            
            # Add to new assignments list
            self.new_assignments.append(new_assign)
            
            # Replace the complex condition with the variable
            node.test = ast.Name(id=var_name, ctx=ast.Load())
            
            self.changes_made.append(f"Extracted complex conditional to variable '{var_name}'")
        
        self.generic_visit(node)

# NEW REFACTORING RULES

def extract_method(code: str) -> Tuple[str, List[str]]:
    """Extract duplicate code into methods"""
    changes = []
    try:
        tree = ast.parse(code)
        extractor = MethodExtractor()
        extractor.visit(tree)
        changes.extend(extractor.changes_made)
        refactored_code = astor.to_source(tree)
        return refactored_code, changes
    except Exception as e:
        return code, [f"Could not extract methods: {str(e)}"]

class MethodExtractor(ast.NodeVisitor):
    def __init__(self):
        self.changes_made = []
        self.duplicate_blocks = {}
    
    def visit_FunctionDef(self, node):
        # Look for duplicate code patterns
        # This is a simplified version - in practice you'd analyze code blocks
        function_body = []
        for item in node.body:
            if isinstance(item, (ast.Assign, ast.Expr, ast.Return)):
                function_body.append(ast.dump(item))
        
        # Check for duplicates in function body
        seen_lines = set()
        for line in function_body:
            if line in seen_lines:
                self.changes_made.append(f"Found duplicate code pattern in function '{node.name}'")
                break
            seen_lines.add(line)
        
        self.generic_visit(node)

def remove_dead_code(code: str) -> Tuple[str, List[str]]:
    """Remove unused variables and imports"""
    changes = []
    try:
        tree = ast.parse(code)
        cleaner = DeadCodeCleaner()
        cleaner.visit(tree)
        changes.extend(cleaner.changes_made)
        refactored_code = astor.to_source(tree)
        return refactored_code, changes
    except Exception as e:
        return code, [f"Could not remove dead code: {str(e)}"]

class DeadCodeCleaner(ast.NodeVisitor):
    def __init__(self):
        self.changes_made = []
        self.used_vars = set()
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id not in self.used_vars:
                self.changes_made.append(f"Found unused variable: {target.id}")
                # Note: In full implementation, you'd remove this assignment
        self.generic_visit(node)