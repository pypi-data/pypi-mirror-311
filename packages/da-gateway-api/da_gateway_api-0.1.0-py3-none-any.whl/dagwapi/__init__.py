from dt_tools.os.project_helper import ProjectHelper
# import pkg_resources

PACKAGE_NAME = 'da-gatweay-api'
__version__ = ProjectHelper.determine_version(PACKAGE_NAME)
# try:
#     __version__ = pkg_resources.get_distribution(PACKAGE_NAME).version
# except:
#     # version based on the mod timestamp of the most current updated python code file
#     file_list = list(pathlib.Path(__file__).parent.glob('**/*.py'))
#     ver_date = dt(2000,1,1,0,0,0,0)
#     for file_nm in file_list:
#         ver_date = max(ver_date, dt.fromtimestamp(file_nm.stat().st_mtime))
#     __version__ = f'{ver_date.year}.{ver_date.month}.{ver_date.day}'
