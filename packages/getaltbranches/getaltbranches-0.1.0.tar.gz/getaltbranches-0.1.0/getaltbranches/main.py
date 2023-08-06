from requests import get, exceptions
from collections import Counter
from json import dumps

BASE_URL = 'https://rdb.altlinux.org/api/export/branch_binary_packages'


def get_branches_packages(first_branch, second_branch, arch=None):
    try:
        first_branch_response = get(f"{BASE_URL}/{first_branch}", params={'arch': arch}).json()
        second_branch_response = get(f"{BASE_URL}/{second_branch}", params={'arch': arch}).json()
        return first_branch_response['packages'], second_branch_response['packages']
    except KeyError:
        print('Wrong branch or architecture')
        raise SystemExit(exceptions.RequestException)


def __unique_packages(first_branch, second_branch, arch=None):
    compared_branches = get_branches_packages(first_branch, second_branch, arch)
    second_branch_set = set(tuple(d.items()) for d in compared_branches[1])
    main_list = [d for d in compared_branches[0] if tuple(d.items()) not in second_branch_set]
    json_main_list = {'packages_in': first_branch, 'packages_not_in': second_branch,
                      'arch': arch, 'length': len(main_list), 'packages': main_list}

    return dumps(json_main_list)


def first_branch_unique_packages(first_branch, second_branch, arch=None):
    return __unique_packages(first_branch, second_branch, arch)


def second_branch_unique_packages(first_branch, second_branch, arch=None):
    return __unique_packages(second_branch, first_branch, arch)


def unique_version_release(first_branch, second_branch, arch=None):
    compared_branches = get_branches_packages(first_branch, second_branch, arch)
    version_release_1 = Counter((e['version'], e['release']) for e in compared_branches[0])
    version_release_2 = Counter((e['version'], e['release']) for e in compared_branches[1])

    first_branch_final = []

    for i, j in version_release_1.items():
        if i in version_release_2 and j > version_release_2.get(i) or i not in version_release_2:
            for k in compared_branches[0]:
                if k['version'] == i[0]:
                    first_branch_final.append(k)
                    break
    first_branch_final = {'version_release_more': first_branch, 'version_release_less': second_branch,
                          'arch': arch, 'length': len(first_branch_final), 'packages': first_branch_final}
    return dumps(first_branch_final)
