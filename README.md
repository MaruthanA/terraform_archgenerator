# Terraform Architecture Generator

A comprehensive tool to parse Terraform state files and automatically generate visual architecture diagrams. This tool supports multiple cloud providers (Azure, AWS, GCP) and can process multiple state files simultaneously.

## Features

- **Multi-Provider Support**: Automatically detects and supports Azure, AWS, and GCP resources
- **Batch Processing**: Process multiple Terraform state files in a directory
- **Visual Architecture Diagrams**: Generate beautiful, organized architecture diagrams
- **Resource Grouping**: Intelligently groups resources by VNets, VPCs, Resource Groups, etc.
- **Dependency Mapping**: Shows relationships between resources based on Terraform dependencies
- **Detailed Analysis**: Provides comprehensive analysis of your infrastructure

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Graphviz (required for diagram generation):
   - **Windows**: Download from https://graphviz.org/download/ and add to PATH
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz` or `sudo yum install graphviz`

## Usage

### Command Line Interface

```bash
# Analyze and generate diagrams for all state files in current directory
python terraform_arch_generator.py

# Specify a different directory
python terraform_arch_generator.py -d /path/to/terraform/states

# Only analyze without generating diagrams
python terraform_arch_generator.py -a

# Specify output directory for diagrams
python terraform_arch_generator.py -o /path/to/output

# Enable verbose output
python terraform_arch_generator.py -v
```

### Python API

```python
from terraform_state_parser import TerraformStateParser
from architecture_visualizer import ArchitectureVisualizer

# Parse a single state file
parser = TerraformStateParser()
result = parser.parse_state_file('terraform.tfstate')

# Generate architecture diagram
visualizer = ArchitectureVisualizer()
diagram_path = visualizer.generate_diagram('terraform.tfstate')
print(f"Diagram generated: {diagram_path}")

# Process multiple files
generated_files = visualizer.generate_multiple_diagrams('/path/to/states')
```

## Supported Resources

### Azure (azurerm)
- Virtual Machines (`azurerm_linux_virtual_machine`, `azurerm_windows_virtual_machine`)
- Virtual Networks (`azurerm_virtual_network`)
- Subnets (`azurerm_subnet`)
- Network Security Groups (`azurerm_network_security_group`)
- Network Interfaces (`azurerm_network_interface`)
- Public IP Addresses (`azurerm_public_ip`)
- Storage Accounts (`azurerm_storage_account`)
- Resource Groups (`azurerm_resource_group`)

### AWS
- EC2 Instances (`aws_instance`)
- VPCs (`aws_vpc`)
- Subnets (`aws_subnet`)
- Internet Gateways (`aws_internet_gateway`)
- NAT Gateways (`aws_nat_gateway`)
- S3 Buckets (`aws_s3_bucket`)
- RDS Instances (`aws_db_instance`)

### Google Cloud Platform
- Compute Instances (`google_compute_instance`)
- VPC Networks (`google_compute_network`)
- Cloud Storage (`google_storage_bucket`)

## File Structure

```
terraform_stateproject/
├── terraform_state_parser.py      # Core state file parsing logic
├── architecture_visualizer.py     # Diagram generation engine
├── terraform_arch_generator.py    # Main CLI application
├── requirements.txt               # Python dependencies
├── README.md                     # This file
└── terraform.tfstateenv_SAPRemote32  # Example state file
```

## Example Output

The tool will generate:

1. **Console Analysis**: Detailed breakdown of resources, providers, and statistics
2. **PNG Diagrams**: Visual architecture diagrams showing:
   - Resource groupings (by VNet, VPC, Resource Group)
   - Resource relationships and dependencies
   - Clear labeling and organization

## Configuration

### Diagram Customization

You can modify the `ArchitectureVisualizer` class to:
- Change diagram layout (`direction="TB"` for top-bottom, `"LR"` for left-right)
- Customize resource icons by extending the resource maps
- Modify clustering logic for different grouping strategies

### Adding New Resource Types

To add support for new Terraform resources:

1. Add the resource type to the appropriate provider map in `architecture_visualizer.py`
2. Import the corresponding icon from the `diagrams` library
3. Update the resource mapping dictionary

Example:
```python
self.azure_resource_map = {
    'azurerm_new_resource': NewResourceIcon,
    # ... existing mappings
}
```

## Troubleshooting

### Common Issues

1. **Graphviz not found**: Ensure Graphviz is installed and in your system PATH
2. **Empty diagrams**: Check that your state files contain resources
3. **Import errors**: Verify all dependencies are installed with `pip install -r requirements.txt`

### Debug Mode

Enable verbose output to see detailed processing information:
```bash
python terraform_arch_generator.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add support for new providers or resource types
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Examples

### Basic Usage
```bash
# Generate diagrams for current directory
python terraform_arch_generator.py

# Output:
# === Terraform State Analysis Summary ===
# 📁 Total state files: 1
# 🔧 Total resources: 15
# ☁️  Providers: azurerm
# 📦 Resource types: 8
# 
# === Generating Architecture Diagrams ===
# ✅ Successfully generated 1 architecture diagrams
```

### Advanced Usage
```bash
# Process specific directory with custom output location
python terraform_arch_generator.py -d ./terraform-states -o ./diagrams -v
```

This tool makes it easy to visualize and understand your Terraform-managed infrastructure across multiple cloud providers and environments.
