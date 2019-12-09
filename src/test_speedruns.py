from src import get_speedruns
from datetime import datetime as dt
from datetime import timedelta

def test_is_new_wr():
    print("GOOD")
    today = dt.today()
    good_wr = today - timedelta(days=3)
    bad_wr = today - timedelta(days=8)

    assert(get_speedruns.is_new_wr(good_wr))
    assert(not get_speedruns.is_new_wr(bad_wr))

if __name__ == '__main__':
    test_is_new_wr()