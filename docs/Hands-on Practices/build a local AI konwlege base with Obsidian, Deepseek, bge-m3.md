**Hands-on Guide to Setting Up Obsidian with DeepSeek and bge-m3 for Local AI-Powered Knowledge Base**

1. **Setup Obsidian**
   - Install and open the Obsidian app on your device.

2. **Setup DeepSeek**
   - Open your terminal or command prompt.
   - Run the following command to start DeepSeek locally:
     ```bash
     % ollama run deepseek-r1:8b -verbose
     ```

3. **Install bge-m3**
   - Pull the bge-m3 model using Ollama:
     ```bash
     % ollama pull bge-m3
     ```

4. **Configure Obsidian to Use Copilot, DeepSeek, and bge-m3 as RAG**
   - In Obsidian’s settings, navigate to the community plugins section.
   - Install the Copilot plugin.
   - Open Copilot settings and configure two models:
     1. **Chat Model**: Use DeepSeek with Ollama.
     2. **Embedding Model**: Use bge-m3 with Ollama.
---

This setup will allow you to leverage DeepSeek and bge-m3 within Obsidian for a localized AI-powered knowledge base, enhancing your note-taking and information management workflow.

Now, use chat capability 