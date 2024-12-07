import os
from playbook.config import config


class Command:

    def __init__(
            self,
            app_name,
            clients,
            git_url,
            git_branch,
            json_backfill_base_url,
            json_backfill_user,
            json_backfill_password,
            only_one,
            rootdir,
            task_id,
            is_debug,
    ):
        self.app_name = app_name
        self.clients = clients
        self.git_url = git_url
        self.git_branch = git_branch
        self.json_backfill_base_url = json_backfill_base_url
        self.json_backfill_user = json_backfill_user
        self.json_backfill_password = json_backfill_password
        self.only_one = only_one
        self.rootdir = rootdir
        self.task_id = task_id
        self.IS_DEBUG = is_debug

    def youqu2_command(self, tags):
        if not self.IS_DEBUG:
            os.system(f"pip3 install -U youqu -i {config.PYPI_MIRROR}")
            os.system(f"youqu-startproject {self.rootdir}")
            os.chdir(self.rootdir)
        cmd = (
            f"python3 manage.py remote -a {self.app_name} -c {'/'.join(self.clients)} -t '{tags}' "
            f"--git_url {self.git_url} -b {self.git_branch} -d 1 "
            f"--json_backfill_base_url {self.json_backfill_base_url} --json_backfill_task_id {self.task_id} "
            f"--json_backfill_user {self.json_backfill_user} --json_backfill_password {self.json_backfill_password} "
            f"{'' if self.only_one else '-y no'} -e"
        )
        return cmd

    def youqu3_command(self, tags):
        if not self.IS_DEBUG:
            os.system(f"pip3 install -U youqu3 sendme -i {config.PYPI_MIRROR}")
            os.system(f"git clone {self.git_url} {self.rootdir} -b {self.git_branch} --depth 1")
            os.chdir(self.rootdir)
        cmd = (
            f'''youqu3 remote -w {self.app_name} -c {'/'.join(self.clients) if self.only_one else f"{{{'/'.join(self.clients)}}}"} -t "{tags}" '''
            f'''--job-end "sendme --base-url {self.json_backfill_base_url} --task-id {self.task_id} '''
            f'''--username {self.json_backfill_user} --password {self.json_backfill_password}"'''
        )
        return cmd
