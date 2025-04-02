import webview

def main_loop(window):
    window.move(10,10)
    window.resize(200,200)
    window.minimize()
def on_closing():
    print("Window is about to close")

window=webview.create_window('Hello world', 'https://pywebview.flowrl.com/')
window.events.closing+=on_closing
webview.start(main_loop,window)
pass
