from typing import Any, Dict, List
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from langchain_core.callbacks import BaseCallbackHandler
import requests

class MintiiTracker(BaseCallbackHandler):
    def __init__(self, api_key: str):
        # Initialize storage for tracking
        self.prompts = []
        self.responses = []
        self.model_info = {}
        self.api_key = api_key
        self.tool_inputs = []
        self.tool_outputs = []
        self.current_agent_action = None
        
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        """Called when chat model starts running."""
        # Store model info with improved model name capture
        self.model_info = {
            "name": serialized.get("name", ""),
            "model": serialized.get("kwargs", {}).get("model", "")
        }
        # Store prompts
        self.prompts.extend([msg.content for msg_list in messages for msg in msg_list])

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Called when LLM ends running."""
        # Store generation responses
        generations = response.generations
        for gen_list in generations:
            for gen in gen_list:
                self.responses.append(gen.text)
        
        # Update model info with usage if available
        if response.llm_output and "usage" in response.llm_output:
            self.model_info["usage"] = response.llm_output["usage"]
            
        # Update model info with model name from llm_output if available
        if response.llm_output and "model_name" in response.llm_output:
            self.model_info["model"] = response.llm_output["model_name"]
        elif response.llm_output and "model" in response.llm_output:
            self.model_info["model"] = response.llm_output["model"]
            
        # Make dummy request
        self._dummy_send_to_mintii()

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Called when a tool starts running."""
        self.tool_inputs.append({
            "tool": serialized.get("name", ""),
            "input": input_str
        })
        self.current_agent_action = {
            "tool": serialized.get("name", ""),
            "input": input_str
        }

    def on_tool_end(
        self, output: str, **kwargs: Any
    ) -> None:
        """Called when a tool ends running."""
        if self.current_agent_action:
            self.tool_outputs.append({
                **self.current_agent_action,
                "output": output
            })
            # Send tool interaction to Mintii
            self._dummy_send_tool_to_mintii(self.current_agent_action["tool"], 
                                          self.current_agent_action["input"], 
                                          output)
            self.current_agent_action = None

    def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
        """Called when agent takes an action."""
        if isinstance(action, dict):
            tool = action.get("tool", "")
            tool_input = action.get("tool_input", "")
            self.tool_inputs.append({
                "tool": tool,
                "input": tool_input
            })

    def get_tracking_info(self) -> Dict[str, Any]:
        """Return all tracked information."""
        return {
            "model_info": self.model_info,
            "prompts": self.prompts,
            "responses": self.responses,
            "tool_interactions": self.tool_outputs
        }
    
    def _dummy_send_to_mintii(self) -> None:
        """Simulate sending tracking information to Mintii Router API."""
        dummy_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        dummy_payload = {
            "model": self.model_info.get("model", ""),
            "prompt": self.prompts[-1] if self.prompts else "",
            "response": self.responses[-1] if self.responses else "",
            "usage": self.model_info.get("usage", {}),
            "type": "llm_interaction"
        }
        
        # Print the dummy request information
        print("\nDummy API Request:")
        print(f"URL: http://localhost:3000/api/router")
        print(f"Headers: {dummy_headers}")
        print(f"Payload: {dummy_payload}")
        print("Dummy request simulated successfully!")

    def _dummy_send_tool_to_mintii(self, tool_name: str, tool_input: str, tool_output: str) -> None:
        """Simulate sending tool interaction to Mintii Router API."""
        dummy_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        dummy_payload = {
            "type": "tool_interaction",
            "tool": tool_name,
            "input": tool_input,
            "output": tool_output,
            "model": self.model_info.get("model", ""),
            "usage": self.model_info.get("usage", {})
        }
        
        # Print the dummy request information
        print("\nDummy Tool API Request:")
        print(f"URL: http://localhost:3000/api/router")
        print(f"Headers: {dummy_headers}")
        print(f"Payload: {dummy_payload}")
        print("Dummy tool request simulated successfully!")
    
    def reset(self):
        """Reset all tracking information."""
        self.prompts = []
        self.responses = []
        self.model_info = {}
        self.tool_inputs = []
        self.tool_outputs = []
        self.current_agent_action = None