import hashlib
import os


def allowed_file(filename):
    """
    Validates if the uploaded file has an allowed image extension.
    
    This function checks the file extension against a whitelist of 
    acceptable image formats. It handles cases where the filename
    might not have an extension.

    Parameters
    ----------
    filename : str
        The original filename from the uploaded file

    Returns
    -------
    bool
        True if file extension is in [.png, .jpg, .jpeg, .gif]
        False if extension is missing or not in allowed list
        
    Examples
    --------
    >>> allowed_file('image.jpg')
    True
    >>> allowed_file('document.pdf')
    False
    >>> allowed_file('noextension')
    False
    """
    
    # Check if the file extension of the filename received is in the set of allowed extensions (".png", ".jpg", ".jpeg", ".gif")
    dir, ext = os.path.splitext(filename)
    return ext.lower() in [".png", ".jpg", ".jpeg", ".gif"] if ext else False


async def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    
    # Get hash name
    result = hashlib.md5(file.file.read()).hexdigest()
    file.file.seek(0)
    extension = file.filename.split('.')[-1]
    new_file_name = f'{result}.{extension}'

    return new_file_name