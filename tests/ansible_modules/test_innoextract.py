import os
import pytest
import shutil

from pathlib import Path

from helpers import (
    set_module_args,
)

from tests.conftest import (
    AnsibleExitJson,
    AnsibleFailJson,
)

from acme.library import (
    innoextract,
)

BASE_PATH = Path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

DEST_PATH = Path("/tmp/yag-test/innoextract")
INSTALLER = BASE_PATH / "data" / "innosetup-6.0.3.exe"
CREATES_PATH = DEST_PATH / "app" / "ISCC.exe"


def test_invalid_arg(mock_ansible_module):
    with pytest.raises(AnsibleFailJson):
        set_module_args({
            'installer': INSTALLER,
            'dest': DEST_PATH,
            'fooooooooooooo': True
        })
        innoextract.main()


def test_required_arg_missing(mock_ansible_module):
    with pytest.raises(AnsibleFailJson):
        set_module_args({})
        innoextract.main()


def test_extract(mock_ansible_module):
    shutil.rmtree(DEST_PATH, ignore_errors=True)
    assert (not DEST_PATH.exists())

    assert(INSTALLER.exists())

    set_module_args({
        'installer': INSTALLER,
        'dest': DEST_PATH,
        'creates': CREATES_PATH
    })
    with pytest.raises(AnsibleExitJson) as result:
        innoextract.main()
    result = result.value.args[0]
    assert (result['changed'])
    assert (CREATES_PATH.exists())

    with pytest.raises(AnsibleExitJson) as result:
        innoextract.main()
    result = result.value.args[0]
    assert (not result['changed'])
    assert (CREATES_PATH.exists())
