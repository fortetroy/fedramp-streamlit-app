# FedRAMP Analysis Hub

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/yourusername/fedramp-analysis-hub)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Update FedRAMP Docs](https://github.com/yourusername/fedramp-analysis-hub/actions/workflows/update-fedramp-daily.yml/badge.svg)](https://github.com/yourusername/fedramp-analysis-hub/actions/workflows/update-fedramp-daily.yml)

A comprehensive data analysis tool for FedRAMP documentation and controls. This Streamlit application was created to facilitate research and analysis of FedRAMP requirements, providing security professionals and compliance teams with powerful search and analysis capabilities across all FedRAMP resources.

## 🎯 Purpose

This project was developed to address common challenges in FedRAMP compliance:

- **Fragmented Documentation**: FedRAMP resources are spread across multiple repositories and formats
- **Search Limitations**: Difficulty finding specific controls or requirements across documents
- **Control Mapping**: Complex relationships between KSIs and NIST baselines
- **Manual Analysis**: Time-consuming process to analyze control coverage
- **Version Control**: Keeping up with frequent updates to FedRAMP documentation

## 🚀 Key Benefits

- **Centralized Access**: All FedRAMP documentation in one place
- **Powerful Search**: Global and control-specific search with fuzzy matching
- **Automated Updates**: Daily synchronization with official FedRAMP repositories
- **Data Export**: Export analysis results for further processing
- **Cross-Reference Analysis**: Understand relationships between different control sets

## Features

### Document Browser
- 📄 Browse all FedRAMP 20x documentation and RFCs
- 🔍 Search for control IDs and keywords within documents
- 🎯 Filter by baselines (Low, Moderate, High)
- 📥 Export controls as CSV or JSON
- 🔄 Automatic daily updates from FedRAMP official repos
- 📅 Last update tracking
- 📝 Access to all FedRAMP RFCs (Request for Comments)
- 🗺️ View FedRAMP roadmap and sprint progress updates

### Advanced Search Capabilities
- 🔍 **Global Search**: Search across all documents, RFCs, roadmap, and control baselines
- 🎯 **Control Search**: Dedicated control search with autocomplete and fuzzy matching
- 📊 **Control Crosswalk**: Compare KSI controls with any FedRAMP baseline
- 🔎 **Smart Features**:
  - Fuzzy search for typos and approximate matches
  - Search history and saved searches
  - Context highlighting in search results
  - Advanced filters by control family, baseline, and KSI status
  - Export search results as CSV

## Setup

1. Clone this repository:
```bash
git clone --recurse-submodules https://github.com/yourusername/fedramp-analysis-hub.git
cd fedramp-analysis-hub
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run Home.py
```

## Deployment

### Streamlit Community Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your repository

### Manual Updates

To manually update the FedRAMP documentation:
```bash
git submodule update --remote fedramp-docs
git add fedramp-docs
git commit -m "Update FedRAMP docs"
git push
```

## Automatic Updates

The app includes a GitHub Action that runs daily at 2 AM UTC to check for updates in the FedRAMP repository. When updates are found, they are automatically committed and the Streamlit app is redeployed.

## Documents Included

### Standards
- Key Security Indicators (with Controls)
- Key Security Indicators
- 20x Low Pilot Requirements
- Minimum Assessment Standard
- Significant Change Notifications

### RFCs (Request for Comments)
- RFC 0001: New Comment Process
- RFC 0002: 3PAO Requirements
- RFC 0003: Review Initiation Check
- RFC 0004: Boundary Policy
- RFC 0005: Minimum Assessment Scope
- RFC 0006: Key Security Indicators
- RFC 0007: Significant Change Notification
- RFC 0008: Continuous Reporting Standard
- RFC 0009: SCN Technical Assistance
- RFC 0010: Scope Interpretation
- RFC 0011: Storing and Sharing Standard
- RFC 0012: Vulnerability Management

### Roadmap
- Roadmap Overview - Overview of FedRAMP teams and delivery approach
- Sprint Progress Updates - Detailed updates on current sprint activities and progress

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repository
5. Set Python version to 3.8 or higher

### Local Deployment

The app can also be deployed locally using Docker or any Python-capable server.

## 📋 Requirements

- Python 3.8 or higher
- 4GB RAM minimum
- Modern web browser

## 🔄 Data Updates

The application automatically syncs with official FedRAMP repositories daily at 2 AM UTC. You can also trigger manual updates through GitHub Actions.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an **unofficial** tool created for analysis purposes. It is not affiliated with, endorsed by, or connected to FedRAMP or any government agency. All FedRAMP documentation is sourced from publicly available repositories.

The tool is provided "as is" without warranty of any kind. Users should verify all information with official FedRAMP sources.

## 🙏 Acknowledgments

- FedRAMP for providing public access to their documentation
- The Streamlit team for their excellent framework
- All contributors to this project

## 📞 Contact

For questions or suggestions, please open an issue in the GitHub repository.