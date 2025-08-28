#!/usr/bin/env python3
"""
Architecture Visualizer for Terraform State Files
Generates visual architecture diagrams from Terraform state data.
"""

# Lazy imports for better performance - only import when needed

import os
from typing import Dict, List, Any, Optional, Tuple
from terraform_state_parser import TerraformStateParser, TerraformResource


class ArchitectureVisualizer:
    """Creates architecture diagrams from Terraform state data."""
    
    def __init__(self):
        # Resource type mappings - actual imports happen lazily
        self.azure_resource_types = {
            'azurerm_virtual_machine': 'VM',
            'azurerm_linux_virtual_machine': 'VM', 
            'azurerm_windows_virtual_machine': 'VM',
            'azurerm_virtual_network': 'VirtualNetworks',
            'azurerm_subnet': 'Subnets',
            'azurerm_network_security_group': 'NetworkSecurityGroups',
            'azurerm_network_interface': 'NetworkInterfaces',
            'azurerm_public_ip': 'PublicIpAddresses',
            'azurerm_storage_account': 'StorageAccounts',
            'azurerm_resource_group': 'ResourceGroups',
        }
        
        self.aws_resource_types = {
            'aws_instance': 'EC2',
            'aws_vpc': 'VPC',
            'aws_subnet': 'PrivateSubnet',
            'aws_internet_gateway': 'InternetGateway',
            'aws_nat_gateway': 'NATGateway',
            'aws_s3_bucket': 'S3',
            'aws_db_instance': 'RDS',
        }
        
        self.gcp_resource_types = {
            'google_compute_instance': 'ComputeEngine',
            'google_compute_network': 'GCP_VPC',
            'google_storage_bucket': 'GCS',
        }
    
    def detect_provider(self, resources: List[TerraformResource]) -> str:
        """Detect the primary cloud provider based on resources."""
        provider_counts = {'azure': 0, 'aws': 0, 'gcp': 0}
        
        for resource in resources:
            if resource.type.startswith('azurerm_'):
                provider_counts['azure'] += 1
            elif resource.type.startswith('aws_'):
                provider_counts['aws'] += 1
            elif resource.type.startswith('google_'):
                provider_counts['gcp'] += 1
        
        return max(provider_counts, key=provider_counts.get)
    
    def _get_diagram_imports(self):
        """Lazy import of diagram components."""
        from diagrams import Diagram, Cluster, Edge
        from diagrams.azure.compute import VM as VirtualMachine
        from diagrams.azure.network import VirtualNetworks, Subnets, NetworkSecurityGroupsClassic as NetworkSecurityGroups, NetworkInterfaces, PublicIpAddresses
        from diagrams.azure.storage import StorageAccounts
        from diagrams.azure.general import Resourcegroups as ResourceGroups
        from diagrams.aws.compute import EC2
        from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, NATGateway, InternetGateway
        from diagrams.aws.storage import S3
        from diagrams.aws.database import RDS
        from diagrams.gcp.compute import ComputeEngine
        from diagrams.gcp.network import VPC as GCP_VPC
        from diagrams.gcp.storage import GCS
        from diagrams.onprem.network import Internet
        
        return {
            'Diagram': Diagram, 'Cluster': Cluster, 'Edge': Edge,
            'VM': VirtualMachine, 'VirtualNetworks': VirtualNetworks, 'Subnets': Subnets,
            'NetworkSecurityGroups': NetworkSecurityGroups, 'NetworkInterfaces': NetworkInterfaces,
            'PublicIpAddresses': PublicIpAddresses, 'StorageAccounts': StorageAccounts,
            'ResourceGroups': ResourceGroups, 'EC2': EC2, 'VPC': VPC, 'PrivateSubnet': PrivateSubnet,
            'PublicSubnet': PublicSubnet, 'NATGateway': NATGateway, 'InternetGateway': InternetGateway,
            'S3': S3, 'RDS': RDS, 'ComputeEngine': ComputeEngine, 'GCP_VPC': GCP_VPC,
            'GCS': GCS, 'Internet': Internet
        }
    
    def get_resource_icon(self, resource: TerraformResource, provider: str):
        """Get the appropriate diagram icon for a resource."""
        icons = self._get_diagram_imports()
        
        if provider == 'azure':
            icon_name = self.azure_resource_types.get(resource.type, 'VM')
            return icons.get(icon_name, icons['VM'])
        elif provider == 'aws':
            icon_name = self.aws_resource_types.get(resource.type, 'EC2')
            return icons.get(icon_name, icons['EC2'])
        elif provider == 'gcp':
            icon_name = self.gcp_resource_types.get(resource.type, 'ComputeEngine')
            return icons.get(icon_name, icons['ComputeEngine'])
        else:
            return icons['VM']  # Default fallback
    
    def group_resources_by_location(self, resources: List[TerraformResource]) -> Dict[str, List[TerraformResource]]:
        """Group resources by location/region."""
        location_groups = {}
        
        for resource in resources:
            location = resource.attributes.get('location', 
                      resource.attributes.get('region', 
                      resource.attributes.get('availability_zone', 'default')))
            
            if location not in location_groups:
                location_groups[location] = []
            location_groups[location].append(resource)
        
        return location_groups
    
    def group_resources_by_resource_group(self, resources: List[TerraformResource]) -> Dict[str, List[TerraformResource]]:
        """Group Azure resources by resource group."""
        rg_groups = {}
        
        for resource in resources:
            rg_name = resource.attributes.get('resource_group_name', 'default')
            
            if rg_name not in rg_groups:
                rg_groups[rg_name] = []
            rg_groups[rg_name].append(resource)
        
        return rg_groups
    
    def create_azure_diagram(self, resources: List[TerraformResource], output_path: str, title: str):
        """Create an Azure architecture diagram."""
        icons = self._get_diagram_imports()
        
        with icons['Diagram'](title, filename=output_path, show=False, direction="TB"):
            # Group by resource groups
            rg_groups = self.group_resources_by_resource_group(resources)
            
            resource_nodes = {}
            
            for rg_name, rg_resources in rg_groups.items():
                with icons['Cluster'](f"Resource Group: {rg_name}"):
                    # Further group by VNet if applicable
                    vnet_groups = {}
                    other_resources = []
                    
                    for resource in rg_resources:
                        if resource.type == 'azurerm_virtual_network':
                            vnet_name = resource.attributes.get('name', resource.name)
                            vnet_groups[vnet_name] = [resource]
                        elif 'subnet_id' in resource.attributes or 'virtual_network_name' in resource.attributes:
                            # Try to find which VNet this belongs to
                            subnet_id = resource.attributes.get('subnet_id', '')
                            if 'virtualNetworks' in subnet_id:
                                vnet_name = subnet_id.split('virtualNetworks/')[1].split('/')[0]
                                if vnet_name not in vnet_groups:
                                    vnet_groups[vnet_name] = []
                                vnet_groups[vnet_name].append(resource)
                            else:
                                other_resources.append(resource)
                        else:
                            other_resources.append(resource)
                    
                    # Create VNet clusters
                    for vnet_name, vnet_resources in vnet_groups.items():
                        if len(vnet_resources) > 1:  # Only cluster if multiple resources
                            with icons['Cluster'](f"VNet: {vnet_name}"):
                                for resource in vnet_resources:
                                    icon_class = self.get_resource_icon(resource, 'azure')
                                    node = icon_class(f"{resource.name}\n({resource.type})")
                                    resource_nodes[resource.full_name] = node
                        else:
                            for resource in vnet_resources:
                                icon_class = self.get_resource_icon(resource, 'azure')
                                node = icon_class(f"{resource.name}\n({resource.type})")
                                resource_nodes[resource.full_name] = node
                    
                    # Create other resources
                    for resource in other_resources:
                        icon_class = self.get_resource_icon(resource, 'azure')
                        node = icon_class(f"{resource.name}\n({resource.type})")
                        resource_nodes[resource.full_name] = node
            
            # Add connections based on dependencies
            self._add_connections(resources, resource_nodes)
    
    def create_aws_diagram(self, resources: List[TerraformResource], output_path: str, title: str):
        """Create an AWS architecture diagram."""
        icons = self._get_diagram_imports()
        
        with icons['Diagram'](title, filename=output_path, show=False, direction="TB"):
            # Group by VPC
            vpc_groups = {}
            other_resources = []
            
            for resource in resources:
                if resource.type == 'aws_vpc':
                    vpc_id = resource.attributes.get('id', resource.name)
                    vpc_groups[vpc_id] = [resource]
                elif 'vpc_id' in resource.attributes:
                    vpc_id = resource.attributes.get('vpc_id')
                    if vpc_id not in vpc_groups:
                        vpc_groups[vpc_id] = []
                    vpc_groups[vpc_id].append(resource)
                else:
                    other_resources.append(resource)
            
            resource_nodes = {}
            
            # Create VPC clusters
            for vpc_id, vpc_resources in vpc_groups.items():
                vpc_name = next((r.name for r in vpc_resources if r.type == 'aws_vpc'), vpc_id)
                with icons['Cluster'](f"VPC: {vpc_name}"):
                    for resource in vpc_resources:
                        icon_class = self.get_resource_icon(resource, 'aws')
                        node = icon_class(f"{resource.name}\n({resource.type})")
                        resource_nodes[resource.full_name] = node
            
            # Create other resources
            for resource in other_resources:
                icon_class = self.get_resource_icon(resource, 'aws')
                node = icon_class(f"{resource.name}\n({resource.type})")
                resource_nodes[resource.full_name] = node
            
            # Add connections
            self._add_connections(resources, resource_nodes)
    
    def create_generic_diagram(self, resources: List[TerraformResource], output_path: str, title: str):
        """Create a generic architecture diagram."""
        icons = self._get_diagram_imports()
        
        with icons['Diagram'](title, filename=output_path, show=False, direction="TB"):
            # Group by module or provider
            module_groups = {}
            
            for resource in resources:
                module_name = resource.module or 'main'
                if module_name not in module_groups:
                    module_groups[module_name] = []
                module_groups[module_name].append(resource)
            
            resource_nodes = {}
            
            for module_name, module_resources in module_groups.items():
                if len(module_groups) > 1:  # Only create cluster if multiple modules
                    with icons['Cluster'](f"Module: {module_name}"):
                        for resource in module_resources:
                            icon_class = self.get_resource_icon(resource, 'azure')  # Default to azure icons
                            node = icon_class(f"{resource.name}\n({resource.type})")
                            resource_nodes[resource.full_name] = node
                else:
                    for resource in module_resources:
                        icon_class = self.get_resource_icon(resource, 'azure')
                        node = icon_class(f"{resource.name}\n({resource.type})")
                        resource_nodes[resource.full_name] = node
            
            # Add connections
            self._add_connections(resources, resource_nodes)
    
    def _add_connections(self, resources: List[TerraformResource], resource_nodes: Dict[str, Any]):
        """Add connections between resources based on dependencies."""
        icons = self._get_diagram_imports()
        
        for resource in resources:
            source_node = resource_nodes.get(resource.full_name)
            if source_node:
                for dependency in resource.dependencies:
                    target_node = resource_nodes.get(dependency)
                    if target_node:
                        source_node >> icons['Edge'](style="dashed") >> target_node
    
    def generate_diagram(self, state_file_path: str, output_dir: str = None) -> str:
        """Generate architecture diagram from a Terraform state file."""
        parser = TerraformStateParser()
        result = parser.parse_state_file(state_file_path)
        
        if not result or not result.get('resources'):
            raise ValueError(f"No resources found in state file: {state_file_path}")
        
        resources = result['resources']
        provider = self.detect_provider(resources)
        
        # Prepare output path
        if output_dir is None:
            output_dir = os.path.dirname(state_file_path)
        
        state_filename = os.path.basename(state_file_path)
        output_name = f"architecture_{state_filename.replace('.', '_')}"
        output_path = os.path.join(output_dir, output_name)
        
        title = f"Architecture Diagram - {state_filename}"
        
        # Generate appropriate diagram based on provider
        if provider == 'azure':
            self.create_azure_diagram(resources, output_path, title)
        elif provider == 'aws':
            self.create_aws_diagram(resources, output_path, title)
        else:
            self.create_generic_diagram(resources, output_path, title)
        
        return f"{output_path}.png"
    
    def generate_multiple_diagrams(self, directory_path: str, output_dir: str = None) -> List[str]:
        """Generate diagrams for all state files in a directory."""
        from pathlib import Path
        
        if output_dir is None:
            output_dir = directory_path
        
        directory = Path(directory_path)
        patterns = ['*.tfstate', 'terraform.tfstate*', '*.tfstateenv*']
        
        state_files = []
        for pattern in patterns:
            state_files.extend(directory.glob(pattern))
        
        generated_files = []
        for state_file in state_files:
            if state_file.is_file():
                try:
                    output_file = self.generate_diagram(str(state_file), output_dir)
                    generated_files.append(output_file)
                    print(f"Generated diagram: {output_file}")
                except Exception as e:
                    print(f"Error generating diagram for {state_file}: {str(e)}")
        
        return generated_files


if __name__ == "__main__":
    visualizer = ArchitectureVisualizer()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        generated_files = visualizer.generate_multiple_diagrams(current_dir)
        print(f"\n=== Generated {len(generated_files)} architecture diagrams ===")
        for file_path in generated_files:
            print(f"📊 {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
