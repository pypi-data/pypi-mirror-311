from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from toolmate import config, isServerAlive, print2, print3
from toolmate.utils.assistant import ToolMate
from toolmate.utils.tool_plugins import Plugins
from pydantic import BaseModel
import requests, argparse, json, uvicorn, re, os


# Create the parser
parser = argparse.ArgumentParser(description="ToolMate AI API server cli options")
# Add arguments
parser.add_argument('-b', '--backend', action='store', dest='backend', help="AI backend")
parser.add_argument('-k', '--key', action='store', dest='key', help="specify the API key for authenticating client access")
parser.add_argument('-ot', '--outputtokens', action='store', dest='outputtokens', help="override default maximum output tokens; accepts non-negative integers")
parser.add_argument('-p', '--port', action='store', dest='port', help="server port")
parser.add_argument('-s', '--server', action='store', dest='server', help="server address; '0.0.0.0' by default")
parser.add_argument('-t', '--temperature', action='store', dest='temperature', help="override default inference temperature; accepted range: 0.0-2.0")
# Parse arguments
args = parser.parse_args()

# app object
app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key") 

# Function to check the API key
async def get_api_key(api_key: str = Depends(api_key_header)):
    correct_key = args.key if args.key else config.toolmate_api_server_key
    if api_key != correct_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

class Request(BaseModel):
    wd: str
    instruction: str | None = "."
    chat: bool | None = False
    chatfile: str | None = None
    chatsystem: str | None = None
    outputtokens: str | None = None
    temperature: str | None = None
    defaulttool: str | None = None
    toolagent: bool | None = None

@app.post("/api/toolmate")
async def process_instruction(request: Request, api_key: str = Depends(get_api_key) if config.toolmate_api_server_key else ""):
    wd = request.wd
    instruction = request.instruction
    chat = request.chat
    chatfile = request.chatfile
    chatsystem = request.chatsystem
    outputtokens = request.outputtokens
    temperature = request.temperature
    defaulttool = request.defaulttool
    toolagent = request.toolagent

    # override chat system message agent once
    if chatsystem:
        current_chatsystem = config.toolmate.getCurrentChatSystemMessage()
        config.toolmate.setCustomSystemMessage(customChatMessage=chatsystem)
        print3(f"Chat system message changed for this request: {chatsystem}")

    # override tool selection agent once
    if toolagent is not None:
        current_toolagent = config.tool_selection_agent
        config.tool_selection_agent = toolagent

    # override default tool once
    if defaulttool and defaulttool in config.allEnabledTools:
        current_defaulttool = config.defaultTool
        config.defaultTool = defaulttool

    # override maximum output tokens once
    if outputtokens:
        current_outputtokens = config.toolmate.getCurrentMaxTokens(showMessage=False)
        try:
            outputtokens = int(outputtokens)
            if outputtokens < 0:
                print2("No change in maximum output tokens! Negative values not accepted!")
            else:
                config.toolmate.setMaxTokens(customMaxtokens=outputtokens)
                print3(f"Maximum output tokens changed for this request: {outputtokens}")
        except:
            print2("No change in maximum output tokens! Non-integer values not accepted!")
    
    # override current temperature once
    if temperature:
        current_temperature = config.llmTemperature
        try:
            temperature = float(temperature)
            if temperature < 0.0 or temperature > 2.0:
                print2("No change in temperature! Given value is out of acceptted range 0.0-2.0!")
            else:
                config.toolmate.setTemperature(temperature=temperature)
                print3(f"Temperature changed for this request: {temperature}")
        except:
            print2("No change in temperature! Non-float values not accepted!")

    if os.path.isdir(wd):
        os.chdir(wd)
    if chatfile and os.path.isfile(chatfile):
        config.currentMessages = config.toolmate.loadMessages(chatfile)
        chat = True
    if not instruction == ".":
        if not chat:
            config.currentMessages = config.toolmate.resetMessages()
        config.toolmate.runMultipleActions(instruction)
    response = [i for i in config.currentMessages if i.get("role", "") in ("user", "assistant")]

    # restore server configurations
    if chatsystem:
        config.toolmate.setCustomSystemMessage(customChatMessage=current_chatsystem)
        print3(f"Chat system message restored: {current_chatsystem}")
    if toolagent is not None:
        config.tool_selection_agent = current_toolagent
        print3(f"Tool selection agent restored: {current_toolagent}")
    if defaulttool and defaulttool in config.allEnabledTools:
        config.defaultTool = current_defaulttool
        print3(f"Default tool restored: {current_defaulttool}")
    if outputtokens:
        config.toolmate.setTemperature(temperature=current_outputtokens)
        print3(f"Maximum output tokens restored: {current_outputtokens}")
    if temperature:
        config.toolmate.setTemperature(temperature=current_temperature)
        print3(f"Temperature changed restored: {current_temperature}")

    return json.dumps(response)

@app.post("/api/tools")
async def process_tools(query: str, api_key: str = Depends(get_api_key) if config.toolmate_api_server_key else ""):
    if query := query.strip():
        searchPattern = query.strip().lower()
        if searchPattern == "@":
            #tools = config.allEnabledTools
            results = Plugins.checkAvailableTools(display=True, includeRequirements=True)
        else:
            results = [i for i in config.allEnabledTools if re.search(searchPattern, i)]
        return json.dumps({"results": results})

@app.post("/api/systems")
async def process_systems(query: str, api_key: str = Depends(get_api_key) if config.toolmate_api_server_key else ""):
    if query := query.strip():
        searchPattern = query.strip().lower()
        if searchPattern == "@":
            results = config.predefinedChatSystemMessages
        else:
            results = [i for i in config.predefinedChatSystemMessages if re.search(searchPattern, i) or re.search(searchPattern, config.predefinedChatSystemMessages[i])]
        return json.dumps({"results": results})

@app.post("/api/contexts")
async def process_contexts(query: str, api_key: str = Depends(get_api_key) if config.toolmate_api_server_key else ""):
    if query := query.strip():
        searchPattern = query.strip().lower()
        if searchPattern == "@":
            results = config.predefinedContexts
        else:
            results = [i for i in config.predefinedContexts if re.search(searchPattern, i) or re.search(searchPattern, config.predefinedContexts[i])]
        return json.dumps({"results": results})

def main():
    host = args.server if args.server else config.toolmate_api_server_host
    port = args.port if args.port else config.toolmate_api_server_port
    if not isServerAlive(host, port):
        # configurations in API server
        config.initialCompletionCheck = False
        config.auto_tool_selection = True
        config.confirmExecution = 'none'
        config.ttsInput = False
        config.ttsOutput = False
        # backend
        backends = ("llamacpp", "llamacppserver", "ollama", "groq", "googleai", "vertexai", "chatgpt", "letmedoit")
        if args.backend and args.backend.lower() in backends:
            config.llmInterface = args.backend.lower()
        # initiate assistant
        config.toolmate = ToolMate()
        # backend-dependent configurations
        if args.outputtokens and args.outputtokens.strip():
            try:
                outputtokens = int(args.outputtokens)
                if outputtokens < 0:
                    print2("No change in maximum output tokens! Negative values not accepted!")
                else:
                    config.toolmate.setMaxTokens(customMaxtokens=outputtokens)
                    print3(f"Maximum output tokens configured: {outputtokens}")
            except:
                print2("No change in maximum output tokens! Non-integer values not accepted!")
        if args.temperature and args.temperature.strip():
            try:
                temperature = float(args.temperature)
                if temperature < 0.0 or temperature > 2.0:
                    print2("No change in temperature! Given value is out of acceptted range 0.0-2.0!")
                else:
                    config.toolmate.setTemperature(temperature=temperature)
                    print3(f"Temperature configured: {temperature}")
            except:
                print2("No change in temperature! Non-float values not accepted!")
        # say hi to test
        config.toolmate.runMultipleActions("Hi!")
        # start server
        uvicorn.run(app, host=host, port=port)
    else:
        print2(f"Toolmate API server at {host}:{port} is up and running. Enjoy!")
    print3("To access: use commands 'tm' or 'tmc'")
    print3("Read more: https://github.com/eliranwong/toolmate/blob/main/package/toolmate/docs/ToolMate%20API%20Server.md")

if __name__ == '__main__':
    main()
