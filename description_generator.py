import requests
import json
import random
import time

class DescriptionGenerator:
    def __init__(self):
        # Multiple free proxy endpoints with rotation
        self.proxy_endpoints = [
            "https://api.openai-proxy.org/v1/chat/completions",
            "https://chatgpt-api.shn.hk/v1/",
            "https://free.churchless.tech/v1/chat/completions",
            "https://api.aios.chat/v1/chat/completions",
            "https://openaigpt.top/v1/chat/completions"
        ]
        self.model = "gpt-3.5-turbo"
        self.current_proxy = random.choice(self.proxy_endpoints)
    
    def generate_description(self, product_name, features, product_type="product"):
        # Rotate to next proxy if previous failed
        self.current_proxy = random.choice(self.proxy_endpoints)
        
        # Create detailed prompt
        prompt = f"""
        Generate a professional e-commerce product description for a {product_type} with these specifications:
        - Product Name: {product_name}
        - Key Features: {features}
        
        The description should:
        - Be 50-100 words
        - Highlight key benefits
        - Use persuasive language
        - Include SEO keywords naturally
        - Target appropriate audience
        - End with a strong call-to-action
        - Avoid markdown formatting
        """
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert e-commerce copywriter."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        try:
            # Make API request with timeout
            response = requests.post(
                self.current_proxy,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=20  # 20-second timeout
            )
            
            # Successful response
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content'].strip()
            
            # Try fallback if response is invalid
            return self._fallback_description(product_name, features, product_type)
            
        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError):
            # Use fallback on any error
            return self._fallback_description(product_name, features, product_type)
    
    def _fallback_description(self, product_name, features, product_type):
        """Generate a simple description if API fails"""
        features_list = [f.strip() for f in features.split(',') if f.strip()]
        
        if not features_list:
            features_formatted = "excellent performance and premium quality"
        elif len(features_list) == 1:
            features_formatted = features_list[0]
        else:
            features_formatted = ', '.join(features_list[:-1]) + ' and ' + features_list[-1]
        
        return (
            f"Introducing the {product_name}, a premium {product_type} designed for exceptional performance. "
            f"This product features {features_formatted}. Built with superior craftsmanship, it offers "
            f"excellent value, durability, and innovation. Perfect for everyday use, the {product_name} "
            f"delivers outstanding results. Experience the difference today - upgrade to quality you can trust!"
        )