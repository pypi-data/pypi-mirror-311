from .types import Service
from ..auth.agent import CartaAgent


def register_service(namespace: str, service: str, url: str) -> Service:
    from pycarta import get_agent
    agent = get_agent()
    response = agent.post(f'service/register/{namespace}/{service}',
                          params={
                              "baseUrl": url,
                          })
    return Service(**response.json())


def unregister_service(namespace: str, service: str) -> bool:
    from pycarta import get_agent
    agent = get_agent()
    agent.delete(f'service/register/{namespace}/{service}')
    return True


def rename_service(namespace: str, current_service: str, new_service: str) -> bool:
    from pycarta import get_agent
    agent = get_agent()
    agent.patch(f'service/register/{namespace}/{current_service}/{new_service}')
    return True


def reserve_namespace(namespace: str):
    from pycarta import get_agent
    agent = get_agent()
    agent.post(f'service/reserve/{namespace}')
    return True


def remove_namespace(namespace: str):
    from pycarta import get_agent
    agent = get_agent()
    agent.delete(f'service/remove/{namespace}')
    return True


class ServiceUtility:

    def __init__(self, agent: CartaAgent, namespace: str, service: str):
        self.agent = agent
        self.service_path = f"service/{namespace}/{service}/"

    def get(self, endpoint: str, **kwargs):
        self.agent.get(self.service_path + endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        self.agent.post(self.service_path + endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        self.agent.put(self.service_path + endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        self.agent.patch(self.service_path + endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        self.agent.post(self.service_path + endpoint, **kwargs)


def utilize_service(namespace: str, service: str) -> ServiceUtility:
    from pycarta import get_agent
    agent = get_agent()
    return ServiceUtility(agent, namespace, service)
