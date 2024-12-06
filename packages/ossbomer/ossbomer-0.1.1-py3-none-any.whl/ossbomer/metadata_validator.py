import json

def validate_metadata(sbom_path):
    """Validate that the SBOM contains required metadata."""
    try:
        with open(sbom_path, 'r') as file:
            sbom = json.load(file)

        metadata = sbom.get("creationInfo", {})
        missing_fields = []
        if not metadata.get("created"):
            missing_fields.append("'created'")
        if not metadata.get("creators"):
            missing_fields.append("'creators'")

        if missing_fields:
            raise ValueError(f"SBOM metadata is missing required fields: {', '.join(missing_fields)}")

    except ValueError as ve:
        print(f"Validation Error: {ve}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

    print("Metadata validation passed.")
    return True
