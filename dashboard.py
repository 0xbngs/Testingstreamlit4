import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# import dataset
@st.cache_data
def load_data(url):
    data = pd.read_csv(url) # ini download dataset
    data['dteday'] = pd.to_datetime(data['dteday'])  # Ubah tipe data
    return data

url = 'https://raw.githubusercontent.com/Flytomarsz/Bike-Sharing-System-Analysis/main/hour.csv'
data = load_data(url)

st.title("Bike Sharing System in 2012 for Registered User Only📊")
st.write(data)

# Visualisasi Pie Chart
fig1, ax1 = plt.subplots()
ax1.pie(
    [data['casual'].sum(), data['registered'].sum()],
    labels=['Casual', 'Registered'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette("pastel")
)
ax1.set_title("User's Segmentation")
st.pyplot(fig1)

# Visualisasi Bar Chart
season_labels = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
data['season_label'] = data['season'].map(season_labels)
total_registered_per_season = data.groupby('season_label')['registered'].sum() # Hitung total pengguna registered per musim
total_registered_2012 = total_registered_per_season.sum()   # Hitung total keseluruhan pengguna registered di tahun 2012
percentage_registered = (total_registered_per_season / total_registered_2012) * 100  # Hitung persentase pengguna registered per musim

fig2, ax2 = plt.subplots()
sns.barplot(
    x=percentage_registered.index,
    y=percentage_registered.values,
    palette='Blues',
    ax=ax2
)
ax2.set_title("Percentage of Registered User on Bike Sharing System Across Season")
ax2.set_xlabel("Season")
ax2.set_ylabel("Percentage (%)")
st.pyplot(fig2)

# Visualisasi Line Chart dengan Slider
hour_range = st.slider("Select hour range:",9,17,(9, 17))
filtered_data = data[
    (data['yr'] == 1) &  # Tahun 2012
    (data['hr'] >= hour_range[0]) &
    (data['hr'] <= hour_range[1]) &
    (data['weekday'] < 5)  # Weekdays
]

fig3, ax3 = plt.subplots()
fig3, ax3 = plt.subplots()
sns.lineplot(data=filtered_data, x='hr', y='registered', marker='o', ax=ax3)

ax3.set_title("Bike Rental Demand during Rush Hour (9 AM - 5 PM) on Weekday (2012 Only)")
ax3.set_xlabel("Hour")
ax3.set_ylabel("Number of Registered Users")
st.pyplot(fig3)