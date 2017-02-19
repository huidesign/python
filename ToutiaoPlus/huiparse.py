"""function used to parse web page"""
import os
import shutil
import socket
import urllib.request

from bs4 import BeautifulSoup

# timeout in seconds
TIMEOUT = 2
socket.setdefaulttimeout(TIMEOUT)
# file location
FILE_LOCATION = "E:\\newphoto\\crazy"


class AppURLopener(urllib.request.FancyURLopener):
    """dirive from FancyURLopenner"""
    version = "Mozilla/5.0"


def generate_full_url(full_url, short_url):
    """ generate new full url"""
    url_list = list(full_url.rpartition('/'))
    url_list[-1] = list(short_url.rpartition('/'))[-1]
    return "".join(url_list)


def generate_full_name(group_id, image_url, file_path):
    """generate image full name"""
    return os.path.join(file_path, group_id + "_" + image_url.rpartition('/')[-1])


def strip_group_id(url):
    """strip group id string from group url"""
    return url.split('/')[-1].split('.')[0].split('_')[0]


def download_work(pics):
    """function do the download work, usually called by other modules"""
    for pic in pics[1]:
        download_pictures(pic, generate_full_name(pics[0], pic, FILE_LOCATION))


def download_pictures(pic_url, file_name):
    """picture downloads"""
    opener = AppURLopener()
    print("Download: ", pic_url)
    try:
        response = opener.open(pic_url)
        if response.closed:
            return
        out_file = open(file_name, 'wb')
        shutil.copyfileobj(response, out_file)
    except Exception as exception:
        raise exception


def deal_group_page(url):
    """
    deal with a new group page, recommend_pages returned
    by this function should be further filtering

    :param  recommend_pages [(groupID1, url1), (groupID2, url2)...]
    :param  image_pages [url1, url2...]
    :returns [(groupID1, url1), (groupID2, url2)...], (groupID, [url1, url2...])
    """
    recommend_pages = []
    image_pages = []
    next_pages = []  # next pages in current group page
    next_url = url
    while next_url not in next_pages and next_url != None:
        next_pages.append(next_url)
        next_url = deal_current_page(next_url, recommend_pages, image_pages)
    return recommend_pages, (strip_group_id(url), image_pages)


def deal_current_page(url, recommend_pages, image_pages):
    """deal with web page"""
    # open current page and parse with beautiful soup
    opener = AppURLopener()
    try:
        html_doc = opener.open(url)
        if html_doc.closed:
            return None
    except Exception as exception:
        raise exception
    soup = BeautifulSoup(html_doc, "lxml", from_encoding='GB18030')
    # strip next page out from current page
    next_page = generate_full_url(url, soup.find(id="photoNext")["href"])
    # strip recommended urls out from current page
    for tag in soup.find(class_="pic-list2 martop clearfix")("a"):
        href = generate_full_url(url, tag["href"])
        # be cautious, this href can be both short and long
        if (strip_group_id(href), href) not in recommend_pages:
            recommend_pages.append((strip_group_id(href), href))
    # strip image urls out from current page
    for tag in soup.find(id="big-pic").find_all("img"):
        image_pages.append(tag["src"])

    return next_page


if __name__ == '__main__':
    RECOMMONDS, PICS = deal_group_page("http://www.361games.com/html/tu/454956.html")
    print("--------------------recommend_pages-----------------")
    print(RECOMMONDS)
    print("--------------------download_pages-----------------")
    print(PICS)
    for img in PICS[1]:
        download_pictures(img, generate_full_name(PICS[0], img, FILE_LOCATION))
