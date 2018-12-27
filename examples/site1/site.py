from electrik import Electrik

k = Electrik()

@k.register_func('/index.html')
def home():
    return "<h1>Hello</h1>"

@k.register_func('/pages/<page>.html')
def pages():
    return {
        "page1": "<h1>This is page 1</h1>",
        "page2": "<h2>This is page 2</h2>"
    }

@k.register_func('/pages.html')
@k.register_dependency(pages)
def pages_index():
    return render_template('something.html', l=pages.values())

if __name__ == "__main__":
    k.render()
