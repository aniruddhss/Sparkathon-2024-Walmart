import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#FOR PROTOTYPE OR WORKING-DEMO

dates = pd.date_range(end=pd.Timestamp.today(), periods=4, freq='W-WED').strftime('%Y-%m-%d').tolist()
#sample stores data
stores_data = {
    'Date of Change': dates,
    'JioMart': [10, 12, 11, 13],
    'D-Mart': [11, 13, 12, 14],
    'Ondoor(local)': [9, 11, 10, 12],
    'Big Bazaar': [10, 11, 12, 14]
}

#sample products
products = ['Coca-Cola', 'Sprite', 'Fanta']

#sample users data
users = {
    'store1': {'city': 'Bhopal', 'password': 'pass1'},
    'store2': {'city': 'Indore', 'password': 'pass2'},
}

def authenticate(store_id, city, password):
    if store_id in users and users[store_id]['city'] == city and users[store_id]['password'] == password:
        return True
    return False

def login_page():
    st.title("Walmart Store Price Decider")
    st.subheader("Log-in")

    store_id = st.text_input("Store ID")
    city = st.text_input("City")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(store_id, city, password):
            st.session_state['authenticated'] = True
            st.session_state['store_id'] = store_id
            st.session_state['city'] = city
        else:
            st.error("Invalid login credentials")

def product_selection_page():
    st.title("Select Product")

    product = st.selectbox("Choose a product", products)

    if st.button("Next"):
        st.session_state['product'] = product
        st.session_state['page'] = 'dashboard'

def dashboard_page():
    st.title("Price Dashboard")

    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    product = st.session_state.get('product', 'Product 1')
    st.write(f"Product: {product}")

    col1, col2 = st.columns([3,1])

    with col1:
        st.subheader("Price History")
        store = st.selectbox("Select a store", options=list(stores_data.keys())[1:])

        prices_df = pd.DataFrame(stores_data)
        prices_df.set_index('Date of Change', inplace=True)
        selected_store_prices = prices_df[store]
        fig = px.line(
            selected_store_prices,
            x=selected_store_prices.index,
            y=selected_store_prices.values,
            title=f'Price History for {store}',
            labels={'x': 'Date of Change', 'y': 'Price'},
        )
        fig.update_traces(mode='lines+markers', line=dict(width=3), marker=dict(size=10))
        fig.update_layout(yaxis=dict(range=[0, max(selected_store_prices) + 1]))

        st.plotly_chart(fig, use_container_width=True)
        
        
        st.write("You can find more details of the project at: https://github.com/aniruddhss/Sparkathon-2024-Walmart")

    with col2:
        st.subheader("Last 4 Price Changes")
        prices_df = pd.DataFrame(stores_data)
        prices_df.set_index('Date of Change', inplace=True)
        st.dataframe(prices_df)
         
        st.subheader("Current Prices")
        current_prices = prices_df.iloc[-1]  
        price_comparison = pd.DataFrame({
            'Store': current_prices.index,
            'Current Price': current_prices.values
        })
        st.table(price_comparison)

        # Recommended price
        min_price = current_prices.min()
        max_price = current_prices.max()
        recommended_price = current_prices.mean()  

        # st.subheader("Recommended Price")
        gauge_fig = go.Figure()

        gauge_fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=recommended_price,
            gauge=dict(
                axis=dict(range=[None, max_price + 5]),
                bar=dict(color="white"),
                bgcolor="rgba(0,0,0,0.5)",  # Semi-transparent dark background
                borderwidth=1,
                bordercolor="black",
                steps=[
                    dict(range=[min_price, recommended_price], color="darkred"),  
                    dict(range=[recommended_price, max_price], color="darkgreen")  
                ]
            ),
            number=dict(
                font=dict(size=40, color="white")
            ),
            title=dict(
                text="Recommended Price",
                font=dict(size=20, color="white")
            )
        ))

        gauge_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
            plot_bgcolor="rgba(0,0,0,0.5)",  # Semi-transparent dark background
            template="plotly_dark"
        )
        gauge_fig.update_layout(width=500, height=300)

        st.plotly_chart(gauge_fig)


def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        login_page()
    elif st.session_state.get('page', '') == 'dashboard':
        dashboard_page()
    else:
        product_selection_page()

if __name__ == "__main__":
    main()
