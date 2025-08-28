#!/usr/bin/env python3
"""
Streamlit Web Application for Terraform Architecture Generator
Upload state files, parse them, and generate architecture diagrams with LLM insights.
"""

import streamlit as st
import json
import tempfile
import os
from pathlib import Path
import base64
from io import BytesIO
import requests
from typing import Dict, Any, List
from datetime import datetime

# Lazy imports for better performance
@st.cache_resource
def get_plotly():
    import plotly.express as px
    import plotly.graph_objects as go
    return px, go

@st.cache_resource
def get_pandas():
    import pandas as pd
    return pd

# Lazy import modules only when needed
def get_terraform_modules():
    """Import modules lazily to improve startup performance."""
    try:
        from terraform_state_parser import TerraformStateParser
        from architecture_visualizer import ArchitectureVisualizer
        return TerraformStateParser, ArchitectureVisualizer
    except ImportError as e:
        st.error(f"Failed to import required modules: {e}")
        return None, None

# Configure Streamlit page
st.set_page_config(
    page_title="Terraform Architecture Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optimized CSS injection with caching
@st.cache_data
def load_custom_css():
    return """
    <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 8px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] { gap: 2px; }
        .stTabs [data-baseweb="tab"] { height: 45px; padding: 0 15px; }
    </style>
    """

st.markdown(load_custom_css(), unsafe_allow_html=True)

def get_app_instance():
    """Get app instance - only create when needed."""
    TerraformStateParser, ArchitectureVisualizer = get_terraform_modules()
    if TerraformStateParser and ArchitectureVisualizer:
        return TerraformStateParser(), ArchitectureVisualizer()
    return None, None

class StreamlitTerraformApp:
    def __init__(self):
        # Lazy initialization - only create when needed
        self.parser = None
        self.visualizer = None
    
    def _ensure_initialized(self):
        """Ensure parser and visualizer are initialized."""
        if self.parser is None or self.visualizer is None:
            self.parser, self.visualizer = get_app_instance()
        
    def analyze_with_llm(self, resources: List[Dict], provider: str) -> str:
        """Generate LLM insights about the infrastructure."""
        try:
            # Prepare context for LLM
            resource_summary = {}
            for resource in resources:
                rtype = resource.get('type', 'unknown')
                resource_summary[rtype] = resource_summary.get(rtype, 0) + 1
            
            context = f"""
            Infrastructure Analysis:
            Provider: {provider}
            Total Resources: {len(resources)}
            Resource Types: {dict(resource_summary)}
            
            Please provide insights about this infrastructure including:
            1. Architecture overview
            2. Security considerations
            3. Cost optimization suggestions
            4. Best practices recommendations
            """
            
            # For demo purposes, return a structured analysis
            # In production, you'd integrate with OpenAI, Anthropic, or other LLM APIs
            return self._generate_mock_llm_response(resource_summary, provider)
            
        except Exception as e:
            return f"LLM Analysis unavailable: {str(e)}"
    
    def _generate_mock_llm_response(self, resource_summary: Dict, provider: str) -> str:
        """Generate a mock LLM response for demonstration."""
        total_resources = sum(resource_summary.values())
        
        analysis = f"""
        ## 🏗️ Infrastructure Analysis
        
        **Provider**: {provider.upper()}  
        **Total Resources**: {total_resources}
        
        ### 📊 Resource Breakdown
        """
        
        for rtype, count in resource_summary.items():
            analysis += f"- **{rtype}**: {count} instances\n"
        
        analysis += """
        
        ### 🔒 Security Recommendations
        - Ensure network security groups have minimal required access
        - Use private subnets for backend resources
        - Enable encryption for storage accounts
        - Implement proper IAM roles and permissions
        
        ### 💰 Cost Optimization
        - Consider using reserved instances for long-running VMs
        - Implement auto-scaling for variable workloads
        - Use appropriate VM sizes based on actual usage
        - Enable cost monitoring and alerts
        
        ### 🎯 Best Practices
        - Tag all resources for better organization
        - Implement backup strategies for critical data
        - Use infrastructure as code (Terraform) consistently
        - Monitor resource utilization and performance
        """
        
        return analysis

def get_provider_info(provider: str) -> Dict[str, str]:
    """Get provider-specific information and styling."""
    providers = {
        'aws': {
            'name': 'Amazon Web Services',
            'icon': '☁️',
            'color': '#FF9900',
            'badge_class': 'aws-badge'
        },
        'azure': {
            'name': 'Microsoft Azure',
            'icon': '🔵',
            'color': '#0078D4',
            'badge_class': 'azure-badge'
        },
        'gcp': {
            'name': 'Google Cloud Platform',
            'icon': '🌐',
            'color': '#4285F4',
            'badge_class': 'gcp-badge'
        }
    }
    return providers.get(provider, {
        'name': provider.upper(),
        'icon': '⚡',
        'color': '#6B7280',
        'badge_class': 'provider-badge'
    })

def create_resource_chart(resources: List[Dict]):
    """Create an interactive chart of resource distribution."""
    px, go = get_plotly()
    
    resource_counts = {}
    for resource in resources:
        rtype = resource.get('type', 'unknown')
        resource_counts[rtype] = resource_counts.get(rtype, 0) + 1
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(resource_counts.keys()),
        values=list(resource_counts.values()),
        hole=0.3,
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title="Resource Distribution",
        showlegend=True,
        height=400,
        font=dict(size=12)
    )
    
    return fig

@st.cache_data
def analyze_resource_relationships(resources_hash, _resources):
    """Cached analysis of resource relationships."""
    relationships = []
    resource_map = {}
    
    # Build resource map (optimized)
    for resource in _resources:
        resource_type = getattr(resource, 'type', resource.get('type', ''))
        resource_name = getattr(resource, 'name', resource.get('name', ''))
        if resource_name:  # Only process named resources
            resource_map[resource_name] = resource_type
    
    # Find relationships (simplified for performance)
    for resource in _resources[:50]:  # Limit to first 50 for performance
        resource_name = getattr(resource, 'name', resource.get('name', ''))
        attributes = getattr(resource, 'attributes', resource.get('attributes', {}))
        
        # Only check key relationship attributes
        key_attrs = ['subnet_id', 'vpc_id', 'security_group_ids', 'network_interface_id']
        for attr_name in key_attrs:
            if attr_name in attributes and attributes[attr_name]:
                relationships.append({
                    'from': resource_name,
                    'to': str(attributes[attr_name])[:50],  # Truncate long values
                    'type': 'network' if 'network' in attr_name or 'subnet' in attr_name or 'vpc' in attr_name else 'security',
                    'attribute': attr_name
                })
    
    return relationships[:100]  # Limit relationships for performance

@st.cache_data
def generate_analysis_summary(resources_hash, provider, relationships_count, resource_types_data):
    """Cached analysis summary generation."""
    compute_count = sum(v for k, v in resource_types_data.items() if any(x in k.lower() for x in ['vm', 'instance', 'compute', 'ec2']))
    network_count = sum(v for k, v in resource_types_data.items() if any(x in k.lower() for x in ['network', 'subnet', 'vpc', 'vnet']))
    storage_count = sum(v for k, v in resource_types_data.items() if any(x in k.lower() for x in ['storage', 'disk', 's3', 'blob']))
    security_count = sum(v for k, v in resource_types_data.items() if any(x in k.lower() for x in ['security', 'firewall', 'acl']))
    
    return f"""
## 🔍 Infrastructure Analysis

**Provider:** {provider.upper()} | **Resources:** {sum(resource_types_data.values())} | **Types:** {len(resource_types_data)} | **Connections:** {relationships_count}

### 📊 Categories
- **🖥️ Compute:** {compute_count} resources
- **🌐 Network:** {network_count} resources  
- **💾 Storage:** {storage_count} resources
- **🔒 Security:** {security_count} resources
"""

@st.cache_data
def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'analysis_complete': False,
        'parsed_data': None,
        'relationships': [],
        'uploaded_file_name': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    # Initialize session state first
    init_session_state()
    
    # Optimized header
    st.markdown('<div class="main-header"><h1>🏗️ Terraform Architecture Generator</h1></div>', unsafe_allow_html=True)
    
    app = StreamlitTerraformApp()
    
    # Enhanced sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Cloud Provider Focus
        st.subheader("🌐 Cloud Provider Focus")
        provider_focus = st.selectbox(
            "Optimize analysis for:",
            ["Auto-detect", "AWS", "Azure", "Google Cloud", "Multi-cloud"],
            help="Choose your primary cloud provider for optimized analysis"
        )
        
        # LLM Provider selection
        st.subheader("🤖 AI Analysis")
        llm_provider = st.selectbox(
            "LLM Provider",
            ["Mock Analysis", "OpenAI GPT-4", "Anthropic Claude", "Azure OpenAI", "Local LLM"],
            help="Select your preferred LLM for infrastructure analysis"
        )
        
        # Analysis options
        st.subheader("📊 Analysis Options")
        generate_diagram = st.checkbox("🎨 Generate Architecture Diagram", value=True)
        llm_analysis = st.checkbox("🤖 AI Infrastructure Analysis", value=True)
        cost_analysis = st.checkbox("💰 Cost Estimation", value=True)
        security_scan = st.checkbox("🔒 Security Assessment", value=True)
        show_raw_data = st.checkbox("🔍 Show Raw Resource Data", value=False)
        
        # Visualization options
        st.subheader("🎯 Visualization")
        diagram_style = st.selectbox(
            "Diagram Style",
            ["Modern", "Classic", "Minimal", "Detailed"],
            help="Choose your preferred diagram style"
        )
        
        show_relationships = st.checkbox("Show Resource Relationships", value=True)
        group_by_service = st.checkbox("Group by Service Type", value=True)
        
        # API Key input
        if llm_provider not in ["Mock Analysis", "Local LLM"]:
            st.subheader("🔑 API Configuration")
            api_key = st.text_input("API Key", type="password", help="Enter your LLM provider API key")
            
        # Export options
        st.subheader("📤 Export Options")
        export_format = st.selectbox(
            "Export Format",
            ["PNG", "SVG", "PDF", "JSON Report"],
            help="Choose export format for diagrams and reports"
        )
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Upload & Parse", "📊 Dashboard", "🎨 Visualization", "🤖 AI Insights"])
    
    with tab1:
        st.header("📁 Upload & Analyze Terraform State File")
        
        # Step 1: File Upload
        st.subheader("Step 1: Upload Your Terraform State File")
        uploaded_file = st.file_uploader(
            "Choose a Terraform state file",
            type=None,  # Accept any file type
            help="Upload your terraform.tfstate file, .json state file, or any Terraform state file",
            accept_multiple_files=False
        )
        
        # Sample files section
        with st.expander("📋 Try Sample Files"):
            sample_col1, sample_col2 = st.columns(2)
            
            with sample_col1:
                if st.button("🔶 Load AWS Sample", use_container_width=True):
                    st.info("AWS sample would be loaded here")
                    
            with sample_col2:
                if st.button("🔵 Load Azure Sample", use_container_width=True):
                    st.info("Azure sample would be loaded here")
        
        # Step 2: Analysis Button
        if uploaded_file is not None:
            st.subheader("Step 2: Analyze Infrastructure")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                analyze_button = st.button(
                    "🔍 Analyze Infrastructure", 
                    use_container_width=True,
                    type="primary",
                    help="Click to analyze your Terraform state file"
                )
            
            # Process file when analyze button is clicked
            if analyze_button or (hasattr(st.session_state, 'uploaded_file_name') and st.session_state.uploaded_file_name == uploaded_file.name):
                if not hasattr(st.session_state, 'uploaded_file_name') or st.session_state.uploaded_file_name != uploaded_file.name:
                    # New file uploaded, reset analysis
                    st.session_state.analysis_complete = False
                    st.session_state.uploaded_file_name = uploaded_file.name
                
                if not st.session_state.analysis_complete:
                    with st.spinner("🔄 Analyzing your infrastructure..."):
                        try:
                            # Read and parse the uploaded file
                            file_content = uploaded_file.read()
                            
                            # Try to parse as JSON (Terraform state files are JSON)
                            try:
                                state_data = json.loads(file_content)
                            except json.JSONDecodeError:
                                st.error("❌ Invalid file format. Please upload a valid Terraform state file (JSON format).")
                                st.stop()
                            
                            # Basic validation for Terraform state file structure
                            if not isinstance(state_data, dict):
                                st.error("❌ Invalid Terraform state file structure.")
                                st.stop()
                            
                            # Check for basic Terraform state file indicators
                            if 'terraform_version' not in state_data and 'version' not in state_data and 'resources' not in state_data:
                                st.warning("⚠️ This doesn't appear to be a standard Terraform state file, but we'll try to process it anyway.")
                            
                            st.success(f"✅ Successfully loaded file: {uploaded_file.name}")
                            
                            # Save to temporary file for processing
                            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                                json.dump(state_data, tmp_file)
                                tmp_file_path = tmp_file.name
                            
                            # Parse the state file
                            if app.parser:
                                parsed_data = app.parser.parse_state_file(tmp_file_path)
                                st.session_state.parsed_data = {
                                    'state_data': state_data,
                                    'parsed_data': parsed_data,
                                    'tmp_file_path': tmp_file_path
                                }
                                
                                # Analyze relationships (cached)
                                resources = parsed_data.get('resources', [])
                                resources_hash = hash(str(len(resources)) + str(resources[0].get('type', '') if resources else ''))
                                st.session_state.relationships = analyze_resource_relationships(resources_hash, resources)
                                st.session_state.analysis_complete = True
                                
                                st.success("✅ Analysis complete! Check the other tabs for results.")
                            else:
                                # Fallback: create a simple parser from the state data directly
                                st.warning("⚠️ Using fallback parser...")
                                
                                # Extract resources directly from state data
                                resources = []
                                if 'resources' in state_data:
                                    for resource in state_data['resources']:
                                        resources.append({
                                            'type': resource.get('type', 'unknown'),
                                            'name': resource.get('name', 'unnamed'),
                                            'provider': resource.get('provider', 'unknown'),
                                            'attributes': resource.get('instances', [{}])[0].get('attributes', {}) if resource.get('instances') else {}
                                        })
                                
                                st.session_state.parsed_data = {
                                    'state_data': state_data,
                                    'parsed_data': {'resources': resources},
                                    'tmp_file_path': tmp_file_path
                                }
                                
                                # Analyze relationships (cached)
                                resources_hash = hash(str(len(resources)) + str(resources[0].get('type', '') if resources else ''))
                                st.session_state.relationships = analyze_resource_relationships(resources_hash, resources)
                                st.session_state.analysis_complete = True
                                
                                st.success("✅ Analysis complete using fallback parser! Check the other tabs for results.")
                                
                        except json.JSONDecodeError:
                            st.error("❌ Invalid JSON file. Please upload a valid Terraform state file.")
                        except Exception as e:
                            st.error(f"❌ Error processing file: {str(e)}")
                
                # Show analysis results if complete
                if st.session_state.analysis_complete and st.session_state.parsed_data:
                    st.subheader("Step 3: Analysis Results")
                    
                    state_data = st.session_state.parsed_data['state_data']
                    parsed_data = st.session_state.parsed_data['parsed_data']
                    resources = parsed_data.get('resources', [])
                    relationships = st.session_state.relationships
                    
                    # Determine provider
                    provider_counts = {'azure': 0, 'aws': 0, 'gcp': 0, 'other': 0}
                    for resource in resources:
                        rtype = getattr(resource, 'type', resource.get('type', ''))
                        if rtype.startswith('azurerm_'):
                            provider_counts['azure'] += 1
                        elif rtype.startswith('aws_'):
                            provider_counts['aws'] += 1
                        elif rtype.startswith('google_'):
                            provider_counts['gcp'] += 1
                        else:
                            provider_counts['other'] += 1
                    
                    primary_provider = max(provider_counts, key=provider_counts.get)
                    
                    # Generate and show analysis (cached)
                    resource_types = {}
                    for resource in resources:
                        rtype = getattr(resource, 'type', resource.get('type', 'unknown'))
                        resource_types[rtype] = resource_types.get(rtype, 0) + 1
                    
                    resources_hash = hash(str(len(resources)) + primary_provider)
                    analysis_summary = generate_analysis_summary(resources_hash, primary_provider, len(relationships), resource_types)
                    st.markdown(analysis_summary)
                    
                    # Quick metrics
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("Resources", len(resources))
                    with metric_col2:
                        unique_types = len(set(getattr(r, 'type', r.get('type', '')) for r in resources))
                        st.metric("Resource Types", unique_types)
                    with metric_col3:
                        st.metric("Relationships", len(relationships))
                    with metric_col4:
                        st.metric("Provider", primary_provider.upper())
        
        else:
            st.info("👆 Please upload a Terraform state file to begin analysis")
        
    
    # Dashboard tab
    with tab2:
        if getattr(st.session_state, 'analysis_complete', False) and getattr(st.session_state, 'parsed_data', None):
            st.header("📊 Infrastructure Dashboard")
            
            # Get cached data
            resources = st.session_state.parsed_data['parsed_data'].get('resources', [])
            relationships = st.session_state.relationships
            
            # Quick calculations
            resource_types = {}
            provider_counts = {'azure': 0, 'aws': 0, 'gcp': 0, 'other': 0}
            
            for resource in resources:
                rtype = getattr(resource, 'type', resource.get('type', 'unknown'))
                resource_types[rtype] = resource_types.get(rtype, 0) + 1
                
                if rtype.startswith('azurerm_'):
                    provider_counts['azure'] += 1
                elif rtype.startswith('aws_'):
                    provider_counts['aws'] += 1
                elif rtype.startswith('google_'):
                    provider_counts['gcp'] += 1
                else:
                    provider_counts['other'] += 1
            
            # Key metrics row
            metric_row1 = st.columns(4)
            with metric_row1[0]:
                st.metric("Total Resources", len(resources), delta="Active")
            with metric_row1[1]:
                st.metric("Resource Types", len(resource_types))
            with metric_row1[2]:
                st.metric("Providers", len([p for p in provider_counts.values() if p > 0]))
            with metric_row1[3]:
                cost_estimate = len(resources) * 50  # Mock cost calculation
                st.metric("Est. Monthly Cost", f"${cost_estimate}", delta="-12%")
            
            # Simplified charts
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("☁️ Provider Distribution")
                provider_data = {k: v for k, v in provider_counts.items() if v > 0}
                if provider_data and len(provider_data) > 1:
                    px, go = get_plotly()
                    fig = go.Figure(data=[go.Pie(labels=list(provider_data.keys()), values=list(provider_data.values()))])
                    fig.update_layout(height=250, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    primary = max(provider_counts, key=provider_counts.get)
                    st.info(f"Primary Provider: **{primary.upper()}**")
            
            with col2:
                st.subheader("🔧 Resource Types")
                st.write(f"**Total Types:** {len(resource_types)}")
                top_3 = sorted(resource_types.items(), key=lambda x: x[1], reverse=True)[:3]
                for rtype, count in top_3:
                    st.write(f"• {rtype}: {count}")
                if len(resource_types) > 3:
                    st.write(f"... and {len(resource_types) - 3} more types")
            
            # Simplified relationships
            if relationships:
                st.subheader("🔗 Resource Relationships")
                rel_types = set(rel['type'] for rel in relationships)
                st.write(f"Found {len(relationships)} connections across {len(rel_types)} types")
                
                with st.expander("View Sample Relationships"):
                    for i, rel in enumerate(relationships[:3]):
                        st.write(f"{i+1}. {rel['from']} → {rel['to']} ({rel['type']})")
            
            # Simplified security overview
            if security_scan:
                st.subheader("🔒 Security Overview")
                sec_resources = sum(1 for r in resources if any(x in getattr(r, 'type', r.get('type', '')).lower() for x in ['security', 'iam', 'acl']))
                st.metric("Security Resources", sec_resources, delta="detected")
                st.info("🛡️ Security analysis available in AI Insights tab")
        else:
            st.info("📁 Upload and analyze a Terraform state file to view the dashboard")
    
    # Visualization tab
    with tab3:
        if getattr(st.session_state, 'analysis_complete', False) and getattr(st.session_state, 'parsed_data', None):
            st.header("🎨 Architecture Visualization")
            
            # Get minimal data needed
            resources = st.session_state.parsed_data['parsed_data'].get('resources', [])
            tmp_file_path = st.session_state.parsed_data['tmp_file_path']
            
            viz_col1, viz_col2 = st.columns([2, 1])
            
            with viz_col1:
                if generate_diagram:
                    st.subheader("🏗️ Architecture Diagram")
                    
                    # Generate diagram button
                    if st.button("🎨 Generate Diagram", type="primary", use_container_width=True):
                        try:
                            with st.spinner("Generating architecture diagram..."):
                                if app.visualizer:
                                    # Generate diagram
                                    diagram_path = app.visualizer.generate_diagram(tmp_file_path)
                                    
                                    if diagram_path and os.path.exists(diagram_path):
                                        # Display the generated diagram
                                        st.image(diagram_path, caption="Infrastructure Architecture Diagram")
                                        
                                        # Provide download button
                                        with open(diagram_path, "rb") as file:
                                            btn = st.download_button(
                                                label="📥 Download Diagram",
                                                data=file,
                                                file_name=f"{st.session_state.uploaded_file_name}_architecture.{export_format.lower()}",
                                                mime=f"image/{export_format.lower()}"
                                            )
                                    else:
                                        st.warning("⚠️ Diagram generation failed. Ensure Graphviz is installed.")
                                else:
                                    st.error("❌ Visualizer not available. Please check module imports.")
                                        
                        except Exception as e:
                            st.error(f"❌ Diagram generation error: {str(e)}")
                            st.info("💡 Make sure Graphviz is installed: `sudo apt-get install graphviz`")
                    
                    else:
                        st.info("👆 Click the button above to generate your architecture diagram")
            
            with viz_col2:
                st.subheader("🎯 Diagram Options")
                
                # Diagram customization
                show_labels = st.checkbox("Show Resource Labels", value=True)
                show_connections = st.checkbox("Show Connections", value=show_relationships)
                color_by_type = st.checkbox("Color by Resource Type", value=True)
                
                st.subheader("📊 Resource Summary")
                st.write(f"**Total Resources:** {len(resources)}")
                
                # Quick resource type count
                type_counts = {}
                for resource in resources[:20]:  # Limit for performance
                    rtype = getattr(resource, 'type', resource.get('type', 'unknown'))
                    type_counts[rtype] = type_counts.get(rtype, 0) + 1
                
                if type_counts:
                    st.write("**Top Resource Types:**")
                    for rtype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                        st.write(f"• {rtype}: {count}")
        else:
            st.info("📁 Upload and analyze a Terraform state file to generate visualizations")
    
    # AI Insights tab
    with tab4:
        if getattr(st.session_state, 'analysis_complete', False) and getattr(st.session_state, 'parsed_data', None):
            st.header("🤖 AI-Powered Infrastructure Insights")
            
            # Get minimal data
            resources = st.session_state.parsed_data['parsed_data'].get('resources', [])
            relationships = st.session_state.relationships
            
            # Quick provider detection
            primary_provider = 'aws'  # Default
            for resource in resources[:5]:  # Check only first 5 for speed
                rtype = getattr(resource, 'type', resource.get('type', ''))
                if rtype.startswith('azurerm_'):
                    primary_provider = 'azure'
                    break
                elif rtype.startswith('google_'):
                    primary_provider = 'gcp'
                    break
            
            if llm_analysis:
                insight_col1, insight_col2 = st.columns([2, 1])
                
                with insight_col1:
                    st.subheader("🧠 Infrastructure Analysis")
                    
                    # Generate cached analysis
                    resource_types = {}
                    for resource in resources:
                        rtype = getattr(resource, 'type', resource.get('type', 'unknown'))
                        resource_types[rtype] = resource_types.get(rtype, 0) + 1
                    
                    resources_hash = hash(str(len(resources)) + primary_provider)
                    analysis_summary = generate_analysis_summary(resources_hash, primary_provider, len(relationships), resource_types)
                    st.markdown(analysis_summary)
                    
                    # Additional AI insights
                    if st.button("🤖 Generate AI Insights", type="primary"):
                        with st.spinner("Analyzing infrastructure with AI..."):
                            analysis = app.analyze_with_llm(resources, primary_provider)
                            st.markdown(analysis)
                
                with insight_col2:
                    st.subheader("💡 Quick Insights")
                    
                    # Cost optimization suggestions
                    if cost_analysis:
                        with st.expander("💰 Cost Optimization"):
                            st.write("• Consider using spot instances for non-critical workloads")
                            st.write("• Implement auto-scaling to reduce idle resources")
                            st.write("• Use reserved instances for predictable workloads")
                    
                    # Security recommendations
                    if security_scan:
                        with st.expander("🔒 Security Recommendations"):
                            st.write("• Enable encryption at rest for all storage")
                            st.write("• Implement least privilege access policies")
                            st.write("• Use private subnets for backend services")
                    
                    # Performance tips
                    with st.expander("⚡ Performance Tips"):
                        st.write("• Use CDN for static content delivery")
                        st.write("• Implement caching strategies")
                        st.write("• Monitor resource utilization")
            
            # Raw data section
            if show_raw_data:
                st.subheader("🔍 Raw Resource Data")
                
                with st.expander("View Raw Terraform State Data"):
                    st.json(state_data)
                
                with st.expander("View Parsed Resources"):
                    for i, resource in enumerate(resources[:10]):  # Show first 10
                        st.subheader(f"Resource {i+1}: {getattr(resource, 'type', resource.get('type', 'unknown'))}")
                        st.json({
                            "name": getattr(resource, 'name', resource.get('name', 'unknown')),
                            "type": getattr(resource, 'type', resource.get('type', 'unknown')),
                            "provider": getattr(resource, 'provider', resource.get('provider', 'unknown')),
                            "attributes": dict(list(getattr(resource, 'attributes', resource.get('attributes', {})).items())[:5])  # First 5 attributes
                        })
                    
                    if len(resources) > 10:
                        st.info(f"Showing first 10 resources. Total: {len(resources)}")
                
                with st.expander("View Resource Relationships"):
                    if relationships:
                        for i, rel in enumerate(relationships[:20]):
                            st.write(f"**{i+1}.** {rel['from']} → {rel['to']}")
                            st.write(f"   Type: {rel['type']}, Attribute: {rel['attribute']}")
                            st.write("---")
                        if len(relationships) > 20:
                            st.info(f"Showing first 20 relationships. Total: {len(relationships)}")
                    else:
                        st.info("No relationships detected")
        else:
            st.info("📁 Upload and analyze a Terraform state file to get AI insights")
    
    # Cleanup temporary file
    if uploaded_file is not None and 'tmp_file_path' in locals():
        try:
            os.unlink(tmp_file_path)
        except:
            pass

if __name__ == "__main__":
    main()
