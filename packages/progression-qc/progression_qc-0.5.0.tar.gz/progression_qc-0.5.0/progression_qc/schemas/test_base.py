{
    "nom": {"required": False, "type": "string"},
    "sortie": {
        "required": True,
        "type": ["string", "integer"],
        "nullable": False,
    },
    "rétroactions": {
        "required": False,
        "type": "dict",
        "schema": "rétroactions",
    },
    "caché": {"required": False, "type": "boolean"},
}
