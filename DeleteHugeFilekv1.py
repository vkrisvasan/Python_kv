import os
import streamlit as st

def find_large_files(start_path='.', num_files=50):
    file_sizes = []
    for foldername, subfolders, filenames in os.walk(start_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            try:
                file_size = os.path.getsize(file_path)
                file_sizes.append((file_size, file_path))
            except:
                pass
    file_sizes.sort(reverse=True)
    return file_sizes[:num_files]

def delete_files(files_to_delete):
    for file in files_to_delete:
        try:
            os.remove(file)
            st.write(f"Deleted {file}")
        except Exception as e:
            st.write(f"Error deleting {file}: {e}")

st.title("Large Files Finder and Delete.. in 6 easy steps")

# Initialize session state variables
if 'current_path' not in st.session_state:
    st.session_state.current_path = os.path.expanduser("~")  # start from the home directory
if 'selected_files' not in st.session_state:
    st.session_state.selected_files = []
if 'large_files' not in st.session_state:
    st.session_state.large_files = []
if 'confirm_delete' not in st.session_state:
    st.session_state.confirm_delete = False

# Sidebar for directory navigation
st.sidebar.title("1st Step: Select the Directory here..")
st.sidebar.header("Directory Navigation")
st.sidebar.write(f"Current path: `{st.session_state.current_path}`")

# List directories in the current path
try:
    with st.spinner('Reading directory...'):
        directories = [d for d in os.listdir(st.session_state.current_path) if os.path.isdir(os.path.join(st.session_state.current_path, d))]
except Exception as e:
    st.sidebar.error(f"An error occurred: {e}")
    directories = []

# Directory navigation in sidebar
for directory in directories:
    if st.sidebar.button(directory):
        st.session_state.current_path = os.path.join(st.session_state.current_path, directory)

# Option to navigate back in sidebar
if st.session_state.current_path != os.path.expanduser("~"):  # or "/" for root directory
    if st.sidebar.button(".. (Go back)"):
        st.session_state.current_path = os.path.dirname(st.session_state.current_path)

# Main content for file display and management
num_files = st.slider("2nd step: Number of files to display:", min_value=10, max_value=200, value=50, step=10)

if st.button("3rd step: Find Largest Files"):
    st.session_state.large_files = find_large_files(st.session_state.current_path, num_files)

if st.session_state.large_files:
    file_options = [f"{path} ({size / (1024 * 1024):.2f} MB)" for size, path in st.session_state.large_files]
    st.session_state.selected_files = st.multiselect("4th step: Select files to delete:", file_options, default=st.session_state.selected_files)

if st.button("5th step: Delete Selected Files"):
    if st.session_state.selected_files:
        st.session_state.confirm_delete = True

if st.session_state.confirm_delete:
    if st.button("6th and final step: Are you sure you want to delete the selected files ? files cant be retrieved"):
        files_to_delete = [file.split(" (")[0] for file in st.session_state.selected_files]
        delete_files(files_to_delete)
        st.session_state.selected_files = []
        st.session_state.confirm_delete = False
    elif st.button("Cancel"):
        st.session_state.confirm_delete = False
else:
    st.warning("No files selected for deletion.")
