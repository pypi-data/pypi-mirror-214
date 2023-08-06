# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dane_server']

package_data = \
{'': ['*'], 'dane_server': ['web/*', 'web/js/*']}

install_requires = \
['dane>=0.3.6,<0.4.0',
 'elasticsearch7',
 'flask-restx',
 'flask>=2.1.0,<2.2.0',
 'pika',
 'requests',
 'werkzeug<2.2.0']

setup_kwargs = {
    'name': 'dane-server',
    'version': '0.3.1',
    'description': "Back-end for the Distributed Annotation 'n' Enrichment (DANE) system",
    'long_description': '# DANE-server\nDANE-server is the back-end component of [DANE](https://github.com/CLARIAH/DANE) and takes care of task routing as well as the (meta)data storage. A task submitted to \nDANE-server is registered in a database, and then its `.run()` function is called. Running a task involves assigning it to a worker via a message queue.\n\nA specific task is run by publishing the task to a [RabbitMQ Topic Exchange](https://www.rabbitmq.com/tutorials/tutorial-five-python.html),\non this exchange the task is routed based on its Task Key. The task key corresponds to the `binding_key` of a worker,\nand each worker with this binding_key listens to a shared queue. Once a worker is available it will take the next task from the queue and process it.\n\nDANE-server depends on the [DANE](https://github.com/CLARIAH/DANE) package for the logic of how to iterate over tasks, and how to interpret a task\nin general.\n\n# Local Installation\n\nDANE-server has been tested with Python 3 and is installable through pip:\n\n    pip install dane-server\n\nBesides the python base, the DANE-server also relies on an [Elasticsearch](https://www.elastic.co/elasticsearch/) server (version 7.9) for storage, \nand [RabbitMQ](https://www.rabbitmq.com/) (tested with version 3.7) for messaging.\n\nAfter installing all dependencies it is necessary to configure the DANE server, how to do this is described here: https://dane.readthedocs.io/en/latest/intro.html#configuration\n\nThe base config for DANE-server consists of the following parameters, which you might want to overwrite:\n\n```\nLOGGING: \n    DIR: "./dane-server-logs/"\n    LEVEL: "DEBUG"\nDANE_SERVER:\n    TEMP_FOLDER: "/home/DANE/DANE-data/TEMP/"\n    OUT_FOLDER: "/home/DANE/DANE-data/OUT/"\n```\n\n# Usage\n\n*NOTE: DANE-server is still in development, as such authorisation (amongst other featueres) has not yet been added. Use at your own peril.*\n\nRun the server component (which listens to the RabbitMQ) as follows:\n\n    dane-server\n\nBesides the server component we also need the API, which we can start with:\n\n    dane-api\n\nIf no errors occur then this should start a webserver (at port 5500) which will handle API requests, \nwhile in the background the server will handle interaction with the DB and RabbitMQ.\n\n## API\n\nThe DANE api is documented with a swagger UI, available at: http://localhost:5500/DANE/\n\n## Examples\n\nExamples of how to work with DANE can be found at: https://dane.readthedocs.io/en/latest/examples.html\n\n# Docker\n\nTo run DANE-server, using Docker make sure to install a Docker Engine, e.g. Docker Desktop for OSX.\n\n## Build the Docker images\n\nAs the DANE-server has two separate processes. Two images need to be created:\n\n- One for running the Task Scheduler\n- One for running the API\n\nRun the following from the main directory of this repo:\n\n```\ndocker build -t dane-server -f Dockerfile.ts .\ndocker build -t dane-server-api -f Dockerfile.api .\n```\n\n**Note**: currently the build relies on the `es-index-cfg` branch of DANE (see `requirements.txt`)\n\nAfter the images have been successfully built, it is possible to run DANE-server via Kubernetes as well\n\n# Kubernetes\n\nThese instructions are optimized for `minikube`, which is for local development only. For deployment to a proper k8s cluster, you\'re on your own for now...\n\nNote that the provided Kubernetes config only provisions your k8s cluster with:\n\n- Endpoint to external Elasticsearch (make sure you got one running)\n- RabbitMQ\n- DANE server (task scheduler)\n- DANE server API\n\nIn order to get a bunch of workers setup, you can check the k8s config files in [DANE-asr-worker](https://github.com/beeldengeluid/DANE-asr-worker) repository (later on more examples should follow).\n\n## Create a configmap for config.yml\n\nFirst make sure to create the config.yml from the config-k8s.yml:\n\n```\ncp config-k8s.yml config.yml\n```\n\nNow before applying the Kubernetes file `dane-server-k8s.yaml` to your cluster, first create a ConfigMap for config.yml\n\n```\nkubectl create configmap dane-server-cfg --from-file config.yml\n```\n\nNow the ConfigMap is there, make sure to check that dane-server-k8s.yml points to a existing Elasticsearch host. After that you can go ahead and run:\n\n```\nkubectl apply -f dane-server-k8s.yaml\n```\n\n## Configure your local DNS to access the API (and RabbitMQ dashboard)\n\nCheck the ip assigned to the `dane-server-ingress` (and `dane-rabbitmq-ingress`) by running:\n\n```\nkubectl get ingress\n```\n\ngrab the IP from the `ADDRESS` column and put this in your `/etc/hosts` file:\n\n```\n{IP}    api.dane.nl rabbitmq.dane.nl\n```\n\n**Note**: you can assign different domain names by editing the Ingresses in `dane-server-k8s.yaml`\n',
    'author': 'Nanne van Noord',
    'author_email': 'n.j.e.vannoord@uva.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CLARIAH/DANE',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
