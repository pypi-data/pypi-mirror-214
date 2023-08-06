import json
import logging
import subprocess
import pkg_resources
import shutil
import typer
from enum import Enum
from pathlib import Path
from jsonschema import validate, ValidationError
from rich import print


from scoamp.utils.api_utils import amp_api_path, load_auth, make_request
from scoamp.utils.helper import str_to_int
from scoamp.utils.error import (NotLoginError, APIError, FileFormatError, SubprocessError, ExitCode, err_wrapper)
from scoamp.utils.logger import get_logger

# constants
with open(pkg_resources.resource_filename('scoamp', 'schema/public-model-meta.json')) as f:
    META_SCHEMA = json.load(f)

MANIFEST_FN = 'manifest.json'
PIPELINE_PLAN_FN = 'plan.txt'
PIPELINE_STATUS_DIR = 'status'
PIPELINE_TMP_DIR = 'tmp'

class PipelineStatus(str, Enum):
    Unknown = 0
    Pending = 1
    Created = 2
    Uploaded = 3
    Finished = 4

logger = get_logger(__name__)

app = typer.Typer(name='public-model', help='public model operation')

@app.command(help="create an empty public model")
@err_wrapper
def create(
    name: str = typer.Argument(..., help='public model name, should be global unique'),
    display_name: str = typer.Option(None, help='display name'),
    ):
    auth_info = load_auth()
    jr = _public_model_create_api(auth_info, name, display_name)
    print(jr['repository_uri'])


@app.command(name='update', help="update meta of a public model")
@err_wrapper
def update_meta(
    name: str = typer.Argument(..., help='public model name'),
    meta_file: Path = typer.Option(..., '-f', '--meta-file', exists=True, file_okay=True, resolve_path=True, help='meta info file'),
    model_path: Path = typer.Option(None, '-m', '--model-path', exists=True, file_okay=False, resolve_path=True, help='model repo path'),
    ):
    meta = _validate_meta(meta_file)
    auth_info = load_auth()
    print(_public_model_update_api(auth_info, name, meta, model_path))

@app.command(name='pipeline', help="Create and init public models in batch")
@err_wrapper
def pipeline(
    src_dir: Path = typer.Argument(..., exists=True, file_okay=False, resolve_path=True, help='origin data directory'),
    work_dir: Path = typer.Argument(..., exists=False, file_okay=False, resolve_path=True, help='working directory'),
    allow_list: Path = typer.Option(None, '-al', '--allow-list', exists=True, dir_okay=False, resolve_path=True, help='allowed model list file'),
    ignore_list: Path = typer.Option(None, '-il', '--ignore-list', exists=True, dir_okay=False, resolve_path=True, help='ignored model list file'),
    ):
    """
    structure of 'src_dir':
        2023-05-01
            |- model-meta
                |- default--bert-base-uncased.json
                |- default--gpt2.json
                |- openai--clip-vit-large-patch14.json
                |- microsoft--layoutlmv3-base.json
            |- model-data
                |- default
                    |- bert-base-uncased.tar
                    |- gpt2.tar
                    |- ...
                |- openai
                    |- ...
                |- microsoft
                    |- ...

    meta schema: #/scoamp/schema/public-model-meta.json
    """
    if not src_dir.is_dir():
        logger.error(f"'{src_dir}' is not a directory")
        raise typer.Exit(ExitCode.DefaultError)

    work_dir.mkdir(exist_ok=True)

    def _log_msg(msg, bar='===================='):
        return f"{bar}{msg}{bar}"

    logger.info(_log_msg("Generate/Read manifest"))
    manifest_path = work_dir / MANIFEST_FN
    if manifest_path.is_file():
        logger.warning(f"{MANIFEST_FN}: already exists, continue processing from last breakpoint")
        with open(manifest_path) as f:
            manifest = json.load(f)
    else:
        manifest = _gen_manifest(src_dir)
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)

    logger.info(_log_msg("Generate pipeline plan (model uploading list)"))
    plan = _gen_plan_list(manifest, allow_list, ignore_list)
    with open(work_dir / PIPELINE_PLAN_FN, 'w') as f:
        for item in plan:
            f.write(f"{item['key']}\n")

    logger.info(_log_msg("Run 'create - upload - update' loop for plan list"))
    status_dir = work_dir / PIPELINE_STATUS_DIR
    status_dir.mkdir(exist_ok=True)
    tmp_dir = work_dir / PIPELINE_TMP_DIR
    tmp_dir.mkdir(exist_ok=True)

    auth_info = load_auth()

    for item in plan:
        key = item['key']
        logger.info(_log_msg(f"----->>> {key} start", bar=''))
        _run_pipeline(auth_info, item, status_dir, tmp_dir)
        logger.info(_log_msg(f"-----<<< {key} finish", bar=''))

    logger.info(_log_msg(f"All Complete: {len(plan)}!"))


# API: create model repo
def _public_model_create_api(auth_info: dict, name: str, display_name: str=None):
    method = 'POST'
    path = amp_api_path('/v1/public/models/create')
    url = auth_info['endpoint'] + path
    json_body = {"name": name, "display_name": display_name or name}

    resp = make_request(auth_info['access_key'], auth_info['secret_key'], method, url, json=json_body)
    if resp.status_code != 200:
        raise APIError(resp)

    return resp.json()


# API: update model meta
def _public_model_update_api(auth_info: dict, name: str, meta: dict, model_path: Path=None):
    method = 'POST'
    path = amp_api_path(f'/v1/public/models/{name}/meta')
    url = auth_info['endpoint'] + path
    json_body = {
        "src_url": meta['url'],
        "downloads_last_month": meta['downloads_last_month'],
        "likes": str_to_int(meta['likes']),
        "owner": meta['owner'],
        "source": meta['source'],
        "tags": meta['tags'],
    }
    model_type= _guess_model_type(model_path)
    if model_type:
        json_body["model_type"] = model_type

    resp = make_request(auth_info['access_key'], auth_info['secret_key'], method, url, json=json_body)
    if resp.status_code != 200:
        raise APIError(resp)

    return resp.json()


def _validate_meta(meta_file):
    try:
        with open(meta_file) as f:
            meta = json.load(f)
        validate(meta, META_SCHEMA)
    except json.JSONDecodeError:
        raise FileFormatError(f"{meta_file}: invalid meta file, not json formatted")
    
    return meta


# TODO more guess ways
def _guess_model_type(model_path: Path):
    if not model_path:
        return ''

    # from config.json
    cfg_path = model_path / 'config.json'
    if cfg_path.is_file():
        with open(cfg_path) as f:
            cfg = json.load(f)
        if 'model_type' in cfg:
            return cfg['model_type']

    # stable-diffusion: from model_index.json
    model_index_path = model_path / 'model_index.json'
    if model_index_path.is_file():
        with open(model_index_path) as f:
            model_index = json.load(f)
        if model_index.get('_class_name') == "StableDiffusionPipeline":
            return 'stable-diffusion'
    return ''


def _gen_manifest(src_dir: Path):
    meta_dir = src_dir / 'model-meta'
    data_dir = src_dir / 'model-data'

    meta_files = meta_dir.glob('*.json')
    manifest = []
    for meta_file in meta_files:
        fn = meta_file.name
        model_key = fn.strip(meta_file.suffix)
        owner, model_name = model_key.split('--', 1)

        # validate meta file
        try:
            meta = _validate_meta(meta_file)
        except (FileFormatError, ValidationError) as exc:
            logger.warning(f"{fn}: invalid meta file: {str(exc)}")
            continue

        if owner != meta['owner']:
            logger.warning(f"{fn}: invalid meta file: 'owner' field does not match filename")
            continue

        if model_name != meta['modelname']:
            logger.warning(f"{fn}: invalid meta file: 'modelname' field does not match filename")
            continue


        data_file = data_dir / owner / f"{model_name}.tar"
        if not data_file.is_file():
            logger.warning(f"{fn}: {data_file} not exists")
            continue

        size = data_file.stat().st_size
        manifest.append({
            'key': model_key,
            'meta': str(meta_file),
            'data': str(data_file),
            'size': size,
        })

    # sort model items by repo size with ascending order
    return sorted(manifest, key=lambda x: x['size'])

def _gen_plan_list(manifest: list, allow_list: Path=None, ignore_list: Path=None):
    candicate = {item['key'] for item in manifest}
    plan_set = set()

    # allow_list and ignore_list won't take effect at the same time
    if allow_list:
        with open(allow_list) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if line not in candicate:
                    logger.warning(f"'{line}' from allow_list not found in manifest")
                    continue
                plan_set.add(line)
    elif ignore_list:
        with open(ignore_list) as f:
            ignore_set = {line.strip() for line in f}
        plan_set = candicate - ignore_set
    else:
        plan_set = candicate

    plan = [item for item in manifest if item['key'] in plan_set]

    return plan


def _record_ctx(fn: Path, ctx: dict):
    with open(fn, 'w') as f:
        json.dump(ctx, f, indent=4)

def _run_pipeline(auth_info: dict, plan_item: dict, status_dir: Path, tmp_dir: Path):
    key, meta_path, data_path = plan_item['key'], plan_item['meta'], plan_item['data']
    with open(meta_path) as f:
        meta = json.load(f)

    status_file = status_dir / key
    if status_file.exists():
        with open(status_file) as f:
            ctx = json.load(f)
        status = PipelineStatus[ctx['status']]
        logger.warning(f"{key}: found status '{status.name}', continue it's last status")
    else:
        status = PipelineStatus.Pending
        ctx = {
            'status': status.name,
        }
        _record_ctx(status_file, ctx)

    # step 1: create a new empty model
    if status < PipelineStatus.Created:
        model_name = meta['modelname']

        jr = _public_model_create_api(auth_info, model_name)
        repo_uri = jr['repository_uri']
        status = PipelineStatus.Created

        ctx.update({
            'status': status.name,
            'model_name': model_name,
            'repo_uri': repo_uri,
        })
        _record_ctx(status_file, ctx)

    # step 2: upload model file via git
    if status < PipelineStatus.Uploaded:
        repo_path = tmp_dir / key
        repo_path.mkdir(exist_ok=True)

        shell_script = f"""
        set -ex
        [ -d "{repo_path}/.git" ] || tar xf {data_path} -C {repo_path} --strip-components=1
        cd {repo_path}
        scoamp lfs setup .
        git config lfs.allowincompletepush true
        git remote add amp {ctx['repo_uri']} >/dev/null 2>&1 || true
        git push amp HEAD:master -f
        """

        proc = subprocess.Popen(
            shell_script,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=repo_path,
            )
        while True:
            output = proc.stdout.readline().decode('utf-8')
            if output == '' and proc.poll() is not None:
                break
            if output:
                print(output.strip())

        retcode = proc.poll()
        if retcode:
            raise SubprocessError(f"something wrong when running model upload shell script, retcode={retcode}")

        status = PipelineStatus.Uploaded
        ctx.update({
            'status': status.name,
            'repo_path': str(repo_path),
        })
        _record_ctx(status_file, ctx)

    # step 3: update model meta
    if status < PipelineStatus.Finished:
        _public_model_update_api(auth_info, ctx['model_name'], meta, Path(ctx['repo_path']))
        status = PipelineStatus.Finished
        ctx.update({
            'status': status.name,
        })
        _record_ctx(status_file, ctx)

    # gc
    tmp_repo_path = Path(ctx['repo_path'])
    if tmp_repo_path.exists():
        shutil.rmtree(tmp_repo_path)

    return ctx['repo_uri']