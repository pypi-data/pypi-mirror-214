import json
import logging
from functools import update_wrapper
from pathlib import Path
from typing import List
from urllib.error import URLError
from urllib.request import urlopen

import click
import requests
from tqdm import tqdm

from pymobiledevice3.cli.cli_common import Command, print_json
from pymobiledevice3.common import get_home_folder
from pymobiledevice3.exceptions import AlreadyMountedError, NotMountedError, UnsupportedCommandError
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.mobile_image_mounter import DeveloperDiskImageMounter, MobileImageMounterService, \
    PersonalizedImageMounter

DISK_IMAGE_TREE = 'https://api.github.com/repos/pdso/DeveloperDiskImage/git/trees/master'
DEVELOPER_DISK_IMAGE_URL = 'https://github.com/pdso/DeveloperDiskImage/raw/master/{ios_version}/{file_name}'

logger = logging.getLogger(__name__)


def catch_errors(func):
    def catch_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AlreadyMountedError:
            logger.error('Given image was already mounted')
        except UnsupportedCommandError:
            logger.error('Your iOS version doesn\'t support this command')

    return update_wrapper(catch_function, func)


@click.group()
def cli():
    """ mounter cli """
    pass


@cli.group()
def mounter():
    """ mounter options """
    pass


@mounter.command('list', cls=Command)
@click.option('--color/--no-color', default=True)
def mounter_list(lockdown: LockdownClient, color):
    """ list all mounted images """
    output = []

    images = MobileImageMounterService(lockdown=lockdown).copy_devices()
    for image in images:
        image_signature = image.get('ImageSignature')
        if image_signature is not None:
            image['ImageSignature'] = image_signature.hex()
        output.append(image)

    print_json(output, colored=color)


@mounter.command('lookup', cls=Command)
@click.option('--color/--no-color', default=True)
@click.argument('image_type')
def mounter_lookup(lockdown: LockdownClient, color, image_type):
    """ lookup mounter image type """
    try:
        signature = MobileImageMounterService(lockdown=lockdown).lookup_image(image_type)
        print_json(signature, colored=color)
    except NotMountedError:
        logger.error(f'Disk image of type: {image_type} is not mounted')


@mounter.command('umount-developer', cls=Command)
@catch_errors
def mounter_umount_developer(lockdown: LockdownClient):
    """ unmount Developer image """
    try:
        DeveloperDiskImageMounter(lockdown=lockdown).umount()
        logger.info('Developer image unmounted successfully')
    except NotMountedError:
        logger.error('Developer image isn\'t currently mounted')


@mounter.command('umount-personalized', cls=Command)
@catch_errors
def mounter_umount_personalized(lockdown: LockdownClient):
    """ unmount Personalized image """
    try:
        PersonalizedImageMounter(lockdown=lockdown).umount()
        logger.info('Personalized image unmounted successfully')
    except NotMountedError:
        logger.error('Personalized image isn\'t currently mounted')


def download_file(url, local_filename):
    logger.debug(f'downloading: {local_filename}')
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))

        with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, dynamic_ncols=True) as progress_bar:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    progress_bar.update(len(chunk))
                    f.write(chunk)

    return local_filename


def get_all_versions() -> List[str]:
    data = urlopen(DISK_IMAGE_TREE).read()
    json_data = json.loads(data)
    return [item.get('path') for item in json_data.get('tree')][0:-3]


@mounter.command('mount-developer', cls=Command)
@click.argument('image', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('signature', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@catch_errors
def mounter_mount_developer(lockdown: LockdownClient, image: str, signature: str):
    """ mount developer image """
    DeveloperDiskImageMounter(lockdown=lockdown).mount(Path(image), Path(signature))
    logger.info('Developer image mounted successfully')


@mounter.command('mount-personalized', cls=Command)
@click.argument('image', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('trust-cache', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('build-manifest', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@catch_errors
def mounter_mount_personalized(lockdown: LockdownClient, image: str, trust_cache: str, build_manifest: str):
    """ mount personalized image """
    PersonalizedImageMounter(lockdown=lockdown).mount(Path(image), Path(build_manifest), Path(trust_cache))
    logger.info('Personalized image mounted successfully')


@mounter.command('auto-mount', cls=Command)
@click.option('-x', '--xcode', type=click.Path(exists=True, dir_okay=True, file_okay=False),
              help='Xcode application path used to figure out automatically the DeveloperDiskImage path')
@click.option('-v', '--version', help='use a different DeveloperDiskImage version from the one retrieved by lockdown'
                                      'connection')
def mounter_auto_mount(lockdown: LockdownClient, xcode: str, version: str):
    """ auto-detect correct DeveloperDiskImage and mount it """
    image_type = 'Developer'

    if xcode is None:
        # avoid "default"-ing this option, because Windows and Linux won't have this path
        xcode = Path('/Applications/Xcode.app')
        if not (xcode.exists()):
            xcode = get_home_folder() / 'Xcode.app'
            xcode.mkdir(parents=True, exist_ok=True)

    image_mounter = DeveloperDiskImageMounter(lockdown=lockdown)
    if image_mounter.is_image_mounted(image_type):
        logger.error('DeveloperDiskImage is already mounted')
        return

    logger.debug('trying to figure out the best suited DeveloperDiskImage')
    if version is None:
        version = lockdown.sanitized_ios_version
    image_dir = f'{xcode}/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{version}'
    image_path = f'{image_dir}/DeveloperDiskImage.dmg'
    signature = f'{image_path}.signature'
    developer_disk_image_dir = Path(image_path).parent

    image_path = Path(image_path)
    signature = Path(signature)

    if not image_path.exists():
        try:
            available_versions = get_all_versions()
            if version not in available_versions:
                logger.error(
                    f'Unable to find DeveloperDiskImage for {version}. available versions: {available_versions}')
                return
        except URLError:
            logger.warning('failed to query DeveloperDiskImage versions')

    try:
        developer_disk_image_dir.mkdir(exist_ok=True)

        if not image_path.exists():
            download_file(DEVELOPER_DISK_IMAGE_URL.format(ios_version=version, file_name=image_path.name), image_path)

        if not signature.exists():
            download_file(DEVELOPER_DISK_IMAGE_URL.format(ios_version=version, file_name=signature.name), signature)

    except PermissionError:
        logger.error(
            f'DeveloperDiskImage could not be saved to Xcode default path ({developer_disk_image_dir}). '
            f'Please make sure your user has the necessary permissions')
        return

    image_mounter.mount(image_path, signature)
    logger.info('DeveloperDiskImage mounted successfully')


@mounter.command('query-developer-mode-status', cls=Command)
@click.option('--color/--no-color', default=True)
def mounter_query_developer_mode_status(lockdown: LockdownClient, color):
    """ Query developer mode status """
    print_json(MobileImageMounterService(lockdown=lockdown).query_developer_mode_status(), colored=color)


@mounter.command('query-nonce', cls=Command)
@click.option('--image-type')
@click.option('--color/--no-color', default=True)
def mounter_query_nonce(lockdown: LockdownClient, image_type: str, color: bool):
    """ Query nonce """
    print_json(MobileImageMounterService(lockdown=lockdown).query_nonce(image_type), colored=color)


@mounter.command('query-personalization-identifiers', cls=Command)
@click.option('--color/--no-color', default=True)
def mounter_query_personalization_identifiers(lockdown: LockdownClient, color):
    """ Query personalization identifiers """
    print_json(MobileImageMounterService(lockdown=lockdown).query_personalization_identifiers(), colored=color)


@mounter.command('query-personalization-manifest', cls=Command)
@click.option('--color/--no-color', default=True)
def mounter_query_personalization_manifest(lockdown: LockdownClient, color):
    """ Query personalization manifest """
    result = []
    mounter = MobileImageMounterService(lockdown=lockdown)
    for device in mounter.copy_devices():
        result.append(mounter.query_personalization_manifest(device['PersonalizedImageType'], device['ImageSignature']))
    print_json(result, colored=color)


@mounter.command('roll-personalization-nonce', cls=Command)
def mounter_roll_personalization_nonce(lockdown: LockdownClient):
    MobileImageMounterService(lockdown=lockdown).roll_personalization_nonce()


@mounter.command('roll-cryptex-nonce', cls=Command)
def mounter_roll_cryptex_nonce(lockdown: LockdownClient):
    """ Roll cryptex nonce (will reboot) """
    MobileImageMounterService(lockdown=lockdown).roll_cryptex_nonce()
