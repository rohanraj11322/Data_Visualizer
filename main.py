import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊  Data Visualizer')

# File upload
uploaded_file = st.file_uploader("Upload file", type=["csv", "xls", "xlsx", "txt", "json", "html"])

if uploaded_file is not None:
    # Read the uploaded file
    file_ext = uploaded_file.name.split(".")[-1]
    if file_ext == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_ext in ['xls', 'xlsx']:
        df = pd.read_excel(uploaded_file)
    elif file_ext == 'txt':
        df = pd.read_csv(uploaded_file, delimiter='\t')
    elif file_ext == 'json':
        df = pd.read_json(uploaded_file)
    elif file_ext == 'html':
        df = pd.read_html(uploaded_file)[0]  # Assuming the first table is the desired one

    # Plot graph
    if not df.empty:
        st.subheader("Plot Graph:")
        x_axis = st.selectbox('Select the X-axis', options=df.columns.tolist())
        y_axis = st.selectbox('Select the Y-axis', options=df.columns.tolist())
        plot_type = st.selectbox('Select the type of plot', options=['Line Plot', 'Bar Chart', 'Scatter Plot', 'Histogram', 'Box Plot'])
        plot_button = st.button('Plot Graph')
        if plot_button:
            fig, ax = plt.subplots()
            if plot_type == 'Line Plot':
                sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
            elif plot_type == 'Histogram':
                sns.histplot(data=df, x=x_axis, ax=ax)
            elif plot_type == 'Box Plot':
                sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
            st.pyplot(fig)

            # Save the plot as an image
            temp_file_path = "temp_plot.png"
            plt.savefig(temp_file_path)
            plt.close()

            # Download the plot
            with open(temp_file_path, "rb") as file:
                plot_data = file.read()
                plot_base64 = base64.b64encode(plot_data).decode("utf-8")
                href = f'<a href="data:image/png;base64,{plot_base64}" download="plot.png">Download Plot as PNG</a>'
                st.markdown(href, unsafe_allow_html=True)

        # Checkbox for sorting data
        sort_data = st.checkbox("Sort Data")
        if sort_data:
            # Sort data
            st.subheader("Sort Data:")
            sort_column = st.selectbox("Select column to sort by", options=df.columns.tolist())
            ascending = st.checkbox("Ascending", True)
            sorted_df = df.sort_values(by=sort_column, ascending=ascending)
            st.subheader("Sorted Data Preview:")
            st.write(sorted_df.head())

        # Checkbox for data cleaning
        clean_data = st.checkbox("Data Clean")
        if clean_data:
            # Data Cleaning
            st.subheader("Data Cleaning:")
            # Placeholder for data cleaning options

        # Checkbox for data analysis
        analyze_data = st.checkbox("Data Analysis")
        if analyze_data:
            # Analyze data
            st.subheader("Data Analysis:")
            st.write(df.describe())

        # Checkbox for summary
        show_summary = st.checkbox("Show Summary")
        if show_summary:
            # Summary
            st.subheader("Summary:")
            st.write(df.head())
          st.write("Copyright © 2024 Rohan Kumar")

if __name__ == '__main__':
    main()
