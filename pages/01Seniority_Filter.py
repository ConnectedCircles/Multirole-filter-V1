import pandas as pd
import streamlit as st
import base64

def app():
    
    # Set title and subtitle, additional text
    st.title("Seniority Profile Filter V2")
    st.subheader("Property of Connected Circles")
    st.write("""This app allows you to filter lists of profiles by seniority. By default, it uses a set of keywords to detect and filter CXO+ level profiles 
    (incl. partners and VPs etc.). It uses 2 sets of keywords, one that is case-sensitive and one that is case insensitive. This avoids errors such as the 
    inclusion of 'aCCOunt managers' when searching for 'CCO'. Both sets of keywords are fully customizable and keywords can be added or removed. Keywords must 
    be separated by a comma, whitespace will be considered a part of a keyword. You can preview the both the labeled and filtered data in the two preview 
    windows below. You can download the data either labeled, filtered or filtered profile URLs only, all as a .csv""")
    
    
    # Define the list of substrings to search for
    # Case sensitive substring
    default_substringsCS = ['CEO', 'COO', 'CFO', 'CTO', 'CHRO', 'CMO', 'CLO', 'CSO', 'CIO', 'CTIO', 'CSIO', 'CCO', 'CDO', 'VP']
    # Case insensitive substring 
    default_substringsCI = ['chief','vice president', 'vice-president', 'partner ', 'owner', 'founder','president']
    
    # Get user input for substrings
    substringsCS = st.text_input("Enter case-sensitive keywords separated by comma").split(",")
    substringsCI = st.text_input("Enter case-insensitive keywords separated by comma").split(",")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file to filter", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Create a boolean mask to identify rows where the "Title" column contains any of the case-sensitive substrings
        maskCS = df['Title'].str.contains('|'.join(substringsCS))

        # Create a boolean mask to identify rows where the "Title" column contains any of the case-insensitive substrings
        maskCI = df['Title'].str.contains('|'.join(substringsCI), case=False)

        # Create a new column called "CXO+" with a value of "Yes" for rows that match either condition, and "No" otherwise
        df['CXO+'] = (maskCS | maskCI).map({True: 'Yes', False: 'No'})

        # Filter to only include CXO+, delete CXO+ column
        dffiltered = df[df["CXO+"]=="Yes"]
        dffiltered = dffiltered.drop("CXO+", axis=1)

        # Download link for filtered data
        csv_filtered = dffiltered.to_csv(index=False)
        b64_filtered = base64.b64encode(csv_filtered.encode('utf-8')).decode()
        href_filtered = f'<a href="data:file/csv;base64,{b64_filtered}" download="filtered_data.csv">Download Filtered CSV File</a>'
        
        # Download link for unfiltered data
        csv_unfiltered = df.to_csv(index=False)
        b64_unfiltered = base64.b64encode(csv_unfiltered.encode('utf-8')).decode()
        href_unfiltered = f'<a href="data:file/csv;base64,{b64_unfiltered}" download="unfiltered_data.csv">Download Unfiltered Labeled CSV File</a>'
        
        # Download link for filtered data URLs only, no header
        url_col = dffiltered["Profile url"].dropna().astype(str)
        csv_url = url_col.to_csv(index=False, header=False)
        b64_url = base64.b64encode(csv_url.encode('utf-8')).decode()
        href_url = f'<a href="data:file/csv;base64,{b64_url}" download="profile_urls.csv">Download Filtered Profile URLs only CSV File</a>'


##### DISPLAY OF RESULTS #####
        
        # Display both filtered and unfiltered data in two windows with links to download each below
        col1, col2 = st.beta_columns(2)
        with col1:
            st.write("Unfiltered Data")
            st.write(df)
            st.markdown(href_unfiltered, unsafe_allow_html=True)
        with col2:
            st.write("Filtered Data")
            st.write(dffiltered)
            st.markdown(href_filtered, unsafe_allow_html=True)
            
        # Display the link to download profile URLs of filtered data only
        st.markdown(href_url, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
