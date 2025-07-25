import streamlit as st
import os
import markdown2
import re
from datetime import datetime
import pandas as pd
from pathlib import Path
import json

st.set_page_config(
    page_title="FedRAMP Document Browser",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
FEDRAMP_DOCS_PATH = Path("fedramp-docs/markdown")
FEDRAMP_RFCS_PATH = Path("fedramp-rfcs/rfc")
FEDRAMP_ROADMAP_PATH = Path("fedramp-roadmap")

DOCUMENTS = {
    "📋 Standards": {
        "Key Security Indicators (with Controls)": ("docs", "FRMR.KSI.key-security-indicators-with-controls.md"),
        "Key Security Indicators": ("docs", "FRMR.KSI.key-security-indicators.md"), 
        "20x Low Pilot Requirements": ("docs", "FRMR.LOW.20x-low-pilot.md"),
        "Minimum Assessment Standard": ("docs", "FRMR.MAS.minimum-assessment-standard.md"),
        "Significant Change Notifications": ("docs", "FRMR.SCN.significant-change-notifications.md")
    },
    "📝 RFCs": {
        "RFC 0001: New Comment Process": ("rfc", "0001.md"),
        "RFC 0002: 3PAO Requirements": ("rfc", "0002.md"),
        "RFC 0003: Review Initiation Check": ("rfc", "0003.md"),
        "RFC 0004: Boundary Policy": ("rfc", "0004.md"),
        "RFC 0005: Minimum Assessment Scope": ("rfc", "0005.md"),
        "RFC 0006: Key Security Indicators": ("rfc", "0006.md"),
        "RFC 0007: Significant Change Notification": ("rfc", "0007.md"),
        "RFC 0008: Continuous Reporting Standard": ("rfc", "0008.md"),
        "RFC 0009: SCN Technical Assistance": ("rfc", "0009.md"),
        "RFC 0010: Scope Interpretation": ("rfc", "0010.md"),
        "RFC 0011: Storing and Sharing Standard": ("rfc", "0011.md"),
        "RFC 0012: Vulnerability Management": ("rfc", "0012.md")
    },
    "🗺️ Roadmap": {
        "Roadmap Overview": ("roadmap", "README.md"),
        "Sprint Progress Updates": ("roadmap", "PROGRESS.md")
    }
}

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "📋 Standards"
if 'selected_doc' not in st.session_state:
    st.session_state.selected_doc = list(DOCUMENTS["📋 Standards"].keys())[0]
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""

def load_markdown_file(doc_type, filename):
    """Load and parse markdown file from FedRAMP docs, RFCs, or roadmap"""
    if doc_type == "docs":
        filepath = FEDRAMP_DOCS_PATH / filename
    elif doc_type == "rfc":
        filepath = FEDRAMP_RFCS_PATH / filename
    elif doc_type == "roadmap":
        filepath = FEDRAMP_ROADMAP_PATH / filename
    else:
        return f"Error: Unknown document type {doc_type}"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File {filename} not found"
    except Exception as e:
        return f"Error loading file: {str(e)}"

def search_in_content(content, search_term):
    """Search for term in content and highlight matches"""
    if not search_term:
        return content
    
    # Escape special regex characters
    escaped_term = re.escape(search_term)
    
    # Case-insensitive search and highlight
    pattern = re.compile(f'({escaped_term})', re.IGNORECASE)
    highlighted = pattern.sub(r'<mark style="background-color: yellow;">\1</mark>', content)
    
    return highlighted

def extract_control_ids(content):
    """Extract control IDs from content (e.g., AC-1, AU-2)"""
    pattern = r'\b[A-Z]{2}-\d{1,2}(?:\(\d+\))?\b'
    controls = list(set(re.findall(pattern, content)))
    return sorted(controls)

def get_last_update_time():
    """Get the last update time of the FedRAMP submodule"""
    try:
        import subprocess
        # First try to get the submodule's last commit date
        result = subprocess.run(
            ['git', 'submodule', 'status', 'fedramp-docs'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0 and result.stdout:
            # Extract commit hash from submodule status
            commit_hash = result.stdout.strip().split()[0].lstrip('+')
            
            # Get the modification time of the submodule directory as fallback
            submodule_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fedramp-docs')
            if os.path.exists(submodule_path):
                mod_time = os.path.getmtime(submodule_path)
                from datetime import datetime
                return datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
        
        return "Just synced"
    except Exception as e:
        return "Recently updated"

# Sidebar
with st.sidebar:
    st.title("🔒 FedRAMP Reference")
    
    # Show last update
    last_update = get_last_update_time()
    st.info(f"📅 Last Updated: {last_update}")
    
    # Category selector
    st.subheader("📁 Select Category")
    selected_category = st.radio(
        "Choose a category",
        options=list(DOCUMENTS.keys()),
        index=list(DOCUMENTS.keys()).index(st.session_state.selected_category)
    )
    st.session_state.selected_category = selected_category
    
    # Document selector
    st.subheader("📄 Select Document")
    doc_options = list(DOCUMENTS[selected_category].keys())
    # Reset selected_doc if category changed
    if st.session_state.selected_doc not in doc_options:
        st.session_state.selected_doc = doc_options[0]
    
    selected_doc = st.selectbox(
        "Choose a document",
        options=doc_options,
        index=doc_options.index(st.session_state.selected_doc) if st.session_state.selected_doc in doc_options else 0
    )
    st.session_state.selected_doc = selected_doc
    
    # Search
    st.subheader("🔍 Search")
    search_term = st.text_input(
        "Search for control IDs or keywords",
        value=st.session_state.search_term,
        placeholder="e.g., AC-1, encryption, logging"
    )
    st.session_state.search_term = search_term
    
    # Baseline filter (placeholder for future)
    st.subheader("🎯 Filter by Baseline")
    baseline = st.multiselect(
        "Select baselines",
        options=["Low", "Moderate", "High"],
        default=["Low", "Moderate", "High"]
    )
    
    # Info
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This app provides easy access to FedRAMP 20x documentation. "
        "It automatically updates daily from the official FedRAMP GitHub repository."
    )

# Main content area
st.title(f"📋 {selected_doc}")

# Load the selected document
doc_type, filename = DOCUMENTS[st.session_state.selected_category][selected_doc]
content = load_markdown_file(doc_type, filename)

# Apply search highlighting if there's a search term
if search_term:
    content = search_in_content(content, search_term)
    
    # Count matches
    matches = len(re.findall(re.escape(search_term), content, re.IGNORECASE))
    if matches > 0:
        st.success(f"Found {matches} matches for '{search_term}'")
    else:
        st.warning(f"No matches found for '{search_term}'")

# Display the content
with st.container():
    # Convert markdown to HTML with tables support
    html_content = markdown2.markdown(
        content, 
        extras=["tables", "fenced-code-blocks", "header-ids"]
    )
    
    # Add custom CSS for better table rendering
    st.markdown("""
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    mark {
        background-color: yellow;
        padding: 2px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the HTML content
    st.markdown(html_content, unsafe_allow_html=True)

# Footer with controls summary
with st.expander("📊 Document Summary"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Extract and display control IDs found
        controls = extract_control_ids(content)
        st.metric("Total Controls Referenced", len(controls))
    
    with col2:
        # Word count
        word_count = len(content.split())
        st.metric("Word Count", f"{word_count:,}")
    
    with col3:
        # Document size
        doc_size = len(content.encode('utf-8'))
        st.metric("Document Size", f"{doc_size / 1024:.1f} KB")
    
    # List all controls
    if controls:
        st.subheader("Controls Found in Document")
        # Display in columns
        cols = st.columns(4)
        for idx, control in enumerate(controls):
            cols[idx % 4].write(control)

# Export functionality
st.markdown("---")
st.subheader("📥 Export Options")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write("Export the current document or control list")

with col2:
    # Export as CSV
    if st.button("💾 Export Controls as CSV"):
        controls = extract_control_ids(content)
        if controls:
            df = pd.DataFrame({
                'Control ID': controls,
                'Document': selected_doc,
                'Export Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"fedramp_controls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No controls found to export")

with col3:
    # Export as JSON
    if st.button("📋 Export Controls as JSON"):
        controls = extract_control_ids(content)
        if controls:
            export_data = {
                'document': selected_doc,
                'export_date': datetime.now().isoformat(),
                'total_controls': len(controls),
                'controls': controls,
                'metadata': {
                    'source': 'FedRAMP Official Documentation',
                    'last_update': get_last_update_time()
                }
            }
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"fedramp_controls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("No controls found to export")