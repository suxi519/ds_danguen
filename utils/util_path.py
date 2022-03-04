import os


class PathUtils:
    project_name = 'ds_danguen'

    def __init__(self):
        pass

    @staticmethod
    def _get_project_path():
        abs_path = os.path.abspath(os.path.curdir).split('\\')
        pivot_index = abs_path.index(PathUtils.project_name)
        return '\\'.join(abs_path[:pivot_index + 1])

    @staticmethod
    def driver_folder_path():
        return PathUtils._get_project_path() + '\\drivers'

    @staticmethod
    def driver_path():
        return PathUtils.driver_folder_path() + '\\chromedriver.exe'

    @staticmethod
    def ui_folder_path():
        return PathUtils._get_project_path() + '\\ui'

    @staticmethod
    def resources_folder_path():
        return PathUtils._get_project_path() + '\\resources'
