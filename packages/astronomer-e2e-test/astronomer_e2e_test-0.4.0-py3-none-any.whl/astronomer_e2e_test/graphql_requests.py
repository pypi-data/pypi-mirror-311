#!/usr/bin/env python3

import json


def delete_deployment(client, workspace_id, deployment_id):
    query = """
    mutation deleteDeployment($id: Uuid!) {
      deleteDeployment(deploymentUuid: $id) {
        id: uuid
        __typename
      }
    }
    """
    variables = {"id": deployment_id, "queryVars": {"workspaceId": workspace_id}}
    client.execute(query, variables=variables)


def delete_workspace(client, workspace_id):
    query = """
    mutation deleteWorkspace($id: Uuid!) {
        deleteWorkspace(workspaceUuid: $id) {
            id: uuid
            __typename
        }
    }
    """
    variables = {"id": workspace_id}
    client.execute(query, variables=variables)


def create_deployment(client, deployment_name, workspace_id, executor="KubernetesExecutor"):
    print(f"Creating deployment {deployment_name}, {executor}")
    query = """
    mutation createDeployment($type: String!,
                              $label: String!,
                              $workspaceId: Uuid!,
                              $version: String,
                              $description: String,
                              $config: JSON,
                              $env: JSON,
                              $properties: JSON) {
      createDeployment(workspaceUuid: $workspaceId,
                       type: $type,
                       label: $label,
                       version: $version,
                       description: $description,
                       config: $config,
                       env: $env,
                       properties: $properties) {
                         ...deployment
                         __typename
                       }
    }
    fragment deployment on Deployment {
      id: uuid
      label
      description
      type
      releaseName
      version
      airflowVersion
      workspace {
        id: uuid
        __typename
      }
      urls {
        type
        url
        __typename
      }
      createdAt
      updatedAt
      config
      env
      properties
      __typename
    }
    """
    variables = {
        "type": "airflow",
        "workspaceId": workspace_id,
        "config": {"executor": executor},
        "label": deployment_name,
    }
    return json.loads(client.execute(query, variables=variables))


def create_workspace(client, workspace_name):
    print(f"Creating workspace {workspace_name}")
    query = """
    mutation createWorkspace($label: String!, $description: String) {
      createWorkspace(label: $label, description: $description) {
        ...workspace
        __typename
      }
    }
    fragment workspace on Workspace {
      id: uuid
      label
      description
      createdAt
      updatedAt
      deploymentCount
      workspaceCapabilities {
        canUpdateIAM
        __typename
      }
      trialEndsAt
      paywallEnabled
      __typename
    }
    """
    variables = {"label": workspace_name}
    return json.loads(client.execute(query, variables=variables))
