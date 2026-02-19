import requests
import sys
import json
import time
from datetime import datetime

class BatasAIAPITester:
    def __init__(self, base_url="https://legal-assist-ai-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'} if not files else {}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=30)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Non-dict response'}")
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_stats(self):
        """Test stats endpoint"""
        success, response = self.run_test("Get Stats", "GET", "stats", 200)
        if success and isinstance(response, dict):
            expected_keys = ['documents', 'translations', 'chat_sessions', 'legal_articles']
            missing_keys = [key for key in expected_keys if key not in response]
            if missing_keys:
                print(f"   ⚠️  Missing keys in stats: {missing_keys}")
            else:
                print(f"   📊 Stats: {response}")
        return success

    def test_legal_knowledge(self):
        """Test legal knowledge endpoint"""
        success, response = self.run_test("Get Legal Knowledge", "GET", "legal-knowledge", 200)
        if success and isinstance(response, dict) and 'laws' in response:
            laws_count = len(response['laws'])
            print(f"   📚 Found {laws_count} legal articles")
            if laws_count >= 6:
                print(f"   ✅ Expected mock laws present")
                # Test a specific law
                sample_law = response['laws'][0] if response['laws'] else None
                if sample_law:
                    print(f"   📖 Sample law: {sample_law.get('title', 'No title')[:50]}...")
            else:
                print(f"   ⚠️  Expected at least 6 mock laws, found {laws_count}")
        return success

    def test_legal_knowledge_search(self):
        """Test legal knowledge search functionality"""
        # Test search by query
        success1, _ = self.run_test("Search Legal Knowledge (query)", "GET", "legal-knowledge?q=Civil", 200)
        
        # Test filter by category
        success2, _ = self.run_test("Search Legal Knowledge (category)", "GET", "legal-knowledge?category=Civil Law", 200)
        
        # Test filter by language
        success3, _ = self.run_test("Search Legal Knowledge (language)", "GET", "legal-knowledge?language=en", 200)
        
        return success1 and success2 and success3

    def test_language_detection(self):
        """Test language detection endpoint"""
        test_data = {"text": "This is a legal contract"}
        success, response = self.run_test("Detect Language", "POST", "detect-language", 200, data=test_data)
        if success and isinstance(response, dict):
            if 'detected_language' in response:
                print(f"   🌐 Detected language: {response['detected_language']}")
            else:
                print(f"   ⚠️  Missing 'detected_language' in response")
        return success

    def test_translation(self):
        """Test translation endpoint (placeholder)"""
        test_data = {
            "text": "This is a legal contract",
            "source_language": "auto",
            "target_language": "tl"
        }
        success, response = self.run_test("Translate Text", "POST", "translate", 200, data=test_data)
        if success and isinstance(response, dict):
            expected_keys = ['original_text', 'translated_text', 'source_language', 'target_language']
            missing_keys = [key for key in expected_keys if key not in response]
            if missing_keys:
                print(f"   ⚠️  Missing keys in translation: {missing_keys}")
            else:
                print(f"   🔄 Translation: {response['translated_text'][:50]}...")
        return success

    def test_legal_chat(self):
        """Test legal chat with Claude Sonnet"""
        test_data = {
            "message": "What is Article 19 of the Civil Code?",
            "session_id": None,
            "context": None
        }
        print("   ⏳ Sending message to Claude Sonnet (may take 10-15 seconds)...")
        success, response = self.run_test("Legal Chat", "POST", "chat", 200, data=test_data)
        if success and isinstance(response, dict):
            if 'response' in response and 'session_id' in response:
                self.session_id = response['session_id']
                print(f"   🤖 AI Response: {response['response'][:100]}...")
                print(f"   🆔 Session ID: {self.session_id}")
                return True
            else:
                print(f"   ⚠️  Missing 'response' or 'session_id' in chat response")
        return success

    def test_chat_follow_up(self):
        """Test follow-up chat message"""
        if not self.session_id:
            print("   ⚠️  Skipping follow-up test - no session ID from previous chat")
            return True
            
        test_data = {
            "message": "What are the requirements for valid marriage in the Philippines?",
            "session_id": self.session_id,
            "context": None
        }
        print("   ⏳ Sending follow-up message...")
        success, response = self.run_test("Legal Chat Follow-up", "POST", "chat", 200, data=test_data)
        if success and isinstance(response, dict):
            if 'response' in response:
                print(f"   🤖 Follow-up Response: {response['response'][:100]}...")
                return True
        return success

    def test_chat_history(self):
        """Test chat history retrieval"""
        if not self.session_id:
            print("   ⚠️  Skipping chat history test - no session ID")
            return True
            
        success, response = self.run_test("Get Chat History", "GET", f"chat/sessions/{self.session_id}", 200)
        if success and isinstance(response, dict) and 'messages' in response:
            messages_count = len(response['messages'])
            print(f"   💬 Found {messages_count} messages in chat history")
        return success

    def test_document_upload(self):
        """Test document upload"""
        # Create a test text file
        test_content = "This is a test legal document for upload testing."
        files = {'file': ('test_document.txt', test_content, 'text/plain')}
        
        success, response = self.run_test("Upload Document", "POST", "documents/upload", 200, files=files)
        if success and isinstance(response, dict):
            if 'id' in response and 'filename' in response:
                print(f"   📄 Uploaded document ID: {response['id']}")
                print(f"   📝 Filename: {response['filename']}")
                return response['id']
            else:
                print(f"   ⚠️  Missing 'id' or 'filename' in upload response")
        return None

    def test_get_documents(self):
        """Test get documents list"""
        success, response = self.run_test("Get Documents", "GET", "documents", 200)
        if success and isinstance(response, dict) and 'documents' in response:
            docs_count = len(response['documents'])
            print(f"   📚 Found {docs_count} documents")
        return success

    def test_get_single_document(self, doc_id):
        """Test get single document"""
        if not doc_id:
            print("   ⚠️  Skipping single document test - no document ID")
            return True
            
        success, response = self.run_test("Get Single Document", "GET", f"documents/{doc_id}", 200)
        if success and isinstance(response, dict):
            if 'content' in response:
                print(f"   📖 Document content: {response['content'][:50]}...")
        return success

    def test_translations_history(self):
        """Test get translations history"""
        success, response = self.run_test("Get Translations History", "GET", "translations", 200)
        if success and isinstance(response, dict) and 'translations' in response:
            trans_count = len(response['translations'])
            print(f"   🔄 Found {trans_count} translations in history")
        return success

def main():
    print("🚀 Starting Batas.AI API Testing...")
    print("=" * 60)
    
    tester = BatasAIAPITester()
    
    # Test basic endpoints
    tester.test_root_endpoint()
    tester.test_stats()
    
    # Test legal knowledge
    tester.test_legal_knowledge()
    tester.test_legal_knowledge_search()
    
    # Test language features
    tester.test_language_detection()
    tester.test_translation()
    tester.test_translations_history()
    
    # Test document features
    doc_id = tester.test_document_upload()
    tester.test_get_documents()
    tester.test_get_single_document(doc_id)
    
    # Test chat features (most important)
    tester.test_legal_chat()
    tester.test_chat_follow_up()
    tester.test_chat_history()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All API tests passed!")
        return 0
    else:
        failed_count = tester.tests_run - tester.tests_passed
        print(f"❌ {failed_count} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())