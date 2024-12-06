from jsonschema import validate
import yaml
import json
from pathlib import Path
from jsonschema.exceptions import ValidationError


def detect_sbom_type(sbom_data):
    """Detect the SBOM type (SPDX or CycloneDX)."""
    if "spdxVersion" in sbom_data:
        return "spdx"
    elif "bomFormat" in sbom_data and sbom_data["bomFormat"] == "CycloneDX":
        return "cyclonedx"
    return None


def get_dataset_directory():
    """Get the directory where datasets are stored in the package."""
    package_dir = Path(__file__).resolve().parent
    dataset_dir = package_dir / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    return dataset_dir


def validate_metadata(sbom_path):
    """Validate that the SBOM contains required metadata based on NTIA's minimum elements."""
    try:
        # Load SBOM file
        with open(sbom_path, 'r') as file:
            if sbom_path.endswith((".yaml", ".yml")):
                sbom = yaml.safe_load(file)
            else:
                sbom = json.load(file)

        # Determine SBOM type
        sbom_type = detect_sbom_type(sbom)
        if sbom_type == "spdx":
            validate_spdx_metadata(sbom)
        elif sbom_type == "cyclonedx":
            validate_cyclonedx_metadata(sbom)
        else:
            raise ValueError("Unsupported SBOM format or type.")

        # Validate NTIA minimum elements
        validate_ntia_minimum_elements(sbom)

    except ValueError as ve:
        print(f"Validation Error: {ve}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

    print("Metadata validation passed.")
    return True


def validate_ntia_minimum_elements(sbom):
    """Validate SBOM against NTIA's minimum elements."""
    missing_fields = []

    # Check for components
    components = sbom.get("components", [])
    if not components:
        missing_fields.append("components")

    for component in components:
        if not component.get("supplier"):
            missing_fields.append("supplier")
        if not component.get("name"):
            missing_fields.append("name")
        if not component.get("version"):
            missing_fields.append("version")
        if not component.get("purl"):
            missing_fields.append("purl")

    # Check for dependency relationships
    if not sbom.get("dependencies"):
        print("Warning: 'dependencies' information is missing in the SBOM.")

    # Check for author and timestamp in metadata
    metadata = sbom.get("metadata", {})
    if not metadata.get("author"):
        missing_fields.append("metadata.author")
    if not metadata.get("timestamp"):
        missing_fields.append("metadata.timestamp")

    if missing_fields:
        raise ValueError(f"SBOM is missing required fields: {', '.join(missing_fields)}")


def validate_schema(sbom_path):
    """Validate an SBOM against the appropriate schema."""
    dataset_dir = get_dataset_directory()
    spdx_path = dataset_dir / "spdx_schema.json"
    cyclone_path = dataset_dir / "cyclonedx_schema.json"

    # Load schemas
    with open(spdx_path, 'r') as spdx_file:
        spdx_schema = json.load(spdx_file)
    with open(cyclone_path, 'r') as cyclone_file:
        cyclonedx_schema = json.load(cyclone_file)

    # Determine format
    try:
        with open(sbom_path, "r") as file:
            if sbom_path.endswith((".yaml", ".yml")):
                sbom_data = yaml.safe_load(file)
            else:
                sbom_data = json.load(file)
    except Exception as e:
        raise ValueError(f"Failed to parse SBOM: {e}")

    # Detect SBOM type
    sbom_type = detect_sbom_type(sbom_data)
    if sbom_type == "spdx":
        schema = spdx_schema
    elif sbom_type == "cyclonedx":
        schema = cyclonedx_schema
    else:
        raise ValueError("Unsupported SBOM format or type.")

    try:
        validate(instance=sbom_data, schema=schema)
        print("SBOM schema validation passed!")
    except ValidationError as e:
        if "'id' is a required property" in str(e):
            print(f"Warning: Missing 'id' in a license: {e.instance}")
        else:
            raise ValueError(f"SBOM schema validation failed: {e.message}")


def validate_sbom(sbom_path):
    """Perform full SBOM validation including metadata, schema, and NTIA requirements."""
    print("Starting SBOM validation...")
    metadata_result = validate_metadata(sbom_path)
    if not metadata_result:
        print("Metadata validation failed.")
        return

    try:
        validate_schema(sbom_path)
        print("SBOM validation completed successfully!")
    except ValueError as e:
        print(f"Validation Error: {e}")
