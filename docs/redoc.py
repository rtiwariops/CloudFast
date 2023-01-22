from starlette.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html

def get_redoc_html(
    *,
    openapi_url: str,
    title: str,
    version: str,
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
        }}
        </style>
        <title>{title}</title>
    </head>
    <body>
        <div id="redoc-container"></div>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"> </script>
        <script src="https://cdn.jsdelivr.net/gh/wll8/redoc-try@1.4.1/dist/try.js"></script>

        <script type="text/javascript">
            initTry({{
                openApi: `{openapi_url}`,
                redocOptions: {{scrollYOffset: 50}},
            }})
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

def setup_redoc(app):
    @app.get("/doc", include_in_schema=False)  
    async def redoc_try_it_out() -> HTMLResponse:  
        title = "CloudFast"
        version = "1.01"
        return get_redoc_html(openapi_url=app.openapi_url, title=title, version=version)
