import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from crm_Project import create_rfm, create_cltv_c, create_cltv_p,check_id,arl_recommender,rules,create_rules

# Upload Data
df = pd.read_excel("./CrmData.xlsx")

# Create DataFrames
rfm_df = create_rfm(df)
rfm_df.reset_index(inplace=True)
cltv_p_df = create_cltv_p(df)
rules = create_rules(df)
cltv_c_df = create_cltv_c(df)
# Sidebar choice Bar
analysis_choice = st.sidebar.radio('Choose Analyze 👇', ('RFM Analyze','CLTV- Expected Purchase Prediction',"CLTV- Expected Profit and CLV Prediction",'CLTV-C Analyze',"Product Recommendation"))

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('AnalyzeWise CRM')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Hakan Gunes](https://www.linkedin.com/in/hakan-g%C3%BCne%C5%9F-a3b14720b/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("In the world of retail, success hinges on mastering data. RetailGenius offers deep retail analytics to empower your business growth.")
    st.markdown("📈 RFM Analysis: Understand customer behaviors and create personalized targeting using RFM analysis.")
    st.markdown("💡 CLTV Analysis: Predict customer lifetime value and boost your profits. Identify which customers are the most valuable for your business.")
    st.markdown("📊 Expected Purchase Values: Create robust sales forecasts to optimize inventory management and meet demand.")
    st.markdown("💼 CLTV- Expected Profit and CLV Prediction: Refers to an analytical method and modeling process that helps predict customers' future profit potential and estimate their Customer Lifetime Value.")
    st.markdown("📬 Product Recommendation: A recommendation system for the opportunity to cross-sell products that have been chosen together.")
    st.markdown("You can find the source code in the [Hakan GitHub Repository](https://github.com/HakanGnes/AnalyzeWise-CRM)")
    st.write("Choose Analyze option from the sidebar.")


if analysis_choice == 'RFM Analyze':
    st.header('RFM Analyze')
    # Segment selection interface
    selected_segment = st.selectbox('Select Segment', rfm_df['segment'].unique())
    # Filter by selected segment
    filtered_customers = rfm_df[rfm_df['segment'] == selected_segment]['CustomerNo']
    st.write(f"Customer numbers of {selected_segment} segment({len(filtered_customers)} customers):")
    st.write(filtered_customers)

    # Calculate the percentage of each segment relative to other segments
    segment_counts = rfm_df['segment'].value_counts()
    segment_percentages = segment_counts / segment_counts.sum() * 100

    # Get percentage of selected segment
    selected_segment_percentage = segment_percentages[selected_segment]

    # Get percentage distribution of other segments (subtract selected segment)
    other_segments_percentage = segment_percentages.drop(index=selected_segment)

    # Create a pie chart showing the selected segment as a percentage distribution relative to other segments
    labels = other_segments_percentage.index.tolist()
    sizes = other_segments_percentage.values.tolist()
    sizes.append(selected_segment_percentage)
    labels.append(selected_segment)
    explode = [0.1 if label == selected_segment else 0 for label in labels]  # Let the first slice separate slightly.

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.subheader(f"Distribution of {selected_segment} segment compared to other segments")
    st.pyplot(fig1)

elif analysis_choice == 'CLTV- Expected Purchase Prediction':
    st.header('CLTV- Expected Purchase Prediction')

    # CLTV ve Segment seçme arayüzü
    selected_segment = st.selectbox('Select Segment', cltv_p_df['segment'].unique())

    # Seçilen segmente göre müşteri numarası seçme arayüzü
    filtered_customers = cltv_p_df[cltv_p_df['segment'] == selected_segment]['CustomerNo']
    selected_customer1 = st.selectbox('Select Customer Number 1', filtered_customers)

    filtered_customers = cltv_p_df[cltv_p_df['segment'] == selected_segment]['CustomerNo']
    selected_customer2 = st.selectbox('Select Customer Number 2', filtered_customers)

    # Seçilen müşteri için beklenen satın alma değerlerini görüntüle - Display for the first customer
    selected_customer_data1 = cltv_p_df[cltv_p_df['CustomerNo'] == selected_customer1]
    st.write(f"{selected_customer1} customer's Expected Purchase Values:")
    st.write("1 week: ", selected_customer_data1['expected_purc_1_week'].values[0])
    st.write("1 month: ", selected_customer_data1['expected_purc_1_month'].values[0])
    st.write("3 month: ", selected_customer_data1['expected_purc_3_month'].values[0])
    st.write("6 month: ", selected_customer_data1['expected_purc_6_month'].values[0])
    st.write("9 month: ", selected_customer_data1['expected_purc_9_month'].values[0])
    st.write("12 month: ", selected_customer_data1['expected_purc_12_month'].values[0])

    # Seçilen müşteri için beklenen satın alma değerlerini görüntüle - Display for the second customer
    selected_customer_data2 = cltv_p_df[cltv_p_df['CustomerNo'] == selected_customer2]
    st.write(f"{selected_customer2} customer's Expected Purchase Values:")
    st.write("1 week: ", selected_customer_data2['expected_purc_1_week'].values[0])
    st.write("1 month: ", selected_customer_data2['expected_purc_1_month'].values[0])
    st.write("3 month: ", selected_customer_data2['expected_purc_3_month'].values[0])
    st.write("6 month: ", selected_customer_data2['expected_purc_6_month'].values[0])
    st.write("9 month: ", selected_customer_data2['expected_purc_9_month'].values[0])
    st.write("12 month: ", selected_customer_data2['expected_purc_12_month'].values[0])

    comparison_data = pd.DataFrame({
        'Months': ['1 Week', '1 Month', '3 Months', '6 Months', '9 Months', '12 Months'],
        f'{selected_customer1}': [
            selected_customer_data1['expected_purc_1_week'].values[0],
            selected_customer_data1['expected_purc_1_month'].values[0],
            selected_customer_data1['expected_purc_3_month'].values[0],
            selected_customer_data1['expected_purc_6_month'].values[0],
            selected_customer_data1['expected_purc_9_month'].values[0],
            selected_customer_data1['expected_purc_12_month'].values[0],
        ],
        f'{selected_customer2}': [
            selected_customer_data2['expected_purc_1_week'].values[0],
            selected_customer_data2['expected_purc_1_month'].values[0],
            selected_customer_data2['expected_purc_3_month'].values[0],
            selected_customer_data2['expected_purc_6_month'].values[0],
            selected_customer_data2['expected_purc_9_month'].values[0],
            selected_customer_data2['expected_purc_12_month'].values[0],
        ]
    })


    # Add the average values
    comparison_data['Average'] = comparison_data.iloc[:, 1:].mean(axis=1)

    # Sort the DataFrame by the 'Average' column
    comparison_data = comparison_data.sort_values(by='Average')

    # Create a bar chart to compare the two customers for each month
    st.bar_chart(comparison_data.set_index('Months'))

elif analysis_choice == 'CLTV- Expected Profit and CLV Prediction':
    st.header('CLTV- Expected Profit and CLV Prediction')

    # Select Segment
    selected_segment = st.selectbox('Select Segment', cltv_p_df['segment'].unique())

    # Customer number selection interface according to the selected segment
    filtered_customers = cltv_p_df[cltv_p_df['segment'] == selected_segment]['CustomerNo']
    selected_customer1 = st.selectbox('Select Customer Number 1', filtered_customers)

    filtered_customers = cltv_p_df[cltv_p_df['segment'] == selected_segment]['CustomerNo']
    selected_customer2 = st.selectbox('Select Customer Number 2', filtered_customers)

    # Display for the first customer
    selected_customer_data1 = cltv_p_df[cltv_p_df['CustomerNo'] == selected_customer1]
    st.write(f"{selected_customer2} customer's Information:")
    st.write("Expected Average Profit: ", selected_customer_data1['expected_average_profit'].values[0])
    st.write("CLV (Customer Lifetime Value): ", selected_customer_data1['clv'].values[0])
    st.write("Segment: ", selected_customer_data1['segment'].values[0])

    # Display for the second customer
    selected_customer_data2 = cltv_p_df[cltv_p_df['CustomerNo'] == selected_customer2]
    st.write(f"{selected_customer2} customer's Information:")
    st.write("Expected Average Profit: ", selected_customer_data2['expected_average_profit'].values[0])
    st.write("CLV (Customer Lifetime Value): ", selected_customer_data2['clv'].values[0])
    st.write("Segment: ", selected_customer_data2['segment'].values[0])

elif analysis_choice == 'CLTV-C Analyze':
    st.header('CLTV-C Analyze')

    # Select Segment
    selected_segment = st.selectbox('Select Segment', cltv_c_df['segment'].unique())

    # Customer number selection interface according to the selected segment
    filtered_customers = cltv_c_df[cltv_c_df['segment'] == selected_segment]['CustomerNo']
    selected_customer = st.selectbox('Select Customer Number', filtered_customers)

    # View CLTV-C value of selected customer
    selected_customer_data = cltv_c_df.loc[selected_customer]
    st.write(f"{selected_customer} customer's CLTV-C Analysis:")
    st.write("Total Number of Transactions: ", selected_customer_data['total_transaction'])
    st.write("Total Number of Products: ", selected_customer_data['total_unit'])
    st.write("Total amount: ", selected_customer_data['total_price'])
    st.write("Average Order Value: ", selected_customer_data['avg_order_value'])
    st.write("Purchase Frequency: ", selected_customer_data['purchase_frequency'])
    st.write("Profit margin: ", selected_customer_data['profit_margin'])
    st.write("Customer Value: ", selected_customer_data['customer_value'])
    st.write("CLTV-C Value: ", selected_customer_data['cltv'])
    st.write("Segment: ", selected_customer_data['segment'])

    # Create a bar chart to compare the selected customer's CLTV-C value with the average CLTV-C value
    customer_cltv = selected_customer_data['cltv']
    avg_cltv = cltv_c_df['cltv'].mean()
    st.bar_chart({'Selected Customer': customer_cltv, 'Average CLTV': avg_cltv})


elif analysis_choice == 'Product Recommendation':
    st.header('Product Recommendations')
    selected_product = st.selectbox('Select Product', df['ProductNo'].unique())
    recommendation_count = st.slider('How Many Product Recommendations Should Be Made?', 1, 10, 5)

    if st.button('View Recommendations'):
        recommendations = arl_recommender(rules, selected_product, recommendation_count)
        st.write(f"{selected_product} for recommended products :")
        for i, recommendation in enumerate(recommendations, start=1):
            st.write(f"{i}. Recommendation: {recommendation}")



