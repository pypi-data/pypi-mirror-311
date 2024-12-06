import json
import os
from pathlib import Path

def get_dataset_directory():
    """Get the directory where datasets are stored in the package."""
    package_dir = Path(__file__).resolve().parent
    dataset_dir = package_dir / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    return dataset_dir

def check_licenses(sbom_path):
    """Check licenses in CycloneDX SBOM components against license rules."""
    dataset_dir = get_dataset_directory()
    license_file = dataset_dir / "license_rules.json"
    
    # Load license rules
    with open(license_file, 'r') as file:
        license_rules = json.load(file)["licenses"]
    
    # Load SBOM file
    with open(sbom_path, 'r') as sbom_file:
        sbom = json.load(sbom_file)

    # Check components for license issues
    components = sbom.get("components", [])
    for component in components:
        # CycloneDX stores licenses in a list under "licenses"
        licenses = component.get("licenses", [])
        if not licenses:
            print(f"Warning: Missing license for component '{component.get('name', 'unknown')}'")
            continue

        for license_entry in licenses:
            license_id = license_entry.get("license", {}).get("id", "NOASSERTION")
            if license_id.lower() == "noassertion":
                print(f"Warning: 'noassertion' license for component '{component.get('name', 'unknown')}'")
                continue

            # Search license_rules for the spdx_id
            matching_rule = next((rule for rule in license_rules if rule["spdx_id"] == license_id), None)
            if matching_rule:
                if not matching_rule["distribution"]:
                    print(f"Blocked license detected for component '{component['name']}': {license_id}")
            else:
                print(f"Unknown license '{license_id}' for component '{component['name']}'")

