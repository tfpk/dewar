from dewar import Site

site = Site()

@site.register('index.html')
def home():
    return "<h1>Hello</h1>"

@site.register('pages/<page>.html')
def pages():
    return {
        "page1": "<h1>This is page 1</h1>",
        "page2": "<h2>This is page 2</h2>"
    }

if __name__ == "__main__":
    site.render()
