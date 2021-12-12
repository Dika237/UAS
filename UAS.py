import streamlit as st
import pandas as pd
import json

# INISIALISASI JSON FILE
df = pd.read_csv("produksi_minyak_mentah.csv")
f = open('kode_negara_lengkap.json')
jsondf = json.load(f)
f.close()
countries = []
for i in jsondf:
    name = i.get('name')
    alpha3 = i.get('alpha-3')
    code = i.get('country-code')
    region = i.get('region')
    subregion = i.get('sub-region')
    countries.append([name, alpha3, code, region, subregion])

# INISIALISASI KUMULATIF DATAFRAM
s = df['kode_negara'].ne(df['kode_negara'].shift()).cumsum()
df['cumulative'] = df.groupby(s)['produksi'].cumsum()
df3 = df[['kode_negara', 'produksi', 'cumulative']]
df3 = df3.sort_values('cumulative').drop_duplicates('kode_negara', keep='last')
batasbawahtahun = int(df.min(axis=0)['tahun'])
batasatastahun = int(df.max(axis=0)['tahun'])

# MAIN ALGORITHM
st.title("""Data Global Produksi Minyak Mentah\nAplikasi penyedia informasi dan grafik""")

# INFO KESELURUHAN
st.header("Informasi")
st.subheader("Jumlah Keseluruhan Tahun")
with st.container():
    col1, col2 = st.columns(2)
    # Jumlah Terbesar
    with col1:
        cekmax = df3.nlargest(1, 'cumulative')
        j = (cekmax.iloc[0]['kode_negara'])
        for i in countries:
            if j == i[1]:
                namamax = str(i[0])
                kodemax = ("[Kode Negara: " + i[2] + "]")
                regionmax = ("Region: " + i[3])
                subregionmax = ("Subregion: " + i[4])
                cummax = str(cekmax.iloc[0]['cumulative'])
                break
        st.success("Jumlah Produksi Terbesar Keseluruhan Tahun")
        st.write("tes")
        st.write(namamax, kodemax)
        st.write(regionmax)
        st.write(subregionmax)
        st.write("")
    # Jumlah Terkecil
    with col2:
        filt = df3[df3['cumulative'] != 0]
        cekmin = filt.nsmallest(1, 'cumulative')
        j = (cekmin.iloc[0]['kode_negara'])
        for i in countries:
            if j == i[1]:
                namamin = str(i[0])
                kodemin = ("[Kode Negara: " + i[2] + "]")
                regionmin = ("Region: " + i[3])
                subregionmin = ("Subregion: " + i[4])
                cummin = str(cekmin.iloc[0]['cumulative'])
                break
        st.error("Jumlah Produksi Terkecil Keseluruhan Tahun")
        st.write("tes")
        st.write(namamin, kodemin)
        st.write(regionmin)
        st.write(subregionmin)
    # Jumlah = Nol
    zero = df3[df3['cumulative'] == 0]
    j = zero['kode_negara'].tolist()
    zerolst = []
    for kodenegara in j:
        for i in countries:
            if i[1] == kodenegara:
                zerolst.append([i[0], i[2], i[3], i[4]])
                break
    zerodf = pd.DataFrame(zerolst, columns=['nama', 'kode negara', 'region', 'subregion'])
    zerodf.index = zerodf.index + 1
    st.info("Jumlah Produksi Nol Keseluruhan Tahun")
    with st.expander("Lihat Tabel"):
        st.table(zerodf)
st.write("")
st.write("")

# INFO PER TAHUN
st.subheader("Jumlah Per Tahun")
with st.container():
    tahunmaxminnol = st.slider('Tahun berapa?', batasbawahtahun, batasatastahun, key = "terbesaar")
    col3, col4 = st.columns(2)
    dftahun = df.loc[df['tahun'] == tahunmaxminnol]
    # Jumlah Terbesar
    with col3:
        cekmax = dftahun.nlargest(1, 'produksi')
        j = (cekmax.iloc[0]['kode_negara'])
        for i in countries:
            if j == i[1]:
                namamax = str(i[0])
                kodemax = ("[Kode Negara: " + i[2] + "]")
                regionmax = ("Region: " + i[3])
                subregionmax = ("Subregion: " + i[4])
                cummax = str(cekmax.iloc[0]['produksi'])
                break
        st.success("Jumlah Produksi Terbesar pada Tahun " + str(tahunmaxminnol))
        st.write("###### Produksi: " + cummax)
        st.write(namamax, kodemax)
        st.write(regionmax)
        st.write(subregionmax)
        st.write("")
    # Jumlah Terkecil
    with col4:
        filt = df[df['produksi'] != 0]
        cekmin = filt.nsmallest(1, 'produksi')
        j = (cekmin.iloc[0]['kode_negara'])
        for i in countries:
            if j == i[1]:
                namamin = str(i[0])
                kodemin = ("[Kode Negara: " + i[2] + "]")
                regionmin = ("Region: " + i[3])
                subregionmin = ("Subregion: " + i[4])
                cummin = str(cekmin.iloc[0]['produksi'])
                break
        st.error("Jumlah Produksi Terkecil pada Tahun " + str(tahunmaxminnol))
        st.write("###### Produksi: " + cummin)
        st.write(namamin, kodemin)
        st.write(regionmin)
        st.write(subregionmin)
    # Jumlah = Nol
    zero = dftahun[dftahun['produksi'] == 0]
    j = zero['kode_negara'].tolist()
    zerolst = []
    for kodenegara in j:
        for i in countries:
            if i[1] == kodenegara:
                zerolst.append([i[0], i[2], i[3], i[4]])
                break
    zerodf = pd.DataFrame(zerolst, columns=['nama', 'kode negara', 'region', 'subregion'])
    zerodf.index = zerodf.index + 1
    st.info("Jumlah Produksi Nol pada Tahun " + str(tahunmaxminnol))
    with st.expander("Lihat Tabel"):
        st.table(zerodf)
st.write("")
st.write("")

# GRAFIK
st.header("Grafik")
# Spesifikasi A
with st.expander("Grafik Jumlah Produksi Minyak Suatu Negara"):
    choice1 = st.selectbox("Pilih Negara", (i[0] for i in countries))
    for i in countries:
        if i[0] == choice1:
            code = i[1]
    if not((df['kode_negara'] == code).any()):
        st.warning("Tidak ada data produksi minyak mentah " + choice1 + ". Coba negara lain")
    else:
        df1 = df.loc[df["kode_negara"] == code]
        dfline1 = df1[["tahun", "produksi"]]
        st.write("Jumlah Produksi Minyak Mentah ", choice1, " terhadap Waktu (Tahun)")
        st.line_chart(dfline1.rename(columns={'tahun':'index'}).set_index('index'))
# Spesifikasi B
with st.expander("Grafik N-Buah Negara dengan Produksi Terbesar per Tahun"):
    tahun2 = st.slider('Tahun berapa?', batasbawahtahun, batasatastahun, key = "<func2>")
    dftahun2 = df.loc[df['tahun'] == tahun2]
    choice2 = int(st.number_input('Berapa negara terbesar?', 1, (dftahun2['kode_negara'].nunique()), key = "<number2>"))
    df2 = dftahun2.nlargest(choice2, 'produksi')
    df2 = df2[['kode_negara', 'produksi']]
    st.line_chart(df2.rename(columns={'kode_negara':'index'}).set_index('index'))
# Spesifikasi C
with st.expander("Grafik N-Buah Negara dengan Produksi Kumulatif Terbesar"):
    choice3 = int(st.number_input('Berapa negara terbesar?', 1, (df['kode_negara'].nunique()), key = "<number3>"))
    df3 = df3.nlargest(choice3, 'cumulative')
    df3 = df3[['kode_negara', 'produksi']]
    st.line_chart(df3.rename(columns={'kode_negara':'index'}).set_index('index'))
