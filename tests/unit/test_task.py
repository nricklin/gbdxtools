'''
Unit tests for the Task class
'''
import pytest
import json

from gbdxtools.task import Task

def test_plain_init():
    t = Task()
    t.name = "Testtask"
    assert isinstance(t, Task)
    assert t.name is not None
    assert t.name == "Testtask"

def test_init_w_args():
    tname = "TestTasks2023"
    test_cd = ["foo","bar","bat"]
    t = Task(name=tname, container_descriptors=test_cd)
    assert isinstance(t, Task)
    assert t.name == "TestTasks2023"
    assert t.container_descriptors is not None
    assert "bar" in t.container_descriptors

def init_from_json():
    task_desc = {
        "name": "test454",
        "properties": {"prop1": "test", "prop2": "testing" },
        "containerDescriptors": ["a","n","j","d"],
        "inputPortDescriptors": ["one","seven"],
        "outputPortDescriptors": ["masters","usopen","open_championship","pga"]
    }
    task_json_string = json.dumps(task_desc)
    t = Task.from_json(task_json_string)

    assert isinstance(t, Task)
    assert t.name == "test454"
    assert t.properties["prop2"] == "testing"
    assert "j" in t.container_descriptors
    assert "one" in t.input_port_descriptors
    assert "pga" in t.output_port_descriptors

def fail_init_from_json():
    task_desc = "someBSString"
    with pytest.raises() as exception:
        t = Task.from_json(task_desc)
        assert str(exception.value) == "Incomplete task descriptor"

def test_to_json():
    t = Task()
    t.name = "Testin125"
    assert isinstance(t, Task)
    task_json = t.to_json()
    assert task_json is not None
    js_task = json.loads(task_json)
    assert js_task["name"] == "Testin125"
