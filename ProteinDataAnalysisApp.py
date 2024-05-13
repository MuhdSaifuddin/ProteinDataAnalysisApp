import streamlit as st
import requests
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

# Define function to retrieve protein data from Uniprot
def fetch_protein_data(uniprot_id):
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Define function to retrieve protein-protein interaction network from STRING DB
def fetch_ppi_network(uniprot_id):
    url = f"https://string-db.org/api/protein_info?identifiers={uniprot_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Define function to perform sequence alignment
def perform_sequence_alignment(seq1, seq2):
    alignments = pairwise2.align.globalxx(seq1, seq2)
    return alignments

# Main function to run the Streamlit web app
def main():
    # Customizing Streamlit's theme
    st.markdown(
        """
        <style>
        body {
            background-color: #f4f4f4;
        }
        .stApp {
            max-width: 800px;
            padding: 2rem;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            padding: 40px;
        }
        .stCheckbox label, .stRadio label {
            color: #333333;
        }
        .stButton {
            background-color: #4caf50;
            color: #ffffff;
            border-radius: 4px;
            transition: background-color 0.3s;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        .stButton:hover {
            background-color: #45a049;
        }
        .stTextInput>div>div>input {
            border-radius: 4px;
            border: 1px solid #cccccc;
            padding: 10px;
            font-size: 16px;
        }
        .stSelectbox>div>div>select {
            border-radius: 4px;
            border: 1px solid #cccccc;
            padding: 10px;
            font-size: 16px;
            background-color: #ffffff;
        }
        .stMarkdown div {
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Protein Data Analysis App")
    
    # Sidebar for user input
    option = st.sidebar.selectbox(
        'Select Input Type',
        ('Uniprot ID', 'Protein Sequence')
    )

    if option == 'Uniprot ID':
        uniprot_id = st.sidebar.text_input('Enter Uniprot ID:')
        if st.sidebar.button('Search', key="search_button"):
            if uniprot_id:
                st.markdown('### Searching for Protein Data...')
                protein_data = fetch_protein_data(uniprot_id)
                if protein_data:
                    st.markdown('### Protein Characteristics')
                    st.json(protein_data)
                    
                    st.markdown('### Searching for Protein-Protein Interaction Network...')
                    ppi_network = fetch_ppi_network(uniprot_id)
                    if ppi_network:
                        st.markdown('### Protein-Protein Interaction Network')
                        st.json(ppi_network)
                    else:
                        st.warning("No interaction network found.")
                else:
                    st.error("Invalid Uniprot ID. Please enter a valid Uniprot ID.")
            else:
                st.warning("Please enter a Uniprot ID to search.")
    elif option == 'Protein Sequence':
        protein_sequence = st.sidebar.text_area('Enter Protein Sequence:')
        if st.sidebar.button('Align', key="align_button"):
            if protein_sequence:
                st.markdown('### Performing Sequence Alignment...')
                seq2 = "Example sequence"  # You need to provide an example sequence for alignment
                alignments = perform_sequence_alignment(protein_sequence, seq2)
                for alignment in alignments:
                    st.markdown(f'```{format_alignment(*alignment)}```')
            else:
                st.warning("Please enter a protein sequence to align.")

# Run the app
if __name__ == '__main__':
    main()

