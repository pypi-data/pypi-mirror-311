import requests, sys, json

base_parameters={
    "api-version":"7.1-preview.1"
}

def create_pr(API_URL, TOKEN, REPO_ID, params, sourceRefName, targetRefName, pr_title) -> object:
    """
    Creates a Pull Request (PR) in a specified repository.

    Args:
        API_URL (str): Base URL of the API for creating PRs.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR will be created.
        params (dict): Additional parameters for creating the PR.
        sourceRefName (str): Name of the source branch for the PR.
        targetRefName (str): Name of the target branch for the PR.
        pr_title (str): Title of the Pull Request.

    Returns:
        object: Dictionary with information about the success or failure of the PR creation, including function code and PR details.
        response: {
                "function_code":value, \n
                "message": value, \n
                "lastMergeSourceCommit": value, \n
                "pullRequestId": value \n
            }
        response={
            "funcition_code":value,
            "message":value
        }
    """

    body_pr=json.dumps({
        "sourceRefName": f"refs/heads/{sourceRefName}",
        "targetRefName": f"refs/heads/{targetRefName}",
        "title": f"{pr_title} {sourceRefName} to {targetRefName}"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f"Basic {TOKEN}"
    }
    if params:
        base_parameters.update(params) 
    try:
        response=json.loads(requests.post(url=f"{API_URL}/repositories/{REPO_ID}/pullrequests", data=body_pr, headers=headers, params=base_parameters).text)
        if response['status_code'] == 201 and response['status'] == "active":
            def_response={
                "function_code":200,
                "message": "PR Creada correctamente",
                "lastMergeSourceCommit": {f"{response['lastMergeSourceCommit']}"},
                "pullRequestId": f"{response['pullRequestId']}"
            }
        else:
            def_response={
                "function_code":f"{response['status_code']}",
                "message":f"{response['message']}"
            }            
        return def_response
    except requests.RequestException as e: 
        print(f"Error al crear la pr \n {e.strerror}")
        sys.exit(1)

def get_pr_data(API_URL, TOKEN, REPO_ID, params, sourceRefName, targetRefName) -> object:
    """
    Retrieves data about a specific Pull Request (PR) based on branch information.

    Args:
        API_URL (str): Base URL of the API for retrieving PR data.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository to search for the PR.
        params (dict): Additional parameters for retrieving PR data.
        sourceBranch (str): Name of the source branch for the PR.
        targetBranch (str): Name of the target branch for the PR.

    Returns:
        object: Dictionary with information about the PR, including function code and response data.
        ok_response={
            "funcition_code":value,
            "response_json":value
        }
        response={
            "funcition_code":value,
            "message":value
        }
    """

    parameters_get_prs={
    "searchCriteria.repositoryId":f"{REPO_ID}",
    "searchCriteria.status":"active",
    "searchCriteria.targetRefName":f"{targetRefName}",
    "searchCriteria.sourceRefName":f"{sourceRefName}"
    }
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {TOKEN}"
    }
    base_parameters.update(parameters_get_prs)
    if params:
        base_parameters.update(params)
    try:
        response=json.loads(requests.get(url=f"{API_URL}/pullrequests", params=base_parameters, headers=headers).text)
        if response['status_code'] == 200:
            def_response={
                    "function_code":200,
                    "response_json": f"{response[0]}"
                }
        else:
            def_response={
                "function_code":f"{response['status_code']}",
                "message":f"{response['message']}"
            } 
        return def_response
    except requests.RequestException as e:
        print(f"Error al obtener datos de la PR: \n {e.strerror}")
        sys.exit(1)

def add_reviwer(API_URL, TOKEN, REPO_ID, params, pullRequestId, reviewerId) -> object:
    """
    Adds a required reviewer to a Pull Request.

    Args:
        API_URL (str): Base URL of the API for adding a reviewer.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for adding the reviewer.
        pullRequestId (str): ID of the Pull Request.
        reviewerId (str): ID of the reviewer to be added.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        response={
            "funcition_code":value,
            "message":value
        }
    """

    data = {
        "vote": 0,
        "isRequired": True
    }
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {TOKEN}"
    }
    if params:
        base_parameters.update(params)
    try:
        response = requests.put(url=f"{API_URL}/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=headers, params=base_parameters, data=json.dumps(data))
        if response.status_code == 200:
            json_response={
                "funcition_code":200,
                "message":f"Revisor {response['displayName']} agregado correctamente a la PR {pullRequestId}."
            }
        else:
            json_response={
                "funcition_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al añadir un reviwer: \n {e.strerror}")
        sys.exit(1)

def approve_pr(API_URL, TOKEN, REPO_ID, params, pullRequestId, reviewerId) -> object:
    """
    Approves a Pull Request as a reviewer.

    Args:
        API_URL (str): Base URL of the API for approving a PR.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for approving the PR.
        pullRequestId (str): ID of the Pull Request to be approved.
        reviewerId (str): ID of the reviewer approving the PR.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        response={
            "funcition_code":value,
            "message":value
        }
    """

    data = {
        "vote": 10  # 10 significa que el revisor aprueba la PR
    }
    headers={
        "Authorization": f"Basic {TOKEN}"
    }
    try:
        response = requests.put(url=f"{API_URL}/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=headers, data=json.dumps(data), params=params)
        if response.status_code == 200:
            json_response={
                "funcition_code":200,
                "message":f"Revisor {response['displayName']} ha aprobado la PR {pullRequestId}."
            }
        else:
            json_response={
                "funcition_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al aprobar la pr: \n {e.strerror}")
        sys.exit(1)

def complete_pr(API_URL, TOKEN, REPO_ID, params, pullRequestId, commitData) -> object:
    """
    Completes (merges) a Pull Request.

    Args:
        API_URL (str): Base URL of the API for completing a PR.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for completing the PR.
        pullRequestId (str): ID of the Pull Request to be completed.
        commitData (dict): Data about the commit to be merged, including 'commitId' and 'url'.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        response={
            "funcition_code":value,
            "message":value
        }
    """

    data = {
        "status": "completed",
        "lastMergeSourceCommit": {
            "commitId": f"{commitData['commitId']}",
            "url": f"{commitData['url']}"
        },
        "completionOptions": {
            "deleteSourceBranch": True,
            "mergeCommitMessage": "PR completada automáticamente",
            "squashMerge": False
        }
    }
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {TOKEN}"
    }
    try:
        response = requests.post(url=f"{API_URL}/repositories/{REPO_ID}/pullrequests/{pullRequestId}", headers=headers, data=json.dumps(data), params=params)
        if response.status_code == 200:
            json_response={
                "funcition_code":200,
                "message":f"PR {pullRequestId} completada y mergeada correctamente."
            }
        else:
            json_response={
                "funcition_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al completar la pr: \n {e.strerror}")
        sys.exit(1)

def get_project(API_URL, TOKEN, name) -> object:
    """
    Retrieves information about a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving project information.
        TOKEN (str): Authorization token for API access.
        name (str): Name of the project to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and project ID.
        response{
            function_code: value,
            projectId: value,
            message: value
            }
    """

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {TOKEN}'
    }
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects", headers=headers, params=base_parameters)
        if response.status_code == 200:
            for project in response['value']:
                if project['name'] == name:
                    json_response={
                        "funcition_code":200,
                        "projectId": f"{project['id']}",
                        "message":f"Obtencion de projectos correcto"
                    }
        else:
            json_response={
                "funcition_code":f"{response.status_code}",
                "projectId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los proyectos: \n {e.strerror}")
        sys.exit(1)

def get_teams_by_projectId(API_URL, TOKEN, project_id, team_name) -> object:
    """
    Retrieves information about a specific team in a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving team information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_name (str): Name of the team to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and team ID.
        response={
            "funcition_code": value,
            "teamId": value,
            "message": value
        }
    """

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {TOKEN}'
    }
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams", headers=headers, params=base_parameters)
        if response.status_code == 200:
            for team in response['value']:
                if team['name'] == team_name:
                    json_response={
                        "funcition_code":200,
                        "teamId": f"{team['id']}",
                        "message":f"Obtencion de equipos correcto"
                    }
        else:
            json_response={
                "funcition_code":f"{response.status_code}",
                "teamId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los equipos: \n {e.strerror}")
        sys.exit(1)

def get_reviewer_id_by_team_id(API_URL, TOKEN, project_id, team_id, user_email) -> object:
    """
    Retrieves the reviewer ID by team ID and user email.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_id (str): ID of the team.
        user_email (str): Email of the user whose reviewer ID is needed.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and reviewer ID.
        response={
            "funcition_code":value,
            "reviwerId": value,
            "message":value
        }
    """

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {TOKEN}'
    }
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams/{team_id}/members", headers=headers, params=base_parameters)
        if response.status_code == 200:
            for user in response:
                if user['uniqueName'] == user_email:
                    json_response={
                        "funcition_code":200,
                        "reviwerId": f"{user['id']}",
                        "message":f"Obtencion de Id de usuario correcto"
                    }
        else:
            json_response={
                "funcition_code":f"{response.status_code}",
                "reviwerId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)
