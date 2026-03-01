// Sync Daily Plan to Amplenote Kanban Board
const https = require('https');
const fs = require('fs');
const path = require('path');

// Load Amplenote token from environments.json
const ENVIRONMENTS_PATH = path.join('G:', 'My Drive', '03_Areas', 'Keys', 'Environments', 'environments.json');
const envConfig = JSON.parse(fs.readFileSync(ENVIRONMENTS_PATH, 'utf8'));
const ACCESS_TOKEN = envConfig.environments.amplenote.credentials.accessToken;

console.log('\n╔════════════════════════════════════════════════════════════╗');
console.log('║         Creating Kanban Board in Amplenote                ║');
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

// Find existing daily plan note
async function findExistingDailyPlan(noteName) {
  try {
    const notes = await apiRequest('GET', '/v4/notes');
    return notes.notes.find(note => note.name === noteName);
  } catch (error) {
    return null;
  }
}

// Delete a note
async function deleteNote(noteUuid) {
  return await apiRequest('DELETE', `/v4/notes/${noteUuid}`, null);
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

// Find latest daily plan file
function findLatestPlanFile() {
  const scriptsDir = __dirname;
  const files = fs.readdirSync(scriptsDir);
  
  const planFiles = files.filter(f => f.startsWith('daily_plan_') && f.endsWith('.json'));
  
  if (planFiles.length === 0) {
    throw new Error('No daily plan files found. Run daily_planner.py first.');
  }
  
  planFiles.sort().reverse();
  return path.join(scriptsDir, planFiles[0]);
}

// Main sync function
async function syncToKanban() {
  try {
    // Load latest plan
    const planFile = findLatestPlanFile();
    console.log(`📄 Loading: ${path.basename(planFile)}\n`);
    
    const plan = JSON.parse(fs.readFileSync(planFile, 'utf8'));
    
    const today = new Date().toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    
    const noteName = `Daily Plan - ${today}`;
    
    // Check for existing daily plan
    console.log('📝 Checking for existing daily plan...');
    let existingNote = await findExistingDailyPlan(noteName);
    
    if (existingNote) {
      console.log(`✅ Found existing plan: ${existingNote.uuid}`);
      console.log('   Deleting old version...');
      await deleteNote(existingNote.uuid);
      console.log('   Creating fresh board...');
    } else {
      console.log('📝 Creating new Kanban board...');
    }
    
    const note = await createNote(noteName, ['daily-plan', 'kanban', 'planning']);
    console.log(`✅ Created: ${note.uuid}`);
    console.log(`   URL: https://www.amplenote.com/notes/${note.uuid}\n`);
    
    // Add header
    await addContent(note.uuid, `# 📋 Daily Action Plan - ${today}`);
    await addContent(note.uuid, `**Generated:** ${new Date(plan.generated).toLocaleString()}`);
    await addContent(note.uuid, `**Total Items:** ${plan.stats.total}`);
    await addContent(note.uuid, '');
    await addContent(note.uuid, '## 📖 How to Use This Plan');
    await addContent(note.uuid, '');
    await addContent(note.uuid, '1. **Start with DO NOW** - These need action today (check emails, complete tasks, attend events)');
    await addContent(note.uuid, '2. **Schedule DO SOON** - Block calendar time for these this week');
    await addContent(note.uuid, '3. **Monitor items** - Keep aware, waiting on others or no action needed yet');
    await addContent(note.uuid, '4. **Check REFERENCE** - Click links to view account numbers, confirmations, credentials');
    await addContent(note.uuid, '5. **Review CONTEXT** - See recent document activity and email summary');
    await addContent(note.uuid, '');
    await addContent(note.uuid, '✅ **Check off tasks as you complete them**');
    await addContent(note.uuid, '🔄 **Run `python daily_planner.py` tomorrow to refresh**');
    await addContent(note.uuid, '');
    await addContent(note.uuid, '---');
    await addContent(note.uuid, '');
    
    // Add DO NOW section
    await addContent(note.uuid, '## 🎯 DO NOW');
    await addContent(note.uuid, `**${plan.stats.do_now} items** - Start here. These are your top priorities.`);
    await addContent(note.uuid, '');
    
    if (plan.do_now && plan.do_now.length > 0) {
      console.log(`🎯 Adding ${plan.do_now.length} items to DO NOW...`);
      for (const item of plan.do_now) {
        const dueInfo = item.due ? ` | Due: ${item.due}` : '';
        const timeInfo = item.time ? ` at ${item.time}` : '';
        const priorityIcon = item.priority === 'high' ? '⚡' : '📌';
        
        let taskText = `${priorityIcon} **${item.title}**${dueInfo}${timeInfo}\n   *Source: ${item.source}*`;
        
        // Add actionable context based on source
        if (item.body) {
          const preview = item.body.substring(0, 200).replace(/\n/g, ' ').trim();
          taskText += `\n   📧 **Action:** ${preview}...`;
        } else if (item.source === 'File Organization') {
          if (item.title.includes('Inbox')) {
            taskText += `\n   📁 **Action:** Review files in G:\\My Drive\\01_Operate\\Inbox and move to proper PARA locations`;
          } else if (item.title.includes('downloads')) {
            taskText += `\n   💾 **Action:** Review Downloads folder and file/delete recent items`;
          }
        } else if (item.source === 'Google Calendar') {
          taskText += `\n   📅 **Action:** Attend this event or update calendar if plans changed`;
        } else if (item.source === 'Todoist') {
          taskText += `\n   ✅ **Action:** Complete this task or update due date if needed`;
        }
        
        await addTask(note.uuid, taskText, item.due, true);
        console.log(`   ✅ ${item.title.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    } else {
      await addContent(note.uuid, 'No urgent items for today! 🎉');
    }
    
    await addContent(note.uuid, '');
    await addContent(note.uuid, '---');
    await addContent(note.uuid, '');
    
    // Add DO SOON section
    await addContent(note.uuid, '## ⏰ DO SOON');
    await addContent(note.uuid, `**${plan.stats.do_soon} items** - Schedule time for these this week.`);
    await addContent(note.uuid, '');
    
    if (plan.do_soon && plan.do_soon.length > 0) {
      console.log(`\n⏰ Adding ${plan.do_soon.length} items to DO SOON...`);
      for (const item of plan.do_soon) {
        const dueInfo = item.due ? ` | Due: ${item.due}` : '';
        const timeInfo = item.time ? ` at ${item.time}` : '';
        
        let taskText = `📅 **${item.title}**${dueInfo}${timeInfo}\n   *Source: ${item.source}*`;
        
        // Add email body preview for actionable context
        if (item.body) {
          const preview = item.body.substring(0, 200).replace(/\n/g, ' ').trim();
          taskText += `\n   📧 **Action needed:** ${preview}...`;
        }
        
        await addTask(note.uuid, taskText, item.due, false);
        console.log(`   ✅ ${item.title.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    } else {
      await addContent(note.uuid, 'Clear week ahead!');
    }
    
    await addContent(note.uuid, '');
    await addContent(note.uuid, '---');
    await addContent(note.uuid, '');
    
    // Add MONITOR section
    if (plan.stats.monitor > 0) {
      await addContent(note.uuid, '## 👀 MONITOR');
      await addContent(note.uuid, `**${plan.stats.monitor} items** - Keep aware but no action needed yet.`);
      await addContent(note.uuid, '');
      
      console.log(`\n� Adding ${plan.monitor.length} items to MONITOR...`);
      for (const item of plan.monitor.slice(0, 10)) {
        const dueInfo = item.due ? ` | Due: ${item.due}` : '';
        const taskText = `ℹ️ **${item.title}**${dueInfo}\n   *Source: ${item.source}*`;
        await addTask(note.uuid, taskText, item.due, false);
        console.log(`   ✅ ${item.title.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 200));
      }
      
      if (plan.monitor.length > 10) {
        await addContent(note.uuid, '');
        await addContent(note.uuid, `... and ${plan.monitor.length - 10} more items to monitor`);
      }
      
      await addContent(note.uuid, '');
      await addContent(note.uuid, '---');
      await addContent(note.uuid, '');
    }
    
    // Add Reference Emails section
    if (plan.reference_emails && plan.reference_emails.length > 0) {
      await addContent(note.uuid, '## 📌 REFERENCE');
      await addContent(note.uuid, `**${plan.reference_emails.length} items** - Click links for account numbers, confirmations, etc.`);
      await addContent(note.uuid, '');
      
      console.log(`\n📌 Creating reference notes for ${plan.reference_emails.length} emails...`);
      
      for (const ref of plan.reference_emails) {
        // Create individual reference note for each email
        const refNoteName = `📧 ${ref.subject} - ${ref.date}`;
        const refNote = await createNote(refNoteName, ['email', 'reference']);
        
        // Add email details to reference note
        await addContent(refNote.uuid, `**From:** ${ref.from}`);
        await addContent(refNote.uuid, `**Date:** ${ref.date}`);
        await addContent(refNote.uuid, `**Subject:** ${ref.subject}`);
        await addContent(refNote.uuid, '');
        await addContent(refNote.uuid, '**Content:**');
        await addContent(refNote.uuid, ref.body);
        
        // Link to reference note in daily plan with context
        await addContent(note.uuid, `- 📄 [${ref.subject}](https://www.amplenote.com/notes/${refNote.uuid})`);
        await addContent(note.uuid, `  *From: ${ref.from}*`);
        
        console.log(`   ✅ Created: ${ref.subject.substring(0, 50)}...`);
        await new Promise(resolve => setTimeout(resolve, 300));
      }
      
      await addContent(note.uuid, '');
      await addContent(note.uuid, '---');
      await addContent(note.uuid, '');
    }
    
    // Add Documents section
    if (plan.documents && (plan.documents.google_drive.length > 0 || plan.documents.sharepoint.length > 0)) {
      await addContent(note.uuid, '## 📊 CONTEXT');
      await addContent(note.uuid, '**Recent Document Activity & Email Summary** - Background information on recent documents and email activity.');
      await addContent(note.uuid, '');
      
      if (plan.documents.google_drive.length > 0) {
        await addContent(note.uuid, '**Google Drive:**');
        for (const doc of plan.documents.google_drive.slice(0, 5)) {
          await addContent(note.uuid, `- 📄 ${doc.name} (${doc.type}) - Modified ${doc.modified}`);
        }
        await addContent(note.uuid, '');
      }
      
      if (plan.documents.sharepoint.length > 0) {
        await addContent(note.uuid, '**SharePoint:**');
        for (const doc of plan.documents.sharepoint.slice(0, 5)) {
          await addContent(note.uuid, `- 📄 ${doc.name} (${doc.type}) - Modified ${doc.modified}`);
        }
        await addContent(note.uuid, '');
      }
      
      if (plan.email_summary) {
        await addContent(note.uuid, '**Email Summary:**');
        await addContent(note.uuid, `- Gmail: ${plan.email_summary.gmail_count} actionable items`);
        await addContent(note.uuid, `- Outlook: ${plan.email_summary.outlook_count} actionable items`);
        await addContent(note.uuid, `- Reference emails: ${plan.email_summary.reference_count} saved`);
      }
      
      await addContent(note.uuid, '');
      await addContent(note.uuid, '---');
      await addContent(note.uuid, '');
    }
    
    // Add instructions
    await addContent(note.uuid, '## 📝 How to Use This Action Plan');
    await addContent(note.uuid, '');
    await addContent(note.uuid, '**🎯 DO NOW** - Start here. These are your top priorities.');
    await addContent(note.uuid, '**⏰ DO SOON** - Schedule time for these this week.');
    await addContent(note.uuid, '**👀 MONITOR** - Keep aware but no action needed yet.');
    await addContent(note.uuid, '**📌 REFERENCE** - Click links for account numbers, confirmations, etc.');
    await addContent(note.uuid, '**📊 CONTEXT** - Background info on documents and email activity.');
    await addContent(note.uuid, '');
    await addContent(note.uuid, '✅ Check off tasks as you complete them');
    await addContent(note.uuid, '🔄 Run `python daily_planner.py` tomorrow to refresh');
    
    console.log('\n╔════════════════════════════════════════════════════════════╗');
    console.log('║       ✅ Kanban Board Created!                             ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');
    
    console.log('📝 Daily Plan Note:');
    console.log(`   ${noteName}`);
    console.log(`   https://www.amplenote.com/notes/${note.uuid}\n`);
    
    console.log('📊 Summary:');
    console.log(`   🎯 DO NOW: ${plan.stats.do_now} items`);
    console.log(`   ⏰ DO SOON: ${plan.stats.do_soon} items`);
    console.log(`   � MONITOR: ${plan.stats.monitor} items`);
    if (plan.reference_emails && plan.reference_emails.length > 0) {
      console.log(`   📌 REFERENCE: ${plan.reference_emails.length} notes created`);
    }
    console.log('');
    
    console.log('🎯 Next Steps:');
    console.log('   1. Open the note in Amplenote');
    console.log('   2. Check off tasks as you complete them');
    console.log('   3. Run daily_planner.py tomorrow to refresh\n');
    
    return note;
    
  } catch (error) {
    console.error('\n❌ Sync failed:', error.message);
    throw error;
  }
}

// Run sync
syncToKanban().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
