import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Commodity Portfolio Weight Simulator")

# ----------------------------------
# Data
# ----------------------------------

data = {
"Commodity":[
"Chicago Wheat","Wheat (Kansas City)","Corn","Soybeans","Coffee",
"Sugar #11","Cocoa","Cotton #2","Lean Hogs","Live Cattle","Feeder Cattle",
"Crude Oil","Heating Oil","RBOB Gasoline","Brent Crude Oil","Gasoil",
"Natural Gas","Aluminum","Copper","Lead","Nickel","Zinc","Gold","Silver"
],

"Ticker":[
"W","KW","C","S","KC","SB","CC","CT","LH","LC","FC",
"CL","HO","RB","LCO","LGO","NG","MAL","MCU","MPB","MNI","MZN","GC","SI"
],

"Weight":[
2.77,1.15,4.36,3.14,0.72,1.54,0.32,1.41,1.27,3.48,1.27,
26.42,4.24,4.48,18.61,5.56,3.11,3.89,4.45,0.78,0.76,1.28,3.72,0.42
],

"Value":[
892.1,369.5,1776.7,2950.7,550.6,508.1,274.8,359.9,268.3,736.1,268.3,
23306.8,3924.5,3954.8,16416.4,4900.4,3900.1,3376.5,6324.9,805.2,1899.2,
2679.1,11008.5,1995.9
]
}

df = pd.DataFrame(data)

# ----------------------------------
# Sidebar sliders
# ----------------------------------

st.sidebar.header("Adjust Commodity Weights")

adjusted_weights = []

for i,row in df.iterrows():

    w = st.sidebar.slider(
        f"{row['Commodity']} ({row['Ticker']})",
        0.0,
        30.0,
        float(row["Weight"])
    )

    adjusted_weights.append(w)

df["Adjusted Weight"] = adjusted_weights

# ----------------------------------
# Calculations
# ----------------------------------

total_value = df["Value"].sum()

df["Adjusted Value"] = total_value * df["Adjusted Weight"] / 100

# ----------------------------------
# Metrics
# ----------------------------------

col1,col2,col3 = st.columns(3)

col1.metric("Original Total Market Value (USD Bn)", round(total_value,2))
col2.metric("Total Adjusted Weight (%)", round(df["Adjusted Weight"].sum(),2))
col3.metric("Adjusted Portfolio Value (USD Bn)", round(df["Adjusted Value"].sum(),2))

# ----------------------------------
# Charts
# ----------------------------------

st.subheader("Original Commodity Weights")

fig1 = px.pie(
    df,
    values="Weight",
    names="Commodity"
)

st.plotly_chart(fig1,use_container_width=True)

st.subheader("Adjusted Commodity Weights")

fig2 = px.pie(
    df,
    values="Adjusted Weight",
    names="Commodity"
)

st.plotly_chart(fig2,use_container_width=True)

st.subheader("Dollar Value Comparison")

fig3 = px.bar(
    df,
    x="Commodity",
    y=["Value","Adjusted Value"],
    barmode="group"
)

st.plotly_chart(fig3,use_container_width=True)

# ----------------------------------
# Data Table
# ----------------------------------

st.subheader("Full Commodity Table")

st.dataframe(df)