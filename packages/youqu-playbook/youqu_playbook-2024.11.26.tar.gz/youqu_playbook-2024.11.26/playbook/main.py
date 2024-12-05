from typing import List, Dict
import itertools
import json
import os
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


class PlayBook:

    def __init__(self, apps: List[Dict], clients: List[str], tags: str):
        self.apps = apps
        self.clients = clients
        self.clients_num = len(clients)
        self.tags = tags
        self.playbook_path = "./playbook.json"

    def make_playbook(self) -> List[List[Dict]]:
        playbook = []
        group = []

        for app_obj in self.apps:
            if app_obj.get("split_run"):
                app_dict = self._create_app_dict(app_obj, split_run=True)
                group.append(app_dict)
                playbook.append(group)
                group = []

        cs = itertools.cycle(self.clients)
        group = []
        for app_obj in self.apps:
            if not app_obj.get("split_run"):
                app_dict = self._create_app_dict(app_obj, split_run=False, client=next(cs))
                group.append(app_dict)
                if len(group) == self.clients_num:
                    playbook.append(group)
                    group = []

        if group:
            playbook.append(group)

        with open(self.playbook_path, "w", encoding="utf-8") as f:
            json.dump(playbook, f, indent=4)

        return playbook

    def _create_app_dict(self, app_obj: Dict, split_run: bool, client: str = None) -> Dict:
        app_name = app_obj.get("app_name")
        _id = app_obj.get("id")
        git_url = app_obj.get("git_url")
        git_branch = app_obj.get("git_branch")
        framework = app_obj.get("framework")
        app_dict = {
            "app_name": app_name,
            "id": _id,
            "git": {
                "url": git_url,
                "branch": git_branch
            },
            "framework": framework,
            "split_run": split_run,
            "clients": self.clients if split_run else [client]
        }
        return app_dict

    def play(self):
        playbooks = self.make_playbook()
        for index, group in enumerate(playbooks):
            print(f"======= 开始执行 group {index + 1} =======")
            executor = ThreadPoolExecutor()
            tasks = []
            only_one = len(group) == 1
            for app in group:
                cmd = self._generate_command(app, only_one)
                print(cmd)
                print("多线程并行")
            #     t = executor.submit(os.system, cmd)
            #     tasks.append(t)
            # wait(tasks, return_when=ALL_COMPLETED)
            print(f"======= 结束执行 group {index + 1} =======\n")

    def _generate_command(self, app: Dict, only_one: bool) -> str:
        framework = app.get("framework")
        clients = app.get("clients")
        app_name = app.get("app_name")
        if framework == "youqu2":
            cmd = f"python3 manage.py remote -a {app_name} -c {'/'.join(clients)} -t '{self.tags}' {'' if only_one else '-y'} -e"
        elif framework == "youqu3":
            cmd = f'''python3 remote -w {app_name} -c {f"{{{'/'.join(clients)}}}" if only_one else '/'.join(clients)} -t "{self.tags}"'''
        else:
            raise EnvironmentError(f"Framework: {framework} not supported")
        return cmd

def playbook(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        info = json.load(f)
    apps = info.get("apps")
    clients = info.get("clients")
    tags = info.get("tags")
    pb = PlayBook(apps=apps, clients=clients, tags=tags)
    pb.play()


if __name__ == '__main__':
    playbook("../info.json")
