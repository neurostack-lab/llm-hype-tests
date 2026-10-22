"""Тест Flint (22.10.2026): задачи на код со скрытыми проверками, исправление багов, следование инструкциям, визуальные.
Код моделей выполняется ТОЛЬКО в песочнице LXC150 (без сети, nobody, лимиты) — см. grade.py."""
import json
import re

CODE_RULES = ("\n\nUse Python 3 standard library only. Return only the code in one ```python``` block: "
              "no explanations, no example usage, no tests.")

CODE = {
 "duration": ("""Write a Python function `parse_duration(s: str) -> int` that converts a duration string to seconds.
Units: d (days), h (hours), m (minutes), s (seconds), case-insensitive. Parts may be separated by spaces or written
together ("1h15m"). Each unit may appear at most once. Examples: "1h 30m 15s" -> 5415, "2h" -> 7200, "1d 1s" -> 86401.
Raise ValueError for an empty string, unknown units, garbage, or a repeated unit.""", """
assert parse_duration("1h 30m 15s") == 5415
assert parse_duration("2h") == 7200
assert parse_duration("45m") == 2700
assert parse_duration("1h15m") == 4500
assert parse_duration("1d 1s") == 86401
assert parse_duration("10S") == 10
for bad in ["", "abc", "10x", "1h 1h", "h"]:
    try:
        parse_duration(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("no ValueError for %r" % bad)
"""),
 "intervals": ("""Write a Python function `merge_intervals(intervals: list[list[int]]) -> list[list[int]]` that merges
overlapping intervals. Intervals that touch ([1,4] and [4,5]) are merged. The input may be unsorted; the result must be
sorted by start. Empty input returns [].""", """
assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert merge_intervals([[1,4],[4,5]]) == [[1,5]]
assert merge_intervals([]) == []
assert merge_intervals([[5,7],[1,2]]) == [[1,2],[5,7]]
assert merge_intervals([[1,10],[2,3],[4,5]]) == [[1,10]]
assert merge_intervals([[2,3],[1,2],[7,9],[3,4]]) == [[1,4],[7,9]]
"""),
 "lru": ("""Write a Python class `LRUCache` with `__init__(self, capacity: int)`, `get(self, key) -> int` (returns the
value or -1) and `put(self, key, value) -> None`. When the cache exceeds capacity, evict the least recently used key.
Both get (of an existing key) and put (insert or update) count as a use.""", """
c = LRUCache(2); c.put(1, 1); c.put(2, 2)
assert c.get(1) == 1
c.put(3, 3)
assert c.get(2) == -1
c.put(4, 4)
assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
c = LRUCache(2); c.put(1, 1); c.put(2, 2); c.put(1, 10); c.put(3, 3)
assert c.get(1) == 10 and c.get(2) == -1
c = LRUCache(1); c.put(1, 1); c.put(2, 2)
assert c.get(1) == -1 and c.get(2) == 2
"""),
 "topwords": ("""Write a Python function `top_words(text: str, k: int) -> list[tuple[str, int]]`. A word is a maximal run of
alphabetic characters (str.isalpha, any language), compared case-insensitively and returned in lowercase. Return the k
most frequent words as (word, count), sorted by count descending, then word ascending. If there are fewer than k
distinct words, return all of them.""", """
assert top_words("the cat and the hat. The end!", 2) == [("the", 3), ("and", 1)]
assert top_words("a b a", 10) == [("a", 2), ("b", 1)]
assert top_words("", 3) == []
assert top_words("Привет, привет мир", 1) == [("привет", 2)]
assert top_words("x1y x", 5) == [("x", 2), ("y", 1)]
"""),
 "ipv4": ("""Write a Python function `is_valid_ipv4(s: str) -> bool`. Valid: exactly four decimal octets 0-255 separated by
single dots, ASCII digits only, no leading zeros (except the single digit "0"), no spaces, signs or other characters.""", """
for ok in ["192.168.0.1", "0.0.0.0", "255.255.255.255", "10.0.10.1"]:
    assert is_valid_ipv4(ok) is True, ok
for bad in ["256.1.1.1", "01.1.1.1", "1.1.1", "1.1.1.1.1", "a.b.c.d", "1.1.1.-1", " 1.1.1.1", "1..1.1", "+1.1.1.1", "1.1.1.1\\n", ""]:
    assert is_valid_ipv4(bad) is False, bad
"""),
 "roman": ("""Write two Python functions: `to_roman(n: int) -> str` for 1 <= n <= 3999 (raise ValueError otherwise) and
`from_roman(s: str) -> int` that accepts only canonical (standard minimal) Roman numerals and raises ValueError for
anything else (e.g. "IIII", "IC", "VX", empty string).""", """
assert to_roman(1994) == "MCMXCIV" and to_roman(3999) == "MMMCMXCIX" and to_roman(4) == "IV"
assert from_roman("MCMXCIV") == 1994 and from_roman("LVIII") == 58
assert all(from_roman(to_roman(i)) == i for i in range(1, 4000))
for bad in ["IIII", "IC", "VX", "", "MMMM", "IIV"]:
    try:
        from_roman(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("no ValueError for %r" % bad)
for bad in [0, 4000]:
    try:
        to_roman(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("no ValueError for %r" % bad)
"""),
 "flatten": ("""Write a Python function `flatten(obj: dict, sep: str = ".") -> dict` that flattens nested dicts and lists.
Keys are joined with sep; list elements use their index as the key part. An empty dict or empty list is kept as the
value at its key.""", """
assert flatten({"a": 1, "b": {"c": 2, "d": {"e": 3}}}) == {"a": 1, "b.c": 2, "b.d.e": 3}
assert flatten({"a": [1, {"b": 2}]}) == {"a.0": 1, "a.1.b": 2}
assert flatten({"x": {}}) == {"x": {}}
assert flatten({"x": []}) == {"x": []}
assert flatten({"a": {"b": 1}}, sep="/") == {"a/b": 1}
assert flatten({}) == {}
"""),
 "anagrams": ("""Write a Python function `group_anagrams(words: list[str]) -> list[list[str]]`. Words are anagrams if their
lowercase letters match as multisets; keep the original spelling and duplicates. Sort the words inside each group with
plain sorted(), and sort the groups by their first element.""", """
assert group_anagrams(["eat","tea","tan","ate","nat","bat"]) == [["ate","eat","tea"],["bat"],["nat","tan"]]
assert group_anagrams([]) == []
assert group_anagrams(["a"]) == [["a"]]
assert group_anagrams(["Listen","Silent","enlist"]) == [["Listen","Silent","enlist"]]
assert group_anagrams(["ab","ba","ab"]) == [["ab","ab","ba"]]
"""),
 "csvline": ("""Write a Python function `parse_csv_line(line: str) -> list[str]` without using the csv module. Fields are
separated by commas. A field may be wrapped in double quotes; inside quotes commas are literal and "" means one literal
double quote. Unquoted fields are returned as is (no trimming). An empty line returns [""]; a trailing comma means a
last empty field.""", r'''
assert parse_csv_line('a,b,c') == ['a', 'b', 'c']
assert parse_csv_line('"a,b",c') == ['a,b', 'c']
assert parse_csv_line('"he said ""hi""",x') == ['he said "hi"', 'x']
assert parse_csv_line('a,,b') == ['a', '', 'b']
assert parse_csv_line('a,') == ['a', '']
assert parse_csv_line("") == [""]
assert parse_csv_line(' a , b') == [' a ', ' b']
assert parse_csv_line('"",x') == ['', 'x']
'''),
 "bizday": ("""Write a Python function `next_business_day(date_str: str, holidays: list[str]) -> str`. Given an ISO date
"YYYY-MM-DD", return the first business day strictly after it as an ISO string, skipping Saturdays, Sundays and any
date listed in holidays (ISO strings).""", """
assert next_business_day("2026-10-22", []) == "2026-10-23"
assert next_business_day("2026-10-23", []) == "2026-10-26"
assert next_business_day("2026-10-24", []) == "2026-10-26"
assert next_business_day("2026-10-23", ["2026-10-26"]) == "2026-10-27"
assert next_business_day("2026-12-31", ["2027-01-01"]) == "2027-01-04"
"""),
}

BUGFIX = {
 "bsearch": ("""This function sometimes hangs forever and sometimes misses an element that is in the list:

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid
        else:
            hi = mid - 1
    return -1
```
Fix it. It must return the index of target in the sorted list arr, or -1 if absent.""", """
assert binary_search([], 1) == -1
assert binary_search([5], 5) == 0 and binary_search([5], 4) == -1
a = [1, 3, 5, 7, 9, 11]
assert all(binary_search(a, v) == i for i, v in enumerate(a))
assert all(binary_search(a, v) == -1 for v in [0, 2, 4, 12])
assert binary_search([1, 2], 2) == 1
"""),
 "movavg": ("""This function loses the last window, and it should raise ValueError when k <= 0 or k > len(xs):

```python
def moving_average(xs, k):
    out = []
    for i in range(len(xs) - k):
        out.append(sum(xs[i:i + k]) / k)
    return out
```
Fix it. It returns the average of every window of k consecutive elements.""", """
assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]
assert moving_average([1, 2, 3], 3) == [2.0]
assert moving_average([5], 1) == [5.0]
for xs, k in [([1, 2], 0), ([1, 2], 3), ([], 1)]:
    try:
        moving_average(xs, k)
    except ValueError:
        pass
    else:
        raise AssertionError("no ValueError for %r" % ((xs, k),))
"""),
 "mutdefault": ("""Tags from previous calls leak into new calls when `tags` is not passed:

```python
def add_tag(tag, tags=[]):
    if tag not in tags:
        tags.append(tag)
    return tags
```
Fix it. When tags is passed, append to that same list in place and return it; when it is not passed, start a new list.""", """
assert add_tag("a") == ["a"]
assert add_tag("b") == ["b"]
l = ["x"]; r = add_tag("y", l)
assert r == ["x", "y"] and r is l
assert add_tag("x", ["x"]) == ["x"]
"""),
}
BUGFIX_RULES = "\n\nReturn only the full fixed function in one ```python``` block, no explanations."


def _instr_json(t):
    d = json.loads(t.strip())
    return (set(d) == {"name", "first_release_year", "paradigms"} and isinstance(d["name"], str)
            and d["first_release_year"] == 1991 and isinstance(d["paradigms"], list) and len(d["paradigms"]) == 3
            and all(isinstance(p, str) and p == p.lower() for p in d["paradigms"]))


def _instr_lines(t):
    lines = [x for x in t.strip().splitlines()]
    return (len(lines) == 3 and all(x.startswith("- ") and 0 < len(x[2:].split()) <= 8 for x in lines)
            and not re.search("[\U0001F300-\U0001FAFF☀-➿]", t))


def _instr_number(t):
    return t.strip() == "4"


def _instr_commit(t):
    lines = t.strip("\n").splitlines()
    if "```" in t or len(lines) < 3:
        return False
    subj, blank, body = lines[0], lines[1], lines[2:]
    return (len(subj) <= 50 and subj[:1].isupper() and not subj.endswith(".") and blank == ""
            and 1 <= len(body) <= 3 and all(0 < len(x) <= 72 for x in body))


INSTR = {
 "json": ("Return ONLY a JSON object (no markdown, no code fences, no other text) describing the Python programming "
          "language with exactly these keys: \"name\" (string), \"first_release_year\" (integer), \"paradigms\" (array "
          "of exactly 3 lowercase strings).", _instr_json),
 "lines": ("Why should developers write tests? Answer in exactly 3 lines. Each line starts with \"- \" and has at most "
           "8 words. No emoji, no other text.", _instr_lines),
 "number": ("How many times does the letter 'e' appear in the word 'excellence'? Reply with the number only.", _instr_number),
 "commit": ("Write a git commit message for this change: fixed an off-by-one error in pagination of the user list. Rules: "
            "the first line is at most 50 characters, starts with a capital letter, uses the imperative mood and has no "
            "trailing period; then exactly one empty line; then a body of 1 to 3 lines, each at most 72 characters. "
            "Output only the commit message, no code fences.", _instr_commit),
}


def extract_code(text):
    m = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    return max(m, key=len).strip() if m else text.strip()


def check_instr(name, text):
    try:
        return bool(INSTR[name][1](text))
    except Exception:  # noqa: BLE001
        return False
