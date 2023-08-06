import argparse
import os
import zipfile
import warnings

from mlproj_manager.file_management import concatenate_results, get_file_paths_that_contain_keywords, get_indices

def read_arguments():

    arguments = argparse.ArgumentParser()
    arguments.add_argument("--results-dir", action="store", type=str, required=True, help="Path to a directory.")
    arguments.add_argument("--skip-list", action="store", type=str, default="",
                           help="Comma separated list with names of directories to skip.")
    arguments.add_argument("--verbose", action="store_true", default=False)
    arguments.add_argument("--zip-original-index-files", action="store_true", default=False)
    arguments.add_argument("--delete-original-index-files", action="store_true", default=False)
    return arguments.parse_args()


def handle_files_in_directory(dir_path: str, list_of_file_paths: list, zip_original_files: bool = True,
                              delete_original_files: bool = False, no_warning: bool = False):
    """

    """

    delete_original_files = zip_original_files and delete_original_files    # only delete files if they're zipped first

    # concatenate results
    indices = get_indices(dir_path)
    concatenate_results(dir_path, store_concatenated_results=True, indices=indices)

    if not zip_original_files: return
    # zip files
    zip_file_name = "indices-{0}-{1}.zip".format(indices[0], indices[-1])
    zip_file_path = os.path.join(dir_path, zip_file_name)
    if not os.path.isfile(zip_file_path):
        with zipfile.ZipFile(zip_file_path, mode="w") as archive:
            for file_path in list_of_file_paths:
                archive.write(file_path)

    if not delete_original_files: return
    # delete original files
    if not no_warning:
        warning_message = "The following files are going to be deleted:"
        for path in list_of_file_paths:
            warning_message += "\n\t{0}".format(path)
        warnings.warn(warning_message)
        input("Press any key to continue...")
    for file_path in list_of_file_paths:
        os.remove(file_path)


def main():
    arguments = read_arguments()

    results_dir = arguments.results_dir
    skip_list = arguments.skip_list.split(",")

    stack_of_dir_path = [os.path.join(results_dir, name) for name in os.listdir(results_dir)]

    while len(stack_of_dir_path) > 0:
        current_dir_path = stack_of_dir_path.pop(0)

        # skip paths containing any keyword in the skip list
        if any(keyword in current_dir_path for keyword in skip_list): continue
        # skip any files
        if os.path.isfile(current_dir_path): continue

        file_paths = get_file_paths_that_contain_keywords(current_dir_path, ("index", "npy"))
        contains_results_files = len(file_paths) > 0

        if not contains_results_files:
            list_of_dir_paths = [os.path.join(current_dir_path, name) for name in os.listdir(current_dir_path)]
            stack_of_dir_path.extend(list_of_dir_paths)
        else:
            handle_files_in_directory(current_dir_path, file_paths,
                                      zip_original_files=arguments.zip_original_index_files,
                                      delete_original_files=arguments.delete_original_index_files)


if __name__ == "__main__":
    main()
