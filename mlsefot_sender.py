"""
Cliente HTTP genérico para enviar peticiones POST a APIs externas
"""
import requests
from typing import Optional, Dict, Any


class APIClient:
    """Cliente genérico para enviar peticiones POST a cualquier API"""
    
    def __init__(self, base_url: str = None, api_key: str = None, headers: Dict[str, str] = None):
        """
        Inicializa el cliente API
        
        Args:
            base_url: URL base de la API (opcional)
            api_key: API key para autenticación (opcional)
            headers: Headers personalizados (opcional)
        """
        self.base_url = base_url
        self.api_key = api_key
        self.default_headers = headers or {}
        
        if api_key:
            self.default_headers["Authorization"] = f"Bearer {api_key}"
        
        if "Content-Type" not in self.default_headers:
            self.default_headers["Content-Type"] = "application/json"
    
    def post(
        self, 
        url: str, 
        data: Dict[str, Any] = None, 
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Envía una petición POST
        
        Args:
            url: URL completa o endpoint (si se configuró base_url)
            data: Datos a enviar en el body
            params: Query parameters (se agregan a la URL)
            headers: Headers adicionales (se mezclan con los default)
            timeout: Timeout en segundos
        
        Returns:
            dict con:
                - success: bool
                - data: Respuesta de la API (si success=True)
                - status_code: Código HTTP
                - error: mensaje de error (si success=False)
        """
        try:
            # Construir URL completa
            full_url = f"{self.base_url}{url}" if self.base_url and not url.startswith("http") else url
            
            # Mezclar headers
            request_headers = {**self.default_headers, **(headers or {})}
            
            print(f"📤 POST {full_url}")
            if params:
                print(f"   Query params: {params}")
            
            response = requests.post(
                full_url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=timeout
            )
            
            response.raise_for_status()
            
            # Intentar parsear JSON
            try:
                response_data = response.json()
            except ValueError:
                response_data = {"text": response.text}
            
            print(f"✅ Respuesta recibida: {response.status_code}")
            
            return {
                "success": True,
                "data": response_data,
                "status_code": response.status_code
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error {response.status_code}: {response.text}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "status_code": response.status_code
            }
            
        except requests.exceptions.Timeout:
            error_msg = f"Timeout después de {timeout}s"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
            
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }


# Función helper para uso rápido
def send_post(url: str, data: Dict[str, Any], params: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:
    """
    Helper para enviar POST rápidamente sin instanciar clase
    
    Args:
        url: URL completa de la API
        data: Datos a enviar en el body
        params: Query parameters
        api_key: API key opcional
    
    Returns:
        Respuesta del servidor
    """
    client = APIClient(api_key=api_key)
    return client.post(url, data, params=params)

if __name__ == "__main__":
    # Ejemplo 1: Uso con clase y query params
    client = APIClient(
        base_url="https://api.example.com",
        api_key="your-api-key-here"
    )
    
    result = client.post(
        "/videos",
        data={"video_url": "https://github.com/user/repo/video.mp4"},
        params={"param1": "value1", "param2": "value2"}
    )
    print(f"Resultado: {result}")
    
    # Ejemplo 2: Uso con helper
    result2 = send_post(
        url="https://api.example.com/videos",
        data={"video_url": "https://github.com/user/repo/video.mp4"},
        params={"param1": "value1", "param2": "value2"},
        api_key="your-api-key"
    )
    print(f"Resultado 2: {result2}")
    print(f"Resultado 2: {result2}")

