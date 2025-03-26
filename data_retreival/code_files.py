import os
import git
import shutil
import ast
from tqdm import tqdm

# Constants
GITHUB_ORG = "https://api.github.com/orgs/asyncapi/repos"
OUTPUT_DIR = "asyncapi_code_data"
 # Ignore these extensions
DOC_EXTENSIONS = {
    # Documentation & Config Files
    ".md", ".yaml", ".yml", ".json", ".toml", ".ini", ".xml", ".cfg", ".conf", ".lock",
    # Logs & Dumps  
    ".log", ".bak", ".tmp", ".swp", ".lock", ".csv", ".tsv",  
    # Environment & Ignore Files  
    ".gitignore", ".gitattributes", ".editorconfig", ".dockerignore", ".npmignore", ".prettierrc",  
    ".jpeg", ".jpg", ".png",
} 

def extract_code_data(repo_path, repo_name):
    """Extract relevant data from code files in a cloned repository."""
    extracted_data = []
    
    for root, _, files in os.walk(repo_path):
        depth_rank = root[len(repo_path):].count(os.sep)  # Calculate depth rank
        
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension not in DOC_EXTENSIONS:  # Process all non-doc files
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                    # Extract features
                    # function_signatures = []
                    # class_definitions = []
                    # import_statements = []
                    # docstrings_comments = []
                    
                    # if file_extension == ".py":  # Use AST for Python
                    #     try:
                    #         tree = ast.parse(content)
                    #         for node in ast.walk(tree):
                    #             if isinstance(node, ast.FunctionDef):
                    #                 params = [arg.arg for arg in node.args.args]
                    #                 return_type = getattr(node.returns, 'id', None)
                    #                 function_signatures.append({
                    #                     "name": node.name,
                    #                     "parameters": params,
                    #                     "return_type": return_type
                    #                 })
                    #             elif isinstance(node, ast.ClassDef):
                    #                 methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    #                 class_definitions.append({"name": node.name, "methods": methods})
                    #             elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    #                 names = [n.name for n in node.names]
                    #                 import_statements.extend(names)
                    #             elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                    #                 docstrings_comments.append(node.value.s)
                    #     except SyntaxError:
                    #         pass  # Ignore files with syntax errors
                    
                    extracted_data.append({
                        "repo_name": repo_name,
                        "file_name": file,
                        "file_extension": file_extension,
                        "file_path": relative_path,
                        "depth_rank": depth_rank,
                        "content": content
                        # "function_signatures": function_signatures,
                        # "class_definitions": class_definitions,
                        # "import_statements": import_statements,
                        # "docstrings_comments": docstrings_comments
                    })
    
    return extracted_data