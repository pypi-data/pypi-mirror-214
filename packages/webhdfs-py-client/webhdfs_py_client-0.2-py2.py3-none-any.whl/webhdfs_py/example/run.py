import os
from streamlit import config as _config
from streamlit.web import bootstrap

def run():
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, 'pages', "main.py")

    _config.set_option("server.headless", False)
    args = []

    bootstrap.run(file_path,'',args, flag_options={})

# if __name__ == "__main__":
#     run()