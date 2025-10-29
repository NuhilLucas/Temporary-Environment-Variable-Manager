from .api import api

_api_ = api()

def runGUI():
    from webview import create_window, start
    from tevm.instance import Path_HTML

    create_window(
        title="TEVM",
        url=f'file://{Path_HTML}',
        js_api=_api_,
        width=1300,
        height=665,
        resizable=False
    )

    start(
        gui="edgechromium",
        # debug=True
    )