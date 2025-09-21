"""
Base Agent class for all agent implementations.
"""

from typing import List, Optional, Any
from .message import Message
from .llm_providers import LLMProvider


class BaseAgent:
    """Base class for all agents with chat functionality."""
    
    def __init__(self, llm_provider: LLMProvider, agent_id: str = None, system_prompt: str = None):
        """
        Initialize base agent.
        
        Args:
            llm_provider: LLM provider instance
            agent_id: Unique identifier for the agent
            system_prompt: System prompt for the agent
        """
        self.system_prompt = system_prompt
        self.llm_provider = llm_provider
        self.agent_id = agent_id or self.__class__.__name__
        self.chat_history: List[Message] = []
        
        # Add system prompt to history
        if system_prompt:
            self.chat_history.append(Message(
                role="system",
                content=system_prompt
            ))
    
    def upload_file(self, file_path: str) -> Any:
        """
        Upload file and return file object.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File object that can be used in content generation
        """
        file = self.llm_provider.upload_file(file_path)
        message = f"This is {file_path}. If you can see the file, response 'OK'"
        self.send_message([message, file], role="user")
        return file
    
    def send_message(self, content: str | List[Any], role: str = "user", config: Any = None) -> str:
        """
        Send message and get LLM response.
        
        Args:
            content: Message content
            role: Message role (user, assistant, tool)
            config: Optional configuration for the LLM
            
        Returns:
            LLM response
        """
        # Add message to history
        message = Message(role=role, content=content)
        self.chat_history.append(message)
        
        # Get response from LLM
        response = self.llm_provider.send_message(content, config=config)
        
        # Add response to history
        if response:
            response_message = Message(role="assistant", content=response)
            self.chat_history.append(response_message)
        
        return response
    
    def generate_content(self, content: str | List[Any], config: Any = None) -> str:
        """
        Generate content for single-turn conversation (no chat session).
        
        Args:
            content: Content to generate response for
            config: Configuration for the content generation (optional)
        """
        response = self.llm_provider.generate_content(content, config=config)

        # Add message to history
        message = Message(role="user", content=content)
        self.chat_history.append(message)

        # Add response to history
        if response:
            response_message = Message(role="assistant", content=response)
            self.chat_history.append(response_message)

        return response
    
    def get_history(self) -> List[Message]:
        """
        Get complete chat history.
        
        Returns:
            List of Message objects
        """
        return self.chat_history.copy()
    
    def reset_session(self) -> None:
        """Reset chat session, keeping only system prompt."""
        system_messages = []
        self.chat_history = system_messages
        
        # Reset LLM provider session with system prompt
        self.llm_provider.reset_chat(self.system_prompt)
    
    def get_last_response(self) -> Optional[str]:
        """
        Get the last assistant response.
        
        Returns:
            Last assistant response or None
        """
        for message in reversed(self.chat_history):
            if message.role == "assistant":
                return message.content
        return None
