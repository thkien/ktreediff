import os
import unicodedata
import hashlib


class Util:
    @staticmethod
    def get_east_asian_width_count(text:str) -> int:
        """Unicode-aware string length calculation

        :param text: text data
        :type text: str
        :return: length of text data
        :rtype: int
        """
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 2
            else:
                count += 1
        return count

    @staticmethod
    def compare_files(left:str, right:str, chunk_size:int=2048) -> bool:
        """Compare binary data of 2 files

        :param left: left file path
        :type left: str
        :param right: right file path
        :type right: str
        :param chunk_size: chunk size to read when comparing, defaults to 2048
        :type chunk_size: int, optional
        :raises RuntimeError: when specified parameters are not files
        :return: True if 2 files are the same, otherwise False
        :rtype: bool
        """

        if not os.path.isfile(left) or not os.path.isfile(right):
            raise RuntimeError("Invalid parameters")

        if os.path.getsize(left) != os.path.getsize(right):
            return False

        # compare binary data when 2 files have the same size
        with open(left, "rb") as fleft, open(right, "rb") as fright:
            while True:
                left_data = fleft.read(chunk_size)
                right_data = fright.read(chunk_size)

                if not left_data or not right_data:
                    break

                if left_data != right_data:
                    # found different data
                    return False
            return True

    @staticmethod
    def list_files(root_dir:str, file_extensions:list[str], recursive:bool=False) -> list[str]:
        """Create list of files in a directory

        :param root_dir: root directory
        :type root_dir: str
        :param file_extensions: file extensions. Ex: ('.txt', '.psd', '.xlsx')
        :type file_extensions: list[str]
        :param recursive: search file recursively, defaults to False
        :type recursive: bool, optional
        :return: list of file paths
        :rtype: list[str]
        """

        result = list()

        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isfile(item_path):
                if file_extensions:
                    for ext in file_extensions:
                        if item_path.lower().endswith(ext):
                            result.append(item_path)
                else:
                    result.append(item_path)
            elif os.path.isdir(item_path):
                if recursive:
                    child_dir_list = Util.list_files(item_path, file_extensions, recursive)
                    result.extend(child_dir_list)

        return result

