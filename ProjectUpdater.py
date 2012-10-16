import urllib
import urllib2
import zipfile
import os
import os.path
import shutil
import json
import tempfile
import distutils.dir_util
import distutils.file_util


class TempFolder(object):
    def __enter__(self):
        self.path = tempfile.mkdtemp()
        return self.path

    def __exit__(self, type, value, traceback):
        #shutil.rmtree(self.path)
        pass


def settings():
    with open(os.getcwd() + "\\Updater\\Settings.conf", "rb") as json_file:
        settings = json.load(json_file)
    return settings


def return_path():
    return os.getcwd()


def unpackfile(filepath, path):
    zfile = zipfile.ZipFile(filepath)
    zfile.extractall(path)
    zfile.close()


def updater(tmp_dir = None, normal_path = None):
    setting = settings()
    for root, dirs, files in os.walk(tmp_dir):
        rel_path = os.path.rel_path(root).split("\\")[0]
        new_path = os.path.realpath(root)[len(tmp_dir):].split("\\")[2:]
        new_path = "\\".join(new_path)
        if not "tmp.zip" in files:
            if not rel_path in setting["Ignored Directories"]:
                dist = os.path.join(normal_path, new_path)
                if dist[-1] != "\\":
                    dist += "\\"
                if not os.path.exists(dist):
                    print "Made dir: %s" % os.path.join(dist)
                    try:
                        distutils.dir_util.mkpath(dist)
                        print "Yay"
                    except distutils.errors.DistutilsFileError:
                        print "Error"
                        distutils.dir_util.remove_tree(dist)
                        distutils.dir_util.mkpath(dist)
                for i in files:
                    if not i in setting["Ignored Files"]:
                        new_dist = os.path.join(dist, i)
                        old_dist = os.path.join(root, i)
                        if os.path.exists(new_dist):
                            try:
                                os.remove(new_dist)
                            except IOError:
                                pass
                        distutils.file_util.copy_file(old_dist, new_dist)


def download(url):
    if "github" in url.lower():
        url += "/zipball/master"
    if "ftp" in url[:3].lower():
        print url
    with TempFolder() as tmp_path:
        packedname = tmp_path + "/tmp.zip"
        urllib.urlretrieve(url, packedname)
        unpackfile(packedname, tmp_path)
        updater(tmp_dir=tmp_path, normal_path=return_path())

if __name__ == '__main__':
    download("https://github.com/Foxboron/PyFoxConway")
    #download("ftp://ajsdbaisd.com")
