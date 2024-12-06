import requests

def send_slack_alert(context, slack_webhook_url, subteam_tag):
    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    execution_date = context.get("execution_date")
    log_url = task_instance.log_url
    params = context.get("params", {})

    params_str = "\n".join([f"{k}: {v}" for k, v in params.items()])

    message = (
        f"⚠️ *DAG Failure Alert* ⚠️\n\n"
        f"{subteam_tag} please take a look at the failure."
        f"*DAG*: `{dag_id}`\n"
        f"*Config Params:*\n{params_str}\n\n"
        f"*Execution Date*: `{execution_date}`\n"
        f"*Log URL*: <{log_url}|Click here>\n"
    )

    headers = {"Content-Type": "application/json"}
    payload = {"text": message}

    response = requests.post(slack_webhook_url, json=payload, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}: {response.text}")