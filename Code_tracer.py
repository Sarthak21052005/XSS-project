import execjs
import json
# 1. Lexical Analyzer using execjs + JavaScript regex
def lexical_analyzer(js_code):
    context = execjs.compile("""
        function tokenize(code) {
            return code.split(/[\\s;\\(\\)\\{\\}\\,\\.\\+\\-\\/\\=\\*\\%\\^\\<\\>\\[\\]]+/).filter(Boolean);
        }
    """)
    tokens = context.call("tokenize", js_code)
    return tokens

# 2. Parser using real Esprima (Node.js)
def parse_js(js_code): 
    context = execjs.compile("""
        const esprima = require('esprima');
        function parseCode(code) {
            return JSON.stringify(esprima.parseScript(code, { loc: true }));
        }
    """)
    ast_json = context.call("parseCode", js_code)
    return json.loads(ast_json)

# 3. Generate a simple linear Control Flow Graph (CFG) from AST body
def generate_cfg(ast):
    cfg = {}
    body = ast.get("body", [])
    for i, node in enumerate(body):
        cfg[i] = {
            "statement_type": node.get("type"),
            "next": i + 1 if i + 1 < len(body) else None
        }
    return cfg

# Sample JS Code
js_code = """
function greet(user) {
    if (user) {
        alert('Hello ' + user);
    } else {
        alert('Hello World');
    }
}
"""
# Step 1: Tokenization
tokens = lexical_analyzer(js_code)
print("\n🔹 Tokens:\n", tokens)
# Step 2: Parse JS
parsed_ast = parse_js(js_code)
print("\n🔹 Parsed AST Top-Level:\n", json.dumps(parsed_ast["body"], indent=2))
# Step 3: Generate CFG
cfg = generate_cfg(parsed_ast)
print("\n🔹 Generated CFG:\n", json.dumps(cfg, indent=2))
