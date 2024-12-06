import re
from langchain.tools import StructuredTool
import json
from typing import Any, Dict, List, Optional, Type

from openai import BaseModel
from pydantic import create_model
import requests

def create_pydantic_model_from_params(
    operation: Dict[str, Any],
    method: str,
    path: str
) -> Type[BaseModel]:
    """
    API 파라미터로부터 Pydantic 모델을 생성합니다.
    
    """
    fields = {}
    required_fields = []
    
    # Path 파라미터 추출
    path_params = re.findall(r'{(\w+)}', path)
    for param in path_params:
        fields[param] = (str, ...)  # ... indicates required field
        required_fields.append(param)
    
    # Operation 파라미터 처리
    if 'parameters' in operation:
        for param in operation['parameters']:
            name = param['name']
            param_schema = param.get('schema', {})
            
            # 기본 타입 매핑
            type_mapping = {
                'string': str,
                'integer': int,
                'number': float,
                'boolean': bool,
                'array': list,
                'object': dict
            }
            
            field_type = type_mapping.get(param_schema.get('type', 'string'), str)
            
            if param.get('required', False):
                fields[name] = (field_type, ...)
                required_fields.append(name)
            else:
                fields[name] = (Optional[field_type], None)
    
    # Request Body 처리
    if method.lower() in ['post', 'put', 'patch'] and 'requestBody' in operation:
        content = operation['requestBody'].get('content', {})
        if 'application/json' in content:
            schema = content['application/json'].get('schema', {})
            if 'properties' in schema:
                for prop_name, prop_schema in schema['properties'].items():
                    prop_type = type_mapping.get(prop_schema.get('type', 'string'), str)
                    if prop_name in schema.get('required', []):
                        fields[prop_name] = (prop_type, ...)
                        required_fields.append(prop_name)
                    else:
                        fields[prop_name] = (Optional[prop_type], None)
    
    # 모델 이름 생성
    model_name = f"{method.capitalize()}{path.replace('/', '_').replace('{', '').replace('}', '')}Params"
    
    # Add 'auth' as an optional field
    fields['header'] = (Optional[dict], None)

    # Pydantic 모델 생성
    return create_model(model_name, **fields)

def create_structured_tools_from_openapi(openapi_spec: str) -> List[StructuredTool]:
    """
    OpenAPI 스펙문서로부터 LangChain StructuredTool 리스트를 생성합니다.
    
    Args:
        openapi_spec (str): OpenAPI 스펙 문서 (YAML 또는 JSON 형식)
    
    Returns:
        List[StructuredTool]: 생성된 LangChain StructuredTool 객체들의 리스트
    """
    try:
        with open(openapi_spec, 'r') as f:
            spec = json.load(f)
    except Exception as e:
        raise ValueError(f"OpenAPI 스펙 파싱 실패: {str(e)}")
    
    tools = []
    base_url = spec.get('servers', [{}])[0].get('url', '')
    
    # 각 API 엔드포인트에 대해 StructuredTool 생성
    for path, path_item in spec['paths'].items():
        for method, operation in path_item.items():
            if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                continue
            
            tool_name = operation.get('operationId', f"{method}_{path.replace('/', '_')}")
            description = operation.get('summary', '') + '\n' + operation.get('description', '')
            
            # Pydantic 모델 생성
            params_model = create_pydantic_model_from_params(operation, method, path)
            
            def create_tool_function(path=path, method=method, base_url=base_url):
                def tool_function(header: Optional[dict] = None, **kwargs) -> Dict[str, Any]:
                    url = base_url + path
                    
                    # Path 파라미터 치환
                    path_params = re.findall(r'{(\w+)}', path)
                    for param in path_params:
                        if param in kwargs:
                            url = url.replace(f"{{{param}}}", str(kwargs.pop(param)))
                    
                    # Request Body와 Query 파라미터 분리
                    if method.lower() in ['post', 'put', 'patch']:
                        body_params = kwargs
                        query_params = {}
                    else:
                        body_params = {}
                        query_params = kwargs
                    
                    try:
                        response = requests.request(
                            method=method.upper(),
                            url=url,
                            json=body_params if body_params else None,
                            params=query_params if query_params else None,
                            headers=header if header else None,
                            verify=False
                        )
                        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
                        
                        try:
                            return response.json()
                        except json.JSONDecodeError:
                            return {"status": response.status_code, "text": response.text}
                            
                    except requests.exceptions.RequestException as e:
                        return {
                            "error": str(e),
                            "status": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
                        }
                
                return tool_function
            
            tool = StructuredTool(
                name=tool_name,
                description=description,
                func=create_tool_function(),
                args_schema=params_model
            )
            tools.append(tool)

    return tools