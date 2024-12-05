import os
import warnings

import logging
from remotemanager.storage.sendablemixin import SendableMixin

logger = logging.getLogger(__name__)


class Dependency(SendableMixin):
    _do_not_package = ["_network"]

    def __init__(self):
        logger.info("new Dependency created")

        self._network = []
        self._parents = []
        self._children = []

    def add_edge(self, primary, secondary):
        pair = (primary, secondary)
        if pair not in self._network:
            logger.info("adding new edge %s", pair)

            self._parents.append(primary.short_uuid)
            self._children.append(secondary.short_uuid)

            self._network.append(pair)

    @property
    def network(self):
        return self._network

    def get_children(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._parents)):
            if self._parents[i] == uuid:
                tmp.append(self.network[i][1])

        return tmp

    def get_parents(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._children)):
            if self._children[i] == uuid:
                tmp.append(self.network[i][0])

        return tmp

    @property
    def ds_list(self):
        datasets = []
        for pair in self.network:
            for ds in pair:
                if ds not in datasets:
                    datasets.append(ds)

        return datasets

    def remove_run(self, id: bool = False) -> bool:
        out = []
        for ds in self.ds_list:
            out.append(ds.remove_run(id=id, dependency_call=True))

        return all(out)

    def clear_runs(self) -> None:
        for ds in self.ds_list:
            ds.wipe_runs(dependency_call=True)

    def clear_results(self, wipe) -> None:
        for ds in self.ds_list:
            ds.reset_runs(wipe, dependency_call=True)

    def wipe_local(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.wipe_local(files_only=files_only, dependency_call=True)

    def wipe_remote(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.wipe_remote(files_only=files_only, dependency_call=True)

    def hard_reset(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.hard_reset(files_only=files_only, dependency_call=True)

    def append_run(
        self, caller, chain_run_args, run_args, force, lazy, *args, **kwargs
    ):
        """
        Appends runs with the same args to all datasets

        Args:
            lazy:
            caller:
                (Dataset): The dataset which defers to the dependency
            chain_run_args (bool):
                for dependency runs, will not propagate run_args to other datasets in
                the chain if False (defaults True)
            run_args (dict):
                runner arguments
            force (bool):
                force append if True
            lazy (bool):
                do not update the database after this append (ensure you call
                ``update_db()`` after appends are complete, or use the
                ``lazy_append()`` contex)
            *args:
                append_run args
            **kwargs:
                append_run keyword args

        Returns:
            None
        """
        logger.info("appending run from %s", caller)

        datasets = self.ds_list
        logger.info("There are %s datasets in the chain)", len(datasets))

        if chain_run_args:
            logger.info("chain_args is True, propagating")
            kwargs.update(run_args)

        for ds in datasets:
            if ds == caller:
                caller_args = {k: v for k, v in kwargs.items()}
                caller_args.update(run_args)
                ds.append_run(
                    dependency_call=True, force=force, lazy=lazy, *args, **caller_args
                )
            else:
                ds.append_run(
                    dependency_call=True, force=force, lazy=lazy, *args, **kwargs
                )

        for ds in datasets:
            parents = self.get_parents(ds)
            if len(parents) > 1:
                warnings.warn(
                    "Multiple parents detected. "
                    "Variable passing in this instance is unstable!"
                )
            for parent in parents:
                # TODO this is broken with multiple parents
                lstr = (
                    f'if os.path.getmtime("'
                    f'{parent.runners[-1].runfile.name}") > '
                    f'os.path.getmtime("'
                    f'{parent.runners[-1].resultfile.name}"):\n'
                    f'\traise RuntimeError("outdated '
                    f'result file for parent")\n'
                    f'repo.loaded = repo.{parent.serialiser.loadfunc_name}("'
                    f'{parent.runners[-1].resultfile.name}")'
                )
                ds.runners[-1]._dependency_info["parent_import"] = lstr

            if not lazy:
                ds.database.update(ds.pack())

    def finish_append(self) -> None:
        for ds in self.ds_list:
            ds.finish_append(dependency_call=True, print_summary=False)

    def run(
        self,
        dry_run: bool = False,
        extra: str = None,
        force_ignores_success: bool = False,
        **run_args,
    ):
        logger.info("dependency internal run call")

        ds_store = {}
        for ds in self.ds_list:
            ds_store[ds] = len(ds.runners)

        if not len(set(ds_store.values())) == 1:
            msg = f"Datasets do not have matching numbers of runners!: {ds_store}"
            logger.critical(msg)
            raise RuntimeError(msg)

        # we need to write a common repo containing all functions
        first = list(ds_store.keys())[0]

        if not os.path.isdir(first.master_script.local_dir):
            os.makedirs(first.master_script.local_dir)
        # prime the repo with no functions
        first._write_to_repo(skip_function=True)
        content = ["\n"]
        for ds in ds_store:
            content.append(f"# Main function for {ds}")
            content.append(ds.function.source)

        first.repofile.sub(
            "# DATASET_CONTENT #", "\n".join(content + ["\n# DATASET_CONTENT #"])
        )

        first.transport.queue_for_push(first.repofile)

        # grab all global extra content from the datasets
        global_extra = []
        for ds in ds_store:
            if ds._global_run_extra is not None:
                global_extra.append(ds._global_run_extra)

        # and now a master script to kick off the chains
        # we need the export for ALL datasets
        master_content = ["sourcedir=$PWD"]
        # update the master targets for ALL runners
        for ds in ds_store:
            for runner in ds.runners:
                master_content.append(
                    f'sed -i -e "s#{runner.short_uuid}_master#$sourcedir#" '
                    f"{runner.jobscript.name}"
                )

        for ds in ds_store:
            # reuse the store as a list of runner uuids for runners_to_update
            ds_store[ds] = []
            i = 0
            for runner in ds.runners:
                tmp = []
                for child in self.get_children(ds):
                    child_runner = child.runners[i]

                    if not child_runner.derived_run_args.get("avoid_nodes", False):
                        submitter = ds.url.submitter
                    else:
                        submitter = ds.url.shell

                    linesubmit = (
                        f"{submitter} {child_runner.jobscript.name} "
                        f"2>> {child_runner.errorfile.name}"
                    )
                    # check first for any error files. This is safe as the master script
                    # deletes any existing ones at run init
                    tmp.append(
                        f"\n[ -s {runner.errorfile.name} ] && cp "
                        f"{runner.errorfile.name} {child_runner.errorfile.name}\n"
                        f"{linesubmit}"
                    )

                parent_check = ""
                for parent in self.get_parents(ds):
                    parent_runner = parent.runners[i]

                    parent_check = f"[ -f {parent_runner.resultfile.name} ] && "

                ready = runner.stage(
                    python=ds.url.python,
                    repo=first.repofile.name,
                    global_extra="\n".join(global_extra),
                    extra=extra,
                    parent_check=parent_check,
                    child_submit=tmp,
                    force_ignores_success=force_ignores_success,
                    **run_args,
                )
                if not ready:
                    continue

                # we only need the runlines for the first dataset, since the chaining
                # is handled by the jobscripts
                if ds == first:
                    jobscript = runner.jobscript.relative_remote_path(
                        ds.master_script.remote_dir
                    )
                    jobpath, jobfile = os.path.split(jobscript)
                    errorpath = runner.errorfile.relative_remote_path(runner.remote_dir)
                    runline = []
                    if runner.remote_dir != runner.run_path:
                        runline.append(f"mkdir -p {runner.run_dir} &&")

                    if not runner.derived_run_args.get("avoid_nodes", False):
                        submitter = ds.url.submitter
                    else:
                        submitter = ds.url.shell

                    runline.append(
                        f"echo $(date +'%d/%m/%Y %H:%M:%S') "
                        f"{runner.short_uuid} submitted >> "
                        f"{first.manifest_log.name} &&"
                    )
                    runline.append(f"{submitter} {jobfile} 2>> {errorpath}")

                    if ds.remote_dir != runner.remote_dir:
                        runline.insert(0, f"cd {jobpath} && ")

                    runline.append(f"$PWD/{first.repofile.name}")

                    asynchronous = runner.derived_run_args["asynchronous"]
                    if asynchronous and submitter == "bash":
                        logger.debug('appending "&" for async run')
                        runline.append("&")

                    master_content.append(" ".join(runline))

                first.transport.queue_for_push(runner.jobscript)
                first.transport.queue_for_push(runner.runfile)

                for file in runner.extra_files["send"]:
                    first.transport.queue_for_push(
                        os.path.split(file)[1],
                        os.path.split(file)[0],
                        runner.remote_dir,
                    )

                ds_store[ds].append(runner.uuid)
                i += 1

        # finally write the script
        if all([ds._fresh_dataset for ds in ds_store]):
            master_starter = [f"rm -f {first.manifest_log.name}\n"]
        else:
            master_starter = []

        master_starter += [
            f"rm -f *{dataset.short_uuid}*error.out\n" for dataset in ds_store
        ]

        first.master_script.write(
            master_starter,
            add_newline=True,
        )
        first.master_script.append(master_content, add_newline=first.add_newline)

        first.transport.queue_for_push(first.master_script)

        first.prepare_for_transfer()

        if not dry_run:
            first.transport.transfer()

            cmd = (
                f"cd {first.remote_dir} && {first.url.shell} {first.master_script.name}"
            )
            first._run_cmd = first.url.cmd(cmd, asynchronous=True)

            for ds in ds_store:
                ds.set_runner_states("submit pending", ds_store[ds])
        else:
            first.transport.wipe_transfers()
            for ds in ds_store:
                ds.set_runner_states("dry run", ds_store[ds])

    def update_runners(self):
        """
        Manifest only needs to be collected once, then all the runners
        can be updated by that call
        """
        runners = []
        for ds in self.ds_list:
            runners += ds.runners

        self.ds_list[0].update_runners(runners=runners, dependency_call=True)

    def check_failure(self):
        """
        Raises a RuntimeError if an error is detected in any of the runners

        Relies on the runner.is_failed property
        """
        for ds in self.ds_list:
            for runner in ds.runners:
                if runner.is_failed:
                    ds.fetch_results()
                    raise RuntimeError(
                        f"Detected a failure in dataset {ds}:\n{ds.errors}"
                    )
