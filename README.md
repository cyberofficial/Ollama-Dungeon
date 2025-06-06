# 🎮 Ollama Dungeon – AI-Powered Text Adventure

<div align="center">

![Python](https://img.shields.io/badge/python-3.12.7-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Ollama](https://img.shields.io/badge/Ollama-Powered-orange.svg)](https://ollama.ai/)

</div>

A sophisticated, locally-hosted AI-powered text adventure game where **the world IS the filesystem**. This modular platform features intelligent AI agents with persistent memories, advanced multi-agent conversation systems, location-aware endless conversation mode, and comprehensive analytics—all running completely offline with automatic backups and save management.

-------------------

⚠⚠⚠⚠ Please note ⚠⚠⚠⚠

This is not fully finished, somethings will break or not function as intended. 

If you encounter an issue, please make a report

items are useless right now, they are just for prop/show. items will be implemented later.


-------------------

## Video Demo
### Video demo of a 3 way conversation.


https://github.com/user-attachments/assets/e9efc5b7-c276-4b24-a530-a111f8ca4bd8


-------------------

<div align="center">
  <img src="https://github.com/user-attachments/assets/1e0b6e0e-8793-434a-877a-a7317300bca5" alt="Ollama Dungeon Screenshot" width="50%"/>
</div>

## ✨ Key Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🌍 Filesystem-Based World</h3>
      <ul>
        <li><b>Dynamic World Creation:</b> Automatically copies <code>world_template</code> to <code>world</code> on first run</li>
        <li><b>Hierarchical Structure:</b> Each folder represents a location, files represent agents and items</li>
        <li><b>Persistent State:</b> All changes to the world are saved to the filesystem</li>
        <li><b>Template Protection:</b> Original <code>world_template</code> is never modified, ensuring clean resets</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🤖 Intelligent AI Agents</h3>
      <ul>
        <li><b>Individual Personalities:</b> Each agent has unique persona, background, goals, and relationships</li>
        <li><b>Persistent Memory:</b> Agents remember conversations through CSV-based long-term memory</li>
        <li><b>Context Awareness:</b> Agents understand their environment, other people, and available items</li>
        <li><b>Emotional Intelligence:</b> Agents have moods, fears, motivations, and personality quirks</li>
        <li><b>Isolated Contexts:</b> Each agent maintains separate conversation history with automatic compression</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>💾 Advanced Save/Load System</h3>
      <ul>
        <li><b>Complete World Saves:</b> Entire world state, agent contexts, and inventory preserved</li>
        <li><b>Multiple Save Slots:</b> Create and manage unlimited named saves</li>
        <li><b>Automatic Backups:</b> Creates timestamped backups before loading or deleting saves</li>
        <li><b>Safe Operations:</b> All destructive operations create recovery backups</li>
        <li><b>Detailed Save Info:</b> Shows timestamp and player location for each save</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🧠 Smart Token Management</h3>
      <ul>
        <li><b>Automatic Compression:</b> Context automatically compressed when approaching token limits</li>
        <li><b>Dual Model System:</b> Main model (40k context) + summary model for efficient compression</li>
        <li><b>Token Monitoring:</b> Real-time token usage tracking and warnings</li>
        <li><b>Manual Control:</b> Manual compression commands for fine-tuning performance</li>
        <li><b>Emergency Handling:</b> Graceful degradation when approaching hard limits</li>
      </ul>
    </td>
  </tr>  <tr>
    <td width="50%" valign="top">
      <h3>🔄 Enhanced Conversation System</h3>
      <ul>
        <li><b>Endless Conversation Mode:</b> Multi-agent conversations that flow naturally between participants</li>
        <li><b>Location-Aware Conversations:</b> Agents automatically join/leave conversations based on location</li>
        <li><b>Following Behavior:</b> Control which agents follow you and participate in conversations</li>
        <li><b>Manual Participant Management:</b> Invite or remove specific agents from ongoing conversations</li>
        <li><b>Context Sharing:</b> Share observations and thoughts with agents in your current location</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🛡️ Privacy & Security</h3>
      <ul>
        <li><b>Fully Offline:</b> All processing happens on your local machine</li>
        <li><b>No Data Collection:</b> Your stories and interactions remain private</li>
        <li><b>Open Architecture:</b> Transparent design with no hidden processes</li>
        <li><b>Local LLM:</b> Uses Ollama for complete privacy and control</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🔄 Context Sharing</h3>
      <ul>
        <li><b>Shared Experiences:</b> Agents can share context within the same location</li>
        <li><b>Player Narration:</b> Share observations and thoughts with all agents in a room</li>
        <li><b>Memory Integration:</b> Shared context becomes part of agent memory systems</li>
        <li><b>Token-Aware:</b> Shared context limited by token budgets to prevent overflow</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>📊 Advanced Analytics</h3>
      <ul>
        <li><b>Game Statistics:</b> Track conversations, locations visited, and agent interactions</li>
        <li><b>Performance Monitoring:</b> Monitor model loading, response times, and system health</li>
        <li><b>Token Usage Analytics:</b> Detailed breakdown of token consumption across all agents</li>
        <li><b>Memory Management:</b> Insights into agent memory compression and optimization</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🛡️ Privacy & Security</h3>
      <ul>
        <li><b>Fully Offline:</b> All processing happens on your local machine</li>
        <li><b>No Data Collection:</b> Your stories and interactions remain private</li>
        <li><b>Open Architecture:</b> Transparent design with no hidden processes</li>
        <li><b>Local LLM:</b> Uses Ollama for complete privacy and control</li>
      </ul>
    </td>
  </tr>
</table>

## 🚀 Quick Start

### Prerequisites

<table>
  <tr>
    <td align="center"><img src="https://via.placeholder.com/50?text=🐍" alt="Python" width="50" height="50"/></td>
    <td><b>Python 3.12.7</b> with pip</td>
  </tr>
  <tr>
    <td align="center"><img src="https://via.placeholder.com/50?text=🦙" alt="Ollama" width="50" height="50"/></td>
    <td><b>Ollama</b> running locally</td>
  </tr>
  <tr>
    <td align="center"><img src="https://via.placeholder.com/50?text=🧠" alt="Models" width="50" height="50"/></td>
    <td><b>Required Models</b>: <code>qwen3:8b</code> (main) and <code>qwen3:4b</code> (summary)</td>
  </tr>
</table>

### Installation

<div class="installation-steps">
  <ol>
    <li>
      <b>Install Dependencies:</b>
      <pre><code class="language-bash">pip install -r requirements.txt</code></pre>
    </li>
    <li>
      <b>Setup Ollama Models:</b>
      <pre><code class="language-bash">ollama pull qwen3:8b
ollama pull qwen3:4b
ollama serve</code></pre>
    </li>
    <li>
      <b>Verify Setup:</b>
      <pre><code class="language-bash">python verify_setup.py</code></pre>
    </li>
    <li>
      <b>Start Playing:</b>
      <pre><code class="language-bash">python main.py</code></pre>
    </li>  </ol>
</div>

##  Commands Reference

<div class="commands-container">
  <div class="command-section">
    <h3>🧭 Movement & Exploration</h3>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Description</th>
          <th>Example</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/look</code>, <code>/l</code></td>
          <td>Describe current room and contents</td>
          <td><code>/look</code></td>
        </tr>
        <tr>
          <td><code>/go &lt;direction&gt;</code></td>
          <td>Move to another location</td>
          <td><code>/go north</code></td>
        </tr>
        <tr>
          <td><code>/move &lt;direction&gt;</code></td>
          <td>Alternative to /go</td>
          <td><code>/move south</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="command-section">
    <h3>💬 Agent Interaction</h3>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Description</th>
          <th>Example</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/say &lt;agent&gt; &lt;message&gt;</code></td>
          <td>Talk to an agent</td>
          <td><code>/say alice Hello there!</code></td>
        </tr>
        <tr>
          <td><code>/talk &lt;agent&gt; &lt;message&gt;</code></td>
          <td>Alternative to /say</td>
          <td><code>/talk bob Hi!</code></td>
        </tr>
        <tr>
          <td><code>/agents</code>, <code>/people</code></td>
          <td>List all people in current room</td>
          <td><code>/agents</code></td>
        </tr>
        <tr>
          <td><code>/memory &lt;agent&gt;</code></td>
          <td>Show agent's recent memories</td>
          <td><code>/memory bob</code></td>
        </tr>
        <tr>
          <td><code>/summarize [target(s)] [context]</code></td>
          <td>Share context with agents</td>
          <td><code>/summarize alice Bob looks worried</code></td>
        </tr>
        <tr>
          <td><code>/share [target(s)] [context]</code></td>
          <td>Alternative to /summarize</td>
          <td><code>/share alice,bob Secret meeting</code></td>
        </tr>        <tr>
          <td><code>/follow &lt;agent&gt;</code></td>
          <td>Have agent follow you</td>
          <td><code>/follow alice</code></td>
        </tr>
        <tr>
          <td><code>/stay &lt;agent&gt;</code></td>
          <td>Make agent stop following and stay in current location</td>
          <td><code>/stay alice</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="command-section">
    <h3>🗣️ Endless Conversation Mode</h3>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Description</th>
          <th>Example</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/conv</code></td>
          <td>Start endless conversation mode with all agents in room</td>
          <td><code>/conv</code></td>
        </tr>
        <tr>
          <td><code>/endconv</code></td>
          <td>End endless conversation mode</td>
          <td><code>/endconv</code></td>
        </tr>
        <tr>
          <td><code>/invite &lt;agent&gt;</code></td>
          <td>Add an agent to current endless conversation</td>
          <td><code>/invite bob</code></td>
        </tr>
        <tr>
          <td><code>/remove &lt;agent&gt;</code></td>
          <td>Remove an agent from current endless conversation</td>
          <td><code>/remove alice</code></td>
        </tr>
        <tr>
          <td><code>/dialog &lt;message&gt;</code></td>
          <td>Send message in endless conversation mode</td>
          <td><code>/dialog What should we do next?</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="command-section">
    <h3>🎒 Inventory Management</h3>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Description</th>
          <th>Example</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/inventory</code>, <code>/inv</code></td>
          <td>View your inventory</td>
          <td><code>/inventory</code></td>
        </tr>
        <tr>
          <td><code>/pickup &lt;item&gt;</code></td>
          <td>Pick up an item</td>
          <td><code>/pickup rusty dagger</code></td>
        </tr>
        <tr>
          <td><code>/take &lt;item&gt;</code></td>
          <td>Alternative to /pickup</td>
          <td><code>/take health potion</code></td>
        </tr>
        <tr>
          <td><code>/use &lt;item&gt;</code></td>
          <td>Use an item from inventory</td>
          <td><code>/use health potion</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="command-section">
    <h3>💾 Save & Load System</h3>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Description</th>
          <th>Example</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/save [name]</code></td>
          <td>Save current game state</td>
          <td><code>/save adventure1</code></td>
        </tr>
        <tr>
          <td><code>/load [name]</code></td>
          <td>Load a saved game</td>
          <td><code>/load adventure1</code></td>
        </tr>
        <tr>
          <td><code>/saves</code></td>
          <td>List all available saves</td>
          <td><code>/saves</code></td>
        </tr>
        <tr>
          <td><code>/delete &lt;name&gt;</code></td>
          <td>Delete a save (creates backup)</td>
          <td><code>/delete old_save</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="command-section">
    <h3>⚙️ System & Debug</h3>
    <table>
      <thead>
        <tr>
          <th>Command</th>
          <th>Description</th>
          <th>Example</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/tokens [agent]</code></td>
          <td>Show token usage statistics</td>
          <td><code>/tokens alice</code></td>
        </tr>
        <tr>
          <td><code>/compress &lt;agent&gt;</code></td>
          <td>Manually compress agent context</td>
          <td><code>/compress bob</code></td>
        </tr>
        <tr>
          <td><code>/compress_all</code></td>
          <td>Compress all agents in current room</td>
          <td><code>/compress_all</code></td>
        </tr>
        <tr>
          <td><code>/status</code></td>
          <td>Show system connectivity and stats</td>
          <td><code>/status</code></td>
        </tr>        <tr>
          <td><code>/reset &lt;agent&gt;</code></td>
          <td>Reset agent's memory and context</td>
          <td><code>/reset alice</code></td>
        </tr>
        <tr>
          <td><code>/analytics</code></td>
          <td>Show detailed game analytics and statistics</td>
          <td><code>/analytics</code></td>
        </tr>
        <tr>
          <td><code>/model_state</code></td>
          <td>Display model loading and performance information</td>
          <td><code>/model_state</code></td>
        </tr>
        <tr>
          <td><code>/help</code></td>
          <td>Show all available commands</td>
          <td><code>/help</code></td>
        </tr>
        <tr>
          <td><code>/quit</code>, <code>/exit</code>, <code>/q</code></td>
          <td>Exit the game</td>
          <td><code>/quit</code></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

## 🏗️ World Structure

### **Directory Layout**

<div class="directory-structure" style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
<pre>
<span style="color: #0366d6; font-weight: bold;">world_template/</span>          <span style="color: #6a737d;"># Protected template (never modified)</span>
├── <span style="color: #0366d6;">town/</span>
│   ├── <span style="color: #032f62;">room.json</span>       <span style="color: #6a737d;"># Room description and exits</span>
│   ├── <span style="color: #0366d6;">tavern/</span>
│   │   ├── <span style="color: #032f62;">room.json</span>
│   │   ├── <span style="color: #032f62;">agent_alice.json</span>     <span style="color: #6a737d;"># Tavern keeper</span>
│   │   ├── <span style="color: #032f62;">agent_bob.json</span>       <span style="color: #6a737d;"># Local scout</span>
│   │   ├── <span style="color: #032f62;">memory_alice.csv</span>     <span style="color: #6a737d;"># Alice's memories</span>
│   │   ├── <span style="color: #032f62;">memory_bob.csv</span>       <span style="color: #6a737d;"># Bob's memories</span>
│   │   ├── <span style="color: #032f62;">rusty_dagger.json</span>    <span style="color: #6a737d;"># Pickupable item</span>
│   │   └── <span style="color: #0366d6;">contexts/</span>            <span style="color: #6a737d;"># Agent conversation contexts</span>
│   │       ├── <span style="color: #032f62;">alice_context.pkl</span>
│   │       └── <span style="color: #032f62;">bob_context.pkl</span>
│   └── <span style="color: #0366d6;">market/</span>
│       ├── <span style="color: #032f62;">room.json</span>
│       └── <span style="color: #032f62;">health_potion.json</span>
└── <span style="color: #0366d6;">forest/</span>
    ├── <span style="color: #032f62;">room.json</span>
    └── <span style="color: #0366d6;">cave/</span>
        ├── <span style="color: #032f62;">room.json</span>
        ├── <span style="color: #032f62;">agent_grix.json</span>     <span style="color: #6a737d;"># Goblin scout</span>
        └── <span style="color: #032f62;">memory_grix.csv</span>

<span style="color: #0366d6; font-weight: bold;">world/</span>                   <span style="color: #6a737d;"># Active world (copied from template)</span>
├── <span style="color: #6a737d;">[same structure as template]</span>

<span style="color: #0366d6; font-weight: bold;">saves/</span>                   <span style="color: #6a737d;"># Save game storage</span>
├── <span style="color: #0366d6;">save1/</span>
│   ├── <span style="color: #032f62;">player_state.json</span>
│   ├── <span style="color: #0366d6;">world/</span>          <span style="color: #6a737d;"># Complete world snapshot</span>
│   └── <span style="color: #0366d6;">inventory/</span>      <span style="color: #6a737d;"># Player inventory snapshot</span>
└── <span style="color: #0366d6;">save2/</span>

<span style="color: #0366d6; font-weight: bold;">backups/</span>                <span style="color: #6a737d;"># Automatic safety backups</span>
├── <span style="color: #0366d6;">world_backup_before_load_save1_20250605_143026/</span>
└── <span style="color: #0366d6;">deleted_save_old_save_20250605_144404/</span>

<span style="color: #0366d6; font-weight: bold;">inventory/</span>              <span style="color: #6a737d;"># Player's items</span>
└── <span style="color: #6a737d;">[item files moved here when picked up]</span>
</pre>
</div>

### **File Formats**

<div class="file-formats">
  <div class="file-format">
    <h4>📄 Room Definition (<code>room.json</code>)</h4>
    <div class="code-block">
      <pre><code class="language-json">{
  "name": "The Prancing Pony Tavern",
  "description": "A warm, dimly lit tavern...",
  "exits": {
    "south": "world/town",
    "up": "world/town/tavern/upstairs"
  }
}</code></pre>
    </div>
  </div>

  <div class="file-format">
    <h4>👤 Agent Definition (<code>agent_alice.json</code>)</h4>
    <div class="code-block">
      <pre><code class="language-json">{
  "name": "Alice",
  "persona": "A friendly tavern keeper who knows everyone's business",
  "background": "Has run this tavern for 20 years",
  "appearance": "A middle-aged woman with graying hair and kind eyes",
  "mood": "cheerful",
  "occupation": "Tavern keeper",
  "memory_file": "memory_alice.csv",
  "knowledge": ["Local gossip", "Brewing techniques", "Town history"],
  "goals": ["Keep customers happy", "Maintain tavern reputation"],
  "fears": ["Economic downturn", "Losing regular customers"],
  "relationships": {
    "Bob": "Good friend and regular customer",
    "Mayor": "Respectful business relationship"
  }
}</code></pre>
    </div>
  </div>

  <div class="file-format">
    <h4>🧪 Item Definition (<code>health_potion.json</code>)</h4>
    <div class="code-block">
      <pre><code class="language-json">{
  "name": "Health Potion",
  "description": "A small vial of red liquid that glows faintly",
  "portable": true,
  "usable": true,
  "use_description": "You feel refreshed and energized!",
  "value": 50
}</code></pre>
    </div>
  </div>
</div>

## 🧰 Technical Features

<div class="features-container">
  <div class="feature-section">
    <div class="feature-card">
      <h3>🤖 AI Architecture</h3>
      <ul>
        <li><b>Local LLM Integration</b>: Uses Ollama for complete privacy and control</li>
        <li><b>Dual Model Strategy</b>: High-capacity main model + efficient summary model</li>
        <li><b>Context Compression</b>: Intelligent summarization prevents token overflow</li>
        <li><b>Session Persistence</b>: Agent contexts saved and restored between sessions</li>
      </ul>
    </div>
    
  <div class="feature-card">
    <h3>🧠 Memory Systems</h3>
    <ul>
      <li><b>CSV-Based Storage</b>: Structuredmemory entries with timestamps</li>
      <li><b>Memory Types</b>: Events, observations,dialogue, emotions</li>
      <li><b>Automatic Summarization</b>: Recentmemories compressed into readable summaries<li>
      <li><b>Cross-Session Persistence</b>: Memoriessurvive game restarts</li>
    </ul>
  </div>
  </div>
  
  <div class="feature-section">
    <div class="feature-card">
      <h3>🛡️ Safety & Reliability</h3>
      <ul>
        <li><b>Automatic Backups</b>: Every destructive operation creates timestamped backups</li>
        <li><b>Template Protection</b>: Original world template never modified</li>
        <li><b>Graceful Degradation</b>: System continues functioning even with AI failures</li>
        <li><b>Error Recovery</b>: Robust error handling with informative messages</li>
      </ul>
    </div>
    
  <div class="feature-card">
    <h3>⚡ Performance Optimization</h3>
    <ul>
      <li><b>Agent Caching</b>: Loaded agents cachedfor better performance</li>
      <li><b>Token Monitoring</b>: Real-timetracking prevents unexpected failures</li>
      <li><b>Lazy Loading</b>: Agents and itemsloaded only when needed</li>
      <li><b>Compression Triggers</b>: Automaticcontext compression based on configurablethresholds</li>
    </ul>
  </div>
  </div>
</div>

## 🎯 Use Cases

<div class="use-cases">
  <div class="use-case">
    <h3>📚 Interactive Storytelling</h3>
    <p>Create dynamic narratives with persistent characters</p>
  </div>
  <div class="use-case">
    <h3>🔬 AI Research</h3>
    <p>Experiment with multi-agent interactions and memory systems</p>
  </div>
  <div class="use-case">
    <h3>🎲 Game Development</h3>
    <p>Use as a foundation for more complex text adventures</p>
  </div>
  <div class="use-case">
    <h3>🎓 Education</h3>
    <p>Learn about AI, file systems, and game architecture</p>
  </div>
  <div class="use-case">
    <h3>🔧 Modding & Customization</h3>
    <p>Easily create new worlds, agents, and items</p>
  </div>
</div>

## 🛠️ Customization

<div class="customization-container">
  <div class="customization-section">
    <h3>👤 Creating New Agents</h3>
    <ol>
      <li>Copy an existing agent file from <code>world_template</code></li>
      <li>Modify the JSON with new personality, goals, and relationships</li>
      <li>Create a corresponding memory CSV file</li>
      <li>Place in appropriate location folder</li>
    </ol>
  </div>
  
  <div class="customization-section">
    <h3>🗺️ Adding New Locations</h3>
    <ol>
      <li>Create a new folder in <code>world_template</code></li>
      <li>Add a <code>room.json</code> file with description and exits</li>
      <li>Update parent room's exits to link to new location</li>
      <li>Add agents and items as desired</li>
    </ol>
  </div>
  
  <div class="customization-section">
    <h3>⚙️ Modifying Game Behavior</h3>
    <ul>
      <li>Edit <code>config.py</code> for token limits, model selection, and game settings</li>
      <li>Modify <code>cli.py</code> to add new commands or change interface</li>
      <li>Adjust <code>game_engine.py</code> for core game mechanics</li>
    </ul>
  </div>
</div>

## 📊 System Requirements

<div class="system-requirements">
  <div class="requirement">
    <span class="requirement-icon">💻</span>
    <span class="requirement-label">RAM:</span>
    <span class="requirement-value">8GB+ recommended (for local LLM)</span>
  </div>
  <div class="requirement">
    <span class="requirement-icon">�️</span>
    <span class="requirement-label">CPU:</span>
    <span class="requirement-value">6+ cores recommended</span>
  </div>
  <div class="requirement">
    <span class="requirement-icon">🎮</span>
    <span class="requirement-label">GPU:</span>
    <span class="requirement-value">At least 6GB VRAM recommended</span>
  </div>
  <div class="requirement">
    <span class="requirement-icon">🌐</span>
    <span class="requirement-label">Network:</span>
    <span class="requirement-value">Required only for initial model download</span>
  </div>
</div>

## 🔧 Troubleshooting

<div class="troubleshooting-container">
  <div class="troubleshooting-section">
    <h3>⚠️ Common Issues</h3>
    <ul>
      <li><b>"Can't connect to Ollama"</b>: Ensure <code>ollama serve</code> is running</li>
      <li><b>"Model not found"</b>: Run <code>ollama pull qwen3:8b</code> and <code>ollama pull qwen3:4b</code></li>
      <li><b>Token warnings</b>: Use <code>/compress_all</code> or <code>/tokens</code> to monitor usage</li>
      <li><b>Agent not responding</b>: Check <code>/status</code> for connectivity issues</li>
    </ul>
  </div>
  
  <div class="troubleshooting-section">
    <h3>📚 Getting Help</h3>
    <ol>
      <li>Run <code>python verify_setup.py</code> to check system health</li>
      <li>Use <code>/status</code> command in-game for real-time diagnostics</li>
      <li>Check agent memory with <code>/memory &lt;agent&gt;</code> for context issues</li>
      <li>Review token usage with <code>/tokens</code> for performance problems</li>      <li><b>See comprehensive guides for detailed documentation:</b>
        <ul>
          <li><a href="Guides/00-getting-started.md">Getting Started Guide</a> - Complete setup and basic gameplay</li>
          <li><a href="Guides/02-interacting-with-npcs.md">Interacting with NPCs</a> - Agent conversations and following behavior</li>
          <li><a href="Guides/04-conversation-system.md">Conversation System</a> - Endless conversation mode and multi-agent chats</li>
          <li><a href="Guides/06-command-reference.md">Command Reference</a> - Complete list of all available commands</li>
          <li><a href="Guides/05-advanced-features.md">Advanced Features</a> - Token management, analytics, and optimization</li>
        </ul>
      </li>
    </ol>
  </div>
</div>

---

<div align="center">
  <p><strong>Note</strong>: This is a fully offline, privacy-focused AI experience. All data stays on your local machine, and the world persists between sessions through the filesystem-based architecture.</p>
  <p>
    <a href="https://github.com/cyberofficial/Ollama-Dungeon">GitHub</a> •
    <a href="Guides/00-getting-started.md">Documentation</a> •
    <a href="LICENSE">License</a>
  </p>
</div>
