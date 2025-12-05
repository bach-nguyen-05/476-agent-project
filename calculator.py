import re
import ast
import operator as op

ACTION_RE = re.compile(r"^\s*(CALCULATE|FINAL)\s*:\s*(.+?)\s*$", re.IGNORECASE | re.DOTALL)

def parse_action(text: str):
    """
    Returns ("CALCULATE", expr) or ("FINAL", answer); raises ValueError on bad format.
    """
    m = ACTION_RE.match(text.strip())
    if not m:
        raise ValueError(f"Unrecognized action format: {text!r}")
    action = m.group(1).upper()
    payload = m.group(2).strip()
    return action, payload

ALLOWED_BINOPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod}
ALLOWED_UNOPS  = {ast.UAdd: op.pos, ast.USub: op.neg}