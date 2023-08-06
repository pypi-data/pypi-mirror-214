from datetime import datetime
import importlib.resources
import json
import mimetypes
import os.path
from urllib.parse import quote_plus

from .apk import is_apk, open_apk
from .ipa import is_ipa, open_ipa
from .templates import render_template

log = __import__('logging').getLogger(__name__)

def push(target, package_paths, *, prefix=None, overwrite_index=False):
    if not prefix:
        prefix = os.path.splitext(os.path.basename(package_paths[0]))[0]

    packages = []
    for package_path in package_paths:
        if is_ipa(package_path):
            with open_ipa(package_path) as ipa:
                ctx = push_ipa(ipa, target, prefix)

        elif is_apk(package_path):
            with open_apk(package_path) as apk:
                ctx = push_apk(apk, target, prefix)

        else:
            raise ValueError('unrecognized package')

        packages.append(ctx)

    index = update_index(target, packages, prefix, overwrite=overwrite_index)

    html_tmpl = importlib.resources.read_text(__package__, 'html.jinja2')
    html = render_template(html_tmpl, context=index)
    url = target.put_object(
        f'{prefix}.html',
        html.encode('utf8'),
        'text/html',
    )
    return url

def push_ipa(ipa, s3, prefix):
    location = f'{prefix}/ipas/{os.path.basename(prefix)}.v{ipa.version}'
    image_url = None
    icon = ipa.find_best_icon(512)
    if icon is not None:
        with ipa.open_asset(icon.name) as fp:
            image_url = s3.put_object(f'{location}.png', fp, 'image/png')

    with open(ipa.filename, 'rb') as fp:
        ipa_url = s3.put_object(f'{location}.ipa', fp, 'application/zip')

    manifest_tmpl = importlib.resources.read_text(
        __package__, 'ipa_manifest.jinja2')
    manifest = render_template(manifest_tmpl, context=dict(
        ipa=ipa,
        ipa_url=ipa_url,
        image_url=image_url,
    ))
    manifest_url = s3.put_object(
        f'{location}.plist',
        manifest.encode('utf8'),
        'text/xml',
    )

    return dict(
        package_type='ipa',
        uploaded_at=datetime.now().isoformat(),
        app_id=ipa.id,
        display_name=ipa.display_name,
        version_name=ipa.short_version,
        version_code=ipa.version,
        minimum_os_version=ipa.minimum_os_version,
        platform=ipa.platform,
        image_url=image_url,
        ipa_url=ipa_url,
        manifest_url=manifest_url,
        install_url=make_ipa_install_url(manifest_url),
        download_url=ipa_url,
    )

def make_ipa_install_url(manifest_url):
    return f'itms-services://?action=download-manifest&url={quote_plus(manifest_url)}'

def push_apk(apk, s3, prefix):
    location = f'{prefix}/apks/{os.path.basename(prefix)}.v{apk.version_code}'
    image_url = None
    icon = apk.get_app_icon(512)
    if icon and not icon.endswith('.xml'):
        image_data = apk.get_file(icon)
        image_ext = os.path.splitext(icon)[1]
        image_type, _ = mimetypes.guess_type(icon, strict=False)
        image_url = s3.put_object(f'{location}{image_ext}', image_data, image_type)

    with open(apk.filename, 'rb') as fp:
        apk_url = s3.put_object(
            f'{location}.apk', fp, 'application/vnd.android.package-archive')

    return dict(
        package_type='apk',
        uploaded_at=datetime.now().isoformat(),
        app_id=apk.package,
        display_name=apk.application,
        version_name=apk.version_name,
        version_code=apk.version_code,
        image_url=image_url,
        apk_url=apk_url,
        install_url=apk_url,
        download_url=apk_url,
    )

def update_index(target, packages, prefix, *, overwrite=False, readonly=False):
    index_path = f'{prefix}/index.json'
    index_url = target.get_url(index_path)
    data = target.get_object(index_path, raise_if_not_found=False)
    if not data or overwrite:
        index = {
            'index_url': index_url,
            'packages': [],
            'created_at': datetime.now().isoformat(),
        }
    else:
        index = json.loads(data.decode('utf8'))

    # old index.json did not have index_url
    if 'index_url' not in index:
        index['index_url'] = index_url

    # de-duplicate packages by using the new copy of the same build
    prev_packages = index['packages']
    out_packages = list(packages)
    codes = {(p['app_id'], p['version_code']) for p in packages}
    for prev_pkg in prev_packages:
        pkg_type = prev_pkg['package_type']
        if (prev_pkg['app_id'], prev_pkg['version_code']) in codes:
            log.debug(
                f'overwriting index entry for '
                f'package={prev_pkg["app_id"]} '
                f'version={prev_pkg["version_code"]}'
            )
            continue
        
        # old index.json did not have install_url so let's add it
        if 'install_url' not in prev_pkg:
            if pkg_type == 'ipa':
                prev_pkg['install_url'] = make_ipa_install_url(prev_pkg['manifest_url'])
            elif pkg_type == 'apk':
                prev_pkg['install_url'] = prev_pkg['apk_url']

        # old index.json did not have download_url so let's add it
        if 'download_url' not in prev_pkg:
            if pkg_type == 'ipa':
                prev_pkg['download_url'] = prev_pkg['ipa_url']
            elif pkg_type == 'apk':
                prev_pkg['download_url'] = prev_pkg['apk_url']

        out_packages.append(prev_pkg)

    out_packages.sort(key=lambda p: p['uploaded_at'], reverse=True)
    index['packages'] = out_packages
    index['updated_at'] = datetime.now().isoformat()

    if not readonly:
        target.put_object(
            index_path,
            json.dumps(index, indent=2).encode('utf8'),
            'application/json',
        )

    return index
