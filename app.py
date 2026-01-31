import streamlit as st
import pandas as pd

# Configure page (centered layout, not wide)
st.set_page_config(page_title="Cellmarker Annotation App", layout="centered")

# Path to the CellMarker database
EXCEL_PATH = "data/Cell_marker_All.xlsx"


@st.cache_data
def load_data():
    """Load the CellMarker Excel file."""
    df = pd.read_excel(EXCEL_PATH)
    return df


def main():
    st.title("Cellmarker Annotation App")
    st.write("Query cell marker information from the CellMarker database.")

    # Load data
    with st.spinner("Loading data..."):
        df = load_data()

    # ============================================================
    # Section 1: Filter by species and tissue_class
    # ============================================================
    st.divider()
    st.header("Section 1: Filter by Species and Tissue Class")

    col1, col2 = st.columns(2)

    # Get unique species
    species_list = df["species"].dropna().unique().tolist()
    species_list = sorted(species_list)

    with col1:
        selected_species = st.selectbox("Select Species", species_list)

    # Filter by species first
    df_filtered = df[df["species"] == selected_species]

    # Get unique tissue_class for selected species
    tissue_class_list = df_filtered["tissue_class"].dropna().unique().tolist()
    tissue_class_list = sorted(tissue_class_list)

    with col2:
        # Set default to "Brain" if available, otherwise first option
        default_tissue_index = tissue_class_list.index("Brain") if "Brain" in tissue_class_list else 0
        selected_tissue_class = st.selectbox("Select Tissue Class", tissue_class_list, index=default_tissue_index)

    # Filter by tissue_class
    df_filtered = df_filtered[df_filtered["tissue_class"] == selected_tissue_class]

    # Group by and count
    groupby_cols = ["cell_type", "cell_name", "marker", "Symbol"]
    df_grouped = (
        df_filtered.groupby(groupby_cols, dropna=False)
        .size()
        .reset_index(name="count")
    )

    # Add species and tissue_class columns at the beginning
    df_grouped.insert(0, "species", selected_species)
    df_grouped.insert(1, "tissue_class", selected_tissue_class)

    # Sort by count (descending by default)
    df_grouped = df_grouped.sort_values("count", ascending=False)

    # Rename columns
    df_grouped = df_grouped.rename(columns={
        "species": "Species",
        "tissue_class": "Tissue class",
        "cell_type": "Normal/Tumor",
        "cell_name": "Cell type",
        "marker": "Marker",
        "Symbol": "Symbol",
        "count": "#Evidence"
    })

    # Display results
    st.subheader(f"Results: {len(df_grouped)} unique marker entries")
    st.write(f"**Species:** {selected_species} | **Tissue Class:** {selected_tissue_class}")

    # Calculate dynamic height based on row count (max 10 rows)
    row_count = min(len(df_grouped), 10)
    # Approximate 40px per row + 50px for header
    dynamic_height = row_count * 40 + 50

    # Display as sortable dataframe with dynamic height
    st.dataframe(
        df_grouped,
        use_container_width=True,
        hide_index=True,
        height=dynamic_height,
    )

    # ============================================================
    # Section 2: Filter by count threshold and display code
    # ============================================================
    st.divider()
    st.header("Section 2: Filter by Count Threshold")

    # Get max count for slider range
    max_count = int(df_grouped["#Evidence"].max())

    count_threshold = st.slider(
        "Count Threshold", min_value=1, max_value=max_count, value=3, step=1
    )

    # Filter by count threshold (using new column name "#Evidence")
    df_grouped_filtered = df_grouped[df_grouped["#Evidence"] >= count_threshold].copy()

    st.write(f"**Filtered to {len(df_grouped_filtered)} entries (count >= {count_threshold})**")

    # Generate Symbol lists by Cell type (filtered by threshold)
    cell_markers = {}
    for cell_name in df_grouped_filtered["Cell type"].dropna().unique():
        symbols = (
            df_grouped_filtered[df_grouped_filtered["Cell type"] == cell_name]["Symbol"]
            .dropna()
            .unique()
            .tolist()
        )
        if symbols:
            cell_markers[cell_name] = symbols

    # Display in tabs
    tab1, tab2 = st.tabs(["R List", "Python Dict"])

    with tab1:
        # R List format
        output_code = "list(\n"
        output_code += ",\n".join(
            [f'    `{cell}` = c({", ".join([f'"{s}"' for s in symbols])})'
             for cell, symbols in cell_markers.items()]
        )
        output_code += "\n)"
        st.code(output_code, language="r")

    with tab2:
        # Python Dict format
        output_code = "{\n"
        output_code += ",\n".join(
            [f'    "{cell}": {symbols}' for cell, symbols in cell_markers.items()]
        )
        output_code += "\n}"
        st.code(output_code, language="python")

    # ============================================================
    # Section 3: Filter raw data by cell_name and marker (cascading)
    # ============================================================
    st.divider()
    st.header("Section 3: Filter Raw Data by Cell Name and Marker")

    # Filter original raw data by Section 1's Cell type and Marker (using new column names)
    section1_cell_names = df_grouped["Cell type"].dropna().unique()
    section1_markers = df_grouped["Marker"].dropna().unique()

    df_candidate = df_filtered[
        df_filtered["cell_name"].isin(section1_cell_names) &
        df_filtered["marker"].isin(section1_markers)
    ].copy()

    # Get all unique values (using new column names from df_grouped)
    all_cell_names = sorted(df_grouped["Cell type"].dropna().unique().tolist())
    all_markers = sorted(df_grouped["Marker"].dropna().unique().tolist())

    # Initialize session state for selections
    if "s3_cell_name" not in st.session_state:
        st.session_state.s3_cell_name = "All"
    if "s3_marker" not in st.session_state:
        st.session_state.s3_marker = "All"

    col3, col4 = st.columns(2)

    with col3:
        selected_cell_name = st.selectbox(
            "Select Cell Name",
            ["All"] + all_cell_names,
            index=all_cell_names.index(st.session_state.s3_cell_name) + 1 if st.session_state.s3_cell_name in all_cell_names else 0,
            key="s3_cell_name_select"
        )

    # If cell_name is selected, filter markers; otherwise show all
    if selected_cell_name != "All":
        available_markers = sorted(
            df_grouped[df_grouped["Cell type"] == selected_cell_name]["Marker"]
            .dropna()
            .unique()
            .tolist()
        )
        # Reset marker if it's no longer in available options
        if st.session_state.s3_marker != "All" and st.session_state.s3_marker not in available_markers:
            st.session_state.s3_marker = "All"
    else:
        available_markers = all_markers

    with col4:
        selected_marker = st.selectbox(
            "Select Marker",
            ["All"] + available_markers,
            index=available_markers.index(st.session_state.s3_marker) + 1 if st.session_state.s3_marker in available_markers else 0,
            key="s3_marker_select"
        )

    # Update session state
    st.session_state.s3_cell_name = selected_cell_name
    st.session_state.s3_marker = selected_marker

    # Apply Section 3 filters (using original column names from raw data)
    df_result = df_candidate.copy()

    if selected_cell_name != "All":
        df_result = df_result[df_result["cell_name"] == selected_cell_name]

    if selected_marker != "All":
        df_result = df_result[df_result["marker"] == selected_marker]

    # Remove unwanted columns
    columns_to_drop = ["uberonongology_id", "cellontology_id"]
    df_result = df_result.drop(columns=[col for col in columns_to_drop if col in df_result.columns])

    # Rename and capitalize columns (replace underscores with spaces)
    column_mapping = {
        "species": "Species",
        "tissue_class": "Tissue class",
        "tissue_type": "Tissue type",
        "cancer_type": "Cancer type",
        "cell_type": "Normal/Tumor",
        "cell_name": "Cell type",
        "marker": "Marker",
        "Symbol": "Symbol",
        "GeneID": "Gene ID",
        "Genetype": "Gene type",
        "Genename": "Gene name",
        "UNIPROTID": "UNIPROT ID",
        "technology_seq": "Technology seq",
        "marker_source": "Marker source",
        "PMID": "PMID",
        "Title": "Title",
        "journal": "Journal",
        "year": "Year"
    }
    df_result = df_result.rename(columns=column_mapping)

    # Create PMID links
    df_result["PMID"] = df_result["PMID"].apply(
        lambda x: f"https://pubmed.ncbi.nlm.nih.gov/{int(x)}/" if pd.notna(x) and x != "" else ""
    )

    # Display results
    st.subheader(f"Raw Data Results: {len(df_result)} entries")

    # Calculate dynamic height based on row count (max 10 rows)
    row_count = min(len(df_result), 10)
    # Approximate 40px per row + 50px for header
    dynamic_height = row_count * 40 + 50

    # Display as sortable dataframe with PMID links and dynamic height
    st.dataframe(
        df_result,
        use_container_width=True,
        hide_index=True,
        height=dynamic_height,
        column_config={
            "PMID": st.column_config.LinkColumn(
                "PMID",
                display_text=r"https://pubmed.ncbi.nlm.nih.gov/(\d+)/",
            ),
        },
    )


if __name__ == "__main__":
    main()
