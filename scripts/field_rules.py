field_rules = {
    "name":        {"required": True, "non_blank": True,  "severity": "error"},
    "type":        {"required": True, "non_blank": False, "severity": "error"},
    "host":        {"required": True, "non_blank": True,  "severity": "error"},
    "developer":   {"required": True, "non_blank": True,  "severity": "error"},
    "tags":        {"required": True, "non_blank": False, "severity": "warning"},
    "emulates":    {"required": True, "non_blank": False, "severity": "warning"},
    "description": {"required": False,"non_blank": False, "recommended": True, "severity": "warning"}
}