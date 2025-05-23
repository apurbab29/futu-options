import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from futu import OpenQuoteContext, SubType, RET_OK

st.set_page_config(page_title="Live US Stock Options Viewer", layout="wide")
st.title("📈 US Options Live Data from Futu API")

# Input ticker
ticker = st.text_input("Enter Ticker (e.g., US.TSLA, US.AAPL, US.NVDA):", value="US.TSLA")

if st.button("Fetch Most Recent 300 Contracts"):

    with st.spinner("🔌 Connecting to FutuOpenD..."):
        ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        st.success(f"📡 Connected to FutuOpenD for {ticker}")

        ret, option_df = ctx.get_option_chain(ticker)
        if ret != RET_OK:
            st.error(f"❌ Failed to retrieve option chain: {option_df}")
            ctx.close()
        else:
            option_df['strike_price'] = pd.to_numeric(option_df['strike_price'], errors='coerce')
            option_df['strike_time'] = pd.to_datetime(option_df['strike_time'], errors='coerce')
            option_df = option_df[option_df['strike_time'] > datetime.today()]
            option_df = option_df.sort_values(by='strike_time').head(300)  # ✅ Only 300 most recent

            codes = option_df['code'].dropna().tolist()
            if not codes:
                st.warning("⚠️ No valid option contracts found.")
                ctx.close()
            else:
                ret, err = ctx.subscribe(codes, [SubType.QUOTE], subscribe_push=False)
                if ret != RET_OK:
                    st.error("❌ Subscription failed. Too many requests or insufficient quota.")
                    ctx.unsubscribe(codes, [SubType.QUOTE])
                    ctx.close()
                else:
                    ret, quote_df = ctx.get_stock_quote(codes)
                    if ret != RET_OK or quote_df.empty:
                        st.error("❌ Failed to retrieve quote data.")
                        ctx.unsubscribe(codes, [SubType.QUOTE])
                        ctx.close()
                    else:
                        # Merge quote data with option metadata
                        merged_df = pd.merge(option_df, quote_df, on='code', how='inner')

                        # Normalize columns if renamed during merge
                        if 'strike_price_x' in merged_df.columns:
                            merged_df.rename(columns={'strike_price_x': 'strike_price'}, inplace=True)
                        if 'option_type_x' in merged_df.columns:
                            merged_df.rename(columns={'option_type_x': 'option_type'}, inplace=True)

                        merged_df['strike_price'] = pd.to_numeric(merged_df['strike_price'], errors='coerce')
                        filtered_df = merged_df[merged_df['open_interest'] > 0]

                        if not filtered_df.empty:
                            csv_filename = f"{ticker.replace('.', '_')}_latest_300_filtered.csv"
                            filtered_df.to_csv(csv_filename, index=False)

                            st.success(f"✅ Fetched {len(filtered_df)} contracts with OI > 0")
                            st.dataframe(filtered_df)

                            st.download_button("📥 Download Filtered CSV", filtered_df.to_csv(index=False),
                                               file_name=csv_filename, mime='text/csv')

                            # 📊 Visualizations
                            st.subheader("📊 Volume and Open Interest by Strike")

                            tab1, tab2 = st.tabs(["📈 Volume", "📈 Open Interest"])

                            with tab1:
                                fig1 = px.bar(filtered_df, x='strike_price', y='volume',
                                              color='option_type', barmode='group',
                                              title="Volume by Strike Price")
                                fig1.update_layout(xaxis_title="Strike Price", yaxis_title="Volume")
                                st.plotly_chart(fig1, use_container_width=True)

                            with tab2:
                                fig2 = px.bar(filtered_df, x='strike_price', y='open_interest',
                                              color='option_type', barmode='group',
                                              title="Open Interest by Strike Price")
                                fig2.update_layout(xaxis_title="Strike Price", yaxis_title="Open Interest")
                                st.plotly_chart(fig2, use_container_width=True)
                        else:
                            st.warning("⚠️ No contracts with OI > 0 found in the latest 300.")

                    ctx.unsubscribe(codes, [SubType.QUOTE])
                    ctx.close()
