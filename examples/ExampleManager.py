import treform as ptm
import os
import shutil
import time

BASE_PATH = os.path.dirname(ptm.__file__)
FORCE_REFRESH = False

def download_relative_path(target_relative_path:str):
    """
    Download sample data from treform github repository
    :param force_refresh: If True, it will delete existing sample data folder and re-download
    :return: None
    The process may install pygithub if it is not installed
    """
    if 'sample_data' in target_relative_path and os.path.exists(os.path.join(BASE_PATH, 'sample_data')):
        if not FORCE_REFRESH:
            print('Sample data folder already exists, set flag force_refresh = True to re-download')
            return
    base_repo = r'https://github.com/MinSong2/treform'
    if not target_relative_path.startswith('/'):
        target_relative_path = '/' + target_relative_path
    target_folder = os.path.join(BASE_PATH, target_relative_path.lstrip('/'))
    print(os.path.abspath(target_folder))
    tmp_path = '/tmp/clone'
    if os.path.exists(tmp_path):
        #  Somehow its being used by other process?
        tmp_path = f'/tmp/clone/{time.strftime("%H%M%S")}'
    if FORCE_REFRESH:
        shutil.rmtree(target_folder)
    try:
        import git
    except (ModuleNotFoundError, ImportError):
        import pip
        print('Installing pygithub to download sample datas')
        pip.main(['install', 'gitpython'])
    import git
    try:
        print(f'Created temporary path {os.path.abspath(tmp_path)}')
        git.Repo.clone_from(base_repo, tmp_path)
        shutil.copytree(os.path.abspath(tmp_path + target_relative_path), target_folder)
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)
        print(f'Removed temporary path {os.path.abspath(tmp_path)}')

def download_samples():
    download_relative_path(r'/sample_data')


class PathManager:
    """
    PathManager is a class that resolves path such as ./sample_data to BASE_PATH/sample_data
    PathManager('./sample_data') -> BASE_PATH/sample_data
    """
    #  resolves path such as ./sample_data to BASE_PATH/sample_data
    def __init__(self, path: str):
        self.path = path
        if self.isSamplePath():
            self.checkSampleExist()
            self.path = os.path.join(BASE_PATH, *self.path.lstrip('./').lstrip('../').split('/'))
        elif self.isRepoPath():
            relative_file = self.path.lstrip('./').lstrip('../')
            # for example stopwords/stopwords_ko.txt
            self.checkFileExist(relative_file)
            print('parsing repo path')
            self.path = os.path.join(BASE_PATH, *self.path.lstrip('./').lstrip('../').split('/'))

    def isSamplePath(self) -> bool:
        return self.path.startswith('./sample_data') or self.path.startswith('../sample_data')

    def isRepoPath(self) -> bool:
        return self.path.startswith('../')

    def checkFileExist(self, relative_file: str) -> None:
        if not os.path.exists(os.path.join(BASE_PATH, relative_file)):
            # check if relative_file is 'file' or directory
            if os.path.isdir(relative_file):
                download_relative_path(relative_file)
            else:
                # rsplit once with '/' to get the directory
                download_relative_path(relative_file.rsplit('/', 1)[0])

    def checkSampleExist(self) -> None:
        treform_sample_path = BASE_PATH + '/sample_data'
        if not os.path.exists(treform_sample_path):
            download_samples()

    def __call__(self, *args) -> str:
        return os.path.join(self.path, *args)

    def __repr__(self) -> str:
        return self.path

    def __str__(self) -> str:
        return self.path
    
    @staticmethod
    def get(path:str):
        return str(PathManager(path))

if __name__ == '__main__':
    if os.path.exists(os.path.join(BASE_PATH, 'sample_data')) and not FORCE_REFRESH:
        print('Sample data folder already exists, set flag force_refresh = True to re-download')
    else:
        download_samples()
