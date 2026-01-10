import requests
import re
from pathlib import Path
import json


def parse_top_level_args(s: str, paren_idx: int):
    args = []
    i = paren_idx + 1
    arg_start = i
    depth = 0
    in_str = False
    str_char = None
    escaped = False
    while i < len(s):
        ch = s[i]
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == str_char:
                in_str = False
        else:
            if ch == '"' or ch == "'":
                in_str = True
                str_char = ch
            elif ch in "([{":
                depth += 1
            elif ch in ")]}":
                if depth == 0:
                    arg = s[arg_start:i].strip()
                    if arg:
                        args.append(arg)
                    break
                depth -= 1
            elif ch == "," and depth == 0:
                arg = s[arg_start:i].strip()
                args.append(arg)
                arg_start = i + 1
        i += 1
    return args


def extract_and_save(url: str = "https://nptel.ac.in/courses"):
    r = requests.get(url)
    Path("data.html").write_text(r.text, encoding="utf-8")

    s: str = r.text

    m = re.search(r"kit\.start\s*\(", s)
    if not m:
        return

    start_paren: int = m.end() - 1
    args = parse_top_level_args(s, start_paren)

    if len(args) >= 3:
        third = args[2]
    else:
        brace_idx = s.find("{", m.end())  # type: ignore
        if brace_idx == -1:
            raise SystemExit
        i = brace_idx
        depth = 0
        in_str = False
        str_char = None
        escaped = False
        end_idx: int = 0
        while i < len(s):
            ch = s[i]
            if in_str:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == str_char:
                    in_str = False
            else:
                if ch == '"' or ch == "'":
                    in_str = True
                    str_char = ch
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end_idx = i
                        break
            i += 1
        third = s[brace_idx : end_idx + 1]

    cleaned: str = third.strip()

    try:
        parsed = json.loads(cleaned)  # type: ignore
    except Exception:
        try:
            import ast

            parsed = ast.literal_eval(cleaned)
        except Exception:
            def _js_to_json(s: str) -> str:
                s2 = re.sub(r"'([^'\\\\]*(?:\\\\.[^'\\\\]*)*)'", r'"\1"', s)
                # god bless AI for this stupid logic 
                s2 = re.sub(
                    r"(?P<prefix>[{,\n\r\t ])(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:",
                    lambda m: f'{m.group("prefix")}"{m.group("key")}":',
                    s2,
                )

                s2 = re.sub(r",\s*([}\]])", r"\1", s2)
                return s2

            transformed = _js_to_json(cleaned)
            try:
                parsed = json.loads(transformed)
            except Exception:
                Path("table_raw.json").write_text(cleaned, encoding="utf-8")
                Path("table_transformed.json").write_text(transformed, encoding="utf-8")
                return

    Path("table.json").write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    extract_and_save()
