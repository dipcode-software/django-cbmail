from tempfile import NamedTemporaryFile


def create_attachment():
    """
    Create temporary file to be used on test
    """
    f = NamedTemporaryFile()
    f.write('unit test')
    f.seek(0)
    attachment = open(f.name, 'rb')
    return [('test.txt', attachment.read(), 'text/plain')]
