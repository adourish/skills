// Refresh Amplenote Access Token
const https = require('https');
const fs = require('fs');
const path = require('path');

const ENVIRONMENTS_PATH = path.join('G:', 'My Drive', '03_Areas', 'Keys', 'Environments', 'environments.json');

console.log('🔄 Refreshing Amplenote access token...\n');

// Load current config
const envConfig = JSON.parse(fs.readFileSync(ENVIRONMENTS_PATH, 'utf8'));
const amplenoteConfig = envConfig.environments.amplenote;

const refreshToken = amplenoteConfig.credentials.refreshToken;
const clientId = amplenoteConfig.oauth.clientId;

// Prepare refresh request
const postData = JSON.stringify({
  grant_type: 'refresh_token',
  refresh_token: refreshToken,
  client_id: clientId
});

const options = {
  hostname: 'api.amplenote.com',
  port: 443,
  path: '/oauth/token',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = https.request(options, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    if (res.statusCode === 200) {
      const tokenResponse = JSON.parse(data);
      
      // Update config with new tokens
      envConfig.environments.amplenote.credentials.accessToken = tokenResponse.access_token;
      if (tokenResponse.refresh_token) {
        envConfig.environments.amplenote.credentials.refreshToken = tokenResponse.refresh_token;
      }
      
      // Save updated config
      fs.writeFileSync(ENVIRONMENTS_PATH, JSON.stringify(envConfig, null, 2));
      
      console.log('✅ Amplenote token refreshed successfully!');
      console.log(`   New access token: ${tokenResponse.access_token.substring(0, 20)}...`);
      console.log(`   Expires in: ${tokenResponse.expires_in} seconds (${tokenResponse.expires_in / 3600} hours)\n`);
      console.log('You can now run sync_plan_to_amplenote.js');
    } else {
      console.error(`❌ Token refresh failed: ${res.statusCode}`);
      console.error(data);
    }
  });
});

req.on('error', (error) => {
  console.error('❌ Error refreshing token:', error);
});

req.write(postData);
req.end();
