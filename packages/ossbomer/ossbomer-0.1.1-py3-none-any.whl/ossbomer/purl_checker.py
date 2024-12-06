import json
import os
import re
from pathlib import Path

def get_dataset_directory():
    """Get the directory where datasets are stored in the package."""
    package_dir = Path(__file__).resolve().parent
    dataset_dir = package_dir / "datasets/package_signatures"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    return dataset_dir

def check_purls(sbom_path):
    """Flag problematic PURLs in the SBOM using package signatures."""
    dataset_dir = get_dataset_directory()
    signature_files = [f for f in os.listdir(dataset_dir) if f.endswith(".json")]

    # Load all signatures
    signatures = []
    for file_name in signature_files:
        file_path = os.path.join(dataset_dir, file_name)
        try:
            with open(file_path, "r") as file:
                signatures.append(json.load(file))
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {file_name} - {e}")

    # Load SBOM file
    with open(sbom_path, "r") as sbom_file:
        sbom = json.load(sbom_file)
    components = sbom.get("components", [])

    for component in components:
        purl = component.get("purl")
        if not purl:
            print(f"Warning: Missing PURL for component {component.get('name', 'unknown')}")
            continue

        for signature in signatures:
            matched = False
            # Check for exact PURL matches
            if "purls" in signature and purl in signature["purls"]:
                print_problem_details(purl, signature)
                matched = True

            # Check for regex matches (support multiple regex patterns)
            if not matched and "regex" in signature:
                regex_list = signature["regex"]
                if isinstance(regex_list, str):
                    regex_list = [regex_list]  # Ensure it's a list
                for regex in regex_list:
                    if re.search(regex, purl):
                        print_problem_details(purl, signature)
                        break  # Stop after the first match in the regex list

def print_problem_details(purl, signature):
    """Print details of a problematic PURL."""
    print(f"Warning: Problematic PURL detected - {purl}")
    print(f"Problem Type: {signature.get('problem_type', 'Unknown')}")
    print(f"Description: {signature.get('description', 'No description provided.')}")
    print(f"Publisher: {signature.get('publisher', 'Unknown')}")
    print(f"Last Updated: {signature.get('last_updated', 'Unknown')}")
