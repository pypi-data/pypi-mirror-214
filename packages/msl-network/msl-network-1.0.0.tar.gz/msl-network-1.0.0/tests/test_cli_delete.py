import os
import shutil
import tempfile

from msl.network import cli

N = 10
ROOT_DIR = os.path.join(tempfile.gettempdir(), 'msl-io-testing')


def get_args(*args):
    parser = cli.configure_parser()
    command = ['delete', '--root', ROOT_DIR, '--yes'] + list(args)
    return parser.parse_args(command)


def create_files():
    if os.path.isdir(ROOT_DIR):
        shutil.rmtree(ROOT_DIR)
    for folder, ext in [('certs', '.crt'), ('keys', '.key'), ('logs', '.log')]:
        directory = os.path.join(ROOT_DIR, folder)
        os.makedirs(directory)
        for i in range(N):
            file = os.path.join(directory, f'{i}{ext}')
            with open(file, mode='w') as fp:
                fp.write('whatever')
        with open(os.path.join(directory, 'remains.txt'), mode='w') as fp:
            fp.write('whatever')
    with open(os.path.join(ROOT_DIR, 'manager.sqlite3'), mode='w') as fp:
        fp.write('whatever')
    with open(os.path.join(ROOT_DIR, 'remains.txt'), mode='w') as fp:
        fp.write('whatever')


# use the capsys fixture of pytest to assert stdout messages
# https://docs.pytest.org/en/6.2.x/reference.html#capsys
def test_database(capsys):
    create_files()

    args = get_args('--database')

    assert not args.all
    assert not args.certs
    assert args.database
    assert not args.keys
    assert not args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f"[Deleted] {os.path.join(ROOT_DIR, 'manager.sqlite3')}" in out

    # the database file is gone, but all other files remain
    assert not os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_logs(capsys):
    create_files()

    args = get_args('--logs')

    assert not args.all
    assert not args.certs
    assert not args.database
    assert not args.keys
    assert args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f'{N} log file(s) will be deleted' in out

    # the .log files are gone, but all other files remain
    assert os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_certs(capsys):
    create_files()

    args = get_args('--certs')

    assert not args.all
    assert args.certs
    assert not args.database
    assert not args.keys
    assert not args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f'{N} certificate(s) will be deleted' in out

    # the .crt files are gone, but all other files remain
    assert os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_keys(capsys):
    create_files()

    args = get_args('--keys')

    assert not args.all
    assert not args.certs
    assert not args.database
    assert args.keys
    assert not args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f'{N} key(s) will be deleted' in out

    # the .key files are gone, but all other files remain
    assert os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_all(capsys):
    create_files()

    args = get_args('--all')

    assert args.all
    assert not args.certs
    assert not args.database
    assert not args.keys
    assert not args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f"[Deleted] {os.path.join(ROOT_DIR, 'manager.sqlite3')}" in out
    assert f'{N} log file(s) will be deleted' in out
    assert f'{N} certificate(s) will be deleted' in out
    assert f'{N} key(s) will be deleted' in out

    # all files are gone
    assert not os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # but the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_keys_logs(capsys):
    create_files()

    args = get_args('--keys', '--logs')

    assert not args.all
    assert not args.certs
    assert not args.database
    assert args.keys
    assert args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f'{N} key(s) will be deleted' in out
    assert f'{N} log file(s) will be deleted' in out

    # all .key and .log files are gone
    assert os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # but the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_database_certs(capsys):
    create_files()

    args = get_args('--database', '--certs')

    assert not args.all
    assert args.certs
    assert args.database
    assert not args.keys
    assert not args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, _ = capsys.readouterr()
    assert f"[Deleted] {os.path.join(ROOT_DIR, 'manager.sqlite3')}" in out
    assert f'{N} certificate(s) will be deleted' in out

    # all .crt files are gone as well as the database
    assert not os.path.isfile(os.path.join(ROOT_DIR, 'manager.sqlite3'))
    for i in range(N):
        assert not os.path.isfile(os.path.join(ROOT_DIR, 'certs', f'{i}.crt'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', f'{i}.key'))
        assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', f'{i}.log'))

    # but the remains.txt files still exist
    assert os.path.isfile(os.path.join(ROOT_DIR, 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'certs', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'keys', 'remains.txt'))
    assert os.path.isfile(os.path.join(ROOT_DIR, 'logs', 'remains.txt'))

    # clean up
    shutil.rmtree(ROOT_DIR)


def test_no_args(capsys):
    args = get_args()

    assert not args.all
    assert not args.certs
    assert not args.database
    assert not args.keys
    assert not args.logs
    assert args.root == ROOT_DIR
    assert not args.quiet
    assert args.yes

    # execute command
    args.func(args)

    out, err = capsys.readouterr()
    assert out.startswith('You must specify what you want to delete')
    assert not err


def test_not_a_directory(capsys):
    try:
        shutil.rmtree(ROOT_DIR)
    except:
        pass

    args = get_args('--logs')
    args.func(args)

    out, err = capsys.readouterr()
    assert out.rstrip() == f'The {ROOT_DIR!r} directory does not exist'
    assert not err


def test_no_files(capsys):
    try:
        shutil.rmtree(ROOT_DIR)
    except:
        pass

    os.makedirs(ROOT_DIR)
    args = get_args('--all')
    args.func(args)

    out, err = capsys.readouterr()
    assert not err
    assert out.splitlines() == [
        'No database file found',
        '',
        'Searching for certificates ... no certificates found',
        '',
        'Searching for keys ... no keys found',
        '',
        'Searching for log files ... no log files found',
    ]

    # cleanup
    shutil.rmtree(ROOT_DIR)
