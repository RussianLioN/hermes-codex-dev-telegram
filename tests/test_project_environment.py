"""Synthetic policy tests: no container, host data or credential access."""
import unittest
import json
from contextlib import ExitStack
from typing import cast
from unittest.mock import patch

from scripts.project_environment import plan_project_environment


# Syntactically valid synthetic digest, not a real/approved image identity.
IMAGE = 'registry.example/team/image@sha256:' + 'a' * 64


def policy(**changes):
    document = {
        'schema_version': 1,
        'owner_id': 'owner1',
        'project_id': 'project1',
        'image_ref': IMAGE,
        'worker_uid': 10001,
        'worker_gid': 10001,
        'resource_class': 'compact',
    }
    document.update(changes)
    return document


class ProjectEnvironmentTests(unittest.TestCase):
    def assert_rejected(self, document, code):
        with self.assertRaises(ValueError) as caught:
            plan_project_environment(document)
        self.assertEqual(str(caught.exception), code)

    def test_rejects_non_plain_objects(self):
        class DictSubclass(dict):
            pass

        for value in (None, [], 'object', 1, True, DictSubclass(policy())):
            self.assert_rejected(value, 'policy_must_be_object')

    def test_rejects_unknown_fields_without_reflecting_values(self):
        for field in ('command', 'env', 'oauth', 'model', 'routing', 'privileged',
                      'socket', 'mounts', 'host_path', 'data_root', 'task_id',
                      'mode', 'runtime_admitted', 'cpu_millicores',
                      'synthetic-sensitive-key'):
            self.assert_rejected(policy(**{field: 'synthetic-sensitive-value'}),
                                 'policy_unknown_fields')
        self.assert_rejected(dict(policy(), **{'extra': None}), 'policy_unknown_fields')
        self.assert_rejected({**policy(), 1: 'not-a-string-key'}, 'policy_unknown_fields')

    def test_rejects_missing_fields(self):
        for field in policy():
            value = policy()
            del value[field]
            self.assert_rejected(value, 'policy_required_fields_missing')

    def test_rejects_schema_coercion(self):
        for value in (True, False, 1.0, '1', 0, 2, None, []):
            self.assert_rejected(policy(schema_version=value), 'policy_schema_version_invalid')

    def test_rejects_noncanonical_identifiers(self):
        for field in ('owner_id', 'project_id'):
            for value in ('', 'A', ' a', 'a ', 'a\n', '../a', '/a', 'a/b',
                          'a-b', 'a_b', '1a', 'а', 'a' * 17, None, True, []):
                self.assert_rejected(policy(**{field: value}), f'policy_{field}_invalid')

    def test_rejects_invalid_worker_ids(self):
        class IntSubclass(int):
            pass

        for field in ('worker_uid', 'worker_gid'):
            for value in (True, False, 0, 999, 65534, -1, 10001.0, '10001', None, [], IntSubclass(10001)):
                self.assert_rejected(policy(**{field: value}), f'policy_{field}_invalid')

    def test_rejects_nonimmutable_or_malformed_image(self):
        digest = '@sha256:' + 'a' * 64
        invalid = ('image:latest', 'image', '@sha256:' + 'a' * 64,
                   IMAGE + '\n', ' ' + IMAGE, IMAGE[:-1], IMAGE + 'a',
                   'image@sha256:' + 'A' * 64, 'image@sha256:' + 'g' * 64,
                   'image@sha512:' + 'a' * 64, 'https://registry/image' + digest,
                   'user@registry/image' + digest, 'repo//image' + digest,
                   '/image' + digest, '../image' + digest, 'repo/./image' + digest,
                   'repo/image:tag' + digest, 'repo\\image' + digest,
                   'repo/IMAGE' + digest, 'registry:0/image' + digest,
                   'registry:65536/image' + digest, 'registry:01/image' + digest,
                   'a' * 256 + digest, None, True, [])
        for value in invalid:
            self.assert_rejected(policy(image_ref=value), 'policy_image_ref_invalid')

    def test_rejects_invalid_resource_class(self):
        for value in ('', 'COMPACT', 'compact ', 'small', None, True, 1, [], {}):
            self.assert_rejected(policy(resource_class=value), 'policy_resource_class_invalid')

    def test_rejects_mixed_repository_separators(self):
        for repo in ('team/image..name', 'team/image._name', 'team/image___name', 'team/image--_name'):
            self.assert_rejected(policy(image_ref=repo + '@sha256:' + 'a' * 64),
                                 'policy_image_ref_invalid')

    def test_valid_policy_boundaries_are_accepted(self):
        for uid in (1000, 65533):
            for repo in ('image', 'team/image_name', 'team/image__name', 'team/image---name', 'registry.example/team/image',
                         'localhost:5000/team/image', 'registry:65535/image'):
                result = plan_project_environment(policy(
                    owner_id='a', project_id='a' * 16, worker_uid=uid, worker_gid=uid,
                    image_ref=repo + '@sha256:' + '0' * 64))
                self.assertIsInstance(result, dict)

    def test_layout_exact_owner_project_binding(self):
        result = plan_project_environment(policy())
        self.assertEqual(result.get('container_name'), 'hproj-owner1-project1')
        self.assertEqual(result.get('project_root'), '/srv/hermes-projects/owner1/project1')
        for field, value in policy().items():
            self.assertEqual(result.get(field), value)

    def test_layout_stable_across_order_and_resource_changes(self):
        value = policy()
        result = plan_project_environment(value)
        self.assertIn('container_name', result)
        self.assertEqual(result, plan_project_environment(dict(reversed(list(value.items())))))
        large = plan_project_environment(policy(resource_class='large'))
        self.assertEqual(result['container_name'], large['container_name'])
        self.assertEqual(result['project_root'], large['project_root'])

    def test_layout_owner_project_pairs_cannot_alias(self):
        # These collide if identifiers are concatenated without a delimiter.
        first = plan_project_environment(policy(owner_id='ab', project_id='c'))
        second = plan_project_environment(policy(owner_id='a', project_id='bc'))
        self.assertNotEqual(first.get('container_name'), second.get('container_name'))
        self.assertNotEqual(first.get('project_root'), second.get('project_root'))
        other_owner = plan_project_environment(policy(owner_id='owner2'))
        other_project = plan_project_environment(policy(project_id='project2'))
        base = plan_project_environment(policy())
        for other in (other_owner, other_project):
            self.assertNotEqual(base['project_root'], other['project_root'])

    def test_layout_worker_mount_excludes_private_and_credentials(self):
        result = plan_project_environment(policy())
        root = '/srv/hermes-projects/owner1/project1'
        self.assertEqual(result.get('worker_mounts'), [
            {'source': root + '/work', 'target': '/workspace', 'read_only': False},
        ])
        self.assertEqual(result.get('private_paths'), {
            'hermes_history': root + '/private/history/hermes',
            'codex_history': root + '/private/history/codex',
            'context': root + '/private/context',
            'checkpoints': root + '/private/checkpoints',
            'results': root + '/private/results',
        })
        self.assertEqual(result.get('cache_path'), root + '/cache')

    def test_layout_input_is_unchanged(self):
        value = policy()
        original = value.copy()
        result = plan_project_environment(value)
        self.assertIn('worker_mounts', result)
        self.assertEqual(value, original)
        self.assertIsNot(result, value)

    def test_resources_exact_profiles(self):
        for name, cpu, memory, pids in (('compact', 500, 1024, 256), ('large', 1000, 2048, 512)):
            result = plan_project_environment(policy(resource_class=name))
            self.assertEqual(result.get('resources'), {
                'cpu_millicores': cpu,
                'memory_mib': memory,
                'memory_swap_mib': memory,
                'pids_limit': pids,
                'disk_quota_mib': 4096,
                'min_host_free_disk_mib': 20480,
                'max_writers': 2,
            })

    def test_resources_never_grant_runtime_admission(self):
        for name in ('compact', 'large'):
            self.assertIs(plan_project_environment(policy(resource_class=name)).get('runtime_admitted'), False)

    def test_resources_result_has_only_data_fields(self):
        result = plan_project_environment(policy())
        self.assertEqual(set(result), set(policy()) | {
            'container_name', 'project_root', 'worker_mounts', 'private_paths',
            'cache_path', 'resources', 'runtime_admitted',
        })
        self.assertEqual(json.loads(json.dumps(result)), result)

    def test_resources_outputs_do_not_share_mutable_state(self):
        first = plan_project_environment(policy())
        self.assertIn('resources', first)
        original = plan_project_environment(policy())
        cast(dict[str, object], first['resources'])['memory_mib'] = 999999
        cast(dict[str, object], first['private_paths'])['context'] = '/not-real'
        cast(list[dict[str, object]], first['worker_mounts'])[0]['source'] = '/not-real'
        self.assertEqual(plan_project_environment(policy()), original)

    def test_resources_do_not_access_runtime_or_files(self):
        with ExitStack() as stack:
            for target in ('builtins.open', 'io.open', 'os.open', 'os.stat',
                           'os.getenv', 'socket.socket', 'subprocess.Popen'):
                stack.enter_context(patch(target, side_effect=AssertionError('unexpected side effect')))
            result = plan_project_environment(policy())
        self.assertIs(result.get('runtime_admitted'), False)


if __name__ == '__main__':
    unittest.main()
