# 使用命令：uvicorn main-v2:app --port 10011
# pip install uvicorn[standard]
# pip install aiofiles
import os
import xml2epub
import psycopg2
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import FileResponse
from bs4 import BeautifulSoup

# 必须先改变路径
# os.chdir("G:\\")


def query_one(query) :
    conn = psycopg2.connect(host='10.130.159.110', port='5432', database='ebooks', user='yuhan', password='YuhanLiu')
    cur = conn.cursor()
    cur.execute(query)
    one = cur.fetchone()
    conn.commit()
    conn.close()
    return one


def get_chapter_one(book_id, chapter_id):
    query = f"SELECT content FROM chapter WHERE id = {book_id} AND chapter = {chapter_id}"
    return query_one(query)


def get_book_info(book_id):
    query = f"SELECT * FROM book WHERE id = {book_id}"
    return query_one(query)


def get_fulfill_book_info():
    query = "SELECT * FROM book WHERE fulfill = 1 ORDER BY random() limit 1;"
    return query_one(query)


def generate_ebook(book_id):
    book = get_book_info(book_id)
    if book is not None:
        print(str(book[0]) + book[1])
        chapters = book[3]['chapter_info']
        author = book[2]
        name = book[1]
        fulfill = book[6]
        publisher = book[10]
        if fulfill != 1:
            return False
        epub_book = xml2epub.Epub(name, creator=author, language='zh-CN', publisher=publisher)
        for i in chapters:
            print(i)
            ch = get_chapter_one(book_id, i['chapter_index'])
            content = ch[0]
            if ch is not None:
                epub_book.add_chapter(xml2epub.create_chapter_from_string(content, title=i['chapter_name'], strict=False))
        epub_book.create_epub('ebooks-download')
        # 改名
        name_processed = ''.join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
        os.rename(os.path.join('ebooks-download', name_processed + '.epub'), os.path.join('ebooks-download', str(book_id) + '.epub'))
        return True
    else:
        return False


async def generate_ebook_ws(book_id, websocket):
    book = get_book_info(book_id)
    if book is not None:
        chapters = book[3]['chapter_info']
        author = book[2]
        name = book[1]
        fulfill = book[6]
        publisher = book[10]
        if fulfill != 1:
            res = {'code': 500, 'msg': '这本书还没有完成入库哦', 'data': book_id}
            await websocket.send_json(res)
        else:
            res = {'code': 300, 'msg': '正在生成电子书！', 'data': book_id}
            await websocket.send_json(res)
            epub_book = xml2epub.Epub(name, creator=author, language='zh-CN', publisher=publisher)
            for i in chapters:
                ch = get_chapter_one(book_id, i['chapter_index'])
                content = ch[0]
                if ch is not None:
                    epub_book.add_chapter(xml2epub.create_chapter_from_string(content, title=i['chapter_name'], strict=False))
                    res = {'code': 301, 'msg': i['chapter_index'], 'data': i}
                    await websocket.send_json(res)
            epub_book.create_epub('ebooks-download')
            # 改名
            name_processed = ''.join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
            os.rename(os.path.join('ebooks-download', name_processed + '.epub'), os.path.join('ebooks-download', str(book_id) + '.epub'))
            res = {'code': 200, 'msg': '已经成功生成电子书！', 'data': book_id}
            await websocket.send_json(res)
    else:
        res = {'code': 400, 'msg': '数据库中不存在这本书，请检查id！', 'data': book_id}
        await websocket.send_json(res)


app = FastAPI()


@app.get("/ebook")
def get_ebook(book_id: int):
    # 先查询本地是否存在
    file_path = os.path.join('ebooks-download', str(book_id) + '.epub')
    if os.path.exists(file_path):
        book = get_book_info(book_id)
        if book is not None:
            author = book[2]
            name = book[1]
            publisher = book[10]
            filename = f'{name}-{author}-{publisher}.epub'
            return FileResponse(file_path, media_type='application/epub+zip', filename=filename)
    else:
        # 生成
        return {'code': 400, 'msg': '请等待生成电子书！', 'data': ''}


@app.websocket("/ebook/{book_id}/ws")
async def websocket_endpoint(websocket: WebSocket, book_id: int):
    await websocket.accept()
    try:
        while True:
            if os.path.exists(os.path.join('ebooks-download', str(book_id) + '.epub')):
                res = {'code': 200, 'msg': '已经生成电子书！', 'data': ''}
                await websocket.send_json(res)
                await websocket.close()
            else:
                await generate_ebook_ws(book_id, websocket)
                await websocket.close()
    except WebSocketDisconnect:
        await websocket.close()

# 注意！！！！用作服务器时，删除以下代码
if __name__ == '__main__':
    # while True:
    #     book = get_fulfill_book_info()
    #     book_id = book[0]
    #     book_name = book[1]
    #     if os.path.exists(os.path.join('ebooks-download', str(book_id) + '.epub')) or book_name[-8:] == '（推荐PC阅读）':
    #         continue
    #     else:
    #         generate_ebook(book_id)
    generate_ebook(30610590)
    # str = """<?xml version="1.0" encoding="utf-8" standalone="no"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title><link href="http://storage.360buyimg.com/ebooks/4fef996658c71fb571c607dce4df3822_new_.css" rel="stylesheet" type="text/css" /></head><body><div class="center"><img alt="" class="fullscreen" src="https://img30.360buyimg.com/ebookadmin/jfs/t1/119167/4/3130/132721/5ea68363E39425bab/57c198177edd7d71.jpg" href="./image/Images/cover.jpg" /></div></body></html>"""
    # bs = BeautifulSoup(str, 'html.parser')
    # print(bs.find('img')['src'])