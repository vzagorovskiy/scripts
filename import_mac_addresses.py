import urllib.request
import progressbar

OUI_URL = "http://standards.ieee.org/develop/regauth/oui/oui.txt"
OUI_FILE = "oui.txt"
MAC_FILE = "mac.txt"
widgets_download = ['Downloading OUI: ',
                    progressbar.Percentage(), ' ',
                    progressbar.Bar(), ' ',
                    progressbar.ETA(), ' ',
                    progressbar.FileTransferSpeed()]

progressbar_download = progressbar.ProgressBar(widgets=widgets_download)

widgets_write = [progressbar.FormatLabel('Processed: %(value)d lines (in: %(elapsed)s)')]
progressbar_write = progressbar.ProgressBar(widgets=widgets_write, maxval=progressbar.UnknownLength)


def download_progress(blocknum, bs, size):
    if progressbar_download.maxval is None:
        progressbar_download.maxval = size
        progressbar_download.start()
    progressbar_download.update(min(blocknum * bs, size))


def import_mac_addresses():
    print('Download OUI database from url "{0}" to file "{1}"'.format(OUI_URL, OUI_FILE))

    urllib.request.urlretrieve(OUI_URL, filename=OUI_FILE, reporthook=download_progress)
    progressbar_download.finish()

    print('Write MAC from OUI database to file "{0}"'.format(MAC_FILE))

    i = 0
    progressbar_write.start()
    with open(MAC_FILE, mode='w', newline='', encoding='utf-8') as mac_file:
        with open(OUI_FILE, mode='r', encoding='utf-8') as oui_file:
            for line in oui_file:
                if '(hex)' in line:
                    mac_file.write('='.join(map(str.strip, line.split('(hex)', maxsplit=1))) + '\n')
                    i += 1
                    progressbar_write.update(i)
    progressbar_write.finish()
    print('Operation is completed.')


if __name__ == "__main__":
    import_mac_addresses()
