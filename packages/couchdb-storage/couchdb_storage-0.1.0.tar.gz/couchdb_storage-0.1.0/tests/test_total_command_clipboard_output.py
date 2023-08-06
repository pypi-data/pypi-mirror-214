from couchdb_storage.termux_node import parse_total_cmd_clipboard_file_list

if __name__ == "__main__":
    d = """
Total commander file list (copy)
Total files: 3
/storage/emulated/0/DCIM
eInvoice - 2023-03-05T004233.579.png	143337	2023-04-15 12:55:35
eInvoice (1) - 2023-03-05T004254.753.png	153777	2023-04-15 12:55:35
eInvoice (2) - 2023-03-05T004314.743.png	134122	2023-04-15 12:55:35
    """
    f = parse_total_cmd_clipboard_file_list(d)
    print(f)
