from fastapi import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from importlib.metadata import version

from amcat4 import elastic
from amcat4.api.auth import get_middlecat_config
from amcat4.config import get_settings

templates = Jinja2Templates(directory="templates")

app_info = APIRouter(tags=["informational"])


@app_info.get("/")
def index(request: Request):
    host = get_settings().host
    es_alive = elastic.ping()
    auth = get_settings().auth
    has_admin_email = bool(get_settings().admin_email)
    middlecat_url = get_settings().middlecat_url
    middlecat_alive = False
    api_version = version("amcat4")
    if middlecat_url:
        try:
            get_middlecat_config(middlecat_url)
            middlecat_alive = True
        except OSError:
            pass
    return templates.TemplateResponse("index.html", locals())
