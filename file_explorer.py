# -------------------- IMPORTS --------------------
# os: For file system operations like create, delete, check directory
# pathlib: For handling paths in a cross-platform way
# streamlit: For building the web-based UI
import os
from pathlib import Path
import streamlit as st

# -------------------- PAGE CONFIGURATION --------------------
# Set up Streamlit page with a title and full-width layout
st.set_page_config(page_title="📁 File Explorer", layout="wide")

# Display the title using HTML for better styling
st.markdown("<h1 style='text-align: center;'>🗂️ Advanced File Explorer</h1><br>", unsafe_allow_html=True)

# -------------------- HELPER FUNCTIONS --------------------

# Function to format file sizes into KB, MB, GB for readability
def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"  # Return human-readable format
        bytes /= 1024
    return f"{bytes:.2f} TB"  # If file is very large

# Function to list files and folders in the provided directory
def list_directory(path):
    files = []
    try:
        # Iterate over all items in the directory
        for item in os.scandir(path):
            files.append({
                "Name": item.name,  # File or folder name
                "Type": "📁 Folder" if item.is_dir() else "📄 File",  # Type icon
                "Size": "-" if item.is_dir() else format_size(item.stat().st_size),  # Size if file
                "Path": item.path  # Full path
            })
        return files
    except Exception as e:
        # Show error message if something goes wrong
        st.error(f"❌ Error: {e}")
        return []

# -------------------- SIDEBAR CONFIG --------------------

# Sidebar title
st.sidebar.markdown("### 🔧 Select Operation")

# Sidebar radio button to choose the operation
operation = st.sidebar.radio("Choose an action:", [
    "📁 Browse Directory", 
    "📄 Create File", 
    "✏️ Edit File", 
    "🗑️ Delete File"
])

# Sidebar input for setting the working directory (default = home folder)
working_dir = st.sidebar.text_input("🗂️ Working Directory:", value=str(Path.home()))

# -------------------- OPERATION: BROWSE DIRECTORY --------------------

if operation == "📁 Browse Directory":
    # Show the current directory being browsed
    st.markdown(f"### 📂 Browsing: `{working_dir}`")
    
    # Check if it's a valid directory
    if os.path.isdir(working_dir):
        files = list_directory(working_dir)  # Get files/folders

        if files:
            st.markdown("#### Contents:")
            st.table(files)  # Display files in a table
        else:
            st.info("📭 Directory is empty.")  # Show if folder is empty
    else:
        st.error("❌ Invalid directory.")  # Show error if path is invalid

# -------------------- OPERATION: CREATE FILE --------------------

elif operation == "📄 Create File":
    st.markdown("### 📄 Create New File")

    # Input for directory and file name
    target_dir = st.text_input("Enter directory where file will be created:", value=working_dir)
    filename = st.text_input("Enter file name (e.g., `notes.txt`):")
    content = st.text_area("Enter content to write into file:")

    # Button to create file
    if st.button("✅ Create File"):
        try:
            os.makedirs(target_dir, exist_ok=True)  # Create folder if it doesn’t exist
            full_path = os.path.join(target_dir, filename)

            # Write the content to the new file
            with open(full_path, 'w') as f:
                f.write(content)

            st.success(f"✅ File created successfully at: `{full_path}`")
        except Exception as e:
            st.error(f"❌ Failed to create file: {e}")

# -------------------- OPERATION: EDIT FILE --------------------

elif operation == "✏️ Edit File":
    st.markdown("### ✏️ Edit Existing File")

    # Input for file to edit
    file_to_edit = st.text_input("Enter full path of file to edit:")

    # If the file exists
    if file_to_edit and os.path.isfile(file_to_edit):
        with open(file_to_edit, 'r') as f:
            current_content = f.read()  # Read current content

        # Text area to edit the content
        new_content = st.text_area("Edit file content:", value=current_content, height=300)

        # Button to save the edited content
        if st.button("💾 Save Changes"):
            try:
                with open(file_to_edit, 'w') as f:
                    f.write(new_content)  # Write updated content
                st.success(f"✅ Changes saved to `{file_to_edit}`")
            except Exception as e:
                st.error(f"❌ Failed to edit file: {e}")

    # If user enters a path but file not found
    elif file_to_edit:
        st.warning("⚠️ File not found or invalid path.")

# -------------------- OPERATION: DELETE FILE --------------------

elif operation == "🗑️ Delete File":
    st.markdown("### 🗑️ Delete File")

    # Input for file to delete
    file_to_delete = st.text_input("Enter full path of file to delete:")

    # Button to delete the file
    if st.button("🗑️ Delete"):
        try:
            os.remove(file_to_delete)  # Remove the file
            st.success(f"🗑️ File deleted: `{file_to_delete}`")
        except Exception as e:
            st.error(f"❌ Error deleting file: {e}")

# -------------------- CUSTOM STYLING --------------------

# Add some CSS for better visuals (buttons, inputs, layout)
st.markdown("""
<style>
    .block-container {
        padding: 2rem 2rem 2rem 2rem;
    }
    .stTextInput>div>input {
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #0073e6;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
    }
    .stTable {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)
