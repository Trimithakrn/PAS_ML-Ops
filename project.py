# importing libraries
import warnings
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import matplotlib.pyplot as plt
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import folium_static
import streamlit as st
warnings.filterwarnings('ignore')

data = pd.read_csv("Produktivitas Pangan.csv")

# Add title and subtitle to the main interface of the app
st.title("Fuzzy Time Series Dengan Dengan Menggunakan Dataset Produksi Pangan di Kabupaten Bondowoso Pada Tahun 2018")
st.markdown("Ketersediaan produk pangan merupakan faktor krusial dalam memastikan kecukupan dan keberlanjutan pasokan pangan di suatu daerah. Kabupaten Bondowoso adalah salah satu daerah di Indonesia yang memiliki potensi pertanian dan perikanan yang cukup besar. Untuk menjaga ketersediaan pangan yang optimal, penting untuk memiliki pemahaman yang baik tentang pola dan tren ketersediaan produk pangan di daerah tersebut.Dalam era modern, teknik-teknik analisis data dan prediksi semakin penting untuk membantu pengambilan keputusan yang lebih baik dalam berbagai bidang. Salah satu teknik yang telah terbukti efektif dalam menganalisis data deret waktu adalah fuzzy time series. Fuzzy time series merupakan metode prediksi yang menggabungkan konsep fuzzy logic dengan analisis deret waktu. Metode ini dapat memberikan hasil prediksi yang lebih akurat dan dapat membantu dalam pengambilan keputusan yang berkaitan dengan ketersediaan produk pangan di Kabupaten Bondowoso.")

# Add sidebar to the app
st.sidebar.title("Daftar Isi")
st.sidebar.markdown(
    "Welcome to my first awesome app. This app is built using Streamlit and uses data source from BPS. I hope you enjoy! For Link Dataset : https://bondowosokab.bps.go.id/statictable/2019/12/16/315/data-ketersediaan-produk-pangan-di-kabupaten-bondowoso-2018-.html")
nav_selection = st.sidebar.radio(
    'Select', ('Home', 'Single Factor Fuzzy Time Series', 'Multi Factor Fuzzy Time Series'))

if nav_selection == 'Home':
    # Display the data
    st.write("Data Produksi Pangan")
    st.write(data)


# Define the function for calculating Fuzzy Time Series with a single factor


def single_factor_fts(data, factor):
    predicted = []
    for i in range(1, len(data[factor])):
        previous = data[factor][i - 1]
        current = data[factor][i]
        predicted.append((previous + current) / 2)
    return predicted

# Define the function for calculating MAE


def calculate_mae(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    return np.mean(np.abs(actual - predicted))


# Run the single_factor_fts function
factor = 'Jumlah Konsumsi'
predicted_single_factor = single_factor_fts(data, factor)

#  Fungsi untuk menghitung MAE


def calculate_mae(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    return np.mean(np.abs(actual - predicted))


# Menghapus entri pertama karena tidak ada prediksi
komoditi = data['Komoditi    '][1:]
jumlah_konsumsi = data['Jumlah Konsumsi'][1:]

# Run the single_factor_fts function
predicted_single_factor = single_factor_fts(data, 'Jumlah Konsumsi')

# Calculate the MAE
mae_single_factor = calculate_mae(
    data['Ketersediaan'][1:], predicted_single_factor)


if nav_selection == 'Single Factor Fuzzy Time Series':
    # Create an interactive plot using plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=komoditi, y=jumlah_konsumsi,
                             name='Tingkat Jumlah Konsumsi Aktual'))
    fig.add_trace(go.Scatter(x=komoditi, y=predicted_single_factor,
                             name='Tingkat Jumlah Konsumsi Prediksi (Single Factor FTS)'))

    fig.update_layout(
        title='Prediksi Tingkat Jumlah Konsumsi Pangan dengan Single Factor FTS',
        xaxis=dict(title='Komoditi'),
        yaxis=dict(title='Tingkat Jumlah Konsumsi'),
        height=500,  # Set the height of the plot
        width=800
    )

    # Display the data
    st.write("Data Produksi Pangan")
    st.write(data)

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    # Display the MAE
    st.write("MAE Single Factor FTS Konsumsi Pangan:", mae_single_factor)


if nav_selection == 'Multi Factor Fuzzy Time Series':
    # Display the data
    st.write("Data Produksi Pangan")
    st.write(data)
    factors = ['Produksi', 'Ketersediaan ', 'Jumlah Penduduk']
    # Fungsi untuk menghitung Fuzzy Time Series dengan multifactor

    def multifactor_fts(data, factors):
        predicted_multifactor = []
        for i in range(1, len(data[factors[0]])):
            previous = data['Jumlah Konsumsi'][i - 1]
            current = data['Jumlah Konsumsi'][i]
            predicted_multifactor.append((previous + current) / 2)
        return predicted_multifactor

    # Run the multifactor_fts function
    predicted_multifactor = multifactor_fts(data, factors)

    # Calculate the MAE
    mae_multifactor = calculate_mae(
        data['Jumlah Konsumsi'][1:], predicted_multifactor)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=komoditi, y=jumlah_konsumsi,
                             name='Tingkat Jumlah Konsumsi Aktual'))
    fig.add_trace(go.Scatter(x=komoditi, y=predicted_multifactor,
                             name='Tingkat Jumlah Konsumsi Prediksi (Multi Factor FTS)'))

    fig.update_layout(
        title='Prediksi Tingkat Jumlah Konsumsi Pangan dengan Multi Factor FTS',
        xaxis=dict(title='Komoditi'),
        yaxis=dict(title='Tingkat Jumlah Konsumsi'),
        height=500,  # Set the height of the plot
        width=800
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    # Display the MAE
    st.write("MAE Multifactor FTS:", mae_multifactor)
