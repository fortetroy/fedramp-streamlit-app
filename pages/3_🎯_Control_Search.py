import streamlit as st
import pandas as pd
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

st.set_page_config(
    page_title="FedRAMP Control Search",
    page_icon="🎯",
    layout="wide"
)

# Constants
EXCEL_PATH = Path("data/baselines/FedRAMP_Security_Controls_Baseline.xlsx")
KSI_PATH = Path("fedramp-docs/markdown/FRMR.KSI.key-security-indicators-with-controls.md")

@st.cache_data
def load_all_controls():
    """Load all controls from baselines and KSI"""
    controls = {}
    
    # Load from Excel baselines
    try:
        all_sheets = pd.read_excel(EXCEL_PATH, sheet_name=None, header=1)
        
        for sheet_name, df in all_sheets.items():
            if 'SORT ID' in df.columns and 'baseline' in sheet_name.lower():
                for _, row in df.iterrows():
                    control_id = str(row['SORT ID']).strip()
                    if control_id and pd.notna(control_id):
                        if control_id not in controls:
                            controls[control_id] = {
                                'id': control_id,
                                'name': row.get('Control Name', ''),
                                'family': row.get('Family', ''),
                                'description': str(row.get('NIST Control Description', ''))[:500],
                                'baselines': [],
                                'fedramp_params': row.get('FedRAMP\nParameter', '') == 'X',
                                'in_ksi': False
                            }
                        controls[control_id]['baselines'].append(sheet_name.replace(' Baseline', ''))
    except Exception as e:
        st.error(f"Error loading Excel: {str(e)}")
    
    # Load KSI controls
    try:
        with open(KSI_PATH, 'r', encoding='utf-8') as f:
            ksi_content = f.read()
        
        # Extract control IDs from KSI
        pattern = r'\b([a-z]{2}-\d{1,2}(?:\.\d+)?)\b'
        ksi_controls = list(set(re.findall(pattern, ksi_content)))
        
        for control in ksi_controls:
            # Normalize to match Excel format
            normalized = control.upper()
            parts = normalized.split('-')
            if len(parts) == 2:
                family, num_part = parts
                if '.' in num_part:
                    num, enhancement = num_part.split('.')
                    num = num.zfill(2)
                    normalized = f"{family}-{num}({enhancement})"
                else:
                    num = num_part.zfill(2)
                    normalized = f"{family}-{num}"
            
            if normalized in controls:
                controls[normalized]['in_ksi'] = True
    except Exception as e:
        st.error(f"Error loading KSI: {str(e)}")
    
    return controls

def get_control_suggestions(query: str, controls: Dict[str, Dict], limit: int = 10) -> List[str]:
    """Get control ID suggestions based on partial input"""
    if not query:
        return []
    
    query = query.upper()
    suggestions = []
    
    # Exact prefix matches first
    for control_id in controls.keys():
        if control_id.startswith(query):
            suggestions.append(control_id)
    
    # Then fuzzy matches
    if len(suggestions) < limit:
        fuzzy_matches = process.extract(
            query, 
            controls.keys(), 
            scorer=fuzz.token_sort_ratio,
            limit=limit - len(suggestions)
        )
        for match, score in fuzzy_matches:
            if score > 70 and match not in suggestions:
                suggestions.append(match)
    
    return suggestions[:limit]

def search_controls(query: str, controls: Dict[str, Dict], search_fields: List[str], fuzzy: bool = False) -> List[Tuple[str, Dict, int]]:
    """Search controls by various fields"""
    results = []
    query_lower = query.lower()
    
    for control_id, control_data in controls.items():
        score = 0
        matched = False
        
        for field in search_fields:
            if field == 'id' and control_id.lower().startswith(query_lower):
                score = 100
                matched = True
                break
            elif field in control_data:
                field_value = str(control_data[field]).lower()
                if fuzzy:
                    match_score = fuzz.partial_ratio(query_lower, field_value)
                    if match_score > 70:
                        score = max(score, match_score)
                        matched = True
                elif query_lower in field_value:
                    score = 90 if field == 'name' else 80
                    matched = True
        
        if matched:
            results.append((control_id, control_data, score))
    
    # Sort by score descending
    return sorted(results, key=lambda x: (-x[2], x[0]))

# Main UI
st.title("🎯 FedRAMP Control Search")
st.markdown("Advanced search for NIST controls across FedRAMP baselines and KSI")

# Search interface
col1, col2 = st.columns([3, 1])

with col1:
    # Control ID search with autocomplete simulation
    control_query = st.text_input(
        "Control ID or Keyword",
        placeholder="Start typing a control ID (e.g., AC, AU-2) or keyword",
        help="Search by control ID, name, or description"
    )

with col2:
    fuzzy_search = st.checkbox("Enable Fuzzy Search", value=True, help="Find approximate matches")

# Search options
search_fields = st.multiselect(
    "Search in fields",
    ["id", "name", "description"],
    default=["id", "name"],
    help="Choose which fields to search"
)

# Filters
with st.expander("🔧 Filters"):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_families = st.multiselect(
            "Control Families",
            ["AC", "AT", "AU", "CA", "CM", "CP", "IA", "IR", "MA", "MP", "PE", "PL", "PS", "RA", "SA", "SC", "SI", "SR"]
        )
    
    with col2:
        filter_baselines = st.multiselect(
            "In Baselines",
            ["Low", "Moderate", "High"]
        )
    
    with col3:
        filter_ksi = st.selectbox(
            "KSI Status",
            ["All", "In KSI", "Not in KSI"]
        )
    
    with col4:
        filter_params = st.selectbox(
            "FedRAMP Parameters",
            ["All", "Has Parameters", "No Parameters"]
        )

# Load controls
with st.spinner("Loading controls..."):
    all_controls = load_all_controls()

# Show suggestions if query is short
if control_query and len(control_query) < 6:
    suggestions = get_control_suggestions(control_query, all_controls)
    if suggestions:
        st.info(f"💡 Did you mean: {', '.join(suggestions[:5])}")

# Search button
if st.button("🔍 Search", type="primary") or control_query:
    if control_query:
        # Perform search
        results = search_controls(control_query, all_controls, search_fields, fuzzy_search)
        
        # Apply filters
        filtered_results = []
        for control_id, control_data, score in results:
            # Family filter
            if filter_families and control_data.get('family') not in filter_families:
                continue
            
            # Baseline filter
            if filter_baselines:
                has_baseline = any(b in control_data.get('baselines', []) for b in filter_baselines)
                if not has_baseline:
                    continue
            
            # KSI filter
            if filter_ksi == "In KSI" and not control_data.get('in_ksi'):
                continue
            elif filter_ksi == "Not in KSI" and control_data.get('in_ksi'):
                continue
            
            # Parameter filter
            if filter_params == "Has Parameters" and not control_data.get('fedramp_params'):
                continue
            elif filter_params == "No Parameters" and control_data.get('fedramp_params'):
                continue
            
            filtered_results.append((control_id, control_data, score))
        
        # Display results
        st.markdown("---")
        st.subheader(f"Search Results ({len(filtered_results)} controls)")
        
        if filtered_results:
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📋 List View", "📊 Table View", "📈 Analytics"])
            
            with tab1:
                # List view with expandable details
                for control_id, control_data, score in filtered_results[:50]:  # Limit to 50
                    with st.expander(f"**{control_id}** - {control_data.get('name', 'N/A')} (Score: {score})"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Family:** {control_data.get('family', 'N/A')}")
                            st.markdown(f"**Description:** {control_data.get('description', 'N/A')}")
                        
                        with col2:
                            st.markdown(f"**Baselines:** {', '.join(control_data.get('baselines', []))}")
                            st.markdown(f"**In KSI:** {'✅' if control_data.get('in_ksi') else '❌'}")
                            st.markdown(f"**FedRAMP Parameters:** {'✅' if control_data.get('fedramp_params') else '❌'}")
            
            with tab2:
                # Table view
                table_data = []
                for control_id, control_data, score in filtered_results:
                    table_data.append({
                        'Control ID': control_id,
                        'Name': control_data.get('name', '')[:50],
                        'Family': control_data.get('family', ''),
                        'Baselines': ', '.join(control_data.get('baselines', [])),
                        'In KSI': '✅' if control_data.get('in_ksi') else '❌',
                        'FedRAMP Params': '✅' if control_data.get('fedramp_params') else '❌',
                        'Score': score
                    })
                
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, height=500)
                
                # Export
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Export Results as CSV",
                    data=csv,
                    file_name=f"control_search_{control_query.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            
            with tab3:
                # Analytics view
                col1, col2 = st.columns(2)
                
                with col1:
                    # Results by family
                    family_counts = {}
                    for _, control_data, _ in filtered_results:
                        family = control_data.get('family', 'Unknown')
                        family_counts[family] = family_counts.get(family, 0) + 1
                    
                    st.markdown("**Results by Control Family:**")
                    for family, count in sorted(family_counts.items()):
                        st.metric(family, count)
                
                with col2:
                    # Results by baseline
                    baseline_counts = {'Low': 0, 'Moderate': 0, 'High': 0}
                    ksi_count = 0
                    param_count = 0
                    
                    for _, control_data, _ in filtered_results:
                        for baseline in control_data.get('baselines', []):
                            if baseline in baseline_counts:
                                baseline_counts[baseline] += 1
                        if control_data.get('in_ksi'):
                            ksi_count += 1
                        if control_data.get('fedramp_params'):
                            param_count += 1
                    
                    st.markdown("**Coverage Metrics:**")
                    st.metric("In Low Baseline", baseline_counts['Low'])
                    st.metric("In Moderate Baseline", baseline_counts['Moderate'])
                    st.metric("In High Baseline", baseline_counts['High'])
                    st.metric("In KSI", ksi_count)
                    st.metric("With FedRAMP Parameters", param_count)
        else:
            st.warning("No controls found matching your search criteria.")

# Quick access controls
with st.sidebar:
    st.subheader("🚀 Quick Access")
    
    # Most searched controls
    common_controls = ["AC-02", "AC-03", "AU-02", "CM-03", "IA-02", "SC-07", "SI-02", "SI-03"]
    st.markdown("**Common Controls:**")
    for control in common_controls:
        if st.button(control, key=f"quick_{control}", use_container_width=True):
            st.session_state.control_query = control
            st.rerun()
    
    st.markdown("---")
    st.markdown("**Search Examples:**")
    st.markdown("""
    - `AC-` - All Access Control controls
    - `encryption` - Controls mentioning encryption
    - `logging` - Controls about logging
    - `IA-02` - Specific control lookup
    """)