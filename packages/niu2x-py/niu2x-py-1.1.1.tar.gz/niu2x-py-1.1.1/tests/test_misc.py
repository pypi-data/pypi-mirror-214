import nxpy


def test_version():
    assert(str(nxpy.version) == "1.1.0")


def test_md5():
    assert(nxpy.md5("Hello".encode('utf-8')) ==
           "8b1a9953c4611296a827abf8c47804d7")


def test_fs():
    nxpy.write_utf8_file("test_tmp/a/b/c/utf8", "hello你好")
    nxpy.write_raw_file("test_tmp/a/b/c/raw", "hello你好".encode('utf-8'))
    assert(nxpy.md5_file('test_tmp/a/b/c/utf8')
           == nxpy.md5_file('test_tmp/a/b/c/raw'))
    nxpy.remove('test_tmp')
