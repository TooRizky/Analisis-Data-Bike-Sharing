import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
sns.set(style='dark')



# Membuat fungsi untuk mengambil data total count rentalbikes per jam
def get_total_count_by_hour(bikeHour_df):
  bikeHour_count_df =  bikeHour_df.groupby(by="hours").agg({"count_rentalbikes": ["sum"]})
  return bikeHour_count_df

# Membuat fungsi untuk mengambil data total count rentalbikes per hari
def count_by_day(bikeDay_df):
    bikeDay_df_count= bikeDay_df.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return bikeDay_df_count

# Membuat fungsi untuk mengambil data total penyewa yang telah registered
def total_registered(bikeDay_df):
   reg_df =  bikeDay_df.groupby(by="date").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df
# Membuat fungsi untuk mengambil data total penyewa yang casual
def total_casual(bikeDay_df):
   cas_df =  bikeDay_df.groupby(by="date").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

# Read data
bikeDay_df = pd.read_csv("dashboard/bikeDay_Cleaned.csv")
bikeHour_df = pd.read_csv("dashboard/bikeHour_Cleaned.csv")

datetime_columns = ["date"]
bikeDay_df.sort_values(by="date", inplace=True)
bikeDay_df.reset_index(inplace=True)   

bikeHour_df.sort_values(by="date", inplace=True)
bikeHour_df.reset_index(inplace=True)

for column in datetime_columns:
    bikeDay_df[column] = pd.to_datetime(bikeDay_df[column])
    bikeHour_df[column] = pd.to_datetime(bikeHour_df[column])

min_date_days = bikeDay_df["date"].min()
max_date_days = bikeDay_df["date"].max()

min_date_hour = bikeHour_df["date"].min()
max_date_hour = bikeHour_df["date"].max()


#Melengkapi Dashboard

# TITLE DASHBOARD
st.title("Bike Sharing Dashboard :bike:")

## Sidebar
st.sidebar.title("Bike Sharing Dashboard :bike:")
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://hackaday.com/wp-content/uploads/2018/08/indego_featured.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = bikeDay_df[(bikeDay_df["date"] >= str(start_date)) & 
                       (bikeDay_df["date"] <= str(end_date))]

main_df_hour = bikeHour_df[(bikeHour_df["date"] >= str(start_date)) & 
                        (bikeHour_df["date"] <= str(end_date))]


hour_count_df = get_total_count_by_hour(main_df_hour)
day_df_count = count_by_day(main_df_days)
reg_df = total_registered(main_df_days)
cas_df = total_casual(main_df_days)

st.sidebar.title("Information:")
st.sidebar.markdown("**• Judul: Proyek Akhir Analisis Data Python**")

st.sidebar.markdown("**• Nama: Luciano Rizky Pratama**")
st.sidebar.markdown(
    "**• Email: lulupratama60@gmail.com**")
st.sidebar.markdown(
    "**• Dicoding: toorizky**")
st.sidebar.markdown(
    "**• Bangkit Study Group: ML-29**")
## Subheader
st.subheader('Daily Sharing :date:')
## Membuat 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count.count_rentalbikes.sum()
    st.metric("Total Sharing Bike", value=total_orders)
with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)


###################### Jumlah penyewaan sepeda tiap bulan di tahun 2011 ######################
st.subheader("Jumlah Penyewaan Sepeda di Tahun 2011")

# Mengurutkan bulan
months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
bikeDay_df["month"] = pd.Categorical(bikeDay_df["month"], categories=months_order, ordered=True)

# Filter data tahun 2011
filtered_data_2011 = bikeDay_df[bikeDay_df["year"] == 2011]


monthly_rentals_2011 = filtered_data_2011.groupby("month")["count_rentalbikes"].sum().reset_index()

# Mencari bulan dengan penyewaan sepeda terbanyak dan terendah
max_rental_month = monthly_rentals_2011[monthly_rentals_2011['count_rentalbikes'] == monthly_rentals_2011['count_rentalbikes'].max()]
min_rental_month = monthly_rentals_2011[monthly_rentals_2011['count_rentalbikes'] == monthly_rentals_2011['count_rentalbikes'].min()]

# Mengambil nilai bulan dan jumlah penyewaan sepeda terbanyak dan terendah
max_month_value = max_rental_month.iloc[0]["month"]
max_rentals_value = max_rental_month.iloc[0]["count_rentalbikes"]
min_month_value = min_rental_month.iloc[0]["month"]
min_rentals_value = min_rental_month.iloc[0]["count_rentalbikes"]

# Membuat bar chart untuk menampilkan penyewaan sepeda per bulan di tahun 2011
st.bar_chart(monthly_rentals_2011.set_index("month"))

st.write("Penyewaan sepeda terbanyak di tahun 2011 berada di bulan:", max_month_value, ", dengan jumlah:", max_rentals_value, "penyewa.")
st.write("Penyewaan sepeda terendah di tahun 2011 berada di bulan:", min_month_value, ", dengan jumlah:", min_rentals_value, "penyewa.")

################################################################################################

###################### Jumlah perbandingan penyewaan sepeda 2011 vs 2012 ######################

st.subheader('Penyewaan Sepeda 2011 vs 2012')

# Mengelompokkan data berdasarkan tahun dan menghitung jumlah penyewaan registered dan casual untuk setiap tahun
rentals_by_year = bikeDay_df.groupby("year").agg({
    "registered": "sum",
    "casual": "sum"
})
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot pie chart for 2011
ax[0].pie(rentals_by_year.loc[2011], labels=rentals_by_year.columns, autopct='%1.1f%%', startangle=140)
ax[0].set_title('Penyewaan Sepeda 2011\nRegistered vs Casual')

# Plot pie chart for 2012
ax[1].pie(rentals_by_year.loc[2012], labels=rentals_by_year.columns, autopct='%1.1f%%', startangle=140)
ax[1].set_title('Penyewaan Sepeda 2012\nRegistered vs Casual')

st.pyplot(fig)

st.write("Dari gambar diatas dapat dilihat pada tahun 2011 penyewaan sepeda untuk kategori registered berjumlah 80.1% dan casual berjumlah 19.9% sedangkan pada tahun 2012 mengalami kenaikan untuk kategori registered yaitu 81.8% dan penurunan untuk kategori casual yaitu 18.2%")

################################################################################################


###################### Wind Speed vs Jumlah Penyewa Registered ######################
st.subheader('Hubungan Wind Speed vs Jumlah Penyewa Registered')

fig = px.scatter(bikeDay_df, x="wind_speed", y="registered")
fig.update_xaxes(title="Wind Speed")
fig.update_yaxes(title="Jumlah Penyewa Registered")

st.plotly_chart(fig)
st.write("Disini kita menggunakan scatter plot untuk mengetahui korelasi antara wind speed dengan jumlah penyewa registered, dari hasil scatter plot diatas diperoleh informasi bahwa semakin kencang wind speed/mendekati 1 maka semakin sedikit jumlah penyewa registered, dan berlaku sebaliknya.")

################################################################################################