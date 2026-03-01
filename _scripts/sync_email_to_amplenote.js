// Sync Email Processing Results to Amplenote
const https = require('https');
const fs = require('fs');
const path = require('path');

// Load Amplenote token
const TOKEN_FILE = path.join(process.env.USERPROFILE || process.env.HOME, 'Desktop', 'amplenote_token.json');
const tokenData = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
const ACCESS_TOKEN = tokenData.access_token;

console.log('\n╔════════════════════════════════════════════════════════════╗');
console.log('║       Syncing Email Processing Results to Amplenote       ║');
console.log('╚════════════════════════════════════════════════════════════╝\n');

// Helper function to make API requests
function apiRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.amplenote.com',
      port: 443,
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${ACCESS_TOKEN}`,
        'Content-Type': 'application/json'
      }
    };

    if (body) {
      const postData = JSON.stringify(body);
      options.headers['Content-Length'] = Buffer.byteLength(postData);
    }

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data ? JSON.parse(data) : {});
        } else {
          reject(new Error(`API Error: ${res.statusCode} - ${data}`));
        }
      });
    });

    req.on('error', reject);
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    
    req.end();
  });
}

// Create note
async function createNote(name, tags = []) {
  const noteData = {
    name: name,
    tags: tags.map(text => ({ text }))
  };
  
  return await apiRequest('POST', '/v4/notes', noteData);
}

// Add content to note
async function addContent(noteUuid, content) {
  const actionData = {
    type: 'INSERT_NODES',
    nodes: [
      {
        type: 'paragraph',
        content: [
          {
            type: 'text',
            text: content
          }
        ]
      }
    ]
  };
  
  return await apiRequest('POST', `/v4/notes/${noteUuid}/actions`, actionData);
}

// Add task to note
async function addTask(noteUuid, text, dueDate = null, important = false) {
  const attrs = {};
  
  if (dueDate) {
    attrs.due = Math.floor(new Date(dueDate).getTime() / 1000);
  }
  
  if (important) {
    attrs.flags = 'I';
  }

  const actionData = {
    type: 'INSERT_NODES',
    nodes: [
      {
        type: 'check_list_item',
        attrs: attrs,
        content: [
          {
            type: 'paragraph',
            content: [
              {
                type: 'text',
                text: text
              }
            ]
          }
        ]
      }
    ]
  };
  
  return await apiRequest('POST', `/v4/notes/${noteUuid}/actions`, actionData);
}

// Find latest email processing file
function findLatestProcessingFile() {
  const scriptsDir = __dirname;
  const files = fs.readdirSync(scriptsDir);
  
  const processingFiles = files.filter(f => f.startsWith('email_processing_') && f.endsWith('.json'));
  
  if (processingFiles.length === 0) {
    throw new Error('No email processing files found. Run email_processor.py first.');
  }
  
  // Sort by filename (which includes timestamp)
  processingFiles.sort().reverse();
  
  return path.join(scriptsDir, processingFiles[0]);
}

// Main sync function
async function syncToAmplenote() {
  try {
    // Find and load latest processing file
    const processingFile = findLatestProcessingFile();
    console.log(`📄 Loading: ${path.basename(processingFile)}\n`);
    
    const results = JSON.parse(fs.readFileSync(processingFile, 'utf8'));
    
    const processedDate = new Date(results.processed_date);
    const weekStart = new Date(processedDate);
    weekStart.setDate(weekStart.getDate() - results.days_processed);
    
    const noteName = `Email Processing - Week of ${weekStart.toLocaleDateString()}`;
    
    // Create weekly processing note
    console.log('📝 Creating weekly email processing note...');
    const note = await createNote(noteName, ['email-processing', 'weekly-review', 'inbox']);
    console.log(`✅ Created: ${note.uuid}`);
    console.log(`   URL: https://www.amplenote.com/notes/${note.uuid}\n`);
    
    // Add header
    await addContent(note.uuid, `# ${noteName}`);
    await addContent(note.uuid, `**Processed:** ${processedDate.toLocaleString()}`);
    await addContent(note.uuid, `**Days Covered:** ${results.days_processed}`);
    await addContent(note.uuid, '');
    
    // Add tasks section
    await addContent(note.uuid, '## 📋 Tasks Extracted');
    
    if (results.tasks.length > 0) {
      console.log(`📋 Adding ${results.tasks.length} tasks...`);
      
      for (const task of results.tasks) {
        const taskText = `${task.title} - ${task.source}`;
        await addTask(note.uuid, taskText, task.due_date, task.priority === 'high');
        console.log(`   ✅ ${task.title.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 200)); // Rate limiting
      }
    } else {
      await addContent(note.uuid, 'No tasks extracted from emails.');
    }
    
    await addContent(note.uuid, '');
    
    // Add events section
    await addContent(note.uuid, '## 📅 Calendar Events');
    
    if (results.events.length > 0) {
      console.log(`\n📅 Adding ${results.events.length} events...`);
      
      for (const event of results.events) {
        const eventText = `${event.title} - ${event.date || 'Date TBD'} ${event.time || ''} ${event.location ? `@ ${event.location}` : ''}`;
        await addContent(note.uuid, `- ${eventText}`);
        console.log(`   ✅ ${event.title.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    } else {
      await addContent(note.uuid, 'No calendar events identified.');
    }
    
    await addContent(note.uuid, '');
    
    // Add notes section
    await addContent(note.uuid, '## 📝 Notes to Create');
    
    if (results.notes.length > 0) {
      console.log(`\n📝 Listing ${results.notes.length} notes...`);
      
      for (const noteInfo of results.notes) {
        await addContent(note.uuid, `- ${noteInfo.subject} (from ${noteInfo.from})`);
        console.log(`   ✅ ${noteInfo.subject.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    } else {
      await addContent(note.uuid, 'No emails marked for note creation.');
    }
    
    await addContent(note.uuid, '');
    
    // Add summary
    await addContent(note.uuid, '## 📊 Summary');
    await addContent(note.uuid, `- **Tasks extracted:** ${results.tasks.length}`);
    await addContent(note.uuid, `- **Events identified:** ${results.events.length}`);
    await addContent(note.uuid, `- **Notes to create:** ${results.notes.length}`);
    await addContent(note.uuid, `- **Processing date:** ${processedDate.toLocaleString()}`);
    
    console.log('\n╔════════════════════════════════════════════════════════════╗');
    console.log('║       ✅ Sync Complete!                                    ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');
    
    console.log('📝 Created Note:');
    console.log(`   ${noteName}`);
    console.log(`   https://www.amplenote.com/notes/${note.uuid}\n`);
    
    console.log('📊 Summary:');
    console.log(`   - Tasks added: ${results.tasks.length}`);
    console.log(`   - Events listed: ${results.events.length}`);
    console.log(`   - Notes referenced: ${results.notes.length}\n`);
    
    return note;
    
  } catch (error) {
    console.error('\n❌ Sync failed:', error.message);
    throw error;
  }
}

// Run sync
syncToAmplenote().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
