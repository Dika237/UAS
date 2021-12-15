from logging import PlaceHolder
import pandas as pd
import plotly.express as px
import streamlit as st
import json

# Membaca isi file
data = pd.read_csv("produksi_minyak_mentah.csv")
with open('kode_negara_lengkap.json') as countrydata:
    ctry = json.load(countrydata)
    countrydata.close()
    dict = []
    for i in ctry:
        name = i.get('name')
        alpha3 = i.get('alpha-3')
        code = i.get('country-code')
        region = i.get('region')
        subregion = i.get('sub-region')
        dict.append([name, alpha3, code, region, subregion])


# Membuat konfigurasi website
st.set_page_config(page_title="Data Global Produksi Minyak Mentah", page_icon="floppy_disk",layout="wide")

# Membuat main page
st.markdown("<h1 style='text-align: center; color: black;'>Data Global Produksi Minyak Mentah</h1>", unsafe_allow_html=True)

# Membagi halaman menjadi 2 kolom
colinfo, colgraph = st.columns(2)

# Fungsi mencari kode negara
def kode(j, dictionary) :
    for i in dictionary :
        if j == i[1] :
            jname = str(i[0])
            jcode = ("Kode Negara : " + i[2])
            jreg = ("Region : " + i[3])
            jsubreg = ("Subregion : " + i[4])
            break
        else :
            jname = ""
            jcode = ""
            jreg = ""
            jsubreg = ""
    
    return jname, jcode, jreg, jsubreg

# Kolom informasi (Soal D)
with colinfo :
    st.header(":page_facing_up: Informasi")

    # Soal keseluruhan tahun
    st.subheader("Keseluruhan Tahun")
    ## Terbesar
    st.info('Jumlah Produksi Terbesar Keseluruhan Tahun')
    df1 = data.sort_values(by='produksi')
    maxall = df1.nlargest(1, 'produksi')
    jmax = maxall.iloc[0, 0]
    jprod = str(maxall.iloc[0,2])
    maxname,maxcode,maxreg,maxsubreg = kode(jmax, dict)
    st.write("###### Jumlah Produksi : " + jprod)
    st.write(maxname)
    st.write(maxcode)
    st.write(maxreg)
    st.write(maxsubreg)
    ## Terkecil
    st.warning('Jumlah Produksi Terkecil Keseluruhan Tahun')
    dffilt = df1[df1['produksi'] != 0]
    minall = dffilt.nsmallest(1, 'produksi')
    jmin = minall.iloc[0, 0]
    jprod = str(minall.iloc[0,2])
    minname,mincode,minreg,minsubreg = kode(jmin, dict)
    st.write("###### Jumlah Produksi : " + jprod)
    st.write(minname)
    st.write(mincode)
    st.write(minreg)
    st.write(minsubreg)
    ## = 0
    st.success('Jumlah Produksi = 0 Keseluruhan Tahun')
    zerofilt = df1[df1['produksi'] == 0]
    zerocode = zerofilt['kode_negara'].tolist()
    listzero = []
    for j in zerocode :
        for i in dict :
            if i[1] == j:
                listzero.append([i[0], i[2], i[3], i[4]])
                break
    dfzero = pd.DataFrame(listzero, columns=['Nama', 'Kode Negara', 'Region', 'Subregion'])
    dfzero = dfzero.drop_duplicates(subset=['Nama'])
    blankIndex=[''] * len(dfzero)
    dfzero.index=blankIndex
    with st.expander("Lihat Tabel"):
        st.dataframe(dfzero)

    st.write("")
    
    # Soal per tahun
    st.subheader("Per Tahun")
    T = st.number_input("Tahun :", int(data.min(axis=0)['tahun']), int(data.max(axis=0)['tahun']))
    yeardata = data.query('tahun == @T')

    ## Terbesar
    st.info("Jumlah Produksi Terbesar pada Tahun {namatahun}".format(namatahun = T))
    with st.expander("Lihat Informasi"):
        maxyeardata = yeardata.nlargest(1, 'produksi')
        jmax = maxyeardata.iloc[0, 0]
        jprod = str(maxyeardata.iloc[0,2])
        maxname,maxcode,maxreg,maxsubreg = kode(jmax, dict)
        st.write("###### Jumlah Produksi : " + jprod)
        st.write(maxname)
        st.write(maxcode)
        st.write(maxreg)
        st.write(maxsubreg)

    ## Terkecil
    st.warning("Jumlah Produksi Terkecil pada Tahun {namatahun}".format(namatahun = T))
    with st.expander("Lihat Informasi"):
        yeardatafilt = yeardata[yeardata['produksi'] != 0]
        minyeardata = yeardatafilt.nsmallest(1, 'produksi')
        jmin = minyeardata.iloc[0, 0]
        jprod = str(minyeardata.iloc[0,2])
        minname,mincode,minreg,minsubreg = kode(jmin, dict)
        st.write("###### Jumlah Produksi : " + jprod)
        st.write(minname)
        st.write(mincode)
        st.write(minreg)
        st.write(minsubreg)

    ## = 0
    st.success("Jumlah Produksi = 0 pada Tahun {namatahun}".format(namatahun = T))
    with st.expander("Lihat Tabel"):
        zerofilter = yeardata[yeardata['produksi'] == 0]
        zerocodeb = zerofilter['kode_negara'].tolist()
        listzeroyeardata = []
        for j in zerocodeb :
            for i in dict :
                if i[1] == j:
                    listzeroyeardata.append([i[0], i[2], i[3], i[4]])
                    break
        dfzeroyd = pd.DataFrame(listzeroyeardata, columns=['Nama', 'Kode Negara', 'Region', 'Subregion'])
        dfzeroyd = dfzeroyd.drop_duplicates(subset=['Nama'])
        blankIndex=[''] * len(dfzeroyd)
        dfzeroyd.index=blankIndex
        st.dataframe(dfzeroyd)

# Kolom grafik (Soal A, B, C)
with colgraph :
    st.header(":bar_chart: Grafik")

    # Opsi grafik
    opt = ["Bar", "Line", "Scatter"]

    # Soal A
    st.markdown("#### Grafik Produksi Minyak Mentah Suatu Negara")
    country = st.selectbox("Negara : ", options=(i[0] for i in dict), key="soala")
    charttype = st.selectbox("Tipe Grafik : ", options=opt, key="soalaa")
    for i in dict:
            if i[0] == country :
                code = i[1]
    if not((data['kode_negara'] == code).any()) :
        st.error("Tidak ada data produksi minyak mentah " + country)
    else :
        with st.expander("Lihat Grafik"):
            soala_selection = data.loc[data["kode_negara"] == code]
            if charttype == "Bar":
                barchart = px.bar(soala_selection, x = "tahun", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title='Grafik Produksi Minyak Mentah {negara}'.format(negara=country), template="seaborn")
                st.plotly_chart(barchart, use_container_width=True)
            elif charttype == "Scatter" :
                scatterchart = px.scatter(soala_selection, x = "tahun", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title='Grafik Produksi Minyak Mentah {negara}'.format(negara=country), template="seaborn")
                st.plotly_chart(scatterchart, use_container_width=True)
            else :
                linechart = px.line(soala_selection, x = "tahun", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title='Grafik Produksi Minyak Mentah {negara}'.format(negara=country), template="seaborn")
                st.plotly_chart(linechart, use_container_width=True)

    # Soal B
    st.markdown("#### Grafik B-Buah Negara dengan Jumlah Produksi Terbesar per Tahun")
    year = st.number_input("Tahun : ", int(data.min(axis=0)['tahun']), int(data.max(axis=0)['tahun']), key="soalb")
    ydata = data.query('tahun == @year')
    b = (st.slider('Jumlah Negara Terbesar : ', 1, ydata['kode_negara'].nunique(), key="soalbb"))
    cydata = ydata.nlargest(int(b), 'produksi')
    charttypeb = st.selectbox("Tipe Grafik : ", options=opt, key="soalbbb")
    judul = "Grafik {jumlah} Buah Negara dengan Jumlah Produksi Terbesar pada Tahun {tahunnya}".format(jumlah = b, tahunnya = year)
    with st.expander("Lihat Grafik"):
        if charttypeb == "Bar":
            barchartb = px.bar(cydata, x = "kode_negara", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title=judul, template="seaborn")
            st.plotly_chart(barchartb, use_container_width=True)
        elif charttypeb == "Scatter" :
            scatterchartb = px.scatter(cydata, x = "kode_negara", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title=judul, template="seaborn")
            st.plotly_chart(scatterchartb, use_container_width=True)
        else :
            linechartb = px.line(cydata, x = "kode_negara", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title=judul, template="seaborn")
            st.plotly_chart(linechartb, use_container_width=True)

    # Soal C
    # Membuat Tabel Akumulatif
    temp = data['kode_negara'].ne(data['kode_negara'].shift()).cumsum()
    data['kumulatif'] = data.groupby(temp)['produksi'].cumsum()
    cumdata = data[['kode_negara', 'produksi', 'kumulatif']]
    cumdata = cumdata.sort_values('kumulatif', ascending=False).drop_duplicates(subset=['kode_negara'])
    
    st.markdown("#### Grafik B-Buah Negara dengan Jumlah Produksi Kumulatif Terbesar")
    c = int(st.slider('Jumlah Negara Terbesar : ', 1, cumdata['kode_negara'].nunique(), key="soalc"))
    cdata = cumdata.nlargest(c, 'kumulatif')
    charttypec = st.selectbox("Tipe Grafik : ", options=opt, key="soalcc")
    with st.expander("Lihat Grafik"):
        if charttypec == "Bar":
            barchartc = px.bar(cdata, x = "kode_negara", y = "kumulatif", labels={'kumulatif' : 'Jumlah Kumulatif', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, title="Grafik {jumlahngr} Buah Negara dengan Jumlah Kumulatif Produksi Terbesar".format(jumlahngr = c), template="seaborn")
            st.plotly_chart(barchartc, use_container_width=True)
        elif charttypec == "Scatter" :
            scatterchartc = px.scatter(cdata, x = "kode_negara", y = "kumulatif", labels={'kumulatif' : 'Jumlah Kumulatif', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, title="Grafik {jumlahngr} Buah Negara dengan Jumlah Kumulatif Produksi Terbesar".format(jumlahngr = c), template="seaborn")
            st.plotly_chart(scatterchartc, use_container_width=True)
        else :
            linechartc = px.line(cdata, x = "kode_negara", y = "kumulatif", labels={'kumulatif' : 'Jumlah Kumulatif', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, title="Grafik {jumlahngr} Buah Negara dengan Jumlah Kumulatif Produksi Terbesar".format(jumlahngr = c), template="seaborn")
            st.plotly_chart(linechartc, use_container_width=True)
