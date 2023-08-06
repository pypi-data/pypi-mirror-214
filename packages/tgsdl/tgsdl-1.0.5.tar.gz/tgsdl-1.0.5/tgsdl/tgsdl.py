import os
import shutil
import requests
import argparse
import threading
from colorclip import red, green,pink,blue,lavender,lime


"""
Attention, script leechers!
This script comes with a built-in karma detector. 
If you dare to copy and claim this code as your own,
prepare for a lifetime of bugs and errors.
May your path be forever haunted by semicolons and syntax nightmares.
Happy coding, 
original thinkers!

https://t.me/onefinalhug

"""
class StickerDownloaderLib:
    def __init__(self):
        self.api_url = "https://tgsapi.vercel.app/api"
        self.pack_name = None

    def url(self, pack_url):
        if pack_url.startswith("https://t.me/addstickers/"):
            pack = pack_url.split("/")[-1]
            self.pack_name = pack
            return pack
        else:
            return red("Use valid sticker pack URL")

    def api(self, pack_url):
        pack = self.url(pack_url)
        params = {'bev': pack}
        req = requests.get(self.api_url, params=params)
        if req.status_code == 200:
            return req.json()
        elif req.status_code == 404:
        	return red("Sticker Pack Not Found")
        else:
            return red("Something went wrong")

    def download_file(self, file_data, folder_name):
        try:
	        name = file_data['name']
	        download_url = file_data['url']
	        filename = os.path.join(folder_name, name)
	        response = requests.get(download_url)
	        response.raise_for_status()
	        with open(filename, 'wb') as file:
	            file.write(response.content)
	            print(pink(f"Downloaded : {filename}"))
        except:
        	pass


    def download_files(self, response_data):
        folder_name = f"Sticker/{self.pack_name}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        threads = []
        for file_data in response_data:
            thread = threading.Thread(target=self.download_file, args=(file_data, folder_name))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        zip_filename = f"Sticker/{self.pack_name}.zip"
        shutil.make_archive(folder_name, 'zip', folder_name)

        shutil.rmtree(folder_name)
        #print(red("Folder removed"))
        return zip_filename


def download_sticker_pack(pack_url):
    downloader = StickerDownloaderLib()
    print(blue("Download started..."))
    response_data = downloader.api(pack_url)
    if isinstance(response_data, list):
        zip_filename = downloader.download_files(response_data)
        print(green(f"Created zip file: {zip_filename}"))
    else:
        print(response_data)


def main():
    parser = argparse.ArgumentParser(description="Telegram Sticker Pack Downloader By : Bevlill (@OneFinalHug)")
    parser.add_argument("pack_url", nargs='?', default=None, help="URL of the sticker pack")

    args = parser.parse_args()
    if args.pack_url:
        download_sticker_pack(args.pack_url)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except:
        pass
