import click
import os
from pathlib import Path
from ossbomer.license_checker import check_licenses
from ossbomer.purl_checker import check_purls
from ossbomer.schema_validator import validate_schema
from ossbomer.dataset_manager import update_datasets, get_inventory
from ossbomer.dataset_manager import update_package_signatures


@click.group()
def main():
    """OSSBOMER CLI for validating SBOMs."""
    pass

@main.command()
@click.argument("sbom_path")
def validate(sbom_path):
    """Validate an SBOM for quality and compliance."""
    if not os.path.isfile(sbom_path):
        click.echo(f"Error: The file '{sbom_path}' does not exist.")
        return
    click.echo("* Checking licenses...")
    check_licenses(sbom_path)
    click.echo("* Checking PURLs...")
    check_purls(sbom_path)
    click.echo("* Validating schema and metadata...")
    validate_schema(sbom_path)
    click.echo("* Validation complete!")

@main.command()
def update():
    """Update datasets from remote sources."""
    update_datasets()
    update_package_signatures()
    click.echo("Datasets updated successfully!")

@main.command()
def version():
    """Show the current version."""
    from ossbomer import __version__
    click.echo(f"OSSBOMER version: {__version__}")

@main.command()
def inventory():
    """Display an inventory of dataset files and versions."""
    get_inventory()
