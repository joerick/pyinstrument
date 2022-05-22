import json

from pyinstrument.renderers.base import Renderer
from pyinstrument.session import Session


class SessionRenderer(Renderer):
    output_file_extension: str = "pyisession"

    def render(self, session: Session) -> str:
        return json.dumps(session.to_json())
