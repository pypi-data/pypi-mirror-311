from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, Response
import httpx
from httpx import Headers
from typing import AsyncGenerator, Union
from urllib.parse import urlparse


def is_streaming(headers: Headers) -> bool:
    """
    判断响应是否为流式响应（如 Transfer-Encoding: chunked 或 Content-Length 不存在）。
    """
    if 'transfer-encoding' in headers and 'chunked' in headers['transfer-encoding'].lower():
        return True
    if 'content-length' not in headers:
        return True
    return False


async def stream_or_non_response_gen(url: str, headers: dict, body: dict) -> AsyncGenerator[Union[dict, bytes], None]:
    """流式 POST 请求, 返回一个异步生成器, 可以自动回退非流式响应"""
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", url, headers=headers, json=body, timeout=600) as response:
                if is_streaming(response.headers):
                    yield {
                        'stream': True,
                        'status_code': response.status_code,
                        'headers': response.headers,
                    }
                else:
                    yield {
                        'stream': False,
                        'status_code': response.status_code,
                        'headers': response.headers,
                        'content': await response.aread(),
                    }
                    return
                async for chunk in response.aiter_bytes():
                        yield chunk
        except httpx.RequestError as e:
            yield {
                'stream': False,
                'status_code': 502,
                'headers': None,
                'content': f"Error contacting upstream server: {e}",
            }


async def stream_or_non_post_request(url: str, headers: dict, body: dict) -> Union[StreamingResponse, Response]:
    """流式或非流式post请求"""
    headers['host'] = urlparse(url).netloc
    stream_gen = stream_or_non_response_gen(url, headers, body)
    first_chunk = await stream_gen.__anext__()
    
    if first_chunk['stream']:
        return StreamingResponse(
            content=stream_gen,
            status_code=first_chunk['status_code'],
            headers=first_chunk['headers'],
        )
    else:
        return Response(
            content=first_chunk['content'],
            status_code=first_chunk['status_code'],
            headers=first_chunk['headers'],
        )


async def get_header_and_body(request: Request) -> tuple[dict, dict]:
    headers = {k.lower(): v for k, v in request.headers.items()}
    for k in ['transfer-encoding', 'content-length']:
        if k in headers:
            del headers[k]
            
    try:
        body = await request.json()
    except BaseException as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON body: {e}")
    
    return headers, body


if __name__ == '__main__':
    app = FastAPI()

    @app.post("/{path:path}")
    async def post_proxy(path: str, request: Request):
        headers, body = await get_header_and_body(request)
        url = f"http://127.0.0.1:12345/{path}"
        return await stream_or_non_post_request(url, headers, body)
    
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=21237)
