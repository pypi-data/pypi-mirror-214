"""
Databases that are used by the Network :class:`~msl.network.manager.Manager`.
"""
import os
import sqlite3
from datetime import datetime

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .constants import DATABASE
from .constants import LOCALHOST_ALIASES
from .utils import _is_username_invalid_regex
from .utils import logger


class Database(object):

    def __init__(self, database, **kwargs):
        """Base class for connecting to a SQLite database.

        Automatically creates the database if it does not already exist.

        Parameters
        ----------
        database : :class:`str`
            The path to the database file, or ``':memory:'`` to open a
            connection to a database that resides in RAM instead of on disk.
        kwargs
            Optional keyword arguments to pass to :func:`sqlite3.connect`.
        """
        self._path = database if database is not None else DATABASE
        self._connection = None

        # open the connection to the database
        if self._path == ':memory:':
            logger.debug('creating a database in RAM')
        elif not os.path.isfile(self._path):
            logger.debug('creating a new database %s', self._path)
        else:
            logger.debug('opening %s', self._path)

        kwargs.setdefault('timeout', 60.0)

        self._connection = sqlite3.connect(self._path, **kwargs)
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def path(self):
        """:class:`str`: The path to the database file."""
        return self._path

    @property
    def connection(self):
        """:class:`sqlite3.Connection`: The connection object."""
        return self._connection

    @property
    def cursor(self):
        """:class:`sqlite3.Cursor`: The cursor object."""
        return self._cursor

    def __del__(self):
        self.close()

    def close(self):
        """Closes the connection to the database."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            try:
                logger.debug('closed %s', self._path)
            except (NameError, ValueError):
                # These errors could occur when Python is exiting
                #   ValueError: I/O operation on closed file
                #   NameError: name 'open' is not defined
                pass

    def execute(self, sql, parameters=None):
        """Wrapper around :meth:`sqlite3.Cursor.execute`.

        Parameters
        ----------
        sql : :class:`str`
            The SQL command to execute
        parameters : :class:`list`, :class:`tuple` or :class:`dict`, optional
            Only required if the `sql` command is parameterized.
        """
        if parameters is None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, parameters)

    def tables(self):
        """:class:`list` of :class:`str`: A list of the names of each table that is in the database."""
        self.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return sorted([t[0] for t in self._cursor.fetchall() if t[0] != 'sqlite_sequence'])

    def table_info(self, name):
        """Returns the information about each column in the specified table.

        Parameters
        ----------
        name : :class:`str`
            The name of the table to get the information of.

        Returns
        -------
        :class:`list` of :class:`tuple`
            The list of the fields in the table. The indices of each tuple correspond to:

            * 0 - id number of the column
            * 1 - the name of the column
            * 2 - the datatype of the column
            * 3 - whether a value in the column can be NULL (0 or 1)
            * 4 - the default value for the column
            * 5 - whether the column is used as a primary key (0 or 1)
        """
        self.execute(f'PRAGMA table_info({name!r});')
        return self._cursor.fetchall()

    def column_names(self, table_name):
        """Returns the names of the columns in the specified table.

        Parameters
        ----------
        table_name : :class:`str`
            The name of the table.

        Returns
        -------
        :class:`list` of :class:`str`
            A list of the names of each column in the table.
        """
        return [item[1] for item in self.table_info(table_name)]

    def column_datatypes(self, table_name):
        """Returns the datatype of each column in the specified table.

        Parameters
        ----------
        table_name : :class:`str`
            The name of the table.

        Returns
        -------
        :class:`list` of :class:`str`
            A list of the datatypes of each column in the table.
        """
        return [item[2] for item in self.table_info(table_name)]


class ConnectionsTable(Database):

    NAME = 'connections'
    """:class:`str`: The name of the table in the database."""

    def __init__(self, *, database=None, as_datetime=False, **kwargs):
        """The database table for devices that have connected to the Network
        :class:`~msl.network.manager.Manager`.

        Parameters
        ----------
        database : :class:`str`, optional
            The path to the database file, or ``':memory:'`` to open a
            connection to a database that resides in RAM instead of on disk.
            If :data:`None` then loads the default database.
        as_datetime : :class:`bool`, optional
            Whether to fetch the timestamps from the database as :class:`datetime.datetime`
            objects. If :data:`False` then the timestamps will be of type :class:`str`.
        kwargs
            Optional keyword arguments to pass to :func:`sqlite3.connect`.
        """
        if as_datetime and 'detect_types' not in kwargs:
            kwargs['detect_types'] = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

        super(ConnectionsTable, self).__init__(database, **kwargs)
        self.execute(f'CREATE TABLE IF NOT EXISTS {self.NAME} ('
                     f'pid INTEGER PRIMARY KEY AUTOINCREMENT, '
                     f'datetime DATETIME NOT NULL, '
                     f'ip_address TEXT NOT NULL, '
                     f'domain TEXT NOT NULL, '
                     f'port INTEGER NOT NULL, '
                     f'message TEXT NOT NULL);')
        self.connection.commit()

    def insert(self, peer, message):
        """Insert a message about what happened when a device connected.

        Parameters
        ----------
        peer : :class:`~msl.network.manager.Peer`
            The peer that connected to the Network :class:`~msl.network.manager.Manager`.
        message : :class:`str`
            The message about what happened (e.g, the connection was successful,
            or it failed).
        """
        now = datetime.now().replace(microsecond=0).isoformat(sep='T')
        self.execute(f'INSERT INTO {self.NAME} VALUES(NULL, ?, ?, ?, ?, ?);',
                     (now, peer.ip_address, peer.domain, peer.port, message))
        self.connection.commit()

    def connections(self, *, start=None, end=None):
        """Return the information of the devices that have connected to the
        Network :class:`~msl.network.manager.Manager`.

        .. versionchanged:: 1.0
           Use ``T`` as the separator between the date and time.
           Renamed `timestamp1` to `start`.
           Renamed `timestamp2` to `end`.

        Parameters
        ----------
        start : :class:`datetime.datetime` or :class:`str`, optional
            Include all records that have a timestamp :math:`\\ge` `start`.
            If a :class:`str` then in the ``yyyy-mm-dd`` or
            ``yyyy-mm-ddTHH:MM:SS`` format.
        end : :class:`datetime.datetime` or :class:`str`, optional
            Include all records that have a timestamp :math:`\\le` `end`.
            If a :class:`str` then in the ``yyyy-mm-dd`` or
            ``yyyy-mm-ddTHH:MM:SS`` format.

        Returns
        -------
        :class:`list` of :class:`tuple`
            The connection records.
        """
        pre = f'SELECT * FROM {self.NAME}'
        if start is None and end is None:
            self.execute(f'{pre};')
        elif start is not None and end is None:
            self.execute(f'{pre} WHERE timestamp >= ?;', (start,))
        elif start is None and end is not None:
            self.execute(f'{self.NAME} WHERE timestamp <= ?;', (end,))
        else:
            self.execute(f'{pre} WHERE timestamp >= ? AND timestamp <= ?;', (start, end))
        return self.cursor.fetchall()


class HostnamesTable(Database):

    NAME = 'auth_hostnames'
    """:class:`str`: The name of the table in the database."""

    def __init__(self, *, database=None, **kwargs):
        """The database table for trusted hostname's that are allowed to connect
        to the Network :class:`~msl.network.manager.Manager`.

        Parameters
        ----------
        database : :class:`str`, optional
            The path to the database file, or ``':memory:'`` to open a
            connection to a database that resides in RAM instead of on disk.
            If :data:`None` then loads the default database.
        kwargs
            Optional keyword arguments to pass to :func:`sqlite3.connect`.
       """
        super(HostnamesTable, self).__init__(database, **kwargs)
        self.execute(f'CREATE TABLE IF NOT EXISTS {self.NAME} '
                     f'(hostname TEXT NOT NULL, UNIQUE(hostname));')
        self.connection.commit()

        if not self.hostnames():
            for hostname in LOCALHOST_ALIASES:
                self.insert(hostname)

    def insert(self, hostname):
        """Insert a hostname.

        If the hostname is already in the table then it does not insert it again.

        Parameters
        ----------
        hostname : :class:`str`
            The trusted hostname.
        """
        self.execute(f'INSERT OR IGNORE INTO {self.NAME} VALUES(?);', (hostname,))
        self.connection.commit()

    def delete(self, hostname):
        """Delete a hostname.

        Parameters
        ----------
        hostname : :class:`str`
            A hostname in the table.

        Raises
        ------
        ValueError
            If `hostname` is not in the table.
        """
        # want to know if this hostname is not in the table
        if hostname not in self.hostnames():
            raise ValueError(f'Cannot delete {hostname!r}. This hostname is not in the table.')
        self.execute(f'DELETE FROM {self.NAME} WHERE hostname = ?;', (hostname,))
        self.connection.commit()

    def hostnames(self):
        """:class:`list` of :class:`str`: Returns all the trusted hostnames."""
        self.execute(f'SELECT * FROM {self.NAME};')
        return sorted([item[0] for item in self.cursor.fetchall()])


class UsersTable(Database):

    NAME = 'auth_users'
    """:class:`str`: The name of the table in the database."""

    def __init__(self, *, database=None, **kwargs):
        """The database table for keeping information about a users login credentials
        for connecting to a Network :class:`~msl.network.manager.Manager`.

        Parameters
        ----------
        database : :class:`str`, optional
            The path to the database file, or ``':memory:'`` to open a
            connection to a database that resides in RAM instead of on disk.
            If :data:`None` then loads the default database.
        kwargs
            Optional keyword arguments to pass to :func:`sqlite3.connect`.
        """
        super(UsersTable, self).__init__(database, **kwargs)
        self.execute(f'CREATE TABLE IF NOT EXISTS {self.NAME} ('
                     f'pid INTEGER PRIMARY KEY AUTOINCREMENT, '
                     f'username TEXT NOT NULL, '
                     f'key BLOB NOT NULL, '
                     f'salt BLOB NOT NULL, '
                     f'is_admin BOOLEAN NOT NULL, '
                     f'UNIQUE(username));')
        self.connection.commit()

        self._salt_size = 16
        self._length = 32
        self._iterations = 100000
        self._algorithm = hashes.SHA256()

    def insert(self, username, password, is_admin):
        """Insert a new user.

        The password is encrypted and stored in the database using PBKDF2_

        .. _PBKDF2: https://en.wikipedia.org/wiki/PBKDF2

        To update the values for a user use :meth:`update`.

        Parameters
        ----------
        username : :class:`str`
            The name of the user.
        password : :class:`str`
            The password of the user in plain-text format.
        is_admin : :class:`bool`
            Does this user have admin rights?

        Raises
        -------
        ValueError
            If the `username` is invalid or if `password` is empty.
        """
        if _is_username_invalid_regex.search(username) is not None:
            raise ValueError('A username cannot end with ":<integer>"')
        if not password:
            raise ValueError(f'You must specify a password for {username!r}')

        salt = os.urandom(self._salt_size)
        kdf = PBKDF2HMAC(
            algorithm=self._algorithm,
            length=self._length,
            salt=salt,
            iterations=self._iterations,
        )
        key = kdf.derive(password.encode())
        try:
            self.execute(f'INSERT INTO {self.NAME} VALUES(NULL, ?, ?, ?, ?);',
                         (username, key, salt, bool(is_admin)))
        except sqlite3.IntegrityError:
            raise ValueError(f'A user with the name {username!r} already exists') from None
        self.connection.commit()

    def update(self, username, *, password=None, is_admin=None):
        """Update either the salt used for the password and/or the admin rights.

        Parameters
        ----------
        username : :class:`str`
            The name of the user.
        password : :class:`str`, optional
            The password of the user in plain-text format.
        is_admin : :class:`bool`, optional
            Does this user have admin rights?

        Raises
        ------
        ValueError
            If `username` is not in the table.
            If both `password` and `is_admin` are not specified.
            If `password` is an empty string.
        """
        self._ensure_user_exists(username, 'update')

        if password is None and is_admin is None:
            raise ValueError('Must specify either the password and/or the admin rights when updating')

        if password is None:
            self.execute(f'UPDATE {self.NAME} SET is_admin=? WHERE username=?;',
                         (bool(is_admin), username))
            self.connection.commit()
            return

        if not password:
            raise ValueError(f'You must specify a password for {username!r}')

        salt = os.urandom(self._salt_size)
        key = PBKDF2HMAC(
            algorithm=self._algorithm,
            length=self._length,
            salt=salt,
            iterations=self._iterations,
        ).derive(password.encode())

        if is_admin is None:
            self.execute(f'UPDATE {self.NAME} SET key=?, salt=? WHERE username=?;',
                         (key, salt, username))
        else:
            self.execute(f'UPDATE {self.NAME} SET key=?, salt=?, is_admin=? WHERE username=?;',
                         (key, salt, bool(is_admin), username))

        self.connection.commit()

    def delete(self, username):
        """Delete a user.

        Parameters
        ----------
        username : :class:`str`
            The name of the user.

        Raises
        ------
        ValueError
            If `username` is not in the table.
        """
        self._ensure_user_exists(username, 'delete')
        self.execute(f'DELETE FROM {self.NAME} WHERE username = ?;', (username,))
        self.connection.commit()

    def get_user(self, username):
        """Get the information about a user.

        Parameters
        ----------
        username : :class:`str`
            The name of the user.

        Returns
        -------
        :class:`tuple`
            Returns (pid, username, key, salt, is_admin) for the specified `username`.
        """
        self.execute(f'SELECT * FROM {self.NAME} WHERE username = ?;', (username,))
        return self.cursor.fetchone()

    def records(self):
        """:class:`list` of :class:`tuple`: Returns [(pid, username, key, salt, is_admin), ...]
        for all users."""
        self.execute(f'SELECT * FROM {self.NAME};')
        return self.cursor.fetchall()

    def usernames(self):
        """:class:`list` of :class:`str`: Returns the names of all registered users."""
        self.execute(f'SELECT username FROM {self.NAME};')
        return [item[0] for item in self.cursor.fetchall()]

    def users(self):
        """:class:`list` of :class:`tuple`: Returns [(username, is_admin), ... ] for all users."""
        self.execute(f'SELECT username,is_admin FROM {self.NAME};')
        return sorted([(item[0], bool(item[1])) for item in self.cursor.fetchall()])

    def is_user_registered(self, username):
        """:class:`bool`: Whether `username` is a registered user."""
        self.execute(f'SELECT count(*) FROM {self.NAME} WHERE username = ?;', (username,))
        return bool(self.cursor.fetchone()[0])

    def is_password_valid(self, username, password):
        """Check whether the password matches the encrypted password in the database.

        Parameters
        ----------
        username : :class:`str`
            The name of the user.
        password : :class:`str`
            The password to check (in plain-text format).

        Returns
        -------
        :class:`bool`
            Whether `password` matches the password in the database for the user.
        """
        self.execute(f'SELECT key,salt FROM {self.NAME} WHERE username = ?;', (username,))
        key_salt = self._cursor.fetchone()
        if not key_salt:
            return False
        kdf = PBKDF2HMAC(
            algorithm=self._algorithm,
            length=self._length,
            salt=key_salt[1],
            iterations=self._iterations,
        )
        try:
            kdf.verify(password.encode(), key_salt[0])
            return True
        except InvalidKey:
            return False

    def is_admin(self, username):
        """Check whether a user has admin rights.

        Parameters
        ----------
        username : :class:`str`
            The name of the user.

        Returns
        -------
        :class:`bool`
            Whether the user has admin rights.
        """
        self.execute(f'SELECT is_admin FROM {self.NAME} WHERE username = ?;', (username,))
        user = self.cursor.fetchone()
        if user:
            return bool(user[0])
        return False

    def _ensure_user_exists(self, username, action):
        # want to know if this user is not in the table
        if username not in self.usernames():
            raise ValueError(
                f'Cannot {action} {username!r}. '
                f'This user is not in the table.'
            )


def convert_datetime(value):
    """Convert a date and time to a :class:`~datetime.datetime` object.

    Parameters
    ----------
    value : :class:`bytes`
        The datetime value from an SQLite database.

    Returns
    -------
    :class:`datetime.datetime`
        The `value` as a datetime object.
    """
    try:
        # datetime.fromisoformat is available in Python 3.7+
        return datetime.fromisoformat(value.decode())
    except AttributeError:
        # mimics the sqlite3.dbapi2.convert_timestamp function
        datepart, timepart = value[:10], value[11:]
        year, month, day = map(int, datepart.split(b'-'))
        timepart_full = timepart.split(b'.')
        hours, minutes, seconds = map(int, timepart_full[0].split(b':'))
        if len(timepart_full) == 2:
            microseconds = int(f'{timepart_full[1].decode():0<6.6}')
        else:
            microseconds = 0
        return datetime(year, month, day, hours, minutes, seconds, microseconds)


# Do not use the builtin TIMESTAMP converter since it does not support
# the T separator between the date and time. Also, according to
# https://www.sqlite.org/lang_datefunc.html the name DATETIME seems
# to be more logical than TIMESTAMP as a field name.
sqlite3.register_converter('DATETIME', convert_datetime)
