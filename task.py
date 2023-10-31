from download_image import DownloadImage


obj = DownloadImage()


def whole_process():
    obj.open_browser()
    obj.search_products_and_load_all()
    obj.search_and_download_image()



if __name__ == "__main__":
    whole_process()
