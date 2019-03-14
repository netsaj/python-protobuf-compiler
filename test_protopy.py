# test_protopy.py

import pytest
import os


def test_build():
    out = os.system("protopy.py -o ./run_test -d ./test -p mytesting -v 1.0.1")
    assert os.path.exists(os.path.join(os.getcwd(),"run_test","mytesting-1.0.1.tar.gz")) == True



