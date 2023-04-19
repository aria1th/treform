import treform as ptm
import os
import shutil
import time

BASE_PATH = os.path.dirname(ptm.__file__)
FORCE_REFRESH = False


def download_samples():
    if os.path.exists(os.path.join(BASE_PATH, 'sample_data')):
        if not FORCE_REFRESH:
            print('Sample data folder already exists, set flag force_refresh = True to re-download')
            return
    base_repo = r'https://github.com/MinSong2/treform'
    target_relative_path = r'/sample_data'
    target_folder = os.path.join(BASE_PATH, 'sample_data')
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
        pip.main(['install', 'pygithub'])
    import git
    try:
        print(f'Created temporary path {os.path.abspath(tmp_path)}')
        repo = git.Repo.clone_from(base_repo, tmp_path)
        shutil.copytree(os.path.abspath(tmp_path + target_relative_path), target_folder)
    finally:
        del repo
        shutil.rmtree(tmp_path, ignore_errors=True)
        print(f'Removed temporary path {os.path.abspath(tmp_path)}')


class PathManager:
    """
    PathManager is a class that resolves path such as ./sample_data to BASE_PATH/sample_data
    PathManager('./sample_data') -> BASE_PATH/sample_data
    """
    #  resolves path such as ./sample_data to BASE_PATH/sample_data
    def __init__(self, path):
        self.path = path
        if self.isSamplePath():
            self.checkSampleExist()
            self.path = os.path.join(BASE_PATH, self.path[2:])

    def isSamplePath(self):
        return self.path.startswith('./sample_data')

    def checkSampleExist(self):
        treform_sample_path = BASE_PATH + '/sample_data'
        if not os.path.exists(treform_sample_path):
            download_samples()

    def __call__(self, *args):
        return os.path.join(self.path, *args)

    def __repr__(self):
        return self.path

    def __str__(self):
        return self.path


if __name__ == '__main__':
    if os.path.exists(os.path.join(BASE_PATH, 'sample_data')) and not FORCE_REFRESH:
        print('Sample data folder already exists, set flag force_refresh = True to re-download')
    else:
        download_samples()
