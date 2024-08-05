import streamlit as st
import pandas as pd
import os
import warnings 
warnings.filterwarnings('ignore')

st.set_page_config(page_title='KINEYS dashboard', page_icon=':bar_chart:',layout='wide')

st.title(':bar_chart: KINESYS Results')
# st.markdown('<style>div.block-container{padding-top:1rem;}<style>',unsafe_allow_html=True)

col1, col2 = st.columns((2))

start_date = '2024-05-28'
end_date = '2024-06-14'
date_series = pd.date_range(start=start_date, end=end_date,freq='D')

ref_date = date_series.min()
scen_date = date_series.max()

with col1:
    date_ref = pd.to_datetime(st.date_input('Reference date', ref_date))
    date_ref_ddmm = date_ref.strftime('%d%m')

with col2:
    date_scen = pd.to_datetime(st.date_input('scenario date', scen_date))
    date_scen_ddmm = date_scen.strftime('%d%m')

def scenario_param(date_ref, date_scen):
    date_list = [date_ref, date_scen]
    run_name_ref = f'nze~0004_{date_list[0]}'
    run_name_scen = f'nze~0004_{date_list[1]}'
    folder_path = '/Attribute CSV/'
    file_path_ref = folder_path + run_name_ref + '/'
    file_path_scen = folder_path + run_name_scen + '/'
    output_folder = 'G:/Departement_ R141/Modelisation TIMES/KINESYS output/Figures/' + run_name_scen + '/'
    os.makedirs(output_folder, exist_ok=True)
    return run_name_ref, run_name_scen, file_path_ref, file_path_scen, output_folder

run_name_ref, run_name_scen, file_path_ref, file_path_scen, output_folder = scenario_param(date_ref_ddmm,date_scen_ddmm)

import nbformat
from nbconvert import PythonExporter

import glob
import importlib.util
import requests
import nbconvert

# folder_path = r'C:\Users\trouvebe\Desktop\Thesis\Chapter 1\Python functions\Kinesys post-processing\Analysis'

# def convert_notebook_to_script(notebook_path, script_path):
#     """Convert Jupyter notebook to Python script."""
#     with open(notebook_path, 'r', encoding='utf-8') as f:
#         notebook_content = nbformat.read(f, as_version=4)
#     exporter = PythonExporter()
#     script, _ = exporter.from_notebook_node(notebook_content)
#     with open(script_path, 'w', encoding='utf-8') as f:
#         f.write(script)

# def import_functions_from_script(script_path):
#     """Import functions starting with 'func_' from a Python script."""
#     module_name = os.path.splitext(os.path.basename(script_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, script_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)

#     functions = {}
#     for name in dir(module):
#         if name.startswith("func_"):
#             func = getattr(module, name)
#             if callable(func):
#                 functions[name] = func
#     return functions


notebook_urls = ['https://raw.githubusercontent.com/BenjaminTrouve/Kinesys-output-app/main/Analysis/H2_new_capacity_Kinesys.ipynb']

def download_notebook(url, notebook_path):
    """Download the notebook from GitHub and save it locally."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
    else:
        raise Exception(f"Failed to download notebook: {response.status_code}")

def convert_notebook_to_script(notebook_path, script_path):
    """Convert Jupyter notebook to Python script."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)
    exporter = nbconvert.PythonExporter()
    script, _ = exporter.from_notebook_node(notebook_content)
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)

def import_functions_from_script(script_path):
    """Import functions starting with 'func_' from a Python script."""
    module_name = os.path.splitext(os.path.basename(script_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    functions = {}
    for name in dir(module):
        if name.startswith("func_"):
            func = getattr(module, name)
            if callable(func):
                functions[name] = func
    return functions

def aggregate_functions_from_notebooks(notebook_urls):
    """Download, convert, and aggregate functions from multiple notebooks."""
    all_functions = {}
    
    for i, url in enumerate(notebook_urls):
        notebook_path = f'notebook_{i}.ipynb'
        script_path = f'notebook_{i}.py'
        
        # Download, convert, and import functions
        download_notebook(url, notebook_path)
        convert_notebook_to_script(notebook_path, script_path)
        functions = import_functions_from_script(script_path)
        
        # Aggregate functions into the dictionary
        all_functions.update(functions)
    
    return all_functions

all_functions = aggregate_functions_from_notebooks(notebook_urls)



# Process all .ipynb files in the folder
# ipynb_files = glob.glob(os.path.join(folder_path, '*.ipynb'))
# ipynb_file_names = [os.path.basename(file) for file in ipynb_files]

# all_functions = {}
# for filename in ipynb_file_names:
#     notebook_path = os.path.join(folder_path, filename)
#     script_path = os.path.join(folder_path, filename.replace(".ipynb", ".py"))
#     convert_notebook_to_script(notebook_path, script_path)
#     functions = import_functions_from_script(script_path)
#     all_functions.update(functions)


def process_string_list(input_list):
    processed_list = []
    for input_string in input_list:
        substrings = input_string.split('_')
        filtered_substrings = [s for s in substrings if "func" not in s]
        result_string = ' '.join(filtered_substrings)
        processed_list.append(result_string)
    return processed_list


# keys_as_strings = [str(key) for key in all_functions.keys() if key.startswith('func_')]
# keys_string = ' '.join(keys_as_strings)


st.sidebar.header('Figure selection')
function_choice = st.sidebar.multiselect('Choose function:', process_string_list(all_functions.keys()))

def inverse_process_string_list(input_list):
    processed_list = []
    for input_string in input_list:
        # Prepend 'func_' to the entire string
        reconstructed_string = 'func_' + '_'.join(input_string.split())
        processed_list.append(reconstructed_string)
    return processed_list

function_choice_list = inverse_process_string_list(function_choice)

if function_choice:
    func = all_functions[function_choice_list[0]]
    # st.set_option('deprecation.showPyplotGlobalUse', False) 
    # figure_func = function_choice[0]
    fig = func(file_path_scen,file_path_ref, run_name_scen,run_name_ref,output_folder)
    st.pyplot(fig)






# notebook_path = r'C:\Users\trouvebe\Desktop\Thesis\Chapter 1\Python functions\Kinesys post-processing\Analysis\H2_new_capacity_Kinesys.ipynb'



# os.makedirs(output_folder, exist_ok=True)


