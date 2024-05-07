from flask import Blueprint, jsonify
from kubernetes import client, config

# Create a blueprint for Kubernetes routes
kubernetes_blueprint = Blueprint('kubernetes', __name__)

# Load the Minikube or default kubeconfig
config.load_kube_config()  # or config.load_incluster_config() for in-cluster config

# API Clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
networking_v1 = client.NetworkingV1Api()

@kubernetes_blueprint.route('/get_all_resources', methods=['GET'])
def get_all_resources():
    # Retrieve Deployments
    deployments = apps_v1.list_deployment_for_all_namespaces()
    deployments_list = [{'namespace': d.metadata.namespace, 'name': d.metadata.name} for d in deployments.items]

    # Retrieve Services
    services = v1.list_service_for_all_namespaces()
    services_list = [{'namespace': s.metadata.namespace, 'name': s.metadata.name} for s in services.items]

    # Retrieve Ingresses
    ingresses = networking_v1.list_ingress_for_all_namespaces()
    ingresses_list = [{'namespace': i.metadata.namespace, 'name': i.metadata.name} for i in ingresses.items]

    # Retrieve Pods
    pods = v1.list_pod_for_all_namespaces()
    pods_list = [{'namespace': p.metadata.namespace, 'name': p.metadata.name} for p in pods.items]

    # Compile all results into a dictionary
    resources = {
        'deployments': deployments_list,
        'services': services_list,
        'ingresses': ingresses_list,
        'pods': pods_list
    }

    # Return all resources as a JSON response
    return jsonify(resources), 200
