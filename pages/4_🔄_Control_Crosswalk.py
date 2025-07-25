import streamlit as st
import pandas as pd
import re
from pathlib import Path
import json

st.set_page_config(
    page_title="FedRAMP Control Crosswalk",
    page_icon="🔄",
    layout="wide"
)

# Constants
EXCEL_PATH = Path("data/baselines/FedRAMP_Security_Controls_Baseline.xlsx")
KSI_PATH = Path("fedramp-docs/markdown/FRMR.KSI.key-security-indicators-with-controls.md")

@st.cache_data
def load_baseline_controls(baseline_name="Low Baseline"):
    """Load the FedRAMP baseline controls from Excel"""
    try:
        # Read all sheets from the Excel file with header in second row
        all_sheets = pd.read_excel(EXCEL_PATH, sheet_name=None, header=1)
        
        # Get sheet names
        sheet_names = list(all_sheets.keys())
        
        # Get the specified baseline sheet
        if baseline_name in all_sheets:
            controls_df = all_sheets[baseline_name]
        else:
            # Default to Low Baseline if not found
            controls_df = all_sheets.get("Low Baseline", all_sheets[sheet_names[0]])
        
        return controls_df, sheet_names, all_sheets
    except Exception as e:
        st.error(f"Error loading Excel file: {str(e)}")
        return None, [], {}

@st.cache_data
def extract_ksi_controls():
    """Extract control IDs from KSI document"""
    try:
        with open(KSI_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract control IDs in lowercase format (e.g., ac-1, au-2, at-2.2)
        pattern = r'\b([a-z]{2}-\d{1,2}(?:\.\d+)?)\b'
        raw_controls = list(set(re.findall(pattern, content)))
        
        # Normalize KSI controls to match baseline format
        normalized_controls = []
        for control in raw_controls:
            # Convert to uppercase
            control = control.upper()
            # Add leading zero if needed (AT-2 -> AT-02)
            parts = control.split('-')
            if len(parts) == 2:
                family, num_part = parts
                # Handle enhancements (e.g., AT-2.2)
                if '.' in num_part:
                    num, enhancement = num_part.split('.')
                    num = num.zfill(2)  # Add leading zero
                    control = f"{family}-{num}({enhancement})"
                else:
                    num = num_part.zfill(2)  # Add leading zero
                    control = f"{family}-{num}"
            normalized_controls.append(control)
        
        # Also extract KSI numbers and their associated controls
        # Pattern: KSI-CATEGORY-NUMBER (e.g., KSI-CED-01, KSI-IAM-02)
        ksi_pattern = r'KSI-[A-Z]+-\d+'
        ksi_numbers = list(set(re.findall(ksi_pattern, content)))
        
        return sorted(normalized_controls), sorted(ksi_numbers), content
    except Exception as e:
        st.error(f"Error loading KSI document: {str(e)}")
        return [], [], ""

def parse_control_id(control):
    """Parse control ID to extract base control and enhancement"""
    match = re.match(r'([A-Z]{2}-\d{1,2})(?:\((\d+)\))?', control)
    if match:
        base = match.group(1)
        enhancement = match.group(2) if match.group(2) else None
        return base, enhancement
    return control, None

# Main app
st.title("🔄 FedRAMP Control Crosswalk")
st.markdown("""
This page provides a crosswalk between:
- **NIST controls** in the Key Security Indicators (KSI) document
- **FedRAMP baseline controls** (Low, Moderate, or High) from the official baseline spreadsheet
""")

# Baseline selector
baseline_options = ["Low Baseline", "Moderate Baseline", "High Baseline"]
selected_baseline = st.selectbox(
    "Select FedRAMP Baseline",
    options=baseline_options,
    index=0,
    help="Choose which FedRAMP baseline to compare with KSI controls"
)

# Load data
with st.spinner("Loading control data..."):
    baseline_df, sheet_names, all_sheets = load_baseline_controls(selected_baseline)
    ksi_controls, ksi_numbers, ksi_content = extract_ksi_controls()

if baseline_df is None:
    st.error("Could not load baseline controls. Please ensure the Excel file exists.")
    st.stop()

# Display sheet information
with st.expander("📊 Excel File Information"):
    st.write(f"Available sheets: {', '.join(sheet_names)}")
    st.write(f"Selected sheet: **{selected_baseline}**")
    st.write(f"Total rows: {len(baseline_df)}")
    if 'SORT ID' in baseline_df.columns:
        st.success("✅ Found 'SORT ID' column with control identifiers")
    st.write("Sample columns:", list(baseline_df.columns)[:5])

# Extract baseline controls using SORT ID column
baseline_controls = set()
if 'SORT ID' in baseline_df.columns:
    for value in baseline_df['SORT ID'].dropna():
        # Clean the control ID - it's already in the format we want (e.g., AC-01, AT-02 (02))
        control_id = str(value).strip()
        # Just remove extra spaces around parentheses
        control_id = re.sub(r'\s*\(\s*', '(', control_id)
        control_id = re.sub(r'\s*\)', ')', control_id)
        baseline_controls.add(control_id)
else:
    st.error("'SORT ID' column not found in the Excel file. Please check the file format.")

baseline_controls = sorted(list(baseline_controls))

# Display summary statistics
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("KSI Controls", len(ksi_controls))
    
with col2:
    st.metric("Baseline Controls", len(baseline_controls))
    
with col3:
    # Extract unique KSI categories
    ksi_categories = set()
    if ksi_numbers:
        for ksi in ksi_numbers:
            parts = ksi.split('-')
            if len(parts) >= 2:
                ksi_categories.add(parts[1])
    
    st.metric("Key Security Indicators", len(ksi_numbers), 
              delta=f"{len(ksi_categories)} categories")

# Debug section to help troubleshoot
with st.expander("🔍 Debug: Sample Control IDs & KSIs"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Sample KSI Controls (first 10):**")
        st.write(ksi_controls[:10] if ksi_controls else "No controls found")
    with col2:
        st.write("**Sample Baseline Controls (first 10):**")
        st.write(baseline_controls[:10] if baseline_controls else "No controls found")
    with col3:
        st.write("**KSI Categories Found:**")
        if ksi_numbers:
            # Extract unique categories
            categories = set()
            for ksi in ksi_numbers:
                parts = ksi.split('-')
                if len(parts) >= 2:
                    categories.add(parts[1])
            st.write(f"Categories: {', '.join(sorted(categories))}")
            st.write(f"Total KSIs: {len(ksi_numbers)}")

# Perform crosswalk analysis
st.markdown("---")
st.subheader("🔍 Crosswalk Analysis")

# Find controls in both
in_both = set(ksi_controls) & set(baseline_controls)
ksi_only = set(ksi_controls) - set(baseline_controls)
baseline_only = set(baseline_controls) - set(ksi_controls)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Controls in Both", len(in_both))
    
with col2:
    st.metric("KSI Only", len(ksi_only))
    
with col3:
    st.metric("Baseline Only", len(baseline_only))

# Detailed view tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Controls in Both", "🔍 KSI Only", f"📊 {selected_baseline} Only", "📈 Analysis", "🎯 KSI Details"])

with tab1:
    st.subheader(f"Controls in Both KSI and {selected_baseline}")
    if in_both:
        # Create DataFrame for display
        df_both = pd.DataFrame({
            'Control ID': sorted(list(in_both)),
            'In KSI': '✅',
            f'In {selected_baseline}': '✅'
        })
        st.dataframe(df_both, use_container_width=True)
        
        # Export option
        csv = df_both.to_csv(index=False)
        st.download_button(
            label="💾 Download as CSV",
            data=csv,
            file_name="controls_in_both.csv",
            mime="text/csv"
        )
    else:
        st.info("No controls found in both documents")

with tab2:
    st.subheader(f"Controls in KSI but not in {selected_baseline}")
    if ksi_only:
        df_ksi = pd.DataFrame({
            'Control ID': sorted(list(ksi_only)),
            'In KSI': '✅',
            f'In {selected_baseline}': '❌',
            'Note': f'Not in {selected_baseline}'
        })
        st.dataframe(df_ksi, use_container_width=True)
        
        # Export option
        csv = df_ksi.to_csv(index=False)
        st.download_button(
            label="💾 Download as CSV",
            data=csv,
            file_name="ksi_only_controls.csv",
            mime="text/csv"
        )
    else:
        st.info(f"All KSI controls are in the {selected_baseline}")

with tab3:
    st.subheader(f"Controls in {selected_baseline} but not in KSI")
    if baseline_only:
        df_baseline = pd.DataFrame({
            'Control ID': sorted(list(baseline_only)),
            'In KSI': '❌',
            f'In {selected_baseline}': '✅',
            'Note': 'Not covered by KSI'
        })
        st.dataframe(df_baseline, use_container_width=True)
        
        # Export option
        csv = df_baseline.to_csv(index=False)
        st.download_button(
            label="💾 Download as CSV",
            data=csv,
            file_name="baseline_only_controls.csv",
            mime="text/csv"
        )
    else:
        st.info(f"All {selected_baseline} controls are covered in KSI")

with tab4:
    st.subheader("📊 Control Family Analysis")
    
    # Analyze by control family
    families = {}
    
    for control in ksi_controls + baseline_controls:
        base, _ = parse_control_id(control)
        family = base.split('-')[0]
        
        if family not in families:
            families[family] = {'ksi': 0, 'baseline': 0, 'both': 0}
        
        if control in ksi_controls and control in baseline_controls:
            families[family]['both'] += 1
        elif control in ksi_controls:
            families[family]['ksi'] += 1
        else:
            families[family]['baseline'] += 1
    
    # Create family analysis DataFrame
    family_data = []
    for family, counts in sorted(families.items()):
        family_data.append({
            'Family': family,
            'In Both': counts['both'],
            'KSI Only': counts['ksi'],
            'Baseline Only': counts['baseline'],
            'Total': counts['both'] + counts['ksi'] + counts['baseline']
        })
    
    if family_data:
        df_families = pd.DataFrame(family_data)
        st.dataframe(df_families, use_container_width=True)
        
        # Visualization
        if len(df_families) > 0:
            st.bar_chart(df_families.set_index('Family')[['In Both', 'KSI Only', 'Baseline Only']])
    else:
        st.info("No control families found for analysis")

with tab5:
    st.subheader("🎯 Key Security Indicators (KSI) Overview")
    
    if ksi_numbers:
        # Group KSIs by category
        ksi_by_category = {}
        for ksi in sorted(ksi_numbers):
            parts = ksi.split('-')
            if len(parts) >= 3:
                category = parts[1]
                if category not in ksi_by_category:
                    ksi_by_category[category] = []
                ksi_by_category[category].append(ksi)
        
        # KSI Category mapping
        category_names = {
            'CED': 'Cybersecurity Education',
            'CMT': 'Change Management',
            'CNA': 'Cloud Native Architecture',
            'IAM': 'Identity and Access Management',
            'INR': 'Incident Reporting',
            'MLA': 'Monitoring, Logging, and Auditing',
            'PIY': 'Policy and Inventory',
            'RPL': 'Recovery Planning',
            'SVC': 'Service Configuration',
            'TPR': 'Third-Party Information Resources'
        }
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total KSI Categories", len(ksi_by_category))
        with col2:
            st.metric("Total KSIs", len(ksi_numbers))
        with col3:
            avg_per_category = len(ksi_numbers) / len(ksi_by_category) if ksi_by_category else 0
            st.metric("Avg KSIs per Category", f"{avg_per_category:.1f}")
        
        st.markdown("---")
        
        # Display KSIs by category
        st.markdown("### KSIs by Category")
        
        for category in sorted(ksi_by_category.keys()):
            category_full = category_names.get(category, category)
            ksis_in_category = ksi_by_category[category]
            
            with st.expander(f"**{category} - {category_full}** ({len(ksis_in_category)} KSIs)"):
                # Show KSIs in this category
                for ksi in sorted(ksis_in_category):
                    st.write(f"• {ksi}")
                
                # Show which controls are referenced in this KSI category
                st.markdown("**Related Controls:**")
                # This would require parsing the KSI content to find associated controls
                st.info("Controls associated with these KSIs are shown in the main crosswalk analysis")
        
        # Export KSI list
        st.markdown("---")
        ksi_export_data = []
        for category, ksis in ksi_by_category.items():
            for ksi in ksis:
                ksi_export_data.append({
                    'KSI ID': ksi,
                    'Category Code': category,
                    'Category Name': category_names.get(category, category),
                    'Total in Category': len(ksis)
                })
        
        df_ksi = pd.DataFrame(ksi_export_data)
        csv = df_ksi.to_csv(index=False)
        st.download_button(
            label="💾 Export KSI List",
            data=csv,
            file_name="fedramp_ksi_list.csv",
            mime="text/csv"
        )
    else:
        st.warning("No KSIs found in the document")

# Export complete crosswalk
st.markdown("---")
st.subheader("📥 Export Complete Crosswalk")

all_controls = sorted(list(set(ksi_controls + baseline_controls)))
crosswalk_data = []

for control in all_controls:
    crosswalk_data.append({
        'Control ID': control,
        'In KSI': '✅' if control in ksi_controls else '❌',
        f'In {selected_baseline}': '✅' if control in baseline_controls else '❌',
        'Status': 'Both' if control in in_both else ('KSI Only' if control in ksi_only else 'Baseline Only')
    })

df_crosswalk = pd.DataFrame(crosswalk_data)

col1, col2 = st.columns(2)
with col1:
    csv = df_crosswalk.to_csv(index=False)
    st.download_button(
        label="💾 Export as CSV",
        data=csv,
        file_name="fedramp_control_crosswalk.csv",
        mime="text/csv"
    )

with col2:
    json_data = df_crosswalk.to_json(orient='records', indent=2)
    st.download_button(
        label="📋 Export as JSON",
        data=json_data,
        file_name="fedramp_control_crosswalk.json",
        mime="application/json"
    )