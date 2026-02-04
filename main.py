# terraform_documenter/main.py

import argparse
from pathlib import Path
import sys
import os

from .diagram_generator import create_conceptual_diagram, create_networking_diagram
from .terraform_parser import find_provider, parse_terraform_directory
from .docx_generator import DocxGenerator
from .utils import PROVIDER_DISPLAY_NAMES

def main():
    """Main function to run the Terraform documentation generator."""
    parser = argparse.ArgumentParser(description="Generate a Solution Design Document from Terraform code.")
    parser.add_argument("-d", "--directory", required=True, help="Path to the directory containing Terraform files.")
    args = parser.parse_args()

    terraform_dir = Path(args.directory)
    if not terraform_dir.is_dir():
        print(f"Error: Directory not found at '{terraform_dir}'")
        sys.exit(1)

    # 1. Detect Provider
    print("Step 1: Detecting cloud provider...")
    provider = find_provider(terraform_dir)
    if not provider:
        print("Error: Could not determine a supported cloud provider (aws, azurerm, google).")
        sys.exit(1)
    provider_name = PROVIDER_DISPLAY_NAMES.get(provider)
    print(f"Provider detected: {provider_name}")

    # 2. Parse Terraform Code
    print("Step 2: Parsing Terraform files...")
    parsed_data = parse_terraform_directory(terraform_dir, provider)
    if not parsed_data.get("resources"):
        print("Warning: No resources found in the Terraform files.")
    print(f"Found {len(parsed_data.get('variables', []))} variables and resources across multiple categories.")
    
    # 3. Generate Diagrams
    print("Step 3: Generating diagrams...")
    conceptual_diagram_path = create_conceptual_diagram(parsed_data, provider, "conceptual_diagram")
    networking_diagram_path = create_networking_diagram(parsed_data, provider, "networking_diagram")
    print(f"Diagrams saved to {conceptual_diagram_path} and {networking_diagram_path}")

    # 4. Generate DOCX Document
    print("Step 4: Generating Solution Design Document...")
    output_filename = f"Solution_Design_Document_{provider_name}.docx"
    doc_generator = DocxGenerator(
        data=parsed_data,
        provider=provider,
        directory=str(terraform_dir),
        conceptual_img=conceptual_diagram_path,
        networking_img=networking_diagram_path
    )
    doc_generator.create_sdd(output_filename)

    # 5. Clean up temporary diagram files from disk
    print("Step 5: Cleaning up temporary diagram files...")
    try:
        os.remove(conceptual_diagram_path)
        os.remove(networking_diagram_path)
        print("Cleanup successful.")
    except OSError as e:
        print(f"Error during file cleanup: {e}")


if __name__ == "__main__":
    main()