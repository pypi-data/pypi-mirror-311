from codemod_json import parse_str

def test_basics():
    assert parse_str("2")._root == 2
    assert parse_str("1.2")._root == 1.2
    assert parse_str("\"x\"")._root == "x"
    assert parse_str("[1,2,3]")._root == [1, 2, 3]
    assert parse_str("{\"x\": \"y\"}")["x"] == "y"

def test_addition():
    doc = parse_str("[1,2,3]")
    doc._root.append(4)
    assert doc.text.decode("utf-8") == "[1, 2, 3, 4]"

def test_addition_discards_comments():
    doc = parse_str("[1,2,\n//foo\n3] // bar")
    doc._root.append(4)
    assert doc.text.decode("utf-8") == "[1, 2, 3, 4] // bar"

def test_object_value_modification():
    doc = parse_str('{\n"a": "b", // c1\n"c": "d" // c2\n} // c3')
    doc["c"] = "foo"
    assert doc.text.decode("utf-8") == '{\n"a": "b", // c1\n"c": "foo"\n} // c3'
