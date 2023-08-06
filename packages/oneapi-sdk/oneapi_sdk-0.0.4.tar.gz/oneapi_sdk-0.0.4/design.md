# Design

## Overview

The design of the project is based on the following principles:
- **Modularity**: The project is divided into several modules, each of which is responsible for a specific task.
- **Extensibility**: The project is designed to be easily extensible, so that new modules can be added without much effort.
- **Simplicity**: The project is designed to be as simple as possible, so that it is easy to understand and maintain.

## Modules

The project is divided into the following modules:
- **oneapi**: The main module, which contains the API client and the resource classes.
- **oneapi.api_resources**: This module contains the API resource classes, which models the data returned by the API.
- **oneapi.api_resources.abstract**: This module contains the abstract API resource classes, which are used to make requests to the API.
- **oneapi.test**: This module contains the unit tests for the project.
- **oneapi.utils**: This module contains utility functions used by the project.

## Main Ideas

The main ideas behind the project, in junction with the principles mentioned above, are:
- **Resource classes**: The resource classes are the models used to represent the data returned by the API, like **Movie** and **Quote**, those can be easily extended to add new functionality.
- **API Requestor**: The API Requestor is the class responsible for making requests to the API, can be extended to better handle errors and other things.
- **API Resource classes**: The API Resource classes are the classes responsible for making requests to the API, they are abstract classes that can be extended to add new functionality.

## Examples of Extensibility

The project is designed to be easily extensible, here are some examples of how it can be extended:
- **Adding new resources**: To add a new resource, you just need to create a new class that inherits from the desired kinds of resource, like **ListableAPIResource** and **RetrievableAPIResource**.
- **Adding new abstract resources**: To add a new abstract resource, you just need to create a new class that inherits from **APIResource** and define its static methods. E.g.:
```python
class CreatableAPIResource(APIResource):
    @staticmethod
    def create(data: dict) -> APIResource:
        raise NotImplementedError
```

## Tests

The project contains unit tests for the main modules, they can be run using the following command:
```bash
python -m pytest
```

## CI/CD

The project uses GitHub Actions for CI/CD, the workflow can be found in [.github/workflows/test.yaml](.github/workflows/test.yaml) and [.github/workflows/build-and-publish.yaml](.github/workflows/build-and-publish.yaml). The workflow is triggered on every push to the repository, and it runs the tests and builds the package. If the tests pass, the package is published to PyPI.
This is just a simple workflow and shouldn't be used in production, it is only used to demonstrate how CI/CD can be implemented using GitHub Actions.