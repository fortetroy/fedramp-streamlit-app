import streamlit as st
import pandas as pd
import re
from pathlib import Path
import time
from typing import Dict, List, Tuple
import json

st.set_page_config(
    page_title="FedRAMP Global Search",
    page_icon="🔍",
    layout="wide"
)

# Constants
FEDRAMP_DOCS_PATH = Path("fedramp-docs/markdown")
FEDRAMP_RFCS_PATH = Path("fedramp-rfcs/rfc")
FEDRAMP_ROADMAP_PATH = Path("fedramp-roadmap")
EXCEL_PATH = Path("data/baselines/FedRAMP_Security_Controls_Baseline.xlsx")

# Initialize session state for search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'saved_searches' not in st.session_state:
    st.session_state.saved_searches = []

@st.cache_data
def load_all_documents():
    """Load all documents for searching"""
    documents = {}
    
    # Load Standards
    for file in FEDRAMP_DOCS_PATH.glob("*.md"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                documents[f"Standards/{file.name}"] = {
                    'content': f.read(),
                    'type': 'Standards',
                    'path': str(file)
                }
        except:
            pass
    
    # Load RFCs
    for file in FEDRAMP_RFCS_PATH.glob("*.md"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                documents[f"RFC/{file.name}"] = {
                    'content': f.read(),
                    'type': 'RFC',
                    'path': str(file)
                }
        except:
            pass
    
    # Load Roadmap
    for file in FEDRAMP_ROADMAP_PATH.glob("*.md"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                documents[f"Roadmap/{file.name}"] = {
                    'content': f.read(),
                    'type': 'Roadmap',
                    'path': str(file)
                }
        except:
            pass
    
    return documents

@st.cache_data
def load_control_baselines():
    """Load all baseline controls"""
    try:
        all_sheets = pd.read_excel(EXCEL_PATH, sheet_name=None, header=1)
        controls = {}
        
        for sheet_name, df in all_sheets.items():
            if 'SORT ID' in df.columns and 'baseline' in sheet_name.lower():
                for _, row in df.iterrows():
                    control_id = str(row['SORT ID']).strip()
                    controls[control_id] = {
                        'baseline': sheet_name,
                        'name': row.get('Control Name', ''),
                        'description': row.get('NIST Control Description', '')[:500] + '...' if pd.notna(row.get('NIST Control Description', '')) else '',
                        'family': row.get('Family', '')
                    }
        
        return controls
    except:
        return {}

def search_documents(query: str, documents: Dict, search_type: str = "all", case_sensitive: bool = False) -> List[Tuple[str, Dict, List[str]]]:
    """Search across all documents"""
    results = []
    
    # Prepare search pattern
    if not case_sensitive:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
    else:
        pattern = re.compile(re.escape(query))
    
    for doc_name, doc_data in documents.items():
        if search_type != "all" and doc_data['type'] != search_type:
            continue
            
        content = doc_data['content']
        matches = list(pattern.finditer(content))
        
        if matches:
            # Extract context around matches
            contexts = []
            for match in matches[:5]:  # Limit to first 5 matches per doc
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end]
                contexts.append({
                    'text': context,
                    'start': match.start(),
                    'match': match.group()
                })
            
            results.append((doc_name, doc_data, contexts))
    
    return results

def search_controls(query: str, controls: Dict) -> List[Tuple[str, Dict]]:
    """Search control IDs and descriptions"""
    results = []
    query_lower = query.lower()
    
    for control_id, control_data in controls.items():
        # Search in control ID, name, and description
        searchable = f"{control_id} {control_data.get('name', '')} {control_data.get('description', '')}".lower()
        
        if query_lower in searchable:
            results.append((control_id, control_data))
    
    return sorted(results, key=lambda x: x[0])

# Main UI
st.title("🔍 FedRAMP Global Search")
st.markdown("Search across all FedRAMP documentation, RFCs, roadmap, and control baselines")

# Search interface
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_query = st.text_input(
        "Search Query",
        placeholder="Enter control ID (e.g., AC-1), keyword, or phrase",
        help="Search across all FedRAMP resources"
    )

with col2:
    search_type = st.selectbox(
        "Document Type",
        ["all", "Standards", "RFC", "Roadmap", "Controls"],
        help="Filter search to specific document types"
    )

with col3:
    case_sensitive = st.checkbox("Case Sensitive", value=False)
    regex_search = st.checkbox("Regex Search", value=False)

# Advanced filters
with st.expander("🔧 Advanced Search Options"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        control_families = st.multiselect(
            "Control Families",
            ["AC", "AT", "AU", "CA", "CM", "CP", "IA", "IR", "MA", "MP", "PE", "PL", "PS", "RA", "SA", "SC", "SI", "SR"],
            help="Filter by control families"
        )
    
    with col2:
        baselines = st.multiselect(
            "Baselines",
            ["Low Baseline", "Moderate Baseline", "High Baseline"],
            help="Filter by FedRAMP baselines"
        )
    
    with col3:
        include_ksi = st.checkbox("Include KSI Controls", value=True)
        include_deprecated = st.checkbox("Include Deprecated", value=False)

# Search button and actions
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])

with col1:
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.search_history = []
        st.rerun()

with col3:
    if search_query and st.button("💾 Save Search", use_container_width=True):
        if search_query not in st.session_state.saved_searches:
            st.session_state.saved_searches.append(search_query)
            st.success("Search saved!")

# Saved searches
if st.session_state.saved_searches:
    with st.expander("📌 Saved Searches"):
        for idx, saved_search in enumerate(st.session_state.saved_searches):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"📍 {saved_search}", key=f"saved_{idx}", use_container_width=True):
                    st.session_state.search_query = saved_search
                    st.rerun()
            with col2:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.saved_searches.pop(idx)
                    st.rerun()

# Perform search
if search_button and search_query:
    # Add to search history
    if search_query not in st.session_state.search_history:
        st.session_state.search_history.insert(0, search_query)
        st.session_state.search_history = st.session_state.search_history[:10]  # Keep last 10
    
    with st.spinner(f"Searching for '{search_query}'..."):
        start_time = time.time()
        
        # Load data
        if search_type in ["all", "Standards", "RFC", "Roadmap"]:
            documents = load_all_documents()
            doc_results = search_documents(search_query, documents, search_type, case_sensitive)
        else:
            doc_results = []
        
        if search_type in ["all", "Controls"]:
            controls = load_control_baselines()
            control_results = search_controls(search_query, controls)
        else:
            control_results = []
        
        search_time = time.time() - start_time
    
    # Display results summary
    st.markdown("---")
    total_results = len(doc_results) + len(control_results)
    st.success(f"Found {total_results} results in {search_time:.2f} seconds")
    
    # Create tabs for different result types
    if total_results > 0:
        tabs = []
        if doc_results:
            tabs.append("📄 Documents")
        if control_results:
            tabs.append("🎯 Controls")
        tabs.append("📊 Summary")
        
        tab_objects = st.tabs(tabs)
        tab_idx = 0
        
        # Document results
        if doc_results and "📄 Documents" in tabs:
            with tab_objects[tab_idx]:
                st.subheader(f"Document Results ({len(doc_results)})")
                
                for doc_name, doc_data, contexts in doc_results:
                    with st.expander(f"**{doc_name}** - {len(contexts)} matches"):
                        st.write(f"**Type:** {doc_data['type']}")
                        st.write(f"**Path:** `{doc_data['path']}`")
                        
                        st.markdown("**Matches:**")
                        for i, context in enumerate(contexts, 1):
                            # Highlight the match
                            highlighted = context['text'].replace(
                                context['match'],
                                f"**:yellow[{context['match']}]**"
                            )
                            st.markdown(f"{i}. ...{highlighted}...")
            tab_idx += 1
        
        # Control results
        if control_results and "🎯 Controls" in tabs:
            with tab_objects[tab_idx]:
                st.subheader(f"Control Results ({len(control_results)})")
                
                # Create DataFrame for controls
                control_data = []
                for control_id, info in control_results:
                    control_data.append({
                        'Control ID': control_id,
                        'Name': info.get('name', ''),
                        'Family': info.get('family', ''),
                        'Baseline': info.get('baseline', ''),
                        'Description': info.get('description', '')[:100] + '...'
                    })
                
                df = pd.DataFrame(control_data)
                st.dataframe(df, use_container_width=True, height=400)
                
                # Export options
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Export Control Results",
                    data=csv,
                    file_name=f"control_search_results_{search_query.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            tab_idx += 1
        
        # Summary tab
        with tab_objects[tab_idx]:
            st.subheader("Search Summary")
            
            # Results by type
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Results by Type:**")
                summary_data = {}
                
                if doc_results:
                    for _, doc_data, _ in doc_results:
                        doc_type = doc_data['type']
                        summary_data[doc_type] = summary_data.get(doc_type, 0) + 1
                
                if control_results:
                    summary_data['Controls'] = len(control_results)
                
                for doc_type, count in summary_data.items():
                    st.metric(doc_type, count)
            
            with col2:
                if control_results:
                    st.markdown("**Control Families Found:**")
                    families = {}
                    for _, info in control_results:
                        family = info.get('family', 'Unknown')
                        families[family] = families.get(family, 0) + 1
                    
                    for family, count in sorted(families.items()):
                        st.write(f"- {family}: {count} controls")

# Search history
if st.session_state.search_history:
    with st.sidebar:
        st.subheader("🕒 Recent Searches")
        for query in st.session_state.search_history:
            if st.button(f"🔍 {query}", key=f"history_{query}", use_container_width=True):
                st.session_state.search_query = query
                st.rerun()

# Tips
with st.sidebar:
    st.markdown("---")
    st.subheader("💡 Search Tips")
    st.markdown("""
    - Use **control IDs** like `AC-1` or `AU-2`
    - Search for **keywords** like `encryption` or `logging`
    - Use **quotes** for exact phrases: `"continuous monitoring"`
    - Enable **regex** for pattern matching
    - Filter by **document type** for faster results
    - **Save searches** you use frequently
    """)