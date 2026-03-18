#!/usr/bin/env python3
"""
Bahtsul Masail Handler for OpenClaw
"""

import json
import requests
import sys
import os
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class BahtsulMasailHandler:
    def __init__(self, api_key: str = "bm_29b2bae43d194501ade693333863a996", base_url: str = "http://127.0.0.1:8080"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.islamic_keywords = [
            'shalat', 'salat', 'sholat', 'puasa', 'zakat', 'nikah', 'talak', 'riba', 
            'haji', 'umrah', 'wudhu', 'tayammum', 'janabah', 'haid', 'nifas', 
            'mazhab', 'fiqh', 'fikih', 'kitab', 'kuning', 'arab', 'islam', 
            'quran', 'hadis', 'hadith', 'sunnah', 'makruh', 'haram', 'halal',
            'wajib', 'sunnah', 'mubah', 'makruh', 'haram', 'murtad', 'kafir',
            'muslim', 'muslimah', 'jilbab', 'hijab', 'aurat', 'mahram', 'muhrim',
            'waris', 'warisan', 'faraid', 'wasiat', 'wakaf', 'sedekah', 'infaq',
            'jumat', 'jumuah', 'jamaah', 'imam', 'makmum', 'masjid', 'musholla',
            'azan', 'adzan', 'iqamah', 'iqomat', 'sholat jumat', 'sholat jenazah',
            'sholat id', 'idul fitri', 'idul adha', 'qurban', 'udhiyah', 'aqiqah',
            'khitan', 'sunat', 'khulu', "li'an", 'iddah', 'mutah', 'muhrim',
            'khalwat', 'ikhtilat', 'aurat', 'tabarruj', 'ghibah', 'fitnah'
        ]
    
    def is_islamic_query(self, query: str) -> bool:
        """Check if query contains Islamic keywords"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.islamic_keywords)
    
    def search(self, query: str, max_results: int = 3, include_ai: bool = True, timeout: int = 15) -> Dict:
        """Search bahtsulmasail API with optimized timeout"""
        url = f"{self.base_url}/api/v1/search"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        # Smart AI decision: disable AI for faster response
        # AI only for complex explanatory queries
        complex_prefixes = ['jelaskan', 'uraikan', 'terangkan', 'apa pendapat', 'bagaimana pandangan']
        query_lower = query.lower()
        
        # If query starts with simple words, disable AI
        if not any(query_lower.startswith(prefix) for prefix in complex_prefixes):
            include_ai = False
        
        payload = {
            "query": query,
            "max_results": max_results,
            "include_ai": include_ai
        }
        
        print(f"[BahtsulMasail] Searching: '{query}' (AI: {include_ai}, timeout: {timeout}s)", file=sys.stderr)
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            # Try without AI synthesis (if not already disabled)
            if include_ai:
                print(f"[BahtsulMasail] AI timeout ({timeout}s), retrying without AI...", file=sys.stderr)
                payload["include_ai"] = False
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    data["ai_timeout"] = True
                    return data
                except Exception as e:
                    print(f"[BahtsulMasail] Second attempt failed: {e}", file=sys.stderr)
            
            return {"error": f"API timeout ({timeout}s)", "query": query, "suggestion": "Coba query lebih spesifik atau tunggu beberapa saat"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "query": query}
    
    def format_response(self, data: Dict) -> str:
        """Format API response for Telegram/OpenClaw"""
        if "error" in data:
            error_msg = data["error"]
            if "timeout" in error_msg.lower():
                return f"⏱️ **API Timeout**\n\nQuery: '{data['query']}'\n\nSistem sedang memproses pertanyaan yang kompleks. Coba:\n1. Query yang lebih spesifik\n2. Tunggu beberapa saat\n3. Cek status backend: `systemctl status kizana-backend`"
            return f"❌ **Error:** {error_msg}\n\nQuery: '{data['query']}'"
        
        output = []
        
        # AI answer if available
        if "ai_answer" in data and data["ai_answer"]:
            output.append(f"🤖 **Jawaban AI:** {data['ai_answer']}")
        elif data.get("ai_timeout"):
            output.append("⏱️ **AI Synthesis Timeout**\n(Sistem terlalu sibuk, menampilkan referensi kitab saja)")
        
        # Results
        if "results" in data and data["results"]:
            result_count = data.get("result_count", len(data["results"]))
            output.append(f"\n📚 **Ditemukan {result_count} referensi:**")
            
            for i, result in enumerate(data["results"], 1):
                book_name = result.get("book_name", "Kitab tidak diketahui")
                author = result.get("author_name", "Pengarang tidak diketahui")
                title = result.get("title", "Tidak ada judul")
                mazhab = result.get("mazhab", "")
                page = result.get("page", "")
                
                # Content snippet (truncated for summary)
                content = result.get("content_snippet", "")
                content_summary = content
                if len(content_summary) > 300:
                    content_summary = content_summary[:297] + "..."
                
                output.append(f"\n**{i}. {title}**")
                output.append(f"   📖 **Kitab:** {book_name}")
                output.append(f"   ✍️ **Pengarang:** {author}")
                if mazhab:
                    output.append(f"   🕌 **Mazhab:** {mazhab}")
                if page:
                    output.append(f"   📄 **Halaman:** {page}")
                if content_summary:
                    output.append(f"   📝 **Ringkasan:** {content_summary}")
                
                # Ibaroh (teks Arab lengkap)
                if content and len(content) > 0:
                    output.append(f"\n   📜 **Ibaroh (Teks Arab Lengkap):**")
                    # Split long Arabic text into manageable chunks
                    arabic_lines = []
                    current_line = ""
                    for char in content:
                        current_line += char
                        if len(current_line) >= 80 and (char in [' ', '.', '،', '؛', '\n'] or len(current_line) >= 100):
                            arabic_lines.append(f"      {current_line.strip()}")
                            current_line = ""
                    if current_line:
                        arabic_lines.append(f"      {current_line.strip()}")
                    
                    # Add first 10 lines (or all if less)
                    for line in arabic_lines[:10]:
                        output.append(line)
                    if len(arabic_lines) > 10:
                        output.append(f"      ... (selengkapnya di halaman {page})")
        
        # Translated terms
        if "translated_terms" in data and data["translated_terms"]:
            terms = ", ".join(data["translated_terms"])
            output.append(f"\n🔤 **Istilah Arab:** {terms}")
        
        # Detected language/domain
        if "detected_language" in data:
            lang = data["detected_language"]
            domain = data.get("detected_domain", "")
            if domain:
                output.append(f"\n🌐 **Bahasa:** {lang} | **Domain:** {domain}")
        
        if not output:
            return "❌ Tidak ditemukan hasil untuk query ini."
        
        return "\n".join(output)
    
    def handle_query(self, query: str) -> str:
        """Main handler for OpenClaw integration"""
        if not self.is_islamic_query(query):
            return None  # Not an Islamic query, let other handlers process
        
        print(f"[BahtsulMasail] Processing Islamic query: {query}", file=sys.stderr)
        
        # Search API
        result = self.search(query, max_results=2, timeout=60)
        
        # Format response
        return self.format_response(result)

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: handler.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    handler = BahtsulMasailHandler()
    response = handler.handle_query(query)
    
    if response:
        print(response)
    else:
        print(f"Query '{query}' tidak terdeteksi sebagai pertanyaan agama Islam.")

if __name__ == "__main__":
    main()