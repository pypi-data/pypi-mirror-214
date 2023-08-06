try:
    import win32clipboard  # 获取剪贴板中的数据
except ImportError:
    pass

from .base_node import BaseNode


class WindowsNode(BaseNode):
    def get_clipboard_file_list(self):
        win32clipboard.OpenClipboard()
        try:
            data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            print(data)
        except:
            data = []
        win32clipboard.CloseClipboard()
        return data
