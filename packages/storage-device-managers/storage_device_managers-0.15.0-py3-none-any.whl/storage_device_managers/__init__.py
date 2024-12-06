from __future__ import annotations

import contextlib
import enum
import secrets
import string
import typing as t
from collections import defaultdict
from importlib import metadata
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Iterator, Optional, Union
from uuid import UUID, uuid4

import shell_interface as sh

try:
    from loguru import logger  # type: ignore[import, unused-ignore]

    logger.disable("storage_device_managers")
except ModuleNotFoundError:
    logger = SimpleNamespace()  # type: ignore[assignment, unused-ignore]
    logger.success = lambda msg: None  # type: ignore[assignment, unused-ignore]
    logger.info = lambda msg: None  # type: ignore[assignment, unused-ignore]

__version__ = metadata.version(__name__)


class DeviceDecryptionError(RuntimeError):
    pass


class InvalidDecryptedDevice(ValueError):
    pass


class UnmountError(RuntimeError):
    pass


class ValidCompressions(enum.Enum):
    LZO = "lzo"
    ZLIB = "zlib"
    ZLIB1 = "zlib:1"
    ZLIB2 = "zlib:2"
    ZLIB3 = "zlib:3"
    ZLIB4 = "zlib:4"
    ZLIB5 = "zlib:5"
    ZLIB6 = "zlib:6"
    ZLIB7 = "zlib:7"
    ZLIB8 = "zlib:8"
    ZLIB9 = "zlib:9"
    ZSTD = "zstd"
    ZSTD1 = "zstd:1"
    ZSTD2 = "zstd:2"
    ZSTD3 = "zstd:3"
    ZSTD4 = "zstd:4"
    ZSTD5 = "zstd:5"
    ZSTD6 = "zstd:6"
    ZSTD7 = "zstd:7"
    ZSTD8 = "zstd:8"
    ZSTD9 = "zstd:9"
    ZSTD10 = "zstd:10"
    ZSTD11 = "zstd:11"
    ZSTD12 = "zstd:12"
    ZSTD13 = "zstd:13"
    ZSTD14 = "zstd:14"
    ZSTD15 = "zstd:15"


@contextlib.contextmanager
def decrypted_device(device: Path, pass_cmd: str) -> Iterator[Path]:
    """Decrypt a given device using pass_cmd

    Given a device and a shell command that outputs a password on STDOUT, this
    context manager will open the device using `cryptsetup`. Upon exit, the
    device is closed again.


    Note that pass_cmd will directly be executed in a subshell. Therefore, DO NOT
    USE UNTRUSTED `pass_cmd`!

    Parameters:
    -----------
    device
        file-like object to be opened with `cryptsetup`
    pass_cmd
        command that prints the device's password on STDOUT

    Returns:
    --------
    Path
        destination of opened device

    Raises:
    -------
    DeviceDecryptionError
        if cryptsetup returns a non-zero exit code
    """
    decrypted = open_encrypted_device(device, pass_cmd)
    logger.success(f"Speichermedium {device} erfolgreich entschlüsselt.")
    try:
        yield decrypted
    finally:
        close_decrypted_device(decrypted)
        logger.success(
            f"Verschlüsselung des Speichermediums {device} erfolgreich geschlossen."
        )


@contextlib.contextmanager
def mounted_device(
    device: Path, compression: Optional[ValidCompressions] = None
) -> Iterator[Path]:
    """Mount a given BtrFS device

    Given a path pointing to a file-like object, this context manager will
    mount it to some temporary directory and return its path. Upon exit, the
    file-like object is unmounted again.

    The filesystem of `device` must be BtrFS. While technically other file
    systems might work too, this behaviour is not guaranteed and might be
    broken without further notice!

    If `compression` is provided, a mount option specifying the transparent
    file system compression is set.

    Parameters:
    -----------
    device
        file-like object to be mounted
    compression
        compression level to be used by BtrFS

    Returns:
    --------
    Path
        directory to which `device` was mounted
    """
    if is_mounted(device):
        unmount_device(device)
    with TemporaryDirectory() as td:
        mount_dir = Path(td)
        mount_btrfs_device(device, Path(mount_dir), compression)
        logger.success(
            f"Speichermedium {device} erfolgreich nach {mount_dir} gemountet."
        )
        try:
            yield Path(mount_dir)
        finally:
            unmount_device(device)
            logger.success(f"Speichermedium {device} erfolgreich ausgehangen.")


@contextlib.contextmanager
def symbolic_link(src: Path, dest: Path) -> Iterator[Path]:
    """Create a symbolic link from `src` to `dest`

    This context manager will create a symbolic link from src to dest. It
    differentiates itself from `Path.link_to()` by …:

        * … creating the link with root privileges. This allows to limit root
          permissions to only the necessary parts of the program.

        * … ensuring that the link gets removed after usage.

    Parameters:
    -----------
    src: Path to source; can be anything that has a filesystem path
    dest: Path to destination file

    Returns:
    --------
    Path
        The value of `dest.absolute()` will be returned.
    """

    if not src.exists():
        raise FileNotFoundError
    if dest.exists():
        raise FileExistsError
    absolute_dest = dest.absolute()
    ln_cmd: sh.StrPathList = ["sudo", "ln", "-s", src.absolute(), absolute_dest]
    sh.run_cmd(cmd=ln_cmd)
    logger.success(f"Symlink von {src} nach {dest} erfolgreich erstellt.")
    try:
        yield absolute_dest
    finally:
        # In case the link destination vanished, the program must not crash. After
        # all, the aimed for state has been reached.
        rm_cmd: sh.StrPathList = ["sudo", "rm", "-f", absolute_dest]
        sh.run_cmd(cmd=rm_cmd)
        logger.success(f"Symlink von {src} nach {dest} erfolgreich entfernt.")


def mount_btrfs_device(
    device: Path, mount_dir: Path, compression: Optional[ValidCompressions] = None
) -> None:
    """
    Mount a given BtrFS device

    Given a path pointing to a file-like object and a target directory, this function
    will mount the device to the target directory.

    The filesystem of `device` must be BtrFS. While technically other file systems
    might work too, this behaviour is not guaranteed and might be broken without
    further notice!

    If `compression` is provided, a mount option specifying the transparent file
    system compression is set.

    Parameters:
    -----------
    device
        file-like object to be mounted
    mount_dir
        directory to which `device` is mounted
    compression
        compression level to be used by BtrFS
    """
    cmd: sh.StrPathList = [
        "sudo",
        "mount",
        device,
        mount_dir,
    ]
    if compression is not None:
        cmd.extend(["-o", f"compress={compression.value}"])
    sh.run_cmd(cmd=cmd)


def is_mounted(device: Path) -> bool:
    """Check whether a given device is mounted

    Parameters:
    -----------
    device
        file-like object to be checked

    Returns:
    --------
    bool
        True if `device` is mounted, False otherwise
    """
    device_as_str = str(device)
    try:
        mount_dest = get_mounted_devices()[device_as_str]
        logger.info(f"Mount des Speichermediums {device} in {mount_dest} gefunden.")
    except KeyError:
        logger.info(f"Kein Mountpunkt für Speichermedium {device} gefunden.")
        return False
    return True


def get_mounted_devices() -> t.Mapping[str, t.Mapping[Path, frozenset[str]]]:
    """Get all mounted devices

    This function will parse the output of `mount` and return everything that
    is mounted to somewhere. Since a source can be mounted to multiple
    destinations, the return value is a dictionary mapping device names to sets
    of mount points.

    Returns:
    --------
    t.Mapping[str, t.Mapping[Path, frozenset[str]]]
        A mapping that maps mount sources (i.e. device names) to their
        destinations and mount options.
    """
    # Example line:
    # /dev/nvme0n1p2 on /boot type ext2 (rw,relatime)
    raw_mounts = sh.run_cmd(cmd=["mount"], capture_output=True)
    mount_lines = raw_mounts.stdout.decode().splitlines()
    mount_points: dict[str, dict[Path, frozenset[str]]] = defaultdict(dict)
    for line in mount_lines:
        device = line.split()[0]
        dest = Path(line.split()[2])
        raw_options = line.split()[5]
        options = frozenset(raw_options.strip("()").split(","))
        mount_points[device][dest] = options
    return dict(mount_points)


def unmount_device(device: Path) -> None:
    """Unmount a given device

    This function will unmount a given device. It relies on the system's
    `umount` programm to do so.

    Parameters:
    -----------
    device
        The device to be unmounted.

    Raises:
    -------
    UnmountError
        if `umount` returns a non-zero exit code
    """
    cmd: sh.StrPathList = ["sudo", "umount", device]
    try:
        sh.run_cmd(cmd=cmd)
    except sh.ShellInterfaceError as e:
        raise UnmountError from e


def open_encrypted_device(device: Path, pass_cmd: str) -> Path:
    """Open an encrypted device

    This function will open an encrypted device. The given path must point to a
    device that can be opened by `cryptsetup`.

    In order to encrypt the device, `pass_cmd` is executed and its output is
    piped into `cryptsetup`. This allows to use any program that can output
    the password to decrypt the device.

    Note that pass_cmd will directly be executed in a subshell. Therefore, DO NOT
    USE UNTRUSTED `pass_cmd`!

    Parameters:
    -----------
    device
        The device to be opened.
    pass_cmd
        The command that outputs the password to decrypt the device.

    Raises:
    -------
    DeviceDecryptionError
        if cryptsetup returns a non-zero exit code
    """
    map_name = device.name
    decrypt_cmd: sh.StrPathList = ["sudo", "cryptsetup", "open", device, map_name]
    try:
        sh.pipe_pass_cmd_to_real_cmd(pass_cmd, decrypt_cmd)
    except sh.ShellInterfaceError as e:
        raise DeviceDecryptionError from e
    return Path("/dev/mapper/") / map_name


def close_decrypted_device(device: Path) -> None:
    """Close a decrypted device

    This function will try to close a device that was previously opened by
    `cryptsetup`. The given path must point into `/dev/mapper`, because
    `cryptsetup` always opens devices into there. If the given path points
    somewhere else, a InvalidDecryptedDevice is raised.

    Parameters:
    -----------
    device
        The device do be closed.

    Raises:
    -------
    InvalidDecryptedDevice
        if `device` does not point into `/dev/mapper`
    shell_interface.ShellInterfaceError
        if the exit code of the close command is non-zero
    """
    if device.parent != Path("/dev/mapper"):
        raise InvalidDecryptedDevice
    map_name = device.name
    close_cmd = ["sudo", "cryptsetup", "close", map_name]
    sh.run_cmd(cmd=close_cmd)


def encrypt_device(device: Path, password_cmd: str) -> UUID:
    """Encrypt a device

    This function will encrypt a device. The device can be any valid file-like
    object like real devices in `/dev/` or suitably sized files in $HOME.

    In order to retrieve the necessary password, the input `password_cmd` is
    executed in a subshell and its STDOUT used as password. Therefore, DO NOT
    USE UNTRUSTED `password_cmd`!

    In order to obtain a safe password_cmd, refer to `generate_passcmd`.

    Parameters:
    -----------
    device
        file-like object to be encrypted
    password_cmd
        Shell command that prints the password to be used to STDOUT

    Returns:
    --------
    UUID
        UUID of the new LUKS partition
    """
    new_uuid = uuid4()
    format_cmd: sh.StrPathList = [
        "sudo",
        "cryptsetup",
        "luksFormat",
        "--uuid",
        str(new_uuid),
        device,
    ]
    sh.pipe_pass_cmd_to_real_cmd(pass_cmd=password_cmd, command=format_cmd)
    return new_uuid


def mkfs_btrfs(device: Path) -> None:
    """Format device with BtrFS

    Parameters:
    -----------
    device
        file-like object to be formatted
    """

    cmd: sh.StrPathList = ["sudo", "mkfs.btrfs", device]
    sh.run_cmd(cmd=cmd)


def generate_passcmd() -> str:
    """
    Generate `echo` safe password and return PassCmd

    Returns
    -------
    str
        password command producing the password
    """
    n_chars = 16
    alphabet = string.ascii_letters + string.digits
    passphrase = "".join(secrets.choice(alphabet) for _ in range(n_chars))
    return f"echo {passphrase}"


def chown(
    file_or_folder: Path,
    /,
    user: Union[int, str],
    group: Optional[Union[int, str]] = None,
    *,
    recursive: bool,
) -> None:
    """Change user and group of a device or folder

    This function will change the ownership as specified. It requires root
    privileges and will ask for them if not available. If no group is given,
    only the owner is changed.

    If recursive is true, ownership information of all files and folders
    contained by `file_or_folder` will be adapted.

    If `file_or_folder` points to a file, `recursive` must be `False`.
    Otherwise a ValueError will be raised.


    Parameters:
    -----------
    user
        user ID, either as name or as UID
    group
        group ID, either as name or as GID
    recursive
        whether or not to change ownership for content

    Raises:
    --------
    ValueError
        if `file_or_folder` is a file but `recursive` is `True`
    """
    if file_or_folder.is_file() and recursive:
        raise ValueError(
            "First argument must point to a directory if `recursive` is `True`!"
        )

    user_spec = str(user) if group is None else f"{user}:{group}"
    chown_cmd: sh.StrPathList = ["sudo", "chown", user_spec, file_or_folder]
    if recursive is not None:
        chown_cmd.append("--recursive")
    sh.run_cmd(cmd=chown_cmd)
