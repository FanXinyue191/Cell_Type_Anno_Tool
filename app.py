import streamlit as st
import pandas as pd

# Configure page (centered layout, not wide)
st.set_page_config(
    page_title="Cell Type Anno",
    page_icon="assets/cellmarker_anno_logo-3.png",
    layout="centered"
)

# Path to the CellMarker database
EXCEL_PATH = "data/Cell_marker_All.xlsx"


@st.cache_data
def load_data():
    """Load the CellMarker Excel file."""
    df = pd.read_excel(EXCEL_PATH)
    return df


def main():
    st.title("🔍 Cell Type Annotation Tool")
    st.write("""
    👋欢迎使用本工具！这是一个**基于文献等证据的cell type注释与marker探索的交互式平台**。
    该工具帮助研究者快速识别、筛选并验证细胞类型注释marker，并提供可追溯的文献支持。
    """)

    st.info("""
    **核心功能**
    - 基于证据数量排序的cell type及其marker
    - 可直接复制细胞类型注释代码(R、Python)
    - 直达原始文献的PMID链接
    """)
    
    st.markdown("""
    #### 数据来源
    本工具使用的数据来源于 [CellMarker 2.0](http://www.bio-bigdata.center/) 数据库，并手工补全缺失的信息，具体过程见文档[整合流程](http://xxx)。未来将整合更多数据库资源，敬请期待...
    """)

    # ---- Workflow Overview ----
    st.markdown("#### How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**1️⃣ Marker探索**")
        st.write("""
        选择物种及组织类型，探索cell type及其marker全景图，
        结果默认按照证据数量进行排序，
        快速识别高置信度且常用的cell type及其marker。
        """)

    with col2:
        st.markdown("**2️⃣ 获取marker清单代码**")
        st.write(""" 
        设置证据数量阈值筛选高置信度marker，
        一键导出R(如Seurat)、Python(如Scanpy)可直接使用的marker 清单代码。
        """)

    with col3:
        st.markdown("**3️⃣ 文献证据追溯**")
        st.write("""
        查看每个marker与cell type关系的原始文献证据。
        点击PMID可跳转至对应论文，并查看详细证据信息，
        确保细胞类型注释具有可解释性与可重复性。
        """)

    # ---- Research Disclaimer ----
    st.warning("""
    本工具仅用于科研用途。  
    细胞类型注释结果应结合实验验证和生物学背景进行解释。
    """)


    # Load data
    with st.spinner("Loading data..."):
        df = load_data()

    # ============================================================
    # Section 1: Marker探索
    # ============================================================
    st.divider()
    st.header("1️⃣ Marker探索")

    col1, col2, col3 = st.columns(3)

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
        default_tissue_index = (
            tissue_class_list.index("Brain") if "Brain" in tissue_class_list else 0
        )
        selected_tissue_class = st.selectbox(
            "Select Tissue", tissue_class_list, index=default_tissue_index
        )

    
    
    # Filter by tissue_class
    df_filtered = df_filtered[df_filtered["tissue_class"] == selected_tissue_class]

    # Group by cell_name
    groupby_cols = ["cell_name"]
    df_grouped = df_filtered.groupby(groupby_cols, dropna=False).size().reset_index(name="count")
    df_grouped = df_grouped.sort_values("count", ascending=False)
    # Get unique celltypes
    celltypes_list = ["All"] + df_grouped["cell_name"].dropna().unique().tolist()
    
    with col3:
        # Set default to "All"
        selected_cell_type = st.selectbox(
        "Select Cell type", celltypes_list, index=celltypes_list.index("All")
    )

    
    # Group by and count
    groupby_cols = ["cell_type", "cell_name", "marker", "Symbol"]
    df_grouped = df_filtered.groupby(groupby_cols, dropna=False).size().reset_index(name="count")

    if selected_cell_type != "All":
        df_grouped = df_grouped[df_grouped["cell_name"] == selected_cell_type]

    
    # Add species and tissue_class columns at the beginning
    df_grouped.insert(0, "species", selected_species)
    df_grouped.insert(1, "tissue_class", selected_tissue_class)

    # Sort by count (descending by default)
    df_grouped = df_grouped.sort_values("count", ascending=False)

    # Rename columns
    df_grouped = df_grouped.rename(
        columns={
            "species": "Species",
            "tissue_class": "Tissue",
            "cell_type": "Normal/Tumor",
            "cell_name": "Cell type",
            "marker": "Marker",
            "Symbol": "Symbol",
            "count": "#Evidence",
        }
    )

    # Display results
    st.subheader(f"Results: {len(df_grouped)} unique marker entries")
    if selected_cell_type == "All":
        st.write(f"**Species:** {selected_species} | **Tissue:** {selected_tissue_class}")
    else:
        st.write(f"**Species:** {selected_species} | **Tissue:** {selected_tissue_class} | **Cell type:** {selected_cell_type}")
    

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
    # Section 2: 获取marker清单代码
    # ============================================================
    st.divider()
    st.header("2️⃣ 获取marker清单代码")

    # Get max count for slider range
    max_count = int(df_grouped["#Evidence"].max())
    default_value = min(max_count, 3)

    if max_count == 1:
        # 禁用滑块并设置值为1
        st.write(f"注：每个cell type & marker pair仅有一条证据，无需调整阈值。")
        count_threshold = 1
    else:
        # 否则显示滑块
        count_threshold = st.slider(
            "#Evidence Threshold", min_value=1, max_value=max_count, value=default_value, step=1
        )

    # Filter by count threshold (using new column name "#Evidence")
    df_grouped_filtered = df_grouped[df_grouped["#Evidence"] >= count_threshold].copy()

    st.write(f"**Filtered to {len(df_grouped_filtered)} entries (#Evidence >= {count_threshold})**")

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
            [
                f"    `{cell}` = c({', '.join([f'"{s}"' for s in symbols])})"
                for cell, symbols in cell_markers.items()
            ]
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
    # Section 3: 文献证据追溯
    # ============================================================
    st.divider()
    st.header("3️⃣ 文献证据追溯")

    # Filter original raw data by Section 1's Cell type and Marker (using new column names)
    section1_cell_names = df_grouped["Cell type"].dropna().unique()
    section1_markers = df_grouped["Marker"].dropna().unique()

    df_candidate = df_filtered[
        df_filtered["cell_name"].isin(section1_cell_names)
        & df_filtered["marker"].isin(section1_markers)
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
            index=all_cell_names.index(st.session_state.s3_cell_name) + 1
            if st.session_state.s3_cell_name in all_cell_names
            else 0,
            key="s3_cell_name_select",
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
        if (
            st.session_state.s3_marker != "All"
            and st.session_state.s3_marker not in available_markers
        ):
            st.session_state.s3_marker = "All"
    else:
        available_markers = all_markers

    with col4:
        selected_marker = st.selectbox(
            "Select Marker",
            ["All"] + available_markers,
            index=available_markers.index(st.session_state.s3_marker) + 1
            if st.session_state.s3_marker in available_markers
            else 0,
            key="s3_marker_select",
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
    df_result = df_result.drop(
        columns=[col for col in columns_to_drop if col in df_result.columns])

    # Rename and capitalize columns (replace underscores with spaces)
    column_mapping = {
        "species": "Species",
        "tissue_class": "Tissue",
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
        "year": "Year",
    }
    df_result = df_result.rename(columns=column_mapping)

    # Create PMID links
    df_result["PMID"] = df_result["PMID"].apply(
        lambda x: f"https://pubmed.ncbi.nlm.nih.gov/{int(x)}/" if pd.notna(x) and x != "" else ""
    )

    # Display results
    st.subheader(f"Raw Data Results: {len(df_result)} entries")

    # Reset index
    df_result = df_result.reset_index(drop=True)

    # Calculate dynamic height based on row count (max 10 rows)
    row_count = min(len(df_result), 10)
    # Approximate 40px per row + 50px for header
    dynamic_height = row_count * 40 + 50

    # Display as sortable dataframe with row selection
    event = st.dataframe(
        df_result,
        use_container_width=True,
        hide_index=True,
        height=dynamic_height,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "PMID": st.column_config.LinkColumn(
                "PMID",
                display_text=r"https://pubmed.ncbi.nlm.nih.gov/(\d+)/",
            ),
        },
    )

    # Check if a row is selected
    # Handle closing details: if s3_selected_row is None (closed), require explicit re-selection
    if event and event.selection.rows:
        selected_row_idx = event.selection.rows[0]
        current_selection = st.session_state.get("s3_selected_row")

        # Only update if:
        # 1. First time selection (current_selection is None and s3_needs_init is not set)
        # 2. Or selecting a different row (current_selection != selected_row_idx)
        # But NOT if s3_selected_row was just set to None (user closed details - requires explicit re-selection)
        s3_just_closed = st.session_state.get("s3_just_closed", False)
        if not s3_just_closed and (
            current_selection is None or current_selection != selected_row_idx
        ):
            st.session_state.s3_selected_row = selected_row_idx
        # Reset the just_closed flag after processing
        if s3_just_closed:
            st.session_state.s3_just_closed = False

    # Display detail card if a row is selected
    current_selection = st.session_state.get("s3_selected_row")
    if current_selection is not None:
        row_idx = current_selection
        if 0 <= row_idx < len(df_result):
            row_data = df_result.iloc[row_idx]

            # Enhanced CSS for styled card
            st.markdown(
                """
            <style>
            .detail-card {
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 24px;
                margin: 20px 0;
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            .detail-card-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: #1e40af;
                margin: 0 0 16px 0;
                padding-bottom: 12px;
                border-bottom: 2px solid #3b82f6;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .detail-section {
                margin: 20px 0;
                padding: 16px;
                background-color: #f0f9ff;
                border-radius: 8px;
                border-left: 4px solid #3b82f6;
            }
            .detail-section-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: #1e3a8a;
                margin: 0 0 12px 0;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            .detail-field {
                padding: 6px 0;
                border-bottom: 1px solid #e5e7eb;
            }
            .detail-field:last-child {
                border-bottom: none;
            }
            .detail-label {
                font-weight: 600;
                color: #374151;
            }
            .detail-value {
                color: #6b7280;
                word-break: break-word;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            # Detail card with enhanced styling
            with st.container(border=True):
                st.markdown(
                    f"""
                <div class="detail-card">
                    <div class="detail-card-title">
                        <span>📋</span>
                        <span>Entry Details (Row {row_idx + 1})</span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Gene information section (two columns)
                gene_cols = ["Symbol", "Gene ID", "Gene name", "Gene type", "UNIPROT ID"]
                available_gene_cols = [col for col in gene_cols if col in df_result.columns]

                if available_gene_cols:
                    st.markdown(
                        """
                    <div class="detail-section">
                        <div class="detail-section-title">
                            <span>🧬</span>
                            <span>Gene Information</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    gene_col1, gene_col2 = st.columns(2)

                    with gene_col1:
                        st.markdown('<div class="detail-field">', unsafe_allow_html=True)
                        for col in available_gene_cols[
                            : len(available_gene_cols) // 2 + len(available_gene_cols) % 2
                        ]:
                            val = row_data[col]
                            if pd.notna(val) and val != "":
                                if isinstance(val, str) and val.startswith("http"):
                                    st.markdown(
                                        f'<span class="detail-label">{col}:</span> <a href="{val}" target="_blank">{val}</a>',
                                        unsafe_allow_html=True,
                                    )
                                elif col == "Gene ID":
                                    # Convert to integer
                                    try:
                                        val_int = int(float(val))
                                        st.markdown(
                                            f'<span class="detail-label">{col}:</span> <span class="detail-value">{val_int}</span>',
                                            unsafe_allow_html=True,
                                        )
                                    except (ValueError, TypeError):
                                        st.markdown(
                                            f'<span class="detail-label">{col}:</span> <span class="detail-value">{val}</span>',
                                            unsafe_allow_html=True,
                                        )
                                else:
                                    st.markdown(
                                        f'<span class="detail-label">{col}:</span> <span class="detail-value">{val}</span>',
                                        unsafe_allow_html=True,
                                    )
                        st.markdown("</div>", unsafe_allow_html=True)

                    with gene_col2:
                        st.markdown('<div class="detail-field">', unsafe_allow_html=True)
                        for col in available_gene_cols[
                            len(available_gene_cols) // 2 + len(available_gene_cols) % 2:
                        ]:
                            val = row_data[col]
                            if pd.notna(val) and val != "":
                                if isinstance(val, str) and val.startswith("http"):
                                    st.markdown(
                                        f'<span class="detail-label">{col}:</span> <a href="{val}" target="_blank">{val}</a>',
                                        unsafe_allow_html=True,
                                    )
                                else:
                                    st.markdown(
                                        f'<span class="detail-label">{col}:</span> <span class="detail-value">{val}</span>',
                                        unsafe_allow_html=True,
                                    )
                        st.markdown("</div>", unsafe_allow_html=True)

                # Cell & Marker information section (two columns)
                cell_marker_cols = [
                    "Species",
                    "Tissue class",
                    "Tissue type",
                    "Cancer type",
                    "Normal/Tumor",
                    "Cell type",
                    "Marker",
                ]
                available_cell_marker_cols = [
                    col for col in cell_marker_cols if col in df_result.columns
                ]

                if available_cell_marker_cols:
                    st.markdown(
                        """
                    <div class="detail-section">
                        <div class="detail-section-title">
                            <span>🔬</span>
                            <span>Cell & Marker Information</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    cell_col1, cell_col2 = st.columns(2)

                    with cell_col1:
                        st.markdown('<div class="detail-field">', unsafe_allow_html=True)
                        for col in available_cell_marker_cols[
                            : len(available_cell_marker_cols) // 2
                            + len(available_cell_marker_cols) % 2
                        ]:
                            val = row_data[col]
                            if pd.notna(val) and val != "":
                                st.markdown(
                                    f'<span class="detail-label">{col}:</span> <span class="detail-value">{val}</span></div>',
                                    unsafe_allow_html=True,
                                )
                        st.markdown("</div>", unsafe_allow_html=True)

                    with cell_col2:
                        st.markdown('<div class="detail-field">', unsafe_allow_html=True)
                        for col in available_cell_marker_cols[
                            len(available_cell_marker_cols) // 2
                            + len(available_cell_marker_cols) % 2:
                        ]:
                            val = row_data[col]
                            if pd.notna(val) and val != "":
                                st.markdown(
                                    f'<div class="detail-field"><span class="detail-label">{col}:</span> <span class="detail-value">{val}</span></div>',
                                    unsafe_allow_html=True,
                                )
                        st.markdown("</div>", unsafe_allow_html=True)

                # Literature information section
                lit_cols = ["PMID", "Title", "journal", "Year"]
                available_lit_cols = [col for col in lit_cols if col in df_result.columns]

                if available_lit_cols:
                    st.markdown(
                        """
                    <div class="detail-section">
                        <div class="detail-section-title">
                            <span>📚</span>
                            <span>Literature Information</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    for col in available_lit_cols:
                        val = row_data[col]
                        if pd.notna(val) and val != "":
                            if col == "PMID" and isinstance(val, str) and val.startswith("http"):
                                st.markdown(
                                    f'<div class="detail-field"><span class="detail-label">{col}:</span> <a href="{val}" target="_blank">📖 View Article</a></div>',
                                    unsafe_allow_html=True,
                                )
                            elif col == "Year":
                                # Convert to integer
                                try:
                                    val_int = int(float(val))
                                    st.markdown(
                                        f'<div class="detail-field"><span class="detail-label">{col}:</span> <span class="detail-value">{val_int}</span></div>',
                                        unsafe_allow_html=True,
                                    )
                                except (ValueError, TypeError):
                                    st.markdown(
                                        f'<div class="detail-field"><span class="detail-label">{col}:</span> <span class="detail-value">{val}</span></div>',
                                        unsafe_allow_html=True,
                                    )
                            else:
                                st.markdown(
                                    f'<div class="detail-field"><span class="detail-label">{col}:</span> <span class="detail-value">{val}</span></div>',
                                    unsafe_allow_html=True,
                                )

                # Other information section
                other_cols = ["Technology seq", "Marker source"]
                available_other_cols = [col for col in other_cols if col in df_result.columns]

                if available_other_cols:
                    st.markdown(
                        """
                    <div class="detail-section">
                        <div class="detail-section-title">
                            <span>⚙️</span>
                            <span>Additional Information</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    for col in available_other_cols:
                        val = row_data[col]
                        if pd.notna(val) and val != "":
                            st.markdown(
                                f'<div class="detail-field"><span class="detail-label">{col}:</span> <span class="detail-value">{val}</span></div>',
                                unsafe_allow_html=True,
                            )

                # Close button
                st.markdown("---")
                col_close1, col_close2, col_close3 = st.columns([1, 2, 1])
                with col_close2:
                    if st.button("✖ Close Details", key="close_detail", use_container_width=True):
                        st.session_state.s3_selected_row = None
                        st.session_state.s3_just_closed = True
                        st.rerun()
    else:
        if len(df_result) == 0:
            st.info("No data to display")

    # 在页面底部添加创建者信息
    st.markdown("---")  # 分隔线
    st.markdown("""
    ### 由以下创建者团队创建
    - **Xinyue**: fanxinyue191@gmail.com
    - **神秘人Ender**
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
