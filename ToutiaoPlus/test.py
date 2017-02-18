"""multithread spider"""
import queue
import threading
from huiparse import deal_group_page
from huiparse import download_work

# max groups to traverse
MAX_GROUPS_TO_TRAVERSE = 10
# images to download : [(groupID1,[url1,url2,..])
DOWNLOAD_QUEUE = queue.Queue()
# groups to be traverse [(groupID1, url1), (groupID2, url2)...]
TRAVERSE_QUEUE = queue.Queue()
# groupID recorder to remember the groups that has been traversed
GROUP_TRAVERSED = []
# producer and consumer
CONDITION = threading.Condition()
# the start group page
START_PAGE = "http://www.361games.com/html/tu/316376.html"


def filter_with_shared_list(condition, share_list, elements):
    """
    filter the elements with shared list
    :param share_list : [groupID1, groupID2...]
    :param elements : [(groupID1, url1), (groupID2, url2)...]
    """
    if condition.acquire():
        for item in elements:
            if item[0] in share_list:
                elements.remove(item)
            else:
                share_list.append(item[0])
        condition.notify()
        condition.release()


def group_page_process(start_page):
    """the main proc tp process a new page"""
    recommends, pics = deal_group_page(start_page)
    # filter_with_shared_list(CONDITION, GROUP_TRAVERSED, recommends)
    if len(recommends) != 0:
        TRAVERSE_QUEUE.put(recommends)
    if len(pics) != 0:
        DOWNLOAD_QUEUE.put(pics)


def producer(name):
    """thread to parse the web page and generate the wanted contents"""
    while True:
        # if DOWNLOAD_QUEUE.qsize() <= 100:
        next_groups = TRAVERSE_QUEUE.get()
        print('Producer %s:' % name)
        for item in next_groups:
            group_page_process(item[1])


def consumer(name):
    """thread to do the downloading works"""
    while True:
        pics = DOWNLOAD_QUEUE.get()
        print('Consumer %s:' % name)
        download_work(pics)


# the main function
if __name__ == '__main__':
    group_page_process(START_PAGE)
    for i in range(1):
        p = threading.Thread(target=producer, args=('zhanghui',))
        p.start()

    for i in range(4):
        c = threading.Thread(target=consumer, args=('wenjing',))
        c.start()
