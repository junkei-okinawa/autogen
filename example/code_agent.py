from autogen import config_list_from_json
import autogen

PROJECT_NAME = "sample_code_agent"

# Get api key
config_list = config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        # "model": ["gpt-3.5-turbo", "gpt-35-turbo", "gpt-35-turbo-0613", "gpt-4", "gpt4", "gpt-4-32k"],
        # "model": ["Xwin-LM-13B-v0.2-GGUF"],
        "model": ["mistralmakise-merged-13b"],
    },
)

llm_config = {
  "config_list": config_list, 
  "seed": 23, 
  "request_timeout": 600,
  "temperature": 0.1,
  }

# Create user proxy agent, coder, product manager
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    # system_message="A human admin who will give the idea and run the code provided by Coder.",
    system_message="""
Reply TERMINATE if the task has been solver at full satisfaction Otherwise, reply CONTINUE, or the reason why the task is not solved yet.
""",
    max_consecutive_auto_reply=10,
    code_execution_config={
      "last_n_messages": 2, 
      "work_dir": f"""groupchat/seed_{llm_config["seed"]}""",
      "use_docker": "python:latest",
      },
    human_input_mode="TERMINATE",
    # human_input_mode="ALWAYS",
)

product_manager = autogen.AssistantAgent(
    name="project_manager",
    system_message=f"""
You are a professional project manager; the goal is to design a concise, usable, efficient project
""",
    llm_config=llm_config,
)

architect = autogen.AssistantAgent(
    name="architect",
    llm_config=llm_config,
    system_message=f"""
You are a professional system architect. You design complete Python systems that are concise, easy to use, and complete.
"""
)

# project_manager = autogen.AssistantAgent(
#     name="project_manager",
#     system_message=f"""
# # most important requirement
# All responses should be limited to {config_list[0]["max_tokens"] / 2} tokens or less. If necessary, split responses into sections.
# # Your mission
# Improve team efficiency and deliver with quality and quantity.
# # Role
# You are a project manager; the goal is to break down tasks according to PRD/technical design, give a task list, and analyze task dependencies to start with the prerequisite modules
# Requirements: Based on the context, fill in the following missing information, each section name is a key in json. Here the granularity of the task is a file, if there are any missing files, you can supplement them
# Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote.

# ## Required Python third-party packages: Provided in requirements.txt format

# ## Required Other language third-party packages: Provided in requirements.txt format

# ## Full API spec: Use OpenAPI 3.0. Describe all APIs that may be used by both frontend and backend.

# """,
#     llm_config=llm_config,
# )

coder = autogen.AssistantAgent(
    name="Coder",
    system_message=f"""
You are a professional Enginner and write code that is elegant, readable, extensible, and efficient with Python.
""",
    llm_config=llm_config,
)

# Create groupchat
groupchat = autogen.GroupChat(
    # agents=[user_proxy, product_manager, architect, coder], messages=[])
    agents=[user_proxy, architect, coder], messages=[])
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

first_message = """
Write code a classic & basic pong game with 2 players in python, and store the created code to a file.
## Requirements
1. screen width should be 1200px, height 600px
2. display a "GameOver" screen when the ball hits the left or right wall. and The GameOver screen also has "Continue" and "End" buttons, and clicking "Continue" will restart the game. Clicking on "Continue" will restart the game, and clicking on "End" will close the screen and end the game.
3. Press "Ctrl" + "C" during a game to safely exit the game
4. As simple as possible
5. Coder to write code.
6. Next to the Coder writing the code, User_proxy should be appointed.
"""
# 4. Programs are created in different files for each function.

# Start the conversation
user_proxy.initiate_chat(
    manager, message=first_message
    )