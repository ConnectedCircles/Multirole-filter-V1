import streamlit as st
import pandas as pd
import gender_guesser.detector as gender
import streamlit as st
import base64

def app():

    # Set title and subtitle, additional text
    st.title("Gender Profile Filter V2")
    st.subheader("Property of Connected Circles")
    st.write("""This app allows you to filter lists of profiles by gender. It does so by isolating the fist name from the surname, prefixes and suffixes
    and subsequently analyzing the first name using the Python library "gender_guesser". Results, which are not certain are labeled as "unknown" are 
    excluded from the filtered results (This may happen for ususual/non-european language first names). You can preview the both the labeled and 
    filtered data in the two preview windows below. You can download the data either labeled, filtered or filtered profile URLs only, all as a .csv""")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file to filter", type="csv")

    # Define radio button options
    gender_options = ['Male', 'Female']

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Create an instance of the gender detector
        detector = gender.Detector()

        # Define a function to get the gender for each name in the DataFrame
        def get_gender(name):
            # Use the detector to guess the gender of the name
            gender_guess = detector.get_gender(name)

            # Map the gender guess to a simplified gender label (male, female, or unknown)
            if gender_guess == 'male':
                return 'M'
            elif gender_guess == 'female':
                return 'F'
            else:
                return 'unknown'

        # Clean name data
        #remove "Dr.", "Prof." etc.
        df['FirstName'] = df['Full name'].str.replace('Dr.', '').str.strip()
        df['FirstName'] = df['FirstName'].str.lower().str.replace('prof.', '').str.strip()
        df['FirstName'] = df['FirstName'].str.lower().str.replace('professor', '').str.strip()
        # change "-" to " "
        df['FirstName'] = df['FirstName'].str.lower().str.replace('-', ' ').str.strip()
        # remove surnames
        df['FirstName'] = df['FirstName'].str.split().str[0]
        # remove all whitespace
        df['FirstName'] = df['FirstName'].str.replace(r'\s+', '', regex=True)
        # capitalize first letter (gender_guesser requires this)
        df['FirstName'] = df['FirstName'].str.title()

        # Apply the get_gender function to create a new "gender" column in the DataFrame
        df['gender'] = df['FirstName'].apply(get_gender)

        # Get selected gender option from radio button
        selected_gender = st.radio('Select a gender to filter by:', gender_options)

        if selected_gender == 'Male':
            # Filter to only include male gender, delete gender column
            dffiltered = df[df["gender"]=="M"]
            dffiltered = dffiltered.drop(["FirstName", "gender"], axis=1)
        elif selected_gender == 'Female':
            # Filter to only include female gender, delete gender column
            dffiltered = df[df["gender"]=="F"]
            dffiltered = dffiltered.drop(["FirstName", "gender"], axis=1)
        else:
            # Keep all observations, delete gender column
            dffiltered = df.drop(["FirstName", "gender"], axis=1)

        # Download link for filtered data
        csv_filtered = dffiltered.to_csv(index=False)
        b64_filtered = base64.b64encode(csv_filtered.encode('utf-8')).decode()
        href_filtered = f'<a href="data:file/csv;base64,{b64_filtered}" download="filtered_data.csv">Download Filtered CSV File</a>'

        # Download link for unfiltered data
        csv_unfiltered = df.to_csv(index=False)
        b64_unfiltered = base64.b64encode(csv_unfiltered.encode('utf-8')).decode()
        href_unfiltered = f'<a href="data:file/csv;base64,{b64_unfiltered}" download="unfiltered_data.csv">Download Unfiltered CSV File</a>'

        # Download link for filtered data URLs only, no header
        url_col = dffiltered["Profile url"].dropna().astype(str)
        csv_url = url_col.to_csv(index=False, header=False)
        b64_url = base64.b64encode(csv_url.encode('utf-8')).decode()
        href_url = f'<a href="data:file/csv;base64,{b64_url}" download="profile_urls.csv">Download Profile URLs CSV File</a>'

        # DISPLAY OF RESULTS #
        
        # Display both filtered and unfiltered data in two windows with links to download each below
        col1, col2 = st.columns(2)
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
