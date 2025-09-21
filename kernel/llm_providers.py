"""
LLM Provider implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
import os
from google import genai
from google.genai import types
from .message import Message


class LLMProvider(ABC):
    """Abstract base class for LLM providers (Chat sessions)."""
    
    @abstractmethod
    def send_message(self, content: str | List[Any], config: Any = None, return_full_response: bool = False) -> Union[str, Any]:
        """Send message to LLM and get response (for chat sessions)."""
        pass
    
    @abstractmethod
    def generate_content(self, content: str | List[Any], config: Any = None, return_full_response: bool = False) -> Union[str, Any]:
        """Generate content for single-turn conversation (no chat session)."""
        pass
    
    @abstractmethod
    def upload_file(self, file_path: str) -> Any:
        """Upload file and return file object."""
        pass
    
    @abstractmethod
    def reset_chat(self, system_prompt: str = None) -> None:
        """Reset chat session."""
        pass
    


class GeminiProvider(LLMProvider):
    """Gemini LLM provider implementation."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        """
        Initialize Gemini provider and create chat session.
        
        Args:
            api_key: Google API key. If None, will try to get from GEMINI_API_KEY environment variable
            model: Gemini model name
        """
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key is None:
                raise ValueError("API key must be provided either as parameter or GEMINI_API_KEY environment variable")
        
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)
        self.chat = self.client.chats.create(model=self.model)
    
    def send_message(self, content: str | List[Any], config: Any = None, return_full_response: bool = False) -> Union[str, Any]:
        """
        Send message to Gemini and get response (for chat sessions).
        
        Args:
            content: Message content to send
            config: Configuration for the message (optional)
            return_full_response: If True, return full response object
            
        Returns:
            Response text from Gemini, or full response object if return_full_response=True
        """
        response = self.chat.send_message(content, config=config)
        if return_full_response:
            return response
        return response.text
    
    def generate_content(self, content: str | List[Any], config: Any = None, return_full_response: bool = False) -> Union[str, Any]:
        """
        Generate content for single-turn conversation (no chat session).
        
        Args:
            content: Content to generate response for
            config: Configuration for the content generation (optional)
            return_full_response: If True, return full response object
            
        Returns:
            Generated content string from Gemini, or full response object if return_full_response=True
        """
        try:
            if config is None:
                config = types.GenerateContentConfig()
            response = self.client.models.generate_content(
                model=self.model,
                contents=content,
                config=config
            )
            if return_full_response:
                return response
            return response.text
        except Exception as e:
            print(f"Error in generate_content: {e}")
            return ""
    
    def upload_file(self, file_path: str) -> Any:
        """
        Upload file to Gemini.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File object that can be used in content generation
        """
        try:
            # Upload file using Gemini API
            file_obj = self.client.files.upload(file=file_path)
            return file_obj
        except Exception as e:
            print(f"Error uploading file {file_path}: {e}")
            return f"file://{file_path}"

    def reset_chat(self, system_prompt: str = None) -> None:
        """
        Reset chat session by creating a new chat.
        
        Args:
            system_prompt: System prompt to send after reset
        """
        self.chat = self.client.chats.create(model=self.model)
        
        # Send system prompt if provided
        if system_prompt:
            self.chat.send_message(system_prompt)
    
