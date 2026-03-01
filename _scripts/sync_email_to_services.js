// Sync Email Processing Results to Todoist, Google Calendar, and Amplenote
const https = require('https');
const fs = require('fs');
const path = require('path');

// Load environments
const ENV_FILE = path.join('G:', 'My Drive', '03_Areas', 'Keys', 'Environments', 'environments.json');
const envConfig = JSON.parse(fs.readFileSync(ENV_FILE, 'utf8'));

// Get API tokens
const TODOIST_TOKEN = envConfig.environments.todoist.credentials.apiToken;
const AMPLENOTE_TOKEN_FILE = path.join(process.env.USERPROFILE || process.env.HOME, 'Desktop', 'amplenote_token.json');
const amplenoteTokenData = JSON.parse(fs.readFileSync(AMPLENOTE_TOKEN_FILE, 'utf8'));
const AMPLENOTE_TOKEN = amplenoteTokenData.access_token;

console.log('\n╔════════════════════════════════════════════════════════════╗');
console.log('║    Syncing Email Results to Todoist/Calendar/Amplenote    ║');
console.log('╚════════════════════════════════════════════════════════════╝\n');

// Helper function for HTTPS requests
function httpsRequest(hostname, path, method, headers, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: hostname,
      port: 443,
      path: path,
      method: method,
      headers: headers
    };

    if (body) {
      options.headers['Content-Length'] = Buffer.byteLength(body);
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
      req.write(body);
    }
    
    req.end();
  });
}

// Todoist API
async function createTodoistTask(content, dueDate = null, priority = 1) {
  const taskData = {
    content: content,
    priority: priority // 1=normal, 2=high, 3=very high, 4=urgent
  };
  
  if (dueDate) {
    taskData.due_string = dueDate;
  }
  
  const body = JSON.stringify(taskData);
  
  return await httpsRequest(
    'api.todoist.com',
    '/rest/v2/tasks',
    'POST',
    {
      'Authorization': `Bearer ${TODOIST_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body
  );
}

// Amplenote API
async function createAmplenoteNote(name, tags, content) {
  const noteData = {
    name: name,
    tags: tags.map(text => ({ text }))
  };
  
  const note = await httpsRequest(
    'api.amplenote.com',
    '/v4/notes',
    'POST',
    {
      'Authorization': `Bearer ${AMPLENOTE_TOKEN}`,
      'Content-Type': 'application/json'
    },
    JSON.stringify(noteData)
  );
  
  // Add content
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
  
  await httpsRequest(
    'api.amplenote.com',
    `/v4/notes/${note.uuid}/actions`,
    'POST',
    {
      'Authorization': `Bearer ${AMPLENOTE_TOKEN}`,
      'Content-Type': 'application/json'
    },
    JSON.stringify(actionData)
  );
  
  return note;
}

// Find latest email processing file
function findLatestProcessingFile() {
  const scriptsDir = __dirname;
  const files = fs.readdirSync(scriptsDir);
  
  const processingFiles = files.filter(f => f.startsWith('email_processing_') && f.endsWith('.json'));
  
  if (processingFiles.length === 0) {
    throw new Error('No email processing files found. Run email_processor.py first.');
  }
  
  processingFiles.sort().reverse();
  return path.join(scriptsDir, processingFiles[0]);
}

// Main sync function
async function syncToServices() {
  try {
    // Load latest processing file
    const processingFile = findLatestProcessingFile();
    console.log(`📄 Loading: ${path.basename(processingFile)}\n`);
    
    const results = JSON.parse(fs.readFileSync(processingFile, 'utf8'));
    
    let todoistCount = 0;
    let amplenoteCount = 0;
    let calendarCount = 0;
    
    // 1. Sync tasks to Todoist
    if (results.tasks.length > 0) {
      console.log(`📋 Syncing ${results.tasks.length} tasks to Todoist...`);
      
      for (const task of results.tasks) {
        try {
          const priority = task.priority === 'high' ? 3 : 1;
          await createTodoistTask(task.title, task.due_date, priority);
          console.log(`   ✅ ${task.title.substring(0, 50)}...`);
          todoistCount++;
          await new Promise(resolve => setTimeout(resolve, 200)); // Rate limiting
        } catch (error) {
          console.log(`   ❌ Failed: ${task.title.substring(0, 50)}... - ${error.message}`);
        }
      }
      console.log('');
    }
    
    // 2. Events to Google Calendar (placeholder - requires OAuth setup)
    if (results.events.length > 0) {
      console.log(`📅 Calendar events identified: ${results.events.length}`);
      console.log('   ⚠️  Google Calendar integration requires OAuth setup');
      console.log('   Events listed below for manual entry:\n');
      
      for (const event of results.events) {
        console.log(`   - ${event.title}`);
        console.log(`     Date: ${event.date || 'TBD'} ${event.time || ''}`);
        console.log(`     Location: ${event.location || 'N/A'}`);
        console.log('');
        calendarCount++;
      }
    }
    
    // 3. Important notes to Amplenote
    if (results.notes.length > 0) {
      console.log(`📝 Creating ${results.notes.length} notes in Amplenote...`);
      
      for (const noteInfo of results.notes) {
        try {
          const noteName = `Email: ${noteInfo.subject}`;
          const content = `**From:** ${noteInfo.from}\n**Date:** ${noteInfo.date}\n**Subject:** ${noteInfo.subject}`;
          
          await createAmplenoteNote(noteName, ['email-archive', 'important'], content);
          console.log(`   ✅ ${noteInfo.subject.substring(0, 50)}...`);
          amplenoteCount++;
          await new Promise(resolve => setTimeout(resolve, 200));
        } catch (error) {
          console.log(`   ❌ Failed: ${noteInfo.subject.substring(0, 50)}... - ${error.message}`);
        }
      }
      console.log('');
    }
    
    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log('║       ✅ Sync Complete!                                    ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');
    
    console.log('📊 Summary:');
    console.log(`   ✅ Tasks synced to Todoist: ${todoistCount}`);
    console.log(`   📅 Events for Google Calendar: ${calendarCount}`);
    console.log(`   📝 Notes created in Amplenote: ${amplenoteCount}\n`);
    
    console.log('🔗 Quick Links:');
    console.log('   Todoist: https://todoist.com/app/today');
    console.log('   Google Calendar: https://calendar.google.com');
    console.log('   Amplenote: https://www.amplenote.com/notes\n');
    
  } catch (error) {
    console.error('\n❌ Sync failed:', error.message);
    throw error;
  }
}

// Run sync
syncToServices().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
