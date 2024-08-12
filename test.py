import streamlit as st
import pandas as pd
import math
import warnings
import matplotlib.pyplot as plt
import altair as alt
from collections import Counter

st.set_page_config(layout="wide")
warnings.simplefilter(action='ignore', category=UserWarning)

def load_excel(file):
    excel_data = pd.ExcelFile(file)
    qa_sheet = pd.read_excel(excel_data, sheet_name='QA Sheet', skiprows=2)
    categories_sheet = pd.read_excel(excel_data, sheet_name='Categories')

    # Remove unnamed columns from categories_sheet
    categories_sheet = categories_sheet.loc[:, ~categories_sheet.columns.str.contains('^Unnamed')]

    return qa_sheet, categories_sheet

st.title('Insert awesome title here')

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

#if uploaded_file is not None:
if uploaded_file is None:
    #qa_sheet, categories_sheet = load_excel(uploaded_file)
    qa_sheet, categories_sheet = load_excel("Bug Report Rando.xlsx")
    
    
    # Adjust QA Sheet preview to start from the third row of actual data
    qa_sheet_data = qa_sheet.iloc[1:].reset_index(drop=True)
    qa_sheet_data.columns = qa_sheet.iloc[0]

    st.subheader('Data Preview - QA Sheet')
    st.dataframe(qa_sheet_data)

    show_cat_sheet = st.checkbox("Show Categories sheet")
    if show_cat_sheet:
        st.subheader('Data Preview - Categories Sheet')
        st.dataframe(categories_sheet)
    
    # List available categories from the Categories Sheet
    category_columns = categories_sheet.columns.tolist()

    # Debug prints
    #print(type(category_columns))
    #print(type(qa_sheet_data.columns.tolist()))
    #print(category_columns)
    category_columns_U = list(map(str.upper, category_columns))
    category_columns_U_N = list(map(lambda x: "CATEGORY" if x == "BUG CATEGORY" else x, category_columns_U))
    #print(category_columns_U)
    #print(qa_sheet_data.columns.tolist())
    
    # Allow user to select a category column
    selected_category = st.selectbox('Select category column to plot', category_columns_U_N, index= category_columns_U_N.index("CATEGORY"))

    # Debug Print
    #print(selected_category)

    if selected_category in qa_sheet_data.columns:
                
        #pass

        #Debug Print
        #print(selected_category)
        selected_category_2 = selected_category
        
        column_values_qa = qa_sheet_data[selected_category].tolist()

        if selected_category_2 == "CATEGORY":
            selected_category_2 = "Bug Category"
            column_values_cat = categories_sheet[selected_category_2].to_list()

        elif selected_category_2 == "ISSUE OWNER":
            selected_category_2 = "Issue Owner"
            column_values_cat = categories_sheet[selected_category_2].to_list()

        elif selected_category_2 == "ISSUE TYPE":
            selected_category_2 = "Issue Type"
            column_values_cat = categories_sheet[selected_category_2].to_list()

        


        else:
            column_values_cat = categories_sheet[selected_category_2.capitalize()].tolist()

        column_values_cat_c = [x for x in column_values_cat if not (isinstance(x, float) and math.isnan(x))]
        temp_count_0 = Counter(column_values_cat_c)
        temp_count_2 = Counter(column_values_qa)
        temp_count_total = temp_count_2 + temp_count_0
        temp_count = Counter({key: value - 1 for key, value in temp_count_total.items()})

        show_zero = st.checkbox("Show Zero Values")


        if show_zero:

            #st.bar_chart(temp_count)
            df2 = pd.DataFrame(temp_count.items(), columns=['Category', 'Count'])
            chart = alt.Chart(df2).mark_bar().encode(
                    x=alt.X('Category:N', title='Category', sort=None), y=alt.Y('Count:Q', title='Count'), tooltip=['Category', 'Count']
                ).properties(
                    title='Counts by Category',
                    width = 800,
                    height = 600
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14 
                ).configure_title(
                    fontSize=16
                )

                # Display the chart in Streamlit
            st.altair_chart(chart, use_container_width=True)
            # keys = list(temp_count.keys())
            # values = list(temp_count.values())
            # fig, ax = plt.subplots()
            # ax.bar(keys, values)
            # st.pyplot(fig)


        
        else:
            st.bar_chart(Counter(column_values_qa))

        if selected_category_2 == "Bug Category":
            show_bug_cat = st.checkbox("Plot Parent Categories")
            if show_bug_cat:
                category_counts = {}
                for key, count in temp_count.items():
                    category = key.split(':')[0]
                    if category in category_counts:
                        category_counts[category] += count
                    else:
                        category_counts[category] = count

                category_counter = Counter(category_counts)

                df1 = pd.DataFrame(category_counter.items(), columns=['Category', 'Count'])

                # Create an Altair chart
                chart = alt.Chart(df1).mark_bar().encode(
                    x=alt.X('Category:N', title='Category', sort=None),  # Treat Category as nominal
                    y=alt.Y('Count:Q', title='Count'),
                    tooltip=['Category', 'Count']
                ).properties(
                    title='Counts by Category'
                ).configure_axis(
                    labelFontSize=12,  # Adjust x-axis label font size
                    titleFontSize=14   # Adjust x-axis title font size
                ).configure_title(
                    fontSize=16  # Adjust chart title font size
                )

                # Display the chart in Streamlit
                st.altair_chart(chart, use_container_width=True)
                #st.bar_chart(category_counter)
            else:
                pass
            
        else:
            pass
        
        
        #print(temp_count)
        #print(column_values)
        #print(Counter(column_values_qa) + Counter(column_values_cat_c))


    else:
        st.warning('Selected category column is not in the QA sheet data')
else:
    st.info('Please upload an Excel file to proceed')
