#!/usr/bin/env python3
"""
Terraform State File Parser
Extracts resource information from Terraform state files for architecture visualization.
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TerraformResource:
    """Represents a Terraform resource with its key attributes."""
    type: str
    name: str
    provider: str
    attributes: Dict[str, Any]
    dependencies: List[str]
    module: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        """Returns the full resource name including module if present."""
        if self.module:
            return f"{self.module}.{self.type}.{self.name}"
        return f"{self.type}.{self.name}"


class TerraformStateParser:
    """Parser for Terraform state files."""
    
    def __init__(self):
        self.resources: List[TerraformResource] = []
        self.outputs: Dict[str, Any] = {}
        self.terraform_version: str = ""
        
    def parse_state_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a single Terraform state file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            self.terraform_version = state_data.get('terraform_version', '')
            self.outputs = state_data.get('outputs', {})
            
            # Parse resources
            resources = state_data.get('resources', [])
            for resource in resources:
                parsed_resource = self._parse_resource(resource)
                if parsed_resource:
                    self.resources.append(parsed_resource)
            
            return {
                'terraform_version': self.terraform_version,
                'outputs': self.outputs,
                'resources': self.resources,
                'resource_count': len(self.resources)
            }
            
        except Exception as e:
            print(f"Error parsing state file {file_path}: {str(e)}")
            return {}
    
    def _parse_resource(self, resource_data: Dict[str, Any]) -> Optional[TerraformResource]:
        """Parse a single resource from the state data."""
        try:
            resource_type = resource_data.get('type', '')
            resource_name = resource_data.get('name', '')
            provider = resource_data.get('provider', '')
            module = resource_data.get('module', '')
            
            # Get the first instance (most resources have only one)
            instances = resource_data.get('instances', [])
            if not instances:
                return None
            
            instance = instances[0]
            attributes = instance.get('attributes', {})
            dependencies = instance.get('dependencies', [])
            
            return TerraformResource(
                type=resource_type,
                name=resource_name,
                provider=provider,
                attributes=attributes,
                dependencies=dependencies,
                module=module
            )
            
        except Exception as e:
            print(f"Error parsing resource: {str(e)}")
            return None
    
    def get_resources_by_type(self, resource_type: str) -> List[TerraformResource]:
        """Get all resources of a specific type."""
        return [r for r in self.resources if r.type == resource_type]
    
    def get_resource_types(self) -> List[str]:
        """Get all unique resource types in the state."""
        return list(set(r.type for r in self.resources))
    
    def get_providers(self) -> List[str]:
        """Get all unique providers in the state."""
        return list(set(r.provider for r in self.resources))
    
    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """Analyze resource dependencies."""
        dependency_map = {}
        for resource in self.resources:
            dependency_map[resource.full_name] = resource.dependencies
        return dependency_map
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the parsed state."""
        resource_counts = {}
        for resource in self.resources:
            resource_counts[resource.type] = resource_counts.get(resource.type, 0) + 1
        
        return {
            'terraform_version': self.terraform_version,
            'total_resources': len(self.resources),
            'resource_types': len(self.get_resource_types()),
            'providers': self.get_providers(),
            'resource_counts': resource_counts,
            'outputs_count': len(self.outputs)
        }


def parse_multiple_state_files(directory_path: str) -> Dict[str, Dict[str, Any]]:
    """Parse all Terraform state files in a directory."""
    results = {}
    directory = Path(directory_path)
    
    # Look for common Terraform state file patterns
    patterns = ['*.tfstate', 'terraform.tfstate*', '*.tfstateenv*']
    
    state_files = []
    for pattern in patterns:
        state_files.extend(directory.glob(pattern))
    
    for state_file in state_files:
        if state_file.is_file():
            parser = TerraformStateParser()
            result = parser.parse_state_file(str(state_file))
            if result:
                results[state_file.name] = result
    
    return results


if __name__ == "__main__":
    # Example usage
    parser = TerraformStateParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Parse all state files in current directory
    results = parse_multiple_state_files(current_dir)
    
    print("=== Terraform State Analysis ===")
    for filename, data in results.items():
        print(f"\nFile: {filename}")
        print(f"Terraform Version: {data.get('terraform_version', 'Unknown')}")
        print(f"Total Resources: {data.get('resource_count', 0)}")
        
        if 'resources' in data:
            resource_types = {}
            for resource in data['resources']:
                resource_types[resource.type] = resource_types.get(resource.type, 0) + 1
            
            print("Resource Types:")
            for rtype, count in sorted(resource_types.items()):
                print(f"  - {rtype}: {count}")
