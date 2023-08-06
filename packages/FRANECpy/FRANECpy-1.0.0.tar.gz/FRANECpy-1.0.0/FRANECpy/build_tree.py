import json
import re
import os
import pandas as pd


#Section of code for managing the files and folder paths and generating the data tree with the function gen_tree().

def extract_root_path_and_name(file_paths, folder_paths):
    """
    Extracts the common root path from the given file and folder paths.

    Args:
        file_paths (list): 
            List of file paths.
            
        folder_paths (list): 
            List of folder paths.

    Returns:
        common_path (string): 
            A string containing the common root path.
    """
    # Get the common path
    common_path = os.path.commonpath(file_paths + folder_paths)

    return common_path

def manage_RID_folders(folder_path, file_paths):
    """
    Retrieves the file paths of DAT files within a specified folder and its subfolders.
    Append it to the list of files path.
    
    Args:
        folder_path (str): 
            The path to the folder to search for RID files.
        
        file_paths (list): 
            A list to store the file paths.

    Returns:
        file_paths(list): 
            The updating list containing also the file paths of the RID files found within the folder and its subfolders.
    """

    # Retrieve the list of files within the folder path
    sub_files = os.listdir(folder_path)

    # Iterate over each file in the list
    for sub_file in sub_files:
        # Check if the file has a ".DAT" extension
        if sub_file.endswith(".DAT"):
            # Construct the full file path
            file_path = folder_path + "/" + sub_file
            # Append the file path to the file_paths list
            file_paths.append(file_path)

    # Return the updated file_paths list
    return file_paths

def manage_ISO_folders(folder_path, file_paths):
    """
    Retrieve AGE files from the ISO folder path and append their paths to the *file_paths* list.

    Args:
        folder_path (str): 
            The path to the ISO folder containing the files.
            
        file_paths (list): 
            The list to which the file paths will be appended.

    Returns:
        file_paths (list): 
            The updated file_paths list contains the paths of ISO files.
    """
    # Retrieve the list of files within the folder path
    sub_files = os.listdir(folder_path)

    # Iterate over each file in the list
    for sub_file in sub_files:
        # Check if the file has a ".DAT" extension
        if sub_file.startswith("AGE"):
            # Construct the full file path
            file_path = folder_path + "/" + sub_file
            # Append the file path to the file_paths list
            file_paths.append(file_path)

    # Return the updated file_paths list
    return file_paths    

def manage_folders(folder_paths, file_paths):
    """
    Manages the folder paths and generates a list of file paths of interest.

    The function processes the given folder paths and extracts relevant file paths based on specific conditions of formation of the data file provided by FRANEC program.

    Args:
        folder_paths (list): 
            A list of folder paths to be processed.
            
        file_paths (list): 
            A list to store the file paths of interest.

    Returns:
        file_paths (list): 
            A list containing the file paths of interest.
    """

    for folder_path in folder_paths:
        folder_name = os.path.basename(folder_path)

        # Manage the tools-driver-out folder
        if folder_name == "tools-driver-out":
            sub_folders = os.listdir(folder_path)
            for sub_folder in sub_folders:
                # Generate the path of the sub folder
                sub_folder_path = folder_path + "/" + sub_folder
                # Generate the path of the only one file of interest in that folder
                file_dat_path = sub_folder_path + "/OUT.DAT"
                file_paths.append(file_dat_path)

        # Manage the Mass folder inside the tools-driver-out folder
        elif folder_name.startswith("M"):
            file_paths.append(folder_path + "/OUT.DAT")

        # Manage the ISO folders
        elif folder_name.startswith("ISO"):
            file_paths= manage_ISO_folders(folder_path, file_paths)
            #print("\033[31mISO folders are not implemented. Excluding:", folder_name, "\033[0m")

        # Manage the RID folders
        elif folder_name.startswith("RID"):
            file_paths = manage_RID_folders(folder_path, file_paths)

        # Manage the tools-isocrone-out folder
        elif folder_name == "tools-isocrone-out":
            sub_folders = os.listdir(folder_path)
            for sub_folder in sub_folders:
                if sub_folder.startswith("RID"):
                    sub_folder_path = folder_path + "/" + sub_folder
                    file_paths = manage_RID_folders(sub_folder_path, file_paths)
                if sub_folder.startswith("ISO"):
                    sub_folder_path = folder_path + "/" + sub_folder
                    file_paths = manage_ISO_folders(sub_folder_path, file_paths)
        
        #Manage the folders that aren't tools-isocrone-out or tools-driver-out
        else:
            print("\033[33m\ The biggests folders that i can manage are tools-isocrone-out and tools-driver-out.Excluding from the tree:",folder_name,"\033[0m")

    return file_paths

##Section where the tree is built:

def build_tree_from_paths(file_paths, common_path):
    """
    Builds a hierarchical tree structure from a list of file paths.

    The function analyzes the file paths, extracts relevant information, and organizes it into a tree-like structure.

    The tree structure is organized for having at the same level the branch of "tools-driver-out" and "tools-isocrone-out", inside that
    there are sub-branches named RAW, RID and ISO.
    Inside these three branches, there are the branches of the metallicities and inside there are the pandas data frames divided by mass.
    
    Args:
        file_paths (list): 
            A list of file paths to be processed.
            
        common_path (str): 
            The common path is shared by all the file paths.

    Returns:
        tree (dict): 
            A hierarchical tree structure whit the data.
    """

    tree = {}

    # Adjust the format of the common folder path
    common_path = os.path.dirname(common_path) + "/"
    common_path = common_path.replace("\\", "/")
       
    for path in file_paths:

        # Remove the common folder path
        rel_path = path.replace(common_path, "", 1)

        components = rel_path.split("/")  # Adjust the delimiter as per your file system

        current_node = tree
        for i, component in enumerate(components):

            # Check if the component of the path is a RID folder
            if component.startswith("RID"):
                # Find and extract the metallicity value
                matches = re.match(r"RID_(Z[\d.]+_He[\d.]+_ML[\d.]+)_", component)
                
                z_he__mx = matches.group(1)

                # If the RID branch doesn't already exist, create it
                if "RID" not in current_node:
                    current_node["RID"] = {}

                # Move to the RID branch
                current_node = current_node["RID"]

                # Create the metallicity branch if it doesn't exist
                if z_he__mx not in current_node:
                    current_node[z_he__mx] = {}

                # Move to the metallicity branch
                current_node = current_node[z_he__mx]
            
            # Check if the component of the path is a ISO folder
            if component.startswith("ISO"):
                # Find and extract the metallicity value
                matches = re.match(r"ISO_(Z[\d.]+_He[\d.]+_ML[\d.]+)_", component)
                
                z_he__mx = matches.group(1)
                
                # If the ISO branch doesn't already exist, create it
                if "ISO" not in current_node:
                    current_node["ISO"] = {}

                # Move to the RID branch
                current_node = current_node["ISO"]

                # Create the metallicity branch if it doesn't exist
                if z_he__mx not in current_node:
                    current_node[z_he__mx] = {}

                # Move to the metallicity branch
                current_node = current_node[z_he__mx]
            
            # Manage the folder inside the tools/driver/out folder
            elif component.startswith("M"):
                # Create the RAW branch if it isn't already present, this is done to have the same depth for all dataframes
                if "RAW" not in current_node:
                    current_node["RAW"] = {}

                # Move to the RAW node
                current_node = current_node["RAW"]

                # Extract the value of metallicty and Helium, etc.
                matches = re.match(r"M([\d.]+)_(Z[\d.]+_He[\d.]+_ML[\d.]+)_", component)
                
                Mass_value = "M" + matches.group(1)
                z_he__mx = matches.group(2)

                # Create the metallicity branch if it doesn't exist
                if z_he__mx not in current_node:
                    current_node[z_he__mx] = {}

                # Move to the metallicity branch
                current_node = current_node[z_he__mx]

                # Create the mass branch if it doesn't exist
                if Mass_value not in current_node:
                    current_node[Mass_value] = {}

            # Load the AGE.dat as a dataframe with their specific formatting
            elif i == len(components) - 1 and component.endswith(".DAT") and component.startswith("AGE"):
                # Extract the mass value
                matches = re.match(r"(AGE[\d.]+)_", component)
                
                AGE = matches.group(1)

                # Define the variable/column names
                variable_names = ['LOG_L/Lo', 'LOG_TE_(K)', 'Mass/Mo', 'R/Ro', 'LOG g', '[Fe/H]']

                # Read the data from the file into a dataframe
                df = pd.read_csv(path, comment='#', delimiter='\s+', header=None, engine='python')

                # Assign the variable/column names to the dataframe columns
                df.columns = variable_names

                current_node[AGE] = df
                           
            # Load the RID.dat as a dataframe with their specific formatting
            elif i == len(components) - 1 and component.endswith(".DAT") and component.startswith("AOUT"):
                # Extract the mass value
                matches = re.match(r"AOUT_(M[\d.]+)_", component)
                
                Mass_value = matches.group(1)

                # Define the variable/column names
                variable_names = ['MOD', 'Time', 'LOG_L/Lo', 'LOG_TE_(K)', 'M', '[Fe/H]', 'R', 'logg', 'Dni', 'nimax']

                # Read the data from the file into a dataframe
                df = pd.read_csv(path, comment='#', delimiter='\s+', header=None, engine='python')

                # Assign the variable/column names to the dataframe columns
                df.columns = variable_names

                current_node[Mass_value] = df

            # Load the raw file.dat as a dataframe with their specific formatting
            elif i == len(components) - 1 and component.endswith(".DAT") and component.startswith("OUT"):
                # Define the variable/column names
                variable_names = ["NMOD", "LOG(T)", "H/HE", "LOG L", "LOG TE", "MASS", "L-GRA", "L-3A", "log(Fe/H)", "[Fe/H]", "R", "Logg", "Dni", "nimax", "Mix_Len"]

                # Read the data from the file into a dataframe
                df = pd.read_csv(path, comment='#', delimiter='\s+', header=None, engine='python')

                # Assign the variable/column names to the dataframe columns
                df.columns = variable_names

                # In difference from the RID file, the leaf is already created, and the program remembers the mass value from the procedure of creating the branch from the folder name.
                # So the only thing to do is to link the dataframe at the leaf address.
                current_node[Mass_value] = df

            if not component.startswith("RID") and not component.startswith("AOUT") and not component.startswith("M") and not component.startswith("OUT") and not component.startswith("ISO") and not component.startswith("AGE"):
                # Check if the component branch exists; if not, create it
                if component not in current_node:
                    current_node[component] = {}
                # Move to the branch just created
                current_node = current_node[component]

    return tree

def generate_tree(file_paths, folder_paths):
    """
    Generates a hierarchical tree structure based on file paths and folder paths.

    The function extracts the common path, manages the folder paths, and builds a tree-like structure based on the file paths.
    For doing that it uses the build_tree_from_paths function.
    
    Args:
        file_paths (list):
            A list of file paths to be processed.
            
        folder_paths (list): 
            A list of folder paths to be processed.

    Returns:
        tree (dict): 
            A hierarchical tree structure whit the data.
    """

    common_path = extract_root_path_and_name(file_paths, folder_paths)

    # Manage the folder paths and generate the file paths of interest
    file_paths = manage_folders(folder_paths, file_paths)

    # Build the tree structure from the file paths
    tree = build_tree_from_paths(file_paths, common_path)
    
    return tree

#Section for implementing the saving and loading of trees

def save_tree_with_shell(tree, folder_path):
    """
    Prompt the user to save a tree and serialize it to a file.

    This function prompts the user to save a tree by providing a file name and saves the serialized tree to a specified folder path. The tree is serialized to JSON format before saving.
    The folder path of input is the main data folder path, the function manages the creation of the *DataTrees* subfolder if it is necessary.
    
    Args:
        tree (dict): 
            The tree object to save.
            
        folder_path (str): 
            The folder path where the tree will be saved.
    """
    while True:
        save_tree = input("\033[34mDo you want to save the tree? (y/n): \033[0m")
        if save_tree.lower() in ["y", "yes"]:
            break
        if save_tree.lower() in ["n", "no"]:
            print("\033[31mTree not saved.\033[0m")
            return
        else:
            print("\033[33mInvalid option! Try again.\033[0m")

    file_name = input("\033[34mEnter a file name: \033[0m")
    if not file_name:
        print("\033[31mFile name is empty. Tree not saved.\033[0m")
        return

    # Create the DataTrees folder if it doesn't exist
    data_trees_folder = os.path.join(folder_path, "DataTrees")
    if not os.path.exists(data_trees_folder):
        os.makedirs(data_trees_folder)

    file_path = os.path.join(data_trees_folder, file_name)

    # Check if the file already exists
    while os.path.exists(file_path):
        overwrite = input("\033[33mA file with the same name already exists. Do you want to overwrite it? (y/n):\033[0m ")
        if overwrite.lower() == "y":
            break
        confirm = input("\033[34mDo you want to choose a different file name? (y/n):\033[0m ")
        if confirm.lower() != "y":
            print("\033[31mTree not saved.\033[0m")
            return
        file_name = input("\033[34mEnter a different file name: \033[0m")
        if not file_name:
            print("\033[31mFile name is empty. Tree not saved.\033[0m")
            return
        file_path = os.path.join(data_trees_folder, file_name)

    # Serialize the tree to JSON
    def serialize_tree(node):
        """Serialize the tree to JSON format recursively.

        This function serializes the tree object to JSON format. It handles dictionary nodes and pandas DataFrame nodes separately.

        Args:
            node: The current node in the tree.

        Returns:
            Serialized node in JSON format.
        """
        if isinstance(node, dict):
            return {k: serialize_tree(v) for k, v in node.items()}
        elif isinstance(node, pd.DataFrame):
            return {"type": "DataFrame", "data": node.to_dict(orient="split")}
        return node

    serialized_tree = serialize_tree(tree)

    # Save the serialized tree to a file
    with open(file_path, "w") as file:
        json.dump(serialized_tree, file)

    print(f"\033[32mTree saved to {file_path}\033[0m")

def load_tree_from_path(file_path):
    """
    Load a serialized tree from a file.

    This function loads a serialized tree from a specified file path. The tree is deserialized, including any serialized DataFrames.

    Args:
        file_path (str): 
            The path of the file containing the serialized tree.

    Returns:
        tree (dict), file_name (str): 
            A tuple containing the loaded tree and the file name.
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The specified file '{file_path}' does not exist.")

    # Get the file name from the file path
    file_name = os.path.basename(file_path)

    # Load the serialized tree from the file
    with open(file_path, "r") as file:
        serialized_tree = json.load(file)

    # Deserialize the tree, including DataFrames
    def deserialize_tree(node):
        """Deserialize the tree from the serialized format.

        This function deserializes the tree object from the serialized format. It handles dictionary nodes and serialized DataFrames separately.

        Args:
            node: The current node in the serialized tree.

        Returns:
            Deserialized node.
        """
        if isinstance(node, dict):
            if "type" in node and node["type"] == "DataFrame":
                # Convert the serialized DataFrame back to a DataFrame object
                data = node["data"]["data"]
                index = node["data"]["index"]
                columns = node["data"]["columns"]
                return pd.DataFrame(data, index=index, columns=columns)
            return {k: deserialize_tree(v) for k, v in node.items()}
        return node

    tree = deserialize_tree(serialized_tree)

    return tree, file_name

def load_trees(tree_paths):
    """
    Load multiple trees from the specified file paths.

    This function loads multiple trees from the given file paths and stores them in a dictionary, where the keys are the tree names (derived from the file names) and the values are the loaded trees. It also includes a special "paths" branch in the dictionary, which contains all the tree paths.

    Args:
        tree_paths (list): 
            A list of file paths to the tree files.

    Returns:
        trees (dict): 
            A dictionary containing the loaded trees and the tree paths.
    """
    trees = {}
    for tree_path in tree_paths:
        tree, tree_name = load_tree_from_path(tree_path)
        trees[tree_name] = tree

    # Create a branch for saving all the tree paths
    trees["paths"] = tree_paths

    return trees
