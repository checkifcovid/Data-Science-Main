import os

def get_newest_file(path="data",file_type=None):
    """
    returns the newest file from a directory

    --
    path: directory to be searched
    file_type: if specified, will filter for this file type

    """

    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]

    # Filter if necessary
    if file_type:
        paths = [x for x in paths if x.endswith(file_type)]

    return max(paths, key=os.path.getctime)
