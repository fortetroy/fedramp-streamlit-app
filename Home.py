import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime
import subprocess
import os

# Initialize submodules if needed
try:
    from setup_submodules import setup_submodules
    setup_submodules()
except:
    pass

st.set_page_config(
    page_title="FedRAMP Analysis Hub",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🏛️ FedRAMP Analysis Hub")
st.markdown("### A comprehensive data analysis tool for FedRAMP documentation and controls")

# Introduction
st.markdown("""
This application was created to facilitate data analysis and research of FedRAMP (Federal Risk and Authorization Management Program) 
documentation, controls, and requirements. It provides a centralized platform for security professionals, compliance teams, 
and cloud service providers to efficiently navigate and analyze FedRAMP resources.
""")

# Purpose section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Purpose")
    st.markdown("""
    This project serves several key objectives:
    
    - **📊 Data Analysis**: Enable comprehensive analysis of FedRAMP controls across different baselines
    - **🔍 Enhanced Searchability**: Provide powerful search capabilities across all FedRAMP documentation
    - **🔄 Control Mapping**: Facilitate crosswalk analysis between KSI controls and NIST baselines
    - **📈 Compliance Insights**: Help organizations understand control coverage and requirements
    - **🚀 Efficiency**: Reduce time spent searching through multiple documents and spreadsheets
    - **🔄 Stay Current**: Automatically sync with official FedRAMP repositories daily
    """)

with col2:
    # Get last update time
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cd', '--date=relative', 'fedramp-docs'],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent)
        )
        if result.returncode == 0 and result.stdout.strip():
            last_update = result.stdout.strip()
        else:
            # Fallback to modification time
            submodule_path = Path(__file__).parent / 'fedramp-docs'
            if submodule_path.exists():
                import os
                mod_time = os.path.getmtime(submodule_path)
                last_update = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
            else:
                last_update = "Unknown"
    except:
        last_update = "Unknown"
    
    st.info(f"""
    **📅 Last Repository Update**
    
    {last_update}
    
    The FedRAMP documentation is automatically synced daily from official repositories.
    """)
    
    # Quick stats
    st.metric("Total Documents", "20+")
    st.metric("Control Baselines", "3")
    st.metric("Key Security Indicators", "51")

# Features overview
st.markdown("---")
st.markdown("### 🛠️ Available Tools")

# Create feature cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    #### 📋 Document Browser
    Browse and search through:
    - FedRAMP 20x Standards
    - Request for Comments (RFCs)
    - Roadmap and Sprint Updates
    - Export controls and findings
    """)
    if st.button("Go to Document Browser →", key="doc_browser"):
        st.switch_page("pages/1_📋_Document_Browser.py")

with col2:
    st.markdown("""
    #### 🔄 Control Crosswalk
    Analyze control relationships:
    - Compare KSI with baselines
    - Identify control gaps
    - Export crosswalk results
    - View KSI categories
    """)
    if st.button("Go to Control Crosswalk →", key="crosswalk"):
        st.switch_page("pages/4_🔄_Control_Crosswalk.py")

with col3:
    st.markdown("""
    #### 🔍 Global Search
    Search across all documents:
    - All FedRAMP docs
    - RFCs and roadmap
    - Full-text search
    - Search history
    """)
    if st.button("Go to Global Search →", key="search"):
        st.switch_page("pages/2_🔍_Global_Search.py")

with col4:
    st.markdown("""
    #### 🎯 Control Search
    Find specific controls:
    - Search by control ID
    - Fuzzy matching
    - Control descriptions
    - Export results
    """)
    if st.button("Go to Control Search →", key="control_search"):
        st.switch_page("pages/3_🎯_Control_Search.py")

# Data sources
st.markdown("---")
st.markdown("### 📚 Data Sources")

sources_col1, sources_col2 = st.columns(2)

with sources_col1:
    st.markdown("""
    This application aggregates data from official FedRAMP repositories:
    
    - **[FedRAMP Documentation](https://github.com/FedRAMP/docs)**: Official standards and requirements
    - **[FedRAMP RFCs](https://github.com/FedRAMP/rfcs)**: Request for Comments and proposals
    - **[FedRAMP Roadmap](https://github.com/FedRAMP/roadmap)**: Development roadmap and updates
    - **Baseline Controls**: Excel spreadsheet with Low, Moderate, and High baselines
    """)

with sources_col2:
    st.markdown("""
    **Key Resources Included:**
    
    - ✅ Key Security Indicators (KSI) with controls mapping
    - ✅ Minimum Assessment Standards (MAS)
    - ✅ Significant Change Notifications (SCN)
    - ✅ 20x Low Pilot Requirements
    - ✅ All 12 published RFCs
    - ✅ Sprint progress updates
    """)

# Use cases
st.markdown("---")
st.markdown("### 💡 Common Use Cases")

use_case_tabs = st.tabs(["For CSPs", "For 3PAOs", "For Agencies", "For Researchers"])

with use_case_tabs[0]:
    st.markdown("""
    **Cloud Service Providers (CSPs)** can use this tool to:
    - Quickly identify applicable controls for their authorization level
    - Search for specific requirement details across all documentation
    - Understand KSI mappings to NIST controls
    - Track changes in FedRAMP requirements through RFCs
    - Export control lists for implementation tracking
    """)

with use_case_tabs[1]:
    st.markdown("""
    **Third Party Assessment Organizations (3PAOs)** can use this tool to:
    - Cross-reference controls between KSI and baselines
    - Search for assessment criteria and guidance
    - Analyze control coverage across different baselines
    - Access the latest assessment standards
    - Prepare assessment documentation
    """)

with use_case_tabs[2]:
    st.markdown("""
    **Federal Agencies** can use this tool to:
    - Review FedRAMP requirements for cloud services
    - Understand control baselines for different impact levels
    - Access current RFCs and roadmap items
    - Search for specific security requirements
    - Analyze control implementation requirements
    """)

with use_case_tabs[3]:
    st.markdown("""
    **Security Researchers and Analysts** can use this tool to:
    - Analyze control distribution across families
    - Study KSI category breakdowns
    - Export data for further analysis
    - Track evolution of FedRAMP requirements
    - Compare control coverage across baselines
    """)

# Getting started
st.markdown("---")
st.markdown("### 🚀 Getting Started")

getting_started_col1, getting_started_col2, getting_started_col3 = st.columns(3)

with getting_started_col1:
    st.markdown("""
    **1. Explore Documents**
    
    Start with the Document Browser to familiarize yourself with available FedRAMP resources.
    """)

with getting_started_col2:
    st.markdown("""
    **2. Search for Controls**
    
    Use Global Search or Control Search to find specific controls or requirements.
    """)

with getting_started_col3:
    st.markdown("""
    **3. Analyze Relationships**
    
    Use the Control Crosswalk to understand how KSIs map to baseline controls.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>This tool is not affiliated with or endorsed by FedRAMP. It aggregates publicly available information for analysis purposes.</p>
    <p>All FedRAMP documentation is sourced from official public repositories.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    # Load some quick stats
    # Count documents
    doc_count = 0
    rfc_count = 0
    debug_info = []
    
    try:
        import os
        
        # Try different path approaches
        base_paths = [
            Path(os.getcwd()),
            Path(__file__).parent,
            Path(".")
        ]
        
        docs_found = False
        rfcs_found = False
        
        for base_path in base_paths:
            docs_path = base_path / "fedramp-docs" / "markdown"
            rfcs_path = base_path / "fedramp-rfcs" / "rfc"
            
            debug_info.append(f"Trying base path: {base_path}")
            debug_info.append(f"Docs path exists: {docs_path.exists()}")
            debug_info.append(f"RFCs path exists: {rfcs_path.exists()}")
            
            if docs_path.exists() and not docs_found:
                md_files = list(docs_path.glob("*.md"))
                doc_count = len([f for f in md_files if f.is_file()])
                docs_found = True
                debug_info.append(f"Found {doc_count} docs in {docs_path}")
            
            if rfcs_path.exists() and not rfcs_found:
                rfc_files = list(rfcs_path.glob("*.md"))
                rfc_count = len([f for f in rfc_files if f.is_file() and f.stem.isdigit()])
                rfcs_found = True
                debug_info.append(f"Found {rfc_count} RFCs in {rfcs_path}")
            
            if docs_found and rfcs_found:
                break
    
    except Exception as e:
        debug_info.append(f"Error: {str(e)}")
    
    # If still zero, use known counts
    if doc_count == 0:
        doc_count = 5  # Known count
        debug_info.append("Using fallback doc count: 5")
    if rfc_count == 0:
        rfc_count = 12  # Known count
        debug_info.append("Using fallback RFC count: 12")
    
    st.metric("Standards Documents", doc_count)
    st.metric("Published RFCs", rfc_count)
    st.metric("Control Families", "18")
    
    # Debug expander (can be removed later)
    with st.expander("Debug Info", expanded=False):
        for info in debug_info:
            st.text(info)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("""
    - [FedRAMP.gov](https://www.fedramp.gov)
    - [FedRAMP Marketplace](https://marketplace.fedramp.gov)
    - [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
    """)
    
    st.markdown("---")
    st.markdown("### 🔄 Repository Status")
    
    # Check each submodule
    submodules = {
        'fedramp-docs': 'Standards Docs',
        'fedramp-rfcs': 'RFCs',
        'fedramp-roadmap': 'Roadmap'
    }
    
    for submodule, name in submodules.items():
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%cd', '--date=short', submodule],
                capture_output=True,
                text=True,
                cwd=str(Path(__file__).parent)
            )
            if result.returncode == 0 and result.stdout.strip():
                date = result.stdout.strip()
                st.write(f"**{name}**: {date}")
            else:
                st.write(f"**{name}**: Unknown")
        except:
            st.write(f"**{name}**: Error")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This analysis tool was created to streamline FedRAMP compliance research and control analysis. 
    It automatically syncs with official repositories to ensure up-to-date information.
    
    **Version**: 1.0.0
    """)