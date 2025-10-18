def process_sig(app, what, name, obj, options, signature, return_annotation):
    if "HTMLRenderer" in name:
        signature = "()"
    return (signature, return_annotation)


def setup(app):
    app.connect("autodoc-process-signature", process_sig)
