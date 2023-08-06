
import os

import streamlit as st
import pandas as pd
from webhdfs_py import PyWebHdfsClient
# from utils import show_code
# pw.PyWebHdfsClient

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(page_title="webhdfs_py Demo", page_icon="📊")
ss = st.session_state
hdfs = None

if not ss:
        ss.pressed_first_button = False
# st.write(ss)
with st.sidebar:
    url = st.sidebar.text_input("URL", "")
    user = st.sidebar.text_input("User", "")
    pwd = st.sidebar.text_input("password", "",type='password')
    home_path = st.sidebar.text_input("Path", f"/user/{user}/")
    
    if st.button('Conectar', key='con') or ss.pressed_first_button:
        # hdfs = "si"
        hdfs = PyWebHdfsClient(base_uri_pattern=url,
                            request_extra_opts={'verify': False,
                                'auth': (user, pwd)
                                })
        st.sidebar.success('Conectado!', icon="✅")
        ss.pressed_first_button = True

with st.container():
    if hdfs != None:
        st.write(
        """Este demo nos permite hacer uso sencillo de la 
        libreria PyWebHdfsClient [REPO](http://data.un.org/Explorer.aspx)""")
        t1, t2 , t3, t4 = st.tabs(['CREATE_FILE','LIST_DIR', 'DOWNLOAD_FILE', 'DELETE_FILE'])
        with t1:
            uploaded_file = st.file_uploader("Subir archivo de prueba", type=['csv'],key='pdf_file')
            over = st.checkbox('Realizar Overwrite', value=True)
            if st.button("Subir Archivo", key='upload'):
                # st.write(home_path)
                with st.spinner("Subiendo... "):
                    hdfs.create_file(home_path+uploaded_file.name, uploaded_file.read(), overwrite=over, permission=777)
                    st.markdown(f"se subio correctamente: **{home_path+uploaded_file.name}** ")
            
            st.divider()
            st.markdown(f"**Modo de Uso:**")
            st.code(""" hdfs = PyWebHdfsClient(host='host',port='50070', user_name='hdfs')
my_dir = 'user/hdfs'
hdfs.list_dir(my_dir)""")
            with t2:
                json_data = hdfs.list_dir(home_path)
                expander = st.expander(home_path)
                expander.write(json_data)
                st.divider()
                st.markdown(f"**Modo de Uso:**")
                st.code(""" my_data = '01010101010101010101010101010101'
    my_file = 'user/hdfs/data/myfile.txt'
    hdfs.create_file(my_file, my_data, overwrite=True, permission=777) """)

            with t3:

                data = hdfs.list_dir(home_path)

                # Filtrar los elementos donde type sea "FILE" y pathSuffix sea "csv"
                filtered_data = ['Seleccionar']
                filtered_data.extend([file["pathSuffix"] for file in data["FileStatuses"]["FileStatus"] if file["type"] == "FILE" and file["pathSuffix"].endswith(".csv")])

                option = st.selectbox(
                'Seleccionar un archivo de los encontrados',
                filtered_data)
                if option != 'Seleccionar':
                    nombre_archivo = home_path+option#os.path.basename(path)
                    # @st.cache_data 
                    # def convert_df(nombre_archivo):
                    #     # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    #     return hdfs.stream_file(nombre_archivo)
                    csv = b''
                    for file in hdfs.stream_file(nombre_archivo):
                        csv += file

                    st.download_button(
                        label="Descargar archivo CSV",
                        data=csv,
                        file_name=option,
                        mime='text/csv',
                    )
                st.divider()
                st.markdown(f"**Modo de Uso:**")
                st.code(
                    """hdfs = PyWebHdfsClient(host='host',port='50070', user_name='hdfs')
my_file = 'user/hdfs/data/myfile.txt'
csv = b''
for file in hdfs.stream_file(my_file):
    csv += file""")
            with t4:
                data = hdfs.list_dir(home_path)

                # Filtrar los elementos donde type sea "FILE" y pathSuffix sea "csv"
                filtered_data = ['Seleccionar']
                filtered_data.extend([file["pathSuffix"] for file in data["FileStatuses"]["FileStatus"] if file["type"] == "FILE" and file["pathSuffix"].endswith(".csv")])

                option = st.selectbox(
                'Seleccionar un archivo para eliminar',
                filtered_data)
                if option != 'Seleccionar':
                    nombre_archivo = home_path+option#os.path.basename(path)
                    if st.button("Eliminar Archivo", key='delete'):
                        with st.spinner("Subiendo... "):
                            hdfs.delete_file_dir(nombre_archivo)
                            st.markdown(f"Se Elimino correctamente: **{nombre_archivo}** ")
                st.divider()
                st.markdown(f"**Modo de Uso:**")
                st.code(
                    """hdfs = PyWebHdfsClient(host='host',port='50070', user_name='hdfs') 
                    my_file = 'user/hdfs/data/myfile.txt' 
                    hdfs.delete_file_dir(my_file)""")


    else:
         st.write(open(BASE_DIR /'README.py', 'r', encoding='utf-8').read())