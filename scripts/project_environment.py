"""Data-only project policy planner. No runtime authority or side effects."""
import re


_FIELDS = frozenset({
    'schema_version', 'owner_id', 'project_id', 'image_ref',
    'worker_uid', 'worker_gid', 'resource_class',
})
_IDENTIFIER = re.compile(r'[a-z][a-z0-9]{0,15}')
_REPOSITORY_PART = re.compile(r'[a-z0-9]+(?:(?:[._]|__|-+)[a-z0-9]+)*')
_REGISTRY = re.compile(r'[a-z0-9]+(?:[.-][a-z0-9]+)*')


def _valid_image(value: object) -> bool:
    """Conservative reference syntax only; no registry lookup or trust claim."""
    if type(value) is not str:
        return False
    repository, separator, digest = value.partition('@sha256:')
    if not separator or not 1 <= len(repository) <= 255:
        return False
    if not re.fullmatch(r'[a-f0-9]{64}', digest):
        return False
    parts = repository.split('/')
    if len(parts) > 1 and ('.' in parts[0] or ':' in parts[0] or parts[0] == 'localhost'):
        host, colon, port = parts.pop(0).partition(':')
        if not _REGISTRY.fullmatch(host):
            return False
        if colon and (not re.fullmatch(r'[1-9][0-9]{0,4}', port) or int(port) > 65535):
            return False
    return all(_REPOSITORY_PART.fullmatch(part) is not None for part in parts)


def plan_project_environment(document: object) -> dict[str, object]:
    """Return a fresh JSON-compatible description, never an authorization.

    No filesystem inspection, credentials, pool reservation or Docker calls.
    A future runtime must independently check owner/revision, actual mounts,
    UID allocation, quota/capacity, credentials and native admission gates.
    """
    if type(document) is not dict:
        raise ValueError('policy_must_be_object')
    if any(type(key) is not str for key in document) or set(document) - _FIELDS:
        raise ValueError('policy_unknown_fields')
    if set(document) != _FIELDS:
        raise ValueError('policy_required_fields_missing')
    if type(document['schema_version']) is not int or document['schema_version'] != 1:
        raise ValueError('policy_schema_version_invalid')
    for field in ('owner_id', 'project_id'):
        value = document[field]
        if type(value) is not str or not _IDENTIFIER.fullmatch(value):
            raise ValueError(f'policy_{field}_invalid')
    for field in ('worker_uid', 'worker_gid'):
        value = document[field]
        if type(value) is not int or not 1000 <= value <= 65533:
            raise ValueError(f'policy_{field}_invalid')
    if not _valid_image(document['image_ref']):
        raise ValueError('policy_image_ref_invalid')
    resource_class = document['resource_class']
    if type(resource_class) is not str or resource_class not in ('compact', 'large'):
        raise ValueError('policy_resource_class_invalid')
    owner = document['owner_id']
    project = document['project_id']
    root = f'/srv/hermes-projects/{owner}/{project}'
    cpu, memory, pids = (500, 1024, 256) if resource_class == 'compact' else (1000, 2048, 512)
    return {
        **document,
        'container_name': f'hproj-{owner}-{project}',
        'project_root': root,
        'worker_mounts': [
            {'source': root + '/work', 'target': '/workspace', 'read_only': False},
        ],
        'private_paths': {
            'hermes_history': root + '/private/history/hermes',
            'codex_history': root + '/private/history/codex',
            'context': root + '/private/context',
            'checkpoints': root + '/private/checkpoints',
            'results': root + '/private/results',
        },
        'cache_path': root + '/cache',
        'resources': {
            'cpu_millicores': cpu,
            'memory_mib': memory,
            'memory_swap_mib': memory,
            'pids_limit': pids,
            'disk_quota_mib': 4096,
            'min_host_free_disk_mib': 20480,
            'max_writers': 2,
        },
        'runtime_admitted': False,
    }
