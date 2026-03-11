import json
import asyncio
from typing import Type, TypeVar
from pydantic import BaseModel
import litellm
from litellm import acompletion
from core.protocol import Message, AgentConfig

T = TypeVar('T', bound=BaseModel)
litellm.drop_params = True
litellm.set_verbose = False

class LLMEngine:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.model = config.model
        self.temperature = config.temperature
    
    async def generate(self, messages: list[Message], response_model: Type[T] | None = None, max_tokens: int = 4000) -> T | str:
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        if response_model:
            schema = response_model.model_json_schema()
            formatted_messages.append({
                "role": "system",
                "content": f"You must respond with valid JSON matching this schema:\n{json.dumps(schema, indent=2)}\n\nCRITICAL: Return ONLY the JSON object, no markdown formatting, no explanations."
            })
        
        try:
            response = await acompletion(
                model=self.model,
                messages=formatted_messages,
                temperature=self.temperature,
                max_tokens=max_tokens,
                timeout=60.0
            )
            
            content = response.choices[0].message.content
            
            if response_model:
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                content = content.strip()
                
                try:
                    data = json.loads(content)
                    return response_model.model_validate(data)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON response: {e}\nContent: {content}")
            
            return content
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")
    
    async def generate_with_retry(self, messages: list[Message], response_model: Type[T] | None = None, max_retries: int = 3) -> T | str:
        for attempt in range(max_retries):
            try:
                return await self.generate(messages, response_model)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        raise RuntimeError("Max retries exceeded")
