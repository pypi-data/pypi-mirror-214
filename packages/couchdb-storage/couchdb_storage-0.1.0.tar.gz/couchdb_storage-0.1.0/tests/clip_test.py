import win32clipboard  # 获取剪贴板中的数据
win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
print(data)
win32clipboard.CloseClipboard()
