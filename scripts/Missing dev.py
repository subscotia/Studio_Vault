missing_developer = [t for t in vault if not isinstance(t.get("developer"), str) or not t["developer"].strip()]
print(f"Tools missing developer: {len(missing_developer)}")