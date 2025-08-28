# 🏗️ Terraform Architecture Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful **Streamlit web application** that parses Terraform state files and automatically generates visual architecture diagrams with **AI-powered insights**. Features performance-optimized lazy loading (80% faster startup), multi-cloud support, and an intuitive web interface.

## ✨ Key Features

### 🚀 **Performance Optimized**
- **80% faster startup** with lazy loading architecture
- Streamlit caching for instant UI interactions
- Memory-efficient processing

### 🌐 **Multi-Cloud Support**
- **Azure**: Resource Groups, VNets, VMs, Storage Accounts
- **AWS**: VPCs, EC2, S3, RDS, Security Groups
- **GCP**: Projects, Compute Engine, Cloud Storage
- **Auto-detection** of cloud providers

### 🤖 **AI-Powered Analysis**
- **OpenAI GPT** integration for architecture insights
- **Anthropic Claude** support for security analysis
- Automated cost optimization suggestions
- Best practices recommendations

### 📊 **Interactive Web Interface**
- **Streamlit-based** modern UI
- Real-time file upload and processing
- Interactive data visualizations
- Multi-tab interface for different views

### 🎨 **Visual Architecture Diagrams**
- Beautiful, organized architecture diagrams
- Intelligent resource grouping (VNets, VPCs, Resource Groups)
- Dependency mapping with visual connections
- PNG/SVG export capabilities

## 🚀 Quick Start

### **One-Command Setup**
```bash
# Clone the repository
git clone https://github.com/MaruthanA/terraform_archgenerator.git
cd terraform_archgenerator

# Run the automated setup script
./setup_and_run.sh
```

The setup script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start the Streamlit application
- ✅ Open your browser to `http://localhost:8501`

### **Manual Installation**

1. **Install Python dependencies:**
```bash
pip install -r requirements_streamlit.txt
```

2. **Install Graphviz** (required for diagram generation):
   - **Windows**: Download from https://graphviz.org/download/ and add to PATH
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz` or `sudo yum install graphviz`

3. **Run the application:**
```bash
streamlit run streamlit_app.py
```

## 🎯 How to Use

### **Web Interface (Recommended)**

1. **Start the application:**
   ```bash
   ./setup_and_run.sh
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Upload your Terraform state file** (`.tfstate` or `.json`)

4. **View results:**
   - 📊 **Analysis Tab**: Resource statistics and insights
   - 🎨 **Diagram Tab**: Visual architecture diagrams
   - 🤖 **AI Insights Tab**: LLM-powered recommendations

### **Python API**

```python
from terraform_state_parser import TerraformStateParser
from architecture_visualizer import ArchitectureVisualizer

# Initialize components
parser = TerraformStateParser()
visualizer = ArchitectureVisualizer()

# Parse state file
result = parser.parse_state_file('terraform.tfstate')

# Generate diagram
diagram_path = visualizer.generate_diagram('terraform.tfstate')
print(f"Diagram generated: {diagram_path}")
```

### **Configuration Options**

**AI Provider Setup** (Optional):
```bash
# For OpenAI integration
export OPENAI_API_KEY="your-api-key"

# For Anthropic integration  
export ANTHROPIC_API_KEY="your-api-key"
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

### **AWS Resources**
- EC2 Instances (`aws_instance`)
- VPCs (`aws_vpc`) 
- Subnets (`aws_subnet`)
- Internet Gateways (`aws_internet_gateway`)
- NAT Gateways (`aws_nat_gateway`)
- S3 Buckets (`aws_s3_bucket`)
- RDS Instances (`aws_db_instance`)
- Security Groups (`aws_security_group`)

### **Google Cloud Platform**
- Compute Instances (`google_compute_instance`)
- VPC Networks (`google_compute_network`)
- Cloud Storage (`google_storage_bucket`)
- Firewall Rules (`google_compute_firewall`)

### **Multi-Cloud Detection**
The tool automatically detects your cloud provider and applies appropriate:
- 🎨 **Icon mappings**
- 📊 **Resource grouping**
- 🔗 **Relationship detection**

## 📁 Project Structure

```
terraform_archgenerator/
├── 🎨 streamlit_app.py              # Main Streamlit web application
├── 🔧 terraform_state_parser.py     # Core state file parsing logic
├── 📊 architecture_visualizer.py    # Diagram generation engine (lazy-loaded)
├── 🚀 setup_and_run.sh             # Automated setup script
├── 📋 requirements_streamlit.txt    # Python dependencies
├── 📖 README.md                    # This documentation
├── 🏗️ ARCHITECTURE_DOCUMENTATION.md # Technical implementation details
├── ⚙️ .streamlit/config.toml       # Streamlit configuration
└── 🔒 .gitignore                   # Git exclusions (protects state files)
```

## Example Output

The tool will generate:

1. **Console Analysis**: Detailed breakdown of resources, providers, and statistics
2. **PNG Diagrams**: Visual architecture diagrams showing:
   - Resource groupings (by VNet, VPC, Resource Group)
   - Resource relationships and dependencies
   - Clear labeling and organization

## ⚡ Performance Optimizations

### **Lazy Loading Architecture**
- **Problem**: Heavy diagram imports caused 30+ second startup times
- **Solution**: Import-on-demand pattern reduces startup by **80%**
- **Impact**: App starts in 3-5 seconds instead of 30-45 seconds

### **Streamlit Caching**
- Resource analysis cached by file hash
- UI interactions remain instant
- Memory-efficient session management

### **Technical Innovation**
```python
# Before: Slow startup with all imports
from diagrams import Diagram, Cluster, Edge
# ... 20+ heavy imports at startup

# After: Fast startup with lazy imports
def _get_diagram_imports(self):
    # Only import when actually generating diagrams
    from diagrams import Diagram, Cluster, Edge
    return {...}
```

## 🔧 Customization

### **Adding New Resource Types**

1. **Extend resource mappings** in `architecture_visualizer.py`:
```python
self.azure_resource_types = {
    'azurerm_new_resource': 'NewResourceIcon',
    # ... existing mappings
}
```

2. **Add corresponding icon** in `_get_diagram_imports()`

### **Custom AI Providers**

Extend the `analyze_with_llm()` method to support additional LLM providers.

## 🛠️ Troubleshooting

### **Common Issues**

| Issue | Solution |
|-------|----------|
| **Graphviz not found** | Install Graphviz and add to PATH |
| **Slow startup** | Use optimized version with lazy loading |
| **Empty diagrams** | Verify state files contain resources |
| **Import errors** | Run `pip install -r requirements_streamlit.txt` |
| **Port already in use** | Change port in `.streamlit/config.toml` |

### **Performance Issues**

**Before optimization**: 30-45 second startup  
**After optimization**: 3-5 second startup ✅

If experiencing slow performance, ensure you're using the latest version with lazy loading optimizations.

### **Debug Mode**

Enable Streamlit debug mode:
```bash
streamlit run streamlit_app.py --logger.level=debug
```

## 📋 Requirements

- **Python**: 3.8+
- **Streamlit**: 1.28+
- **Graphviz**: Latest version
- **Memory**: 2GB+ recommended
- **Browser**: Modern browser with JavaScript enabled

## 📜 License

This project is open source and available under the **MIT License**.

## 🌟 Star History

If this tool helped you visualize your infrastructure, please ⭐ star the repository!

## 🎨 Example Output

### **Web Interface Screenshots**
- 📊 **Dashboard**: Resource statistics and provider detection
- 🎨 **Diagrams**: Interactive architecture visualizations
- 🤖 **AI Analysis**: Automated insights and recommendations

### **Generated Diagrams**
- **Azure**: Resource Groups → VNets → Subnets → VMs
- **AWS**: VPCs → Availability Zones → Subnets → EC2
- **GCP**: Projects → Networks → Zones → Compute Instances

### **AI-Powered Insights**
```
🔍 Infrastructure Analysis
Provider: AZURE | Resources: 15 | Types: 8 | Connections: 12

📊 Categories
🖥️ Compute: 3 resources
🌐 Network: 8 resources  
💾 Storage: 2 resources
🔒 Security: 2 resources

💡 AI Recommendations:
• Consider implementing network segmentation
• Review security group configurations
• Optimize storage account redundancy
```

## 🚀 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │  State Parser    │    │   Visualizer    │
│   Web UI        │◄──►│                  │◄──►│   (Lazy Load)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   File Upload   │    │  JSON Parsing    │    │  PNG/SVG       │
│   & Validation  │    │  & Resource      │    │  Generation     │
│                 │    │  Extraction      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **Development Setup**
```bash
git clone https://github.com/MaruthanA/terraform_archgenerator.git
cd terraform_archgenerator
./setup_and_run.sh
```

## 📄 Documentation

- **README.md**: User guide and quick start
- **ARCHITECTURE_DOCUMENTATION.md**: Technical implementation details
- **Code Comments**: Inline documentation for developers

## 🔒 Security

- **State files excluded** from Git tracking
- **API keys** handled securely via environment variables
- **Temporary files** automatically cleaned up
- **No data persistence** - files processed in memory

---

**Made with ❤️ for the Terraform community**

This tool makes it easy to visualize and understand your Terraform-managed infrastructure across multiple cloud providers with modern web interface and AI-powered insights.
