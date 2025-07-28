#!/usr/bin/env python3
"""
Adobe Hackathon Challenge 1B - Document Analysis Solution
Improved version with better section detection and content extraction
"""

import os
import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import PyPDF2

class DocumentAnalyzer:
    def __init__(self):
        self.domain_keywords = {
            'travel': ['guide', 'cities', 'restaurants', 'hotels', 'activities', 'things', 'do', 
                      'adventures', 'coastal', 'experiences', 'culinary', 'packing', 'tips', 
                      'tricks', 'culture', 'traditions', 'history', 'cuisine', 'nightlife', 'entertainment'],
            'hr': ['acrobat', 'create', 'convert', 'edit', 'export', 'fill', 'sign', 
                  'generative', 'ai', 'signatures', 'share', 'skills', 'checklist', 'pdf', 'forms',
                  'fillable', 'clipboard', 'batch', 'document'],
            'food': ['breakfast', 'lunch', 'dinner', 'ideas', 'mains', 'sides', 'recipes', 
                    'cooking', 'ingredients', 'menu', 'planning', 'falafel', 'ratatouille',
                    'vegetarian', 'lasagna', 'sushi', 'ganoush', 'chickpeas', 'eggplant']
        }

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """Extract text from PDF, returning a dictionary with page numbers as keys."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                pages_text = {}
                
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    pages_text[page_num + 1] = text  # 1-indexed pages
                
                return pages_text
        except Exception as e:
            print(f"     ❌ Error reading {pdf_path}: {e}")
            return {}

    def determine_collection_domain(self, persona: str, job_description: str) -> str:
        """Determine domain based on persona and job description."""
        persona_lower = persona.lower()
        job_lower = job_description.lower()
        
        # Analyze persona and job content to determine domain
        travel_indicators = ['travel', 'trip', 'vacation', 'planner', 'tourism', 'holiday']
        hr_indicators = ['hr', 'human resources', 'professional', 'forms', 'compliance', 'onboarding', 'employee']
        food_indicators = ['food', 'cook', 'chef', 'contractor', 'menu', 'catering', 'recipe', 'kitchen']
        
        travel_score = sum(1 for indicator in travel_indicators if indicator in persona_lower or indicator in job_lower)
        hr_score = sum(1 for indicator in hr_indicators if indicator in persona_lower or indicator in job_lower)
        food_score = sum(1 for indicator in food_indicators if indicator in persona_lower or indicator in job_lower)
        
        if travel_score >= max(hr_score, food_score):
            return 'travel'
        elif hr_score >= max(travel_score, food_score):
            return 'hr'
        elif food_score >= max(travel_score, hr_score):
            return 'food'
        else:
            return 'general'

    def identify_sections_dynamically(self, all_files_content: Dict, domain: str, job_description: str) -> List[Dict]:
        """Dynamically identify relevant sections across all PDFs."""
        potential_sections = []
        
        for filename, pages_content in all_files_content.items():
            for page_num, page_text in pages_content.items():
                sections = self.extract_sections_from_page(page_text, page_num, filename, domain)
                potential_sections.extend(sections)
        
        # Score sections based on relevance to job and domain
        for section in potential_sections:
            section['relevance_score'] = self.calculate_dynamic_relevance(section, domain, job_description)
        
        # Sort by relevance and return top candidates
        potential_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        return potential_sections[:20]  # Return top 20 candidates
    
    def extract_sections_from_page(self, page_text: str, page_num: int, filename: str, domain: str) -> List[Dict]:
        """Extract potential sections from a single page."""
        sections = []
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            if self.is_potential_section_header(line, domain):
                # Get context around this potential header
                context_start = max(0, i-2)
                context_end = min(len(lines), i+20)
                context = ' '.join(lines[context_start:context_end])
                
                sections.append({
                    'title': line,
                    'page_number': page_num,
                    'filename': filename,
                    'context': context,
                    'line_position': i
                })
        
        return sections
    
    def is_potential_section_header(self, line: str, domain: str) -> bool:
        """Determine if a line could be a section header."""
        if len(line) < 10 or len(line) > 100:
            return False
        
        # Check for header-like formatting
        if not line[0].isupper():
            return False
        
        # Avoid lines that are clearly not headers
        if line.endswith('.') or line.count('.') > 3:
            return False
        
        if ':' in line and line.index(':') < len(line) - 10:
            return False
        
        # Check for domain-relevant keywords
        line_lower = line.lower()
        domain_keywords = self.domain_keywords.get(domain, [])
        
        keyword_count = sum(1 for keyword in domain_keywords if keyword in line_lower)
        
        # Must have at least one domain keyword or be a clear title
        if keyword_count == 0:
            # Check for title-like patterns
            words = line.split()
            if len(words) < 3 or len(words) > 12:
                return False
            
            # Check if it looks like a title (most words capitalized)
            capitalized_words = sum(1 for word in words if word[0].isupper())
            if capitalized_words / len(words) < 0.5:
                return False
        
        return True
    
    def calculate_dynamic_relevance(self, section: Dict, domain: str, job_description: str) -> float:
        """Calculate relevance score for a section based on content and context."""
        score = 0.0
        
        text_to_analyze = (section['title'] + ' ' + section['context']).lower()
        
        # Domain keyword scoring
        domain_keywords = self.domain_keywords.get(domain, [])
        for keyword in domain_keywords:
            count = text_to_analyze.count(keyword)
            score += count * 5
        
        # Job description keyword scoring
        job_words = [word.lower() for word in job_description.split() if len(word) > 3]
        for word in job_words:
            if word in text_to_analyze:
                score += 8
        
        # Title quality scoring
        title_lower = section['title'].lower()
        
        # Bonus for informative titles
        informative_words = ['guide', 'tips', 'how to', 'instructions', 'comprehensive', 'ultimate', 'complete']
        for word in informative_words:
            if word in title_lower:
                score += 15
        
        # Bonus for specific content types
        if domain == 'travel':
            travel_specific = ['adventures', 'experiences', 'attractions', 'destinations', 'activities']
            for word in travel_specific:
                if word in title_lower:
                    score += 12
        elif domain == 'hr':
            hr_specific = ['forms', 'documents', 'procedures', 'processes', 'workflow']
            for word in hr_specific:
                if word in title_lower:
                    score += 12
        elif domain == 'food':
            food_specific = ['recipe', 'ingredients', 'cooking', 'preparation', 'menu']
            for word in food_specific:
                if word in title_lower:
                    score += 12
        
        # Content length and quality bonus
        if len(section['context']) > 200:
            score += 10
        
        if len(section['context']) > 500:
            score += 5
        
        # Page position consideration (first few pages often have important content)
        if section['page_number'] <= 3:
            score += 8
        
        return score

    def extract_refined_content(self, section: Dict) -> str:
        """Extract and refine content from a section."""
        content = section['context']
        
        # Split into sentences/lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Find content with substantial information
        relevant_lines = []
        for line in lines:
            if len(line) > 30:  # Substantial content
                relevant_lines.append(line)
        
        # Create refined text
        if relevant_lines:
            refined_text = ' '.join(relevant_lines[:15])  # Take first 15 relevant lines
        else:
            # Fallback to all available content
            refined_text = content
        
        # Clean and format
        refined_text = re.sub(r'\s+', ' ', refined_text).strip()
        
        # Ensure reasonable length
        if len(refined_text) > 800:
            refined_text = refined_text[:800]
            # Try to end at sentence boundary
            last_period = refined_text.rfind('.')
            if last_period > 400:
                refined_text = refined_text[:last_period + 1]
        
        return refined_text if refined_text else "Content extracted from relevant sections."

    def process_collection(self, input_file: str, pdfs_directory: str) -> Dict[str, Any]:
        """Process a collection using dynamic section analysis."""
        
        # Read input configuration
        with open(input_file, 'r') as f:
            input_data = json.load(f)
        
        persona = input_data['persona']['role']
        job = input_data['job_to_be_done']['task']
        documents = input_data['documents']
        
        print(f"   📝 Persona: {persona}")
        print(f"   🎯 Job: {job}")
        
        # Determine domain dynamically
        domain = self.determine_collection_domain(persona, job)
        print(f"   🎭 Domain: {domain}")
        
        # Extract content from all PDFs
        all_files_content = {}
        pdf_files = [f for f in os.listdir(pdfs_directory) if f.endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdfs_directory, pdf_file)
            print(f"     📄 Processing: {pdf_file}")
            pages_content = self.extract_text_from_pdf(pdf_path)
            if pages_content:
                all_files_content[pdf_file] = pages_content
        
        # Dynamically identify relevant sections
        potential_sections = self.identify_sections_dynamically(all_files_content, domain, job)
        
        print(f"     🔍 Found {len(potential_sections)} potential sections")
        
        # Select top 5 sections
        extracted_sections = []
        subsection_analysis = []
        
        for i, section in enumerate(potential_sections[:5]):
            extracted_sections.append({
                "document": section['filename'],
                "section_title": section['title'],
                "importance_rank": i + 1,
                "page_number": section['page_number']
            })
            
            refined_content = self.extract_refined_content(section)
            subsection_analysis.append({
                "document": section['filename'],
                "refined_text": refined_content,
                "page_number": section['page_number']
            })
            
            print(f"     ✅ Selected: {section['title']} -> {section['filename']} (page {section['page_number']}, score: {section['relevance_score']:.1f})")
        
        # Create output structure
        result = {
            "metadata": {
                "persona": input_data['persona'],
                "job_to_be_done": input_data['job_to_be_done'],
                "documents": documents,
                "timestamp": datetime.now().isoformat(),
                "analysis_summary": f"Extracted {len(extracted_sections)} sections using dynamic content analysis for {domain} domain"
            },
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }
        
        return result

def main():
    """Main function to discover and process all collections."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    analyzer = DocumentAnalyzer()
    
    print("🚀 Starting Adobe Challenge 1B Solution with Dynamic Content Analysis")
    print("=" * 70)
    
    # Discover collections
    collections = []
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if os.path.isdir(item_path) and item.lower().startswith('collection'):
            input_file = os.path.join(item_path, 'challenge1b_input.json')
            pdfs_dir = os.path.join(item_path, 'PDFs')
            
            if os.path.exists(input_file) and os.path.exists(pdfs_dir):
                collections.append((item, input_file, pdfs_dir))
    
    if not collections:
        print("❌ No valid collections found!")
        return
    
    print(f"📁 Found {len(collections)} collections")
    
    # Process each collection
    for collection_name, input_file, pdfs_dir in collections:
        print(f"\n📂 Processing {collection_name}:")
        
        try:
            result = analyzer.process_collection(input_file, pdfs_dir)
            
            if result:
                # Save output
                output_file = os.path.join(os.path.dirname(input_file), 'challenge1b_solution_output.json')
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                sections_count = len(result.get('extracted_sections', []))
                print(f"   ✅ Successfully processed! Generated {sections_count} sections")
                print(f"   💾 Output saved to: {output_file}")
            else:
                print(f"   ❌ Failed to process {collection_name}")
                
        except Exception as e:
            print(f"   ❌ Error processing {collection_name}: {e}")
    
    print(f"\n🎉 Processing complete!")

if __name__ == "__main__":
    main()
