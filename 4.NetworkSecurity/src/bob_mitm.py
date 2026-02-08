from mitmproxy import http
def response(flow: http.HTTPFlow) -> None:
    if "This is Bob's web server!" in flow.response.get_text():
        flow.response.set_text("This is not Bob!")
        print("Content modified successfully!")
    pass
