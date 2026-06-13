from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import plotly.express as px

from io import BytesIO
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOGIN CONFIGURATION
# =========================

USERNAME = "admin"
PASSWORD = "1234"

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN FUNCTION
# =========================

def login():

    st.title("🔐 Sales Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()

        else:
            st.error("Invalid Username or Password ❌")

# =========================
# SHOW LOGIN PAGE
# =========================

if not st.session_state.logged_in:
    login()
    st.stop()


# =========================
# CUSTOM DASHBOARD STYLING
# =========================

st.markdown("""
<style>

/* Main background */
.main {
    background-color: #0E1117;
}

/* Chart containers */
div[data-testid="stPlotlyChart"] {
    border: 2px solid #4CAF50;
    border-radius: 15px;
    padding: 10px;
    background-color: #1E1E1E;
    box-shadow: 0px 0px 15px rgba(76, 175, 80, 0.3);
    margin-bottom: 25px;
}

/* KPI cards */
div[data-testid="metric-container"] {
    border: 2px solid #4CAF50;
    padding: 15px;
    border-radius: 12px;
    background-color: #1E1E1E;
    box-shadow: 0px 0px 10px rgba(76, 175, 80, 0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Titles */
h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)



#===========================
#PAGE CONFIG
#============================

st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }

    h1, h2, h3 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide"
    )

#============================
#LOAD DATA
#============================

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "data" / "cleaned_sales.csv"

df = pd.read_csv(csv_path)

#Convert sales column
df["Sales"] = pd.to_numeric(df["Sales"], errors='coerce')
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')

# Create estimated profit column
df["Profit"] = df["Sales"] * 0.20

#Remove null values
df = df.dropna()


# =========================
# NAVIGATION
# =========================

page = st.sidebar.selectbox(
    "📌 Navigation",
    [
        "🏠 Dashboard",
        "📈 Sales Trend",
        "🌍 Sales by Region",
        "💹 Profit Analysis",
        "🔮 Forecasting",
        "📄 Reports"
    ]
)

analysis_option = st.sidebar.selectbox(
        "📌Statistical Analysis",
        [
            "📊 Summary Statistics",
            "📈 Correlation Analysis",
            "📉 Distribution Analysis",
            "🧮 Mean Median Mode",
            "📍 Variance & Standard Deviation"
        ]
    )


#==============================
#SLIDEBAR FILTERS
#==============================

st.sidebar.title("🔍 Filters")

#Category filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

#Region filter
region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

#Segment filter
segment_filter = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

#Apply filter
filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Region"].isin(region_filter)) &
    (df["Segment"].isin(segment_filter))
]

# =========================
# CREATE MONTH_YEAR COLUMN
# =========================

filtered_df["Month_Year"] = (
    filtered_df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

# =========================
# EXCEL DOWNLOAD FUNCTION
# =========================

from io import BytesIO

def to_excel(dataframe):

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(
            writer,
            index=False,
            sheet_name='Sales Report'
        )

    processed_data = output.getvalue()

    return processed_data

# =========================
# DASHBOARD PAGE
# =========================

st.title("📊 Advanced Sales Analytics Dashboard")


if page == "🏠 Dashboard":


    st.markdown("---")

    total_sales = filtered_df["Sales"].sum()
    total_orders = filtered_df["Order ID"].nunique()
    total_customers = filtered_df["Customer ID"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("🛒 Total Orders", total_orders)
    col3.metric("👥 Total Customers", total_customers)

    st.markdown("---")

    

    st.markdown("---")

    st.subheader("📄 Dataset Preview")
    


    st.dataframe(filtered_df)
    st.markdown("----")

# =========================
# SALES TREND PAGE
# =========================

elif page == "📈 Sales Trend":

    st.title("📈 Sales Trend Analysis")

    filtered_df["Month_Year"] = (
        filtered_df["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        filtered_df.groupby("Month_Year")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Month_Year",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )

    st.plotly_chart(fig, use_container_width=True)

    
    with st.expander("Insights"):
        st.success(""" 
   
🔹  📈 Sales Trend\n
🔹  Analyzes sales performance over time.\n
🔹  Identifies:\n 
    🔹  seasonal growth,\n
    🔹  peak sales periods,\n
    🔹 low-performing months.\n
🔹 Helps businesses predict future demand.\n
🔹 Useful for sales forecasting and inventory planning.\n
🔹 Example insight:\n
         Sales are increasing month by month, showing positive business growth.
""") 

# =========================
# SALES BY REGION PAGE
# =========================

elif page == "🌍 Sales by Region":

    st.title("🌍 Sales by Region")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    # =========================
    # PIE CHART
    # =========================

    fig_region = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales Distribution by Region",
        hole=0.4
    )

    fig_region.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )

    st.plotly_chart(fig_region, use_container_width=True)
    

    # =========================
    # BAR CHART
    # =========================

    fig_bar = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Regional Sales Comparison",
        text_auto=True
    )

    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # =========================
    # REGION DATA TABLE
    # =========================

    st.subheader("📄 Region Sales Data")

    st.dataframe(
        region_sales,
        use_container_width=True
    ) 

   

    
    with st.expander("Insights"):
        st.success(""" 
           
🔹 🌍 Sales by Region\n
   
🔹 Compares sales performance across regions.\n
   
🔹 Helps identify:\n
   🔹  highest-performing region,\n
   🔹  low-performing markets,\n
    🔹 regional demand patterns.\n
🔹 Useful for regional marketing and expansion strategies.\n


🔹 Example regional comparison:\n
        🔹  Sales by Region\n
                        Comparison of regional sales performance.

    """)     

# =========================
# PROFIT ANALYSIS PAGE
# =========================

elif page == "💹 Profit Analysis":

    st.title("💹 Profit Analysis")

    profit_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        profit_category,
        x="Category",
        y="Profit",
        title="Profit by Category",
        text_auto=True
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )

    st.plotly_chart(fig2, use_container_width=True)

    

    
    with st.expander("Insights"):
        st.success(""" 

🔹 💹 Profit Analysis\n
🔹  Evaluates profitability across categories or products.\n
🔹  Helps identify:\n
    🔹  most profitable products,\n
    🔹  loss-making segments,\n
    🔹  business efficiency.\n
🔹  Useful for pricing and cost optimization.\n
🔹  Example insight:\n
            Some categories generate high sales but low profit margins.

    """) 

# =========================
# FORECASTING PAGE
# =========================

elif page == "🔮 Forecasting":

    st.title("🔮 Sales Forecasting")

    monthly_sales_forecast = (
        filtered_df.groupby("Month_Year")["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales_forecast["Month_Index"] = np.arange(
        len(monthly_sales_forecast)
    )

    X = monthly_sales_forecast[["Month_Index"]]
    y = monthly_sales_forecast["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_months = np.arange(
        len(monthly_sales_forecast),
        len(monthly_sales_forecast) + 6
    ).reshape(-1, 1)

    future_predictions = model.predict(future_months)

    future_df = pd.DataFrame({
        "Future Month": [f"Future {i+1}" for i in range(6)],
        "Predicted Sales": future_predictions
    })

    st.dataframe(future_df)

    fig3 = px.line(
        future_df,
        x="Future Month",
        y="Predicted Sales",
        markers=True,
        title="Future Sales Prediction"
    )

    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )

    st.plotly_chart(fig3, use_container_width=True)    

# =========================
# FORECASTING PAGE
# =========================

elif page == "🔮 Forecasting":

    st.title("🔮 Sales Forecasting")

    monthly_sales_forecast = (
        filtered_df.groupby("Month_Year")["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales_forecast["Month_Index"] = np.arange(
        len(monthly_sales_forecast)
    )

    X = monthly_sales_forecast[["Month_Index"]]
    y = monthly_sales_forecast["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_months = np.arange(
        len(monthly_sales_forecast),
        len(monthly_sales_forecast) + 6
    ).reshape(-1, 1)

    future_predictions = model.predict(future_months)

    future_df = pd.DataFrame({
        "Future Month": [f"Future {i+1}" for i in range(6)],
        "Predicted Sales": future_predictions
    })

    st.dataframe(future_df)

    fig3 = px.line(
        future_df,
        x="Future Month",
        y="Predicted Sales",
        markers=True,
        title="Future Sales Prediction"
    )

    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )

    st.plotly_chart(fig3, use_container_width=True)


    st.markdown("----")

    with st.expander("📌 Forecasting Insights"):
         st.success("""
🔹 Forecasting predicts future sales using historical data.

🔹 Helps businesses:
    ➤ Plan inventory
    ➤ Allocate budget
    ➤ Estimate future revenue

🔹 Useful for strategic business planning.

🔹 Forecast trend shows expected business growth over upcoming months.
""")

# =========================
# REPORTS PAGE
# =========================

elif page == "📄 Reports":

    st.title("📄 Download Reports")
   
    # CSV Download
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name='filtered_sales_report.csv',
        mime='text/csv'
    )

    # Excel Download
    excel_data = to_excel(filtered_df)

    st.download_button(
        label="📊 Download Excel Report",
        data=excel_data,
        file_name="filtered_sales_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    with st.expander("Insights"):
         st.success("""
        
🔹 📄 Reports\n
🔹 Allows exporting dashboard data into CSV or Excel reports.\n
🔹 Helps users:\n
    🔹  share analysis,\n
    🔹  maintain records,\n
    🔹  generate business documentation.\n
🔹 Useful for management reporting and presentations.\n
🔹 Example insight:\n
        Automated reports reduce manual analysis effort and improve decision-making speed.
""")

# ===================================
# STATISTICAL ANALYSIS PAGE
# ===================================    

st.title("📊 Statistical Analysis")


if analysis_option == "📊 Summary Statistics":


        st.subheader("Summary Statistics")
        st.dataframe(df.describe())
        with st.expander("Insights"):
             st.success("""
               📊 Summary Statistics\n
                Displays:\n
                    mean,\n
                    median,\n
                    minimum,\n
                    maximum,\n
                    count,\n
                    quartiles.\n
                Provides a quick overview of dataset distribution. 
""")

    # CORRELATION
elif analysis_option == "📈 Correlation Analysis":

        st.subheader("Correlation Matrix")

        corr = df.corr(numeric_only=True)

        st.dataframe(corr)

        st.line_chart(corr)
        with st.expander("Insights"):
            st.success("""
            
🔹 📈 Correlation Analysis\n
🔹 Shows relationships between numerical variables.\n
🔹 Helps determine:\n
    🔹 which variables impact sales,\n
    🔹 positive or negative relationships.\n
    🔹  Example insight:\n
            Profit and sales may show strong positive correlation.    
""")

    # DISTRIBUTION
elif analysis_option == "📉 Distribution Analysis":

        st.subheader("Sales Distribution")

        st.area_chart(df["Sales"])
        with st.expander("Insights"):
             st.success("""
            
🔹 📉 Distribution Analysis\n
🔹 Visualizes data spread and frequency.\n
🔹  Helps identify:\n
    🔹 skewed data,\n
    🔹 normal distribution,\n
    🔹 unusual patterns.\n

""")

    # MEAN MEDIAN MODE
elif analysis_option == "🧮 Mean Median Mode":

        st.subheader("Mean Median Mode")

        st.write("Mean:", df["Sales"].mean())
        st.write("Median:", df["Sales"].median())
        st.write("Mode:", df["Sales"].mode()[0])

        with st.expander("Insights"):
             st.success("""
       
🔹 🧮 Mean Median Mode\n
🔹 Helps understand central tendency of data.\n
🔹 Useful for identifying typical sales values.\n
🔹 Example insight:\n
            If mean > median, data may contain high-value outliers.
""")

    # VARIANCE
elif analysis_option == "📍 Variance & Standard Deviation":

        st.subheader("Variance & Standard Deviation")

        st.write("Variance:", df["Sales"].var())
        st.write("Standard Deviation:", df["Sales"].std())
        with st.expander("Insights"):
             st.success("""
               
🔹 📍 Variance & Standard Deviation\n
🔹 Measures data variability and consistency.\n
🔹 High standard deviation indicates unstable sales trends.\n
🔹 Low standard deviation indicates stable business performance.""")    



