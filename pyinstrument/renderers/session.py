import json

from pyinstrument.renderers.base import Renderer
from pyinstrument.session import Session


class SessionRenderer(Renderer):
    output_file_extension: str = "pyisession"

    def __init__(self, tree_format: bool = False):
        super().__init__()
        self.tree_format = tree_format

    def render(self, session: Session) -> str:
        return json.dumps(session.to_json())
