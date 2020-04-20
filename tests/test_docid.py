import pytest
from os_docid import docid


def test_from_url():
    test_data = [
        (
            "http://www.google.com/",
            "1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd",
        ),
        (
            "http://www.google.com",
            "1d5920f4b44b27a8-ed646a3334ca891f-ed646a3334ca891fd3467db131372140",
        ),
        (
            "http://www.google.com.hk/abc",
            "da90da7194dbc779-a735b82241adc4d2-d896d112b3ee45903c11a2cf67d4059f",
        ),
        (
            "http://abcint.cn/",
            "b0236e4c461a7416-dd4b201bc72e5660-6d7f1e7cd2b2adf7b1874094404c014d",
        ),
    ]
    for url, expected in test_data:
        assert str(docid(url)) == expected


def test_from_docid():
    test_data = [
        (
            "1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd",
            "1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd",
        ),
        (
            "1d5920f4b44b27a8ed646a3334ca891fff90821feeb2b02a33a6f9fc8e5f3fcd",
            "1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd",
        ),
    ]
    for data, expected in test_data:
        assert str(docid(data)) == expected


def test_invalid_data():
    test_data = [
        "30b30b6c3013fff8-3c29e52969d51cf5-2e8873d882b4eb4b73b35f5214d2e9d",
        "abc",
    ]
    for data in test_data:
        with pytest.raises(NotImplementedError):
            docid(data)


def test_equal():
    url = "http://g.com/"
    assert docid(url) == docid(url)
    assert docid(url) != docid(url + "a")


def test_benchmark_docid(benchmark):
    result = benchmark(docid, "http://www.google.com/")
    assert (
        str(result)
        == "1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd"
    )
