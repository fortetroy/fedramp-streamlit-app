import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime
import subprocess
import os

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
col1, col2, col3 = st.columns(3)

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
        st.switch_page("pages/4_Document_Browser.py")

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
        st.switch_page("pages/1_Control_Crosswalk.py")

with col3:
    st.markdown("""
    #### 🔍 Advanced Search
    Powerful search capabilities:
    - Global search across all docs
    - Control-specific search
    - Fuzzy matching
    - Search history
    """)
    if st.button("Go to Global Search →", key="search"):
        st.switch_page("pages/2_Global_Search.py")

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
    try:
        # Count documents
        docs_path = Path("fedramp-docs/markdown")
        rfcs_path = Path("fedramp-rfcs/rfc")
        doc_count = len(list(docs_path.glob("*.md"))) if docs_path.exists() else 0
        rfc_count = len(list(rfcs_path.glob("*.md"))) if rfcs_path.exists() else 0
        
        st.metric("Standards Documents", doc_count)
        st.metric("Published RFCs", rfc_count)
        st.metric("Control Families", "18")
        
    except:
        pass
    
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