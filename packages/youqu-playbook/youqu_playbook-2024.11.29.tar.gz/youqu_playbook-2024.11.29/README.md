# PlayBook

YouQu 任务调度框架

## 安装

```bash
pip3 install youqu-playbook
```

## 运行

```bash
playbook --input-json-path path/to/json/file.json
```

比如在当前目录下运行：

```bash
playbook --input-json-path ./info.json
```

## 输入JSON配置文件

JSON 配置示例：
```json
{
  "apps": [
    {
      "app_name": "autotest_dde_file_manager",
      "git_url": "git_url",
      "git_branch": "at-develop/eagle",
      "framework": "youqu2",
      "split_run": true,
      "order": 1
    },
    {
      "app_name": "kernel",
      "git_url": "git_url",
      "git_branch": "at-develop/v25",
      "framework": "youqu3",
      "split_run": false,
      "order": 2
    },
    ...
  ],
  "clients": [
    "uos@10.8.15.19",
    "uos@10.8.15.20",
    ...
  ],
  "tags": "CICD",
  "task_id": "xxxx",
  "json_backfill_base_url": "xxxx",
  "json_backfill_user": "xxxx",
  "json_backfill_password": "xxxx",
  "pms_task_id": "xxxx",
  "pms_user": "xxxx",
  "pms_password": "xxxx"
}
```

## 流程示意图

![](./images/playbook.png)