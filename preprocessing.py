"""
Preprocessing class for cropping, restructuring and renaming original images.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# suppress pandas warning
pd.options.mode.chained_assignment = None


class Preprocessor:
    """
    This class is responsible for preprocessing the dataset by cropping images, restructuring them, 
    and renaming them according to a specific format. It also handles the creation of necessary 
    directories and the retrieval of file and folder lists.
    """
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.prep_path = r'.\images'
        self.prep_img_paths = None

    @staticmethod
    def get_files_list(dir_path):
        """
        Retrieves a sorted list of file paths from the specified directory, excluding any 
        subdirectories.
        """
        dir_paths = sorted(  # 'sorted()' sorts elements of the list
            [  # construct list of input files from directory through list comprehension
                os.path.join(dir_path, fname).replace("\\", "/")
                # 'os.listdir(path)' returns a list containing the names of the entries in the
                # directory given by path
                for fname in os.listdir(dir_path)
                if not os.path.isdir(os.path.join(dir_path, fname).replace("\\", "/"))
            ]
        )
        return dir_paths

    @staticmethod
    def get_folders_list(dir_path):
        """
        Retrieves a sorted list of folder paths from the specified directory, excluding any
        files.
        """
        dir_paths = sorted(  # 'sorted()' sorts elements of the list
            [  # construct list of input images from directory through list comprehension
                os.path.join(dir_path, fname).replace("\\", "/")
                # 'os.listdir(path)' returns a list containing the names of the entries in the
                # directory given by path
                for fname in os.listdir(dir_path)
                if os.path.isdir(os.path.join(dir_path, fname).replace("\\", "/"))
            ]
        )
        return dir_paths

    @staticmethod
    def create_directory(f_path):
        """
        Creates a directory at the specified path if it does not already exist.
        """
        if not os.path.exists(f_path):
            os.mkdir(f_path)

    def dataset_preprocessing(self):
        """
        Preprocesses the dataset by cropping images, restructuring them, and renaming them 
        according to a specific format. The preprocessed images are saved in a designated
        directory.
        """
        # create prep path if does not exist
        self.create_directory(self.prep_path)
        # obtain subfolder paths
        subfolders_list = self.get_folders_list(self.dataset_path)
        # itereate through subfolder paths
        for _, t in enumerate(subfolders_list):
            # obtain current folder name
            curr_subfolder_name = os.path.basename(t)
            # obtain subfolder content paths
            curr_image_paths = self.get_files_list(t)
            # itereate through subfolder content paths
            for q_ind, q in enumerate(curr_image_paths):
                # read image
                pic = plt.imread(q)
                # gather minimum image dimension and index
                pic_dim_min = min(pic.shape[:-1])
                pic_dim_min_index = pic.shape[:-1].index(pic_dim_min)
                # crop image into square
                cropped_pic = None
                if pic_dim_min_index == 0:
                    crop_loc1 = int((pic.shape[1] - pic.shape[0]) / 2)
                    crop_loc2 = int(pic.shape[1] - crop_loc1)
                    cropped_pic = pic[:, crop_loc1:crop_loc2, :]
                elif pic_dim_min_index == 1:
                    crop_loc1 = int((pic.shape[0] - pic.shape[1]) / 2)
                    crop_loc2 = int(pic.shape[0] - crop_loc1)
                    cropped_pic = pic[crop_loc1:crop_loc2, :, :]
                # assemble preprocessing image name string
                curr_prep_image_str = curr_subfolder_name + '_' + f'{(q_ind + 1):03d}' + '.png'
                curr_prep_filename = \
                    os.path.join(self.prep_path, curr_prep_image_str).replace("\\", "/")
                # save preprocessed image
                if cropped_pic is None:
                    raise ValueError(r'Cropped image variable is None.')
                mpimg.imsave(curr_prep_filename, cropped_pic)
        self.prep_img_paths = self.get_files_list(self.prep_path)

if __name__ == '__main__':

    # --- preprocess dataset ---
    EXAMPLE_DATA_PATH = r'.\dataset'
    example_data = Preprocessor(EXAMPLE_DATA_PATH)
    example_data.dataset_preprocessing()
