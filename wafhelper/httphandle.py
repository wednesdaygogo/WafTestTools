def update_http_request_content_len(request:str):
    # 以空行分割请求头和请求体
    if not request.startswith('POST') and not request.startswith('PUT'):
        return request
    request_lines = request.splitlines()
    #找到空行
    empty_line_index = request_lines.index('')
    #找到请求头
    headers = request_lines[:empty_line_index]
    #找到请求体
    body = request_lines[empty_line_index+1:]

    # 更新 content-length 字段
    body_str = '\r\n'.join(body)
    content_length = len(body_str.encode('utf-8'))
    for i, header in enumerate(headers):
        if header.startswith('Content-Length:'):
            headers[i] = 'Content-Length: ' + str(content_length)
            break
    else:
        headers.append('Content-Length: ' + str(content_length))

    # 拼接更新后的请求报文
    updated_request = '\r\n'.join(headers) + '\r\n\r\n' + body_str

    return updated_request
