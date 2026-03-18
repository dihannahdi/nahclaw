#!/usr/bin/env python3
"""
Simple Bahtsul Masail Search - No AI, just references
"""

import json
import requests
import sys

API_KEY = "bm_29b2bae43d194501ade693333863a996"
API_URL = "http://127.0.0.1:8080/api/v1/search"

def search(query: str, max_results: int = 2) -> dict:
    """Search without AI synthesis"""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    payload = {
        "query": query,
        "max_results": max_results,
        "include_ai": False  # No AI to avoid timeout
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "query": query}
    except requests.exceptions.Timeout:
        return {"error": "API timeout (30s)", "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}

def format_result(data: dict) -> str:
    """Format result for Telegram"""
    if "error" in data:
        return f"❌ **Error:** {data['error']}\n\nQuery: '{data['query']}'"
    
    output = [f"🔍 **Bahtsul Masail**\n**Query:** {data.get('query', '')}"]
    
    # Results
    if "results" in data and data["results"]:
        result_count = data.get("result_count", len(data["results"]))
        output.append(f"\n📚 **{result_count} referensi ditemukan:**")
        
        for i, result in enumerate(data["results"], 1):
            book = result.get("book_name", "Kitab tidak diketahui")
            author = result.get("author_name", "Pengarang tidak diketahui")
            title = result.get("title", "Tidak ada judul")
            mazhab = result.get("mazhab", "")
            page = result.get("page", "")
            
            # Short content for summary
            content = result.get("content_snippet", "")
            content_summary = content
            if len(content_summary) > 250:
                content_summary = content_summary[:247] + "..."
            
            output.append(f"\n**{i}. {title}**")
            output.append(f"   📖 {book}")
            output.append(f"   ✍️ {author}")
            if mazhab:
                output.append(f"   🕌 {mazhab}")
            if page:
                output.append(f"   📄 Halaman {page}")
            if content_summary:
                output.append(f"   📝 {content_summary}")
            
            # Ibaroh (teks Arab lengkap)
            if content and len(content) > 0:
                output.append(f"   📜 **Ibaroh (Teks Arab Lengkap):**")
                # Split long Arabic text into manageable chunks
                arabic_lines = []
                current_line = ""
                for char in content:
                    current_line += char
                    if len(current_line) >= 70 and (char in [' ', '.', '،', '؛', '\n'] or len(current_line) >= 90):
                        arabic_lines.append(f"      {current_line.strip()}")
                        current_line = ""
                if current_line:
                    arabic_lines.append(f"      {current_line.strip()}")
                
                # Add first 6 lines (or all if less)
                for line in arabic_lines[:6]:
                    output.append(line)
                if len(arabic_lines) > 6:
                    output.append(f"      ... (selengkapnya di halaman {page})")
    
    # Translated terms
    if "translated_terms" in data and data["translated_terms"]:
        terms = ", ".join(data["translated_terms"])
        output.append(f"\n🔤 **Istilah Arab:** {terms}")
    
    # Language info
    if "detected_language" in data:
        lang = data["detected_language"]
        domain = data.get("detected_domain", "")
        if domain:
            output.append(f"\n🌐 **Bahasa:** {lang} | **Domain:** {domain}")
    
    if len(output) <= 2:  # Only header
        return f"❌ Tidak ditemukan referensi untuk: '{data.get('query', '')}'"
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: simple_search.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    result = search(query)
    formatted = format_result(result)
    print(formatted)

if __name__ == "__main__":
    main()