import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="US Options Data Visualizer", layout="wide")
st.title("📊 US.TSLA Options Data (from Futu API Sample)")

@st.cache_data
def load_data():
    df = pd.read_csv("US_TSLA_filtered_options.csv")
    df['strike_price_x'] = pd.to_numeric(df['strike_price_x'], errors='coerce')
    df['strike_time'] = pd.to_datetime(df['strike_time'], errors='coerce')
    df = df[df['strike_time'] > datetime.today()]
    df = df[df['open_interest'] > 0]
    return df

df = load_data()

if df.empty:
    st.warning("⚠️ No data available with OI > 0 and expiry > today.")
else:
    st.subheader("Filtered Option Contracts")
    st.dataframe(df)

    tab1, tab2 = st.tabs(["📈 Volume by Strike", "📈 OI by Strike"])

    with tab1:
        st.write("### Volume vs Strike Price")
        fig_vol = px.bar(
            df,
            x='strike_price_x',
            y='volume',
            color='option_type',
            barmode='group',
            labels={'strike_price_x': 'Strike Price'},
            title='Volume by Strike Price (CALL vs PUT)'
        )
        fig_vol.update_layout(xaxis_title='Strike Price', yaxis_title='Volume')
        st.plotly_chart(fig_vol, use_container_width=True)

    with tab2:
        st.write("### Open Interest vs Strike Price")
        fig_oi = px.bar(
            df,
            x='strike_price_x',
            y='open_interest',
            color='option_type',
            barmode='group',
            labels={'strike_price_x': 'Strike Price'},
            title='Open Interest by Strike Price (CALL vs PUT)'
        )
        fig_oi.update_layout(xaxis_title='Strike Price', yaxis_title='Open Interest')
        st.plotly_chart(fig_oi, use_container_width=True)

