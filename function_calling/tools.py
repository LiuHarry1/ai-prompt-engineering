global tools

tools = [{"name": "shut_down_component",
          "inputs": ["component name"],
          "description": "a tool to shut down a certain component. ",
          "web_url": "web rest api shut_down_component",
          "return_message": "The announcement component is now down. ",
          "error_message": "error while calling the tool of shut_down_component"
          },
        {"name": "start_up_component",
         "inputs": ["component name"],
         "description": "a tool to start up or roll out a certain component. ",
         "web_url": "web rest api start_up_component",
         "return_message": "The announcement component is now started and ready for use.",
         "error_message": "error while calling the tool of start_up_component"
         },
        {"name": "scale_component",
         "inputs": ["component name", "the number of pods to be scaled to"],
         "description": "a tool to scale up or down to a certain number of pods.",
         "web_url": "web rest api scale_component",
         "return_message": "The number of announcement pods is 2.",
         "error_message": "error while calling the tool of scale_component"
         },
        {"name": "select_pod_count",
         "inputs": ["component name"],
         "description": "a tool to select the current number of pods for a certain component. ",
         "web_url": "web rest api select_pod_count",
         "return_message": "The number of announcement pods is 3.",
         "error_message": "error while calling the tool of select_pod_count"
         }
]


def get_tool_name_and_descpritions():
    tool_name_and_descriptions = []
    for tool in tools:
        tool_name_and_descriptions.append({"name": tool['name'], "inputs": tool["inputs"],  "description": tool["description"]})
    return tool_name_and_descriptions

def get_tool_names():
    tool_names = []
    for tool in tools:
        tool_names.append(tool['name'])
    return tool_names

def get_web_url(tool_name):
    for tool in tools:
        if tool_name == tool['name']:
            return tool["web_url"]

def get_tool(tool_name):
    for tool in tools:
        if tool_name == tool['name']:
            return tool

def call_tool(tool_name, inputs):
    print(f"calling {tool_name} with input: {inputs}")

    return_message, url, json_data = web_call(tool_name, inputs)
    return return_message, url, json_data

def web_call(tool_name, inputs ):
    tool = get_tool(tool_name)
    url = tool["web_url"]
    json_data = {}
    try:
        print(f"calling {url} with json {json_data}")
    except Exception as e:
        return tool["error_message"]

    return tool["return_message"], url, json_data


if __name__ == '__main__':
    # print(get_tool_name_and_descpritions())
    # print(call_tool("select_pod_count", "announcement"))
    print(tools)
    tools[0]['name'] = 'fuck'

    print(tools)
    print(get_tool_name_and_descpritions())


