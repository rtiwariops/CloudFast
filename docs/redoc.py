from starlette.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html

def get_redoc_html(
    *,
    openapi_url: str,
    title: str,
    redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: bool = True,
) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
     <head>
    <meta charset="utf-8" />
    <link rel="shortcut icon" href="./favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
    <style>
      body {{
        margin: 0;
        padding: 0;
        background-color: '#ffffff';
      }}
    </style>
    <title>OpenAPI Specification</title>
  </head>
        <body>
            <noscript>You need to enable JavaScript to run this app.</noscript>
            <div id="redoc-container"></div>
            <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
            <script type="text/javascript">
            (function() {{
            Redoc.init(
                "https://pointnet.github.io/redoc-editor/openapi.yaml",
                {{
                "untrustedSpec" : true
                }},
                document.getElementById('redoc-container'))
            }})();
            </script>
        </body>
        </html>
    """
    return HTMLResponse(html)

def setup_redoc(app):
    @app.get("/doc", include_in_schema=False)  
    async def redoc_try_it_out() -> HTMLResponse:  
        title = app.title + ""  
        return get_redoc_html(openapi_url=app.openapi_url, title=title)
