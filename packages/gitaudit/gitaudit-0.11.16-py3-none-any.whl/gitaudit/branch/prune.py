"""Prune changelogs"""

from typing import List

from gitaudit.git.change_log_entry import ChangeLogEntry


def first_parent_prune_by_file_list(changelog: List[ChangeLogEntry], file_list: List[str]):
    """
    Prune entries from the changelog based on a provided file list.

    This function traverses the given changelog, and checks whether each entry
    has any associated file in the provided file list. If an entry does not
    have any associated file in the file list either in its numstat or in its
    submodule updates, the entry is pruned from the changelog.

    Additionally, if a submodule update becomes empty after pruning, it is
    also removed from the changelog entry.

    Parameters
    ----------
    changelog : List[ChangeLogEntry]
        The changelog entries to be pruned. Each entry contains 'numstat'
        and 'submodule_updates' attributes.
    file_list : List[str]
        The list of file paths used for pruning. If a changelog entry is
        associated with a file in this list, it remains in the pruned changelog.

    Returns
    -------
    List[ChangeLogEntry]
        The pruned changelog.

    Notes
    -----
    This function directly modifies the given changelog, rather than creating
    a new one.
    """
    remove_indices = []

    for index, entry in enumerate(changelog):
        matches_in_numstat = any(
            map(lambda x: x.path in file_list, entry.numstat))

        remove_submodules = []

        for sub_path, sub_module_update in entry.submodule_updates.items():
            sub_module_update.entries = first_parent_prune_by_file_list(
                sub_module_update.entries, file_list)

            if not sub_module_update.entries:
                remove_submodules.append(sub_path)

        for sub_path in remove_submodules:
            entry.submodule_updates.pop(sub_path)

        matches_in_submodules = any(
            filter(lambda sub: sub.entries, entry.submodule_updates.values()))

        if not matches_in_numstat and not matches_in_submodules:
            remove_indices.append(index)

    for index in reversed(remove_indices):
        changelog.pop(index)

    return changelog
