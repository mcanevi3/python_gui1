import webview

class Api:
    def test(self,arg):
        print(f"test arg: {arg}")

def main_loop(window):
    pass
def on_closing():
    print("Window is about to close")

window=webview.create_window('TestApp', 'assets/index.html',min_size=(400,300),js_api=Api())
window.events.closing+=on_closing
webview.start(func=main_loop,args=window,ssl=True)
pass
