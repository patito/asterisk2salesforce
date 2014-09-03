from app import AsteriskHandler

if __name__ == '__main__':
    ast = AsteriskHandler()
    ast.connect()
    ast.subscribe_cdr_event()
    ast.get_all_extensions()
    ast.loop()
