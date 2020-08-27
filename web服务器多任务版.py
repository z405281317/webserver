import socket
import threading
import os

def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定ip and port
    tcp_socket.bind(("", 443))
    # listen   128表示最大等待数
    tcp_socket.listen(128)
    # 循环等待客户端的连接
    while True:
        # 等待client 的连接请求  会返回一个新的socket连接 和 client 的ip
        new_socket, ip = tcp_socket.accept()
        # 接受客户端的请求
        recv_data = new_socket.recv(4096)
        # 对request的信息 解码
        recv_content = recv_data.decode("utf-8")
        print(recv_content)
        # 分割request请求   获取请求路径
        request_list = recv_content.split(" ", maxsplit=2)
        request_path = request_list[1]
        print('请求路径：' + request_path)

        if request_path == "/":
            request_path = "/index.html"
        #os.path.exists("./static"+request_path)
        try:
            # 打开index 文件
            with open("./static" + request_path, "rb") as file:  # 这里的 file 代表打开这个文件的对象
                file_data = file.read()
            # with open 作用 是  可以不用 open.close 来关闭文件  程序自动帮你关闭
        except Exception as msg:
             #代码执行到此 说明没有所请求的文件‘
             # 响应行
             respones_line = "HTTP/1.1 404 Not Found \r\n"
             # 响应头
             respones_header = "Server: pythonServer \r\n"
             # 空行
             # 响应体
             # 打开index 文件
             with open("./static/error.html", "rb") as file:  # 这里的 file 代表打开这个文件的对象
                 file_data = file.read()
             # with open 作用 是  可以不用 open.close 来关闭文件  程序自动帮你关闭
             respones_body = file_data
             # 要把返回的数据封装成 http 响应报文 格式
             respones = (respones_line + respones_header + "\r\n").encode("utf-8") + respones_body
             new_socket.send(respones)
        else:
            # 响应行
            respones_line = "HTTP/1.1 200 OK \r\n"
            # 响应头
            respones_header = "Server: pythonServer \r\n"
            # 空行
            # 响应体
            respones_body = file_data

            # 要把返回的数据封装成 http 响应报文 格式
            respones = (respones_line + respones_header + "\r\n").encode("utf-8") + respones_body
            new_socket.send(respones)
        finally:
            # close socket
            new_socket.close()


def create_socket(new_socket,ip):
    print("客户端ip："+ip[0])
    # 接受客户端的请求
    recv_data = new_socket.recv(4096)
    # 对request的信息 解码
    recv_content = recv_data.decode("utf-8")
    print("request请求\r\n"+recv_content)
    # 分割request请求   获取请求路径
    request_list = recv_content.split(" ", maxsplit=2)
    request_path = request_list[1]
    print('请求路径：' + request_path)

    if request_path == "/":
        request_path = "/index.html"
    # os.path.exists("./static"+request_path)
    try:
        # 打开index 文件
        with open("./static" + request_path, "rb") as file:  # 这里的 file 代表打开这个文件的对象
            file_data = file.read()
        # with open 作用 是  可以不用 open.close 来关闭文件  程序自动帮你关闭
    except Exception as msg:
        # 代码执行到此 说明没有所请求的文件‘
        # 响应行
        respones_line = "HTTP/1.1 404 Not Found \r\n"
        # 响应头
        respones_header = "Server: pythonServer \r\n"
        # 空行
        # 响应体
        # 打开index 文件
        with open("./static/error.html", "rb") as file:  # 这里的 file 代表打开这个文件的对象
            file_data = file.read()
        # with open 作用 是  可以不用 open.close 来关闭文件  程序自动帮你关闭
        respones_body = file_data
        # 要把返回的数据封装成 http 响应报文 格式
        respones = (respones_line + respones_header + "\r\n").encode("utf-8") + respones_body
        new_socket.send(respones)
    else:
        # 响应行
        respones_line = "HTTP/1.1 200 OK \r\n"
        # 响应头
        respones_header = "Server: pythonServer \r\n"
        # 空行
        # 响应体
        respones_body = file_data

        # 要把返回的数据封装成 http 响应报文 格式
        respones = (respones_line + respones_header + "\r\n").encode("utf-8") + respones_body
        new_socket.send(respones)
    finally:
        # close socket
        new_socket.close()

    pass





if __name__ == '__main__':
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    # 绑定ip and port
    tcp_socket.bind(("", 8080))
    # listen   128表示最大等待数
    tcp_socket.listen(128)
    # 循环等待客户端的连接
    # 等待client 的连接请求  会返回一个新的socket连接 和 client 的ip
    while True:
        new_socket, ip = tcp_socket.accept()

        sub_threading=threading.Thread(target=create_socket,args=(new_socket,ip))
        sub_threading.setDaemon(True)
        sub_threading.start()
