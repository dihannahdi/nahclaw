#!/usr/bin/env python3
"""
Lightweight Bahtsul Masail Handler for Telegram/OpenClaw
"""

import json
import requests
import sys
import os

def search_bahtsulmasail(query: str, api_key: str = "bm_29b2bae43d194501ade693333863a996") -> str:
    """Search bahtsulmasail API with optimized timeout"""
    url = "http://127.0.0.1:8080/api/v1/search"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    
    # Smart AI decision: disable AI for faster response
    # Only enable AI for complex explanatory queries
    query_lower = query.lower()
    complex_prefixes = ['jelaskan', 'uraikan', 'terangkan', 'apa pendapat', 'bagaimana pandangan']
    
    include_ai = any(query_lower.startswith(prefix) for prefix in complex_prefixes)
    
    payload = {
        "query": query,
        "max_results": 2,
        "include_ai": include_ai
    }
    
    # First attempt: 8 seconds
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            data = response.json()
            return format_response(data, query)
    except requests.exceptions.Timeout:
        if include_ai:
            # Try without AI
            payload["include_ai"] = False
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return format_response(data, query, ai_timeout=True)
            except requests.exceptions.Timeout:
                return f"⏱️ **API Timeout (13 detik)**\n\nQuery: '{query}'\n\nBackend terlalu sibuk. Coba:\n• Query lebih spesifik\n• Gunakan !bahtsul <query> nanti"
            except Exception as e:
                return f"❌ **Error:** {str(e)}\n\nQuery: '{query}'"
        else:
            return f"⏱️ **API Timeout (8 detik)**\n\nQuery: '{query}'\n\nSistem sedang overload. Tunggu beberapa saat."
    except Exception as e:
        return f"❌ **Error:** {str(e)}\n\nQuery: '{query}'"
    
    return f"❌ Tidak bisa menghubungi API bahtsulmasail.tech\n\nQuery: '{query}'"

def format_response(data: dict, query: str, ai_timeout: bool = False) -> str:
    """Format response for Telegram"""
    output = []
    
    # Header
    output.append(f"🔍 **Bahtsul Masail Search**")
    output.append(f"**Query:** {query}")
    
    # AI answer
    if "ai_answer" in data and data["ai_answer"]:
        ai_answer = data["ai_answer"]
        if len(ai_answer) > 1000:
            ai_answer = ai_answer[:997] + "..."
        output.append(f"\n🤖 **Jawaban AI:** {ai_answer}")
    elif ai_timeout:
        output.append(f"\n⏱️ **AI Synthesis Timeout**\n(Sistem sibuk, menampilkan referensi kitab saja)")
    
    # Results
    if "results" in data and data["results"]:
        result_count = data.get("result_count", len(data["results"]))
        output.append(f"\n📚 **Referensi ({result_count}):**")
        
        for i, result in enumerate(data["results"], 1):
            book_name = result.get("book_name", "Kitab tidak diketahui")
            author = result.get("author_name", "Pengarang tidak diketahui")
            title = result.get("title", "Tidak ada judul")
            mazhab = result.get("mazhab", "")
            page = result.get("page", "")
            
            # Short content for summary
            content = result.get("content_snippet", "")
            content_summary = content
            if len(content_summary) > 200:
                content_summary = content_summary[:197] + "..."
            
            output.append(f"\n**{i}. {title}**")
            output.append(f"   📖 {book_name}")
            output.append(f"   ✍️ {author}")
            if mazhab:
                output.append(f"   🕌 {mazhab}")
            if page:
                output.append(f"   📄 Halaman: {page}")
            if content_summary:
                output.append(f"   📝 {content_summary}")
            
            # Ibaroh (teks Arab lengkap)
            if content and len(content) > 0:
                output.append(f"\n   📜 **Ibaroh (Teks Arab Lengkap):**")
                # Split long Arabic text into manageable chunks
                arabic_lines = []
                current_line = ""
                for char in content:
                    current_line += char
                    if len(current_line) >= 60 and (char in [' ', '.', '،', '؛', '\n'] or len(current_line) >= 80):
                        arabic_lines.append(f"      {current_line.strip()}")
                        current_line = ""
                if current_line:
                    arabic_lines.append(f"      {current_line.strip()}")
                
                # Add first 8 lines (or all if less) for Telegram
                for line in arabic_lines[:8]:
                    output.append(line)
                if len(arabic_lines) > 8:
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
    
    if not output:
        return f"❌ Tidak ditemukan hasil untuk: '{query}'"
    
    return "\n".join(output)

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: telegram_handler.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    response = search_bahtsulmasail(query)
    print(response)

if __name__ == "__main__":
    main()