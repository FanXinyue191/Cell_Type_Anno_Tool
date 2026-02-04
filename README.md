# Cell Type Annotation Tool

A Streamlit-based web application for querying and exploring cell marker information from the CellMarker2.0 database.

## Overview

This application provides an interactive interface to search, filter, and analyze cell marker data. It features three main sections for different levels of data exploration:

- **Section 1**: Filter cell markers by species and tissue class with aggregated evidence counts
- **Section 2**: Apply evidence count thresholds and export marker lists as code (R List or Python Dict)
- **Section 3**: Explore raw data with detailed filtering and individual entry inspection

## Features

### Section 1: Filter by Species and Tissue Class

- Select from available species (Human, Mouse, etc.)
- Filter by tissue class (defaults to "Brain" if available)
- View aggregated results grouped by cell type and marker
- Sortable table with evidence counts
- Displays unique marker entries with configurable evidence thresholds

### Section 2: Filter by Count Threshold

- Dynamic slider to set minimum evidence count (1 to maximum available)
- Export filtered markers as ready-to-use code snippets
- Two output formats:
    - **R List**: Named list format for R programming
    - **Python Dict**: Dictionary format for Python programming

### Section 3: Filter Raw Data

- Cascading filters by cell type and marker (cell type selection updates available markers)
- View complete raw data with all evidence details
- Click any row to view detailed information card
- PMID links to PubMed articles
- Organized detail sections:
    - Gene Information (Symbol, Gene ID, Gene name, Gene type, UNIPROT ID)
    - Cell & Marker Information (Species, Tissue class, Cell type, Marker, etc.)
    - Literature Information (PMID, Title, Journal, Year)
    - Additional Information (Technology seq, Marker source)

## Installation

### Prerequisites

- Miniforge or Anaconda with mamba
- Python 3.8+

### Setup Environment

1. Clone or download this repository

2. Ensure the CellMarker database file is in place:

   ```
   data/Cell_marker_All.xlsx
   ```

3. Install dependencies:

   ```bash
   # Using the deployment script
   ./deploy.sh --install

   # Or manually with mamba
   /home/hzl/miniforge3/bin/mamba run -n cellmarkerAnno pip install -r requirements.txt
   ```

## Usage

### Quick Start

Run the application using the deployment script:

```bash
./deploy.sh
```

The app will be available at: **<http://localhost:6052>**

### Manual Execution

If you prefer to run the app manually:

```bash
/home/hzl/miniforge3/bin/mamba run -n cellmarkerAnno streamlit run app.py --server.port 6052
```

### Stopping the App

Press `Ctrl+C` in the terminal to stop the server.

## Configuration

### Port Configuration

To change the default port (6052), edit `deploy.sh`:

```bash
PORT="YOUR_PORT_HERE"
```

### Database Path

To use a different CellMarker database file, edit `app.py`:

```python
EXCEL_PATH = "path/to/your/Cell_marker_All.xlsx"
```

### Conda Environment

To use a different conda environment, edit both `deploy.sh`:

```bash
CONDA_ENV="your_environment_name"
```

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── deploy.sh              # Deployment script with dependency checking
├── requirements.txt       # Python package dependencies
├── data/                  # Data directory
│   └── Cell_marker_All.xlsx  # CellMarker database
├── README.md              # Project documentation
└── CLAUDE.md              # Development instructions
```

## Dependencies

- **streamlit** >= 1.28.0 - Web application framework
- **pandas** >= 1.5.0 - Data manipulation and analysis
- **openpyxl** >= 3.0.0 - Excel file reading support

## Database Schema

The CellMarker database contains the following key columns:

| Column         | Description                                  |
|----------------|----------------------------------------------|
| species        | Species (Human, Mouse, etc.)                 |
| tissue_class   | Tissue classification (Brain, Abdomen, etc.) |
| tissue_type    | Specific tissue type                         |
| cancer_type    | Cancer type (if applicable)                  |
| cell_type      | Cell classification (Normal/Tumor)           |
| cell_name      | Specific cell type name                      |
| marker         | Marker name                                  |
| Symbol         | Gene symbol                                  |
| GeneID         | NCBI Gene ID                                 |
| Genetype       | Gene type (e.g., protein_coding)             |
| Genename       | Full gene name                               |
| UNIPROTID      | UniProt identifier                           |
| technology_seq | Sequencing technology used                   |
| marker_source  | Source of marker data                        |
| PMID           | PubMed publication ID                        |
| Title          | Article title                                |
| journal        | Journal name                                 |
| year           | Publication year                             |

## Example Workflow

1. **Start Exploration**: Select your species of interest (e.g., "Human")
2. **Choose Tissue**: Select tissue class (e.g., "Brain")
3. **Review Results**: Browse the aggregated marker table with evidence counts
4. **Set Threshold**: Adjust the count threshold in Section 2 to filter for well-supported markers
5. **Export Code**: Copy the R List or Python Dict for use in your analysis
6. **Deep Dive**: Use Section 3 to explore raw data
   - Select a specific cell type
   - Choose a marker of interest
   - Click any row to view detailed information including literature references

## Troubleshooting

### Dependencies Not Found

If you see dependency errors:

```bash
./deploy.sh --install
```

### Port Already in Use

If port 6052 is occupied, either:

- Stop the process using port 6052
- Or modify the PORT variable in `deploy.sh`

### Data File Not Found

Ensure `data/Cell_marker_All.xlsx` exists in the project directory.

### Excel Reading Issues

Make sure `openpyxl` is installed:

```bash
/home/hzl/miniforge3/bin/mamba run -n cellmarkerAnno pip install openpyxl
```

## License

This application is provided as-is for research and educational purposes.

## Acknowledgments

- CellMarker database for providing comprehensive cell marker information
- Streamlit framework for the web application interface
