import os

class ServiceDNS(object):
    """
    Cheap and simple DNS to lookup microservices on Google Cloud Run
    """
    _DNS =  {
        'backend-service': {

            'development': {
                'hostname': 'localhost',
                'port': 50051
            },
            'production': {
                'hostname': os.getenv("BACKEND_SERVICE_URL", None),
                'port': 443
            },
        }
    }

    @staticmethod
    def get_dns(service:str, environment:str) -> (str, str):
        """
        Get the DNS details for a service and the environment

        :param  service:        The service being looked up, i.e. data-service
        :param environment:     The environment details to get, i.e. production
        :returns:               The hostname:str and port:int
        :raises:                ValueError if not found
        """
        if service in ServiceDNS._DNS:
            service_dns = ServiceDNS._DNS[service]
            if environment in service_dns:
                return service_dns[environment]['hostname'], service_dns[environment]['port']
            else:
                raise ValueError(f"The Service {service} does not have details for environment {environment}")
        else:
            raise ValueError(f"The Service {service} doesn't exist.")