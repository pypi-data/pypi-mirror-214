# Datatonic Pipeline Components

Reusable pipeline components for Vertex Pipelines.

## Install

Run `poetry add git+https://github.com/teamdatatonic/datatonic-pipeline-components.git#main` in your project.

## Use

```python 
import datatonic_pipeline_components as dtpc

@pipeline
def my_pipeline():
    dtpc.gpt_tokenize()
```

The following figure summarises the overall workflow of using components:

![Cloud Architecture](docs/images/usage_workflow.png)
