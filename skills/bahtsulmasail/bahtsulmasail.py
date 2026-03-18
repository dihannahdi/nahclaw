#!/usr/bin/env python3
"""
Bahtsul Masail API Client for OpenClaw
"""

import json
import requests
import sys
from typing import Dict, List, Optional

class BahtsulMasailClient:
    def __init__(self, api_key: str = "bm_29b2bae43d194501ade693333863a996", base_url: str = "http://127.0.0.1:8080"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
    def search(self, query: str, max_results: int = 3, include_ai: bool = True) -> Dict:
        """Search for Islamic references"""
        url = f"{self.base_url}/api/v1/search"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        payload = {
            "query": query,
            "max_results": max_results,
            "include_ai": include_ai
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "query": query}
    
    def format_response(self, data: Dict) -> str:
        """Format API response into readable text"""
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        output = []
        
        # AI answer if available
        if "ai_answer" in data and data["ai_answer"]:
            output.append(f"🤖 **AI Answer:** {data['ai_answer']}")
        
        # Results
        if "results" in data and data["results"]:
            output.append(f"📚 **Found {data.get('result_count', 0)} results:**")
            
            for i, result in enumerate(data["results"], 1):
                book_name = result.get("book_name", "Unknown Book")
                author = result.get("author_name", "Unknown Author")
                title = result.get("title", "No Title")
                mazhab = result.get("mazhab", "")
                page = result.get("page", "")
                
                # Content snippet (truncated)
                content = result.get("content_snippet", "")
                if len(content) > 500:
                    content = content[:497] + "..."
                
                output.append(f"\n**{i}. {title}**")
                output.append(f"   📖 Kitab: {book_name}")
                output.append(f"   ✍️ Pengarang: {author}")
                if mazhab:
                    output.append(f"   🕌 Mazhab: {mazhab}")
                if page:
                    output.append(f"   📄 Halaman: {page}")
                output.append(f"   📝 Isi: {content}")
        
        # Translated terms
        if "translated_terms" in data and data["translated_terms"]:
            terms = ", ".join(data["translated_terms"])
            output.append(f"\n🔤 **Istilah Arab:** {terms}")
        
        if not output:
            return "❌ Tidak ditemukan hasil untuk query ini."
        
        return "\n".join(output)

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: bahtsulmasail.py <query> [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    client = BahtsulMasailClient()
    result = client.search(query, max_results)
    formatted = client.format_response(result)
    print(formatted)

if __name__ == "__main__":
    main()