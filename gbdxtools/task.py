'''
Authors: Donnie Marino, Kostas Stamatiou
Contact: dmarino@digitalglobe.com

Class to represent a workflow task
'''
import json, uuid

class Task:

    def __init__(self, interface, task_name, **kwargs):
        '''Construct an instance of GBDX Task

         Args:
            optional keywords:
                name (string): The task name.
                input_port_descriptors (list): A list of the input port descriptors.
                output_port_descriptors (list): A list of the output port descriptors.
                container_descriptors (list): A list of the container descriptors.
                properties (dict): A dictionary of task properties.
        Returns:
            An instance of Task.
            
        '''

        self.input_data = []
        self.id = task_name + '_' + str(uuid.uuid4())

        self.interface = interface
        self.name = task_name
        self.definition = self.interface.workflow.describe_task(task_name)
        self.domain = self.definition['containerDescriptors'][0]['properties'].get('domain','default')

        # all the other kwargs are input port values or sources
        self.set(**kwargs)
   
    # get a reference to the output port
    def get_output(self, port_name):
        output_port_names = [p['name'] for p in self.output_ports]
        if port_name not in output_port_names:
            raise Exception('Invalid output port %s.  Valid output ports for task %s are: %s' % (port_name, self.name, output_port_names))

        return "source:" + self.id + ":" + port_name

    # set input ports source or value
    def set( self, **kwargs ):
        input_port_names = [p['name'] for p in self.input_ports]
        for input_port in kwargs.keys():
            if input_port in input_port_names:
                self.input_data.append({input_port: kwargs[input_port]})
                # set the value/source
            else:
                raise Exception('Invalid input port %s.  Valid input ports for task %s are: %s' % (input_port, self.name, input_port_names))

    @property
    def input_ports(self):
        return self.definition['inputPortDescriptors']

    @input_ports.setter
    def input_ports(self, value):
        raise NotImplementedError("Cannot set input ports")

    @property
    def output_ports(self):
        return self.definition['outputPortDescriptors']

    @output_ports.setter
    def output_ports(self, value):
        raise NotImplementedError("Cannot set output ports")

    @classmethod
    def from_json(cls,task_desc):
        '''Contstruct a new instance of task from the task descriptor

        Args:
            task_desc (string): JSON string task description.

        Returns:
            An instance of Task.

        '''
        """
        {
        "containerDescriptors": [{
            "properties": {"domain": "raid"}}],
        "name": "AOP",
        "inputs": [{
            "name": "data",
            "value": "INPUT_BUCKET"
        }, {
            "name": "bands",
            "value": "Auto"
        },
           {
            "name": "enable_acomp",
            "value": "false"
        }, {
            "name": "enable_dra",
            "value": "false"
        }, {
            "name": "ortho_epsg",
            "value": "EPSG:4326"
        }, {
            "name": "enable_pansharpen",
            "value": "false"
        }],
        "outputs": [{
            "name": "data"
        }, {
            "name": "log"
        }],
        "timeout": 36000,
        "taskType": "AOP_Strip_Processor",
        "containerDescriptors": [{"properties": {"domain": "raid"}}]
        }
        """
        js_task = json.loads(task_desc)
        
        # validate the descriptor
        if (
                (js_task["name"] is None) or 
                (js_task["properties"] is None) or 
                (js_task["inputPortDescriptors"] is None) or 
                (js_task["outputPortDescriptors"] is None) or 
                (js_task["containerDescriptors"] is None)
           ):
            raise("Incomplete task descriptor")

        t = Task(
            name=js_task["name"],
            properties=js_task["properties"],
            input_port_descriptors=js_task["inputPortDescriptors"],
            output_port_descriptors=js_task["outputPortDescriptors"],
            container_descriptors=js_task["containerDescriptors"]
        )

        return t

    def to_json(self):
        d = {
            "name": self.name,
            "properties": self.properties,
            "containerDescriptors": self.container_descriptors,
            "inputPortDescriptors": self.input_port_descriptors,
            "outputPortDescriptors": self.output_port_descriptors
        }
        return json.dumps(d)


class Workflow:
    def __init__(self, interface, tasks, **kwargs):
        self.interface = interface

        self.definition = self.workflow_skeleton()

        for task in tasks:
            print task.id

    def workflow_skeleton(self):
        return {
            "tasks": [],
            "name": "StageToS3",
        }


