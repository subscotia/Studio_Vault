#this script will spot dodgy descriptors like "UviSoundsource", "kontakt-like",
# or whatever else is sneaking past the gatekeepers.
#🔧 Script Enhancements:
#- New operators: "startswith", "endswith", and "matches_regex"
#- A toggle: enable_regex = False
#- When False, any "matches_regex" condition is ignored (and logged as skipped)
#- When True, full pattern support is enabled using Python’s re module


import re

enable_regex = False  # ← Toggle this ON/OFF as needed

def match_entry(entry):
    results = []
    for field, op, val in conditions:
        actual = str(entry.get(field, "") or "")
        test_result = False

        try:
            if op == "==":
                test_result = actual == val
            elif op == "!=":
                test_result = actual != val
            elif op == "in":
                test_result = actual in val
            elif op == "not in":
                test_result = actual not in val
            elif op == "contains":
                test_result = val.lower() in actual.lower()
            elif op == "startswith":
                test_result = actual.lower().startswith(str(val).lower())
            elif op == "endswith":
                test_result = actual.lower().endswith(str(val).lower())
            elif op == "matches_regex":
                if enable_regex:
                    test_result = re.search(val, actual) is not None
                else:
                    print(f"⚠️ Regex disabled: skipping condition on '{field}' with pattern '{val}'")
        except Exception as e:
            print(f"❗ Error evaluating condition ({field}, {op}, {val}): {e}")

        results.append(test_result)

    return all(results) if match_mode == "AND" else any(results)