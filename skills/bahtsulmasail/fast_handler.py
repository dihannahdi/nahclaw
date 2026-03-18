#!/usr/bin/env python3
"""
Fast Bahtsul Masail Handler - Optimized for Telegram timeout
"""

import json
import requests
import sys
import os
import time
from typing import Dict, List, Optional
from functools import lru_cache

class FastBahtsulHandler:
    def __init__(self, api_key: str = "bm_29b2bae43d194501ade693333863a996", base_url: str = "http://127.0.0.1:8080"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes cache
        
        # Simple Islamic keywords
        self.islamic_keywords = [
            'shalat', 'salat', 'sholat', 'puasa', 'zakat', 'nikah', 'talak', 'riba', 
            'haji', 'umrah', 'wudhu', 'tayammum', 'janabah', 'haid', 'nifas',
            'mazhab', 'fiqh', 'fikih', 'kitab', 'quran', 'hadis', 'hadith',
            'sunnah', 'makruh', 'haram', 'halal', 'wajib', 'sunnah', 'mubah'
        ]
    
    def is_islamic_query(self, query: str) -> bool:
        """Fast keyword check"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.islamic_keywords)
    
    def search_fast(self, query: str, max_results: int = 2) -> Dict:
        """Fast search with aggressive timeout"""
        cache_key = f"{query}:{max_results}"
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_timeout:
                print(f"[FastBahtsul] Cache hit: {query}", file=sys.stderr)
                return cached_data
        
        url = f"{self.base_url}/api/v1/search"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        # Determine if we need AI synthesis
        # Simple queries don't need AI
        simple_queries = ['apa', 'bagaimana', 'boleh', 'bolehkah', 'apakah', 'hukum']
        query_words = query.lower().split()
        include_ai = not any(word in simple_queries for word in query_words[:2])
        
        payload = {
            "query": query,
            "max_results": max_results,
            "include_ai": include_ai  # Try without AI first for speed
        }
        
        print(f"[FastBahtsul] Searching: '{query}' (AI: {include_ai})", file=sys.stderr)
        
        try:
            # First attempt: 8 seconds timeout
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            response.raise_for_status()
            data = response.json()
            
            # Cache successful result
            self.cache[cache_key] = (time.time(), data)
            return data
            
        except requests.exceptions.Timeout:
            print(f"[FastBahtsul] Timeout (8s), trying without AI...", file=sys.stderr)
            
            # Second attempt: without AI, 5 seconds
            payload["include_ai"] = False
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=5)
                response.raise_for_status()
                data = response.json()
                data["ai_timeout"] = True
                
                # Cache timeout result
                self.cache[cache_key] = (time.time(), data)
                return data
                
            except requests.exceptions.Timeout:
                print(f"[FastBahtsul] Complete timeout (13s total)", file=sys.stderr)
                return {
                    "error": "API timeout (13s)",
                    "query": query,
                    "suggestion": "Backend sedang overload. Coba query lebih spesifik atau tunggu beberapa saat."
                }
                
        except requests.exceptions.RequestException as e:
            print(f"[FastBahtsul] Request error: {e}", file=sys.stderr)
            return {"error": str(e), "query": query}
    
    def format_fast_response(self, data: Dict) -> str:
        """Fast formatting for Telegram"""
        if "error" in data:
            error = data["error"]
            if "timeout" in error.lower():
                return f"⏱️ **Timeout (13 detik)**\n\nQuery: '{data['query']}'\n\nBackend sedang memproses. Coba:\n• Query lebih spesifik\n• Gunakan !bahtsul <query> nanti\n• Cek: `systemctl status kizana-backend`"
            return f"❌ **Error:** {error}\n\nQuery: '{data['query']}'"
        
        output = []
        
        # AI answer (if available and not too long)
        if "ai_answer" in data and data["ai_answer"]:
            ai_answer = data["ai_answer"]
            # Truncate if too long
            if len(ai_answer) > 1500:
                ai_answer = ai_answer[:1497] + "..."
            output.append(f"🤖 **Jawaban:** {ai_answer}")
        elif data.get("ai_timeout"):
            output.append("⏱️ **AI timeout** - Menampilkan referensi kitab saja")
        
        # Results (limit to 2)
        if "results" in data and data["results"]:
            results = data["results"][:2]  # Max 2 results
            output.append(f"\n📚 **Referensi ({len(results)}):**")
            
            for i, result in enumerate(results, 1):
                book_name = result.get("book_name", "Kitab")
                author = result.get("author_name", "")
                title = result.get("title", "Tidak ada judul")
                mazhab = result.get("mazhab", "")
                page = result.get("page", "")
                
                # Very brief snippet for summary
                content = result.get("content_snippet", "")
                content_summary = content
                if content_summary and len(content_summary) > 100:
                    content_summary = content_summary[:97] + "..."
                
                line = f"{i}. **{title}**"
                if book_name:
                    line += f" ({book_name})"
                if author:
                    line += f" - {author}"
                if mazhab:
                    line += f" [{mazhab}]"
                if page:
                    line += f" (halaman {page})"
                
                output.append(line)
                
                if content_summary:
                    output.append(f"   📝 {content_summary}")
                
                # Ibaroh (teks Arab lengkap) - limited for fast mode
                if content and len(content) > 0:
                    output.append(f"   📜 **Ibaroh:**")
                    # Show first 150 characters of Arabic text
                    arabic_preview = content[:150]
                    if len(content) > 150:
                        arabic_preview += "..."
                    output.append(f"      {arabic_preview}")
        
        if not output:
            return f"❌ Tidak ada hasil untuk '{data.get('query', 'query')}'"
        
        # Add footer
        output.append(f"\n⚡ **Fast Mode** - Query: '{data.get('query', '')}'")
        
        return "\n".join(output)
    
    def handle(self, query: str) -> str:
        """Main handler - returns response or None if not Islamic query"""
        if not self.is_islamic_query(query):
            return None
        
        print(f"[FastBahtsul] Processing: {query}", file=sys.stderr)
        start_time = time.time()
        
        # Fast search
        result = self.search_fast(query)
        
        # Format
        response = self.format_fast_response(result)
        
        elapsed = time.time() - start_time
        print(f"[FastBahtsul] Completed in {elapsed:.2f}s", file=sys.stderr)
        
        return response

def main():
    """Test CLI"""
    if len(sys.argv) < 2:
        print("Usage: fast_handler.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    handler = FastBahtsulHandler()
    
    start = time.time()
    response = handler.handle(query)
    elapsed = time.time() - start
    
    if response:
        print(f"\n=== Response ({elapsed:.2f}s) ===")
        print(response)
    else:
        print(f"Not Islamic query: '{query}'")

if __name__ == "__main__":
    main()