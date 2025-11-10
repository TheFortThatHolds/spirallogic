              consent_verified: true,
              consent_token: this.consentToken
            });
          }
        } else {
          console.error('Failed to add item to cart');
        }
        
      } catch (error) {
        console.error('Cart operation failed:', error);
      }
    }
  }
}
</script>

} complete {
  vue_shopping_cart_functionality_complete()
}
```

---

## Library-Specific JavaScript Conversions

### Axios HTTP Library

**Before:**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 5000
});

// Get user data
const userData = await api.get('/user/profile');

// Update user profile
await api.put('/user/profile', {
  name: 'John Doe',
  email: 'john@example.com'
});
```

**After:**
```spirallogic
ritual.api_client_setup {
  intent: "Configure HTTP client for external API communication",
  consent: user.permits("external_api_configuration"),
  zone: 2,  // Casual - API setup
  external_service: "api.example.com",
  language: javascript
} execute {
  
  import axios from 'axios';
  
  const api = axios.create({
    baseURL: 'https://api.example.com',
    timeout: 5000,
    headers: {
      'User-Agent': 'SpiralLogic-Client/1.0',
      'X-Consent-Aware': 'true'
    }
  });
  
  // Add consent interceptor
  api.interceptors.request.use(config => {
    config.headers['X-Consent-Token'] = getCurrentConsentToken();
    return config;
  });
  
} complete {
  api_client_configured_with_consent()
}

ritual.user_profile_retrieval {
  intent: "Fetch user profile data from external API",
  consent: user.permits("external_profile_data_access"),
  zone: 3,  // Trusted - personal profile data
  data_types: ["user_profile_information"],
  external_service: "api.example.com",
  language: javascript
} execute {
  
  const userData = await api.get('/user/profile', {
    headers: {
      'X-Data-Purpose': 'display_user_dashboard',
      'X-Consent-Verified': 'true'
    }
  });
  
  console.log('User profile loaded with consent verification');
  
} complete {
  audit_external_api_call("user_profile", consent_verified=true)
}

ritual.profile_update_operation {
  intent: "Update user profile information via external API",
  consent: user.permits("profile_modification"),
  zone: 3,  // Trusted - modifying personal data
  data_types: ["user_profile_updates"],
  reversible: true,
  language: javascript
} execute {
  
  await api.put('/user/profile', {
    name: 'John Doe',
    email: 'john@example.com',
    consent_granted: true,
    last_modified: new Date().toISOString()
  }, {
    headers: {
      'X-Operation-Type': 'profile_update',
      'X-Consent-Token': getValidConsentToken()
    }
  });
  
} complete {
  audit_profile_modification("external_api", consent_verified=true)
}
```

### Lodash Utility Library

**Before:**
```javascript
import _ from 'lodash';

const users = [
  { id: 1, name: 'John', age: 30, email: 'john@example.com' },
  { id: 2, name: 'Jane', age: 25, email: 'jane@example.com' }
];

// Group users by age
const usersByAge = _.groupBy(users, 'age');

// Filter users
const adults = _.filter(users, user => user.age >= 18);

// Extract emails
const emails = _.map(users, 'email');
```

**After:**
```spirallogic
ritual.user_data_processing {
  intent: "Process user data collection for analysis and grouping",
  consent: user.permits("user_data_analysis"),
  zone: 3,  // Trusted - processing personal user data
  data_types: ["user_demographics", "email_addresses"],
  purpose: "data_analysis_and_reporting",
  language: javascript
} execute {
  
  import _ from 'lodash';
  
  const users = [
    { id: 1, name: 'John', age: 30, email: 'john@example.com' },
    { id: 2, name: 'Jane', age: 25, email: 'jane@example.com' }
  ];
  
  // Verify we have consent to process this user data
  if (!verifyDataProcessingConsent(users)) {
    throw new ConsentViolationError('User data processing requires consent');
  }
  
} complete {
  user_data_loaded_with_consent(users.length)
}

ritual.demographic_analysis {
  intent: "Group users by demographic characteristics for analysis",
  consent: user.permits("demographic_analysis"),
  zone: 3,  // Trusted - analyzing personal demographics
  data_types: ["age_demographics"],
  analysis_type: "grouping_by_age",
  language: javascript
} execute {
  
  // Group users by age with consent logging
  const usersByAge = _.groupBy(users, 'age');
  
  console.log(`Grouped ${users.length} users by age with consent`);
  console.log('Age groups:', Object.keys(usersByAge));
  
} complete {
  audit_demographic_analysis("age_grouping", groups=Object.keys(usersByAge).length)
}

ritual.user_filtering {
  intent: "Filter user records based on age criteria",
  consent: user.permits("user_record_filtering"),
  zone: 3,  // Trusted - filtering personal data
  filter_criteria: "age_based",
  purpose: "adult_user_identification",
  language: javascript
} execute {
  
  // Filter users with audit trail
  const adults = _.filter(users, user => {
    const isAdult = user.age >= 18;
    if (isAdult) {
      logUserIncludedInFilter(user.id, 'adult_filter');
    }
    return isAdult;
  });
  
  console.log(`Filtered to ${adults.length} adult users with consent`);
  
} complete {
  audit_user_filtering("age_filter", adults_found=adults.length)
}

ritual.email_extraction {
  intent: "Extract email addresses from user records for communication",
  consent: user.permits("email_address_extraction"),
  zone: 4,  // Sacred - extracting contact information
  data_types: ["email_addresses"],
  purpose: "communication_list_creation",
  language: javascript
} execute {
  
  // Extract emails with explicit consent for each
  const emails = _.map(users, user => {
    logEmailExtraction(user.id, 'communication_list');
    return user.email;
  });
  
  console.log(`Extracted ${emails.length} email addresses with user consent`);
  
  // Add consent metadata to extracted data
  const emailsWithConsent = emails.map(email => ({
    email,
    consent_granted: true,
    extracted_at: new Date().toISOString(),
    purpose: 'communication_list_creation'
  }));
  
} complete {
  audit_email_extraction("communication_list", emails_extracted=emails.length)
}
```

### Chart.js Visualization Library

**Before:**
```javascript
import Chart from 'chart.js/auto';

const ctx = document.getElementById('salesChart').getContext('2d');

const salesData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
  datasets: [{
    label: 'Sales Revenue',
    data: [12000, 19000, 15000, 25000, 22000],
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
    borderColor: 'rgba(54, 162, 235, 1)'
  }]
};

new Chart(ctx, {
  type: 'line',
  data: salesData,
  options: {
    responsive: true
  }
});
```

**After:**
```spirallogic
ritual.chart_visualization_setup {
  intent: "Create data visualization chart for business analytics display",
  consent: user.permits("business_data_visualization"),
  zone: 2,  // Casual - business analytics display
  data_types: ["sales_metrics", "revenue_data"],
  purpose: "business_intelligence_dashboard",
  language: javascript
} execute {
  
  import Chart from 'chart.js/auto';
  
  const ctx = document.getElementById('salesChart').getContext('2d');
  
} complete {
  chart_canvas_initialized()
}

ritual.sales_data_visualization {
  intent: "Display sales revenue data in chart format for analysis",
  consent: user.permits("sales_data_display"),
  zone: 3,  // Trusted - business financial data
  data_types: ["sales_revenue", "monthly_metrics"],
  purpose: "executive_dashboard",
  language: javascript
} execute {
  
  const salesData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Sales Revenue (Consent Verified)',
      data: [12000, 19000, 15000, 25000, 22000],
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      // Add consent metadata to chart
      metadata: {
        consent_granted: true,
        data_source: 'internal_sales_system',
        last_updated: new Date().toISOString()
      }
    }]
  };
  
  const chart = new Chart(ctx, {
    type: 'line',
    data: salesData,
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Sales Revenue - Data Accessed with Consent'
        },
        subtitle: {
          display: true,
          text: 'All data visualization complies with consent protocols'
        }
      },
      // Add consent information to tooltip
      interaction: {
        intersect: false,
        callbacks: {
          afterTitle: function() {
            return 'Data consent: Verified ✓';
          }
        }
      }
    }
  });
  
  // Log chart creation
  console.log('Sales chart created with consent-verified data');
  
} complete {
  audit_data_visualization("sales_chart", data_points=salesData.datasets[0].data.length)
}
```

---

## Node.js Package Conversions

### Express Middleware

**Before:**
```javascript
const express = require('express');
const session = require('express-session');
const rateLimit = require('express-rate-limit');

const app = express();

// Session middleware
app.use(session({
  secret: 'session-secret',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false, maxAge: 24 * 60 * 60 * 1000 }
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);
```

**After:**
```spirallogic
ritual.session_middleware_setup {
  intent: "Configure user session management with secure cookie handling",
  consent: user.permits("session_management"),
  zone: 3,  // Trusted - user session tracking
  data_types: ["session_identifiers", "user_state"],
  purpose: "maintain_user_authentication",
  language: javascript
} execute {
  
  const express = require('express');
  const session = require('express-session');
  
  const app = express();
  
  // Session middleware with consent awareness
  app.use(session({
    secret: process.env.SESSION_SECRET || 'session-secret',
    resave: false,
    saveUninitialized: false, // Don't create session without user consent
    cookie: { 
      secure: process.env.NODE_ENV === 'production',
      maxAge: 24 * 60 * 60 * 1000,
      sameSite: 'strict'
    },
    name: 'consent-session',
    // Add consent check before creating session
    genid: function(req) {
      if (!req.headers['x-consent-session']) {
        return null; // Don't create session without consent
      }
      return require('uuid').v4();
    }
  }));
  
} complete {
  session_middleware_configured_with_consent()
}

ritual.rate_limiting_setup {
  intent: "Implement API rate limiting for service protection",
  consent: user.permits("api_usage_monitoring"),
  zone: 2,  // Casual - API usage tracking
  data_types: ["api_usage_patterns", "ip_addresses"],
  purpose: "service_protection_and_fair_usage",
  language: javascript
} execute {
  
  const rateLimit = require('express-rate-limit');
  
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: {
      error: 'Too many requests',
      consent_note: 'Rate limiting active for service protection'
    },
    // Add consent-aware rate limiting
    keyGenerator: function(req) {
      // Use consent token if available, otherwise IP
      return req.headers['x-consent-token'] || req.ip;
    },
    onLimitReached: function(req, res) {
      console.log(`Rate limit reached for ${req.ip} - consent protocols maintained`);
    }
  });
  
  app.use('/api/', limiter);
  
} complete {
  api_rate_limiting_configured("consent_aware")
}
```

### Database Operations (MongoDB)

**Before:**
```javascript
const mongoose = require('mongoose');

// User schema
const userSchema = new mongoose.Schema({
  email: String,
  profile: {
    name: String,
    age: Number,
    preferences: Object
  },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// Create user
async function createUser(userData) {
  const user = new User(userData);
  return await user.save();
}

// Find users
async function getUsers(filters) {
  return await User.find(filters).lean();
}

// Update user
async function updateUser(userId, updates) {
  return await User.findByIdAndUpdate(userId, updates, { new: true });
}
```

**After:**
```spirallogic
ritual.database_schema_definition {
  intent: "Define user data schema with consent and audit capabilities",
  consent: user.permits("database_schema_creation"),
  zone: 4,  // Sacred - defining personal data structure
  data_types: ["user_personal_information", "profile_data"],
  language: javascript
} execute {
  
  const mongoose = require('mongoose');
  
  // Enhanced user schema with consent tracking
  const userSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    profile: {
      name: String,
      age: Number,
      preferences: Object
    },
    // Consent and audit fields
    consent_granted: {
      data_storage: { type: Boolean, default: false },
      profile_processing: { type: Boolean, default: false },
      analytics: { type: Boolean, default: false },
      granted_at: { type: Date },
      expires_at: { type: Date }
    },
    audit_log: [{
      action: String,
      timestamp: { type: Date, default: Date.now },
      consent_verified: Boolean,
      ip_address: String,
      user_agent: String
    }],
    createdAt: { type: Date, default: Date.now },
    data_retention_until: Date,
    deletion_requested: { type: Boolean, default: false }
  });
  
  // Add consent validation middleware
  userSchema.pre('save', function(next) {
    if (!this.consent_granted.data_storage) {
      return next(new Error('Cannot save user without data storage consent'));
    }
    next();
  });
  
  const User = mongoose.model('User', userSchema);
  
} complete {
  database_schema_defined_with_consent()
}

ritual.user_creation_operation {
  intent: "Create new user record with consent verification",
  consent: user.permits("user_record_creation"),
  zone: 4,  // Sacred - creating personal data records
  data_types: ["new_user_personal_data"],
  purpose: "user_account_creation",
  language: javascript
} execute {
  
  async function createUser(userData, consentData) {
    // Verify consent before creating user
    if (!consentData || !consentData.data_storage) {
      throw new ConsentViolationError('User creation requires data storage consent');
    }
    
    const user = new User({
      ...userData,
      consent_granted: {
        data_storage: true,
        profile_processing: consentData.profile_processing || false,
        analytics: consentData.analytics || false,
        granted_at: new Date(),
        expires_at: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000) // 1 year
      },
      audit_log: [{
        action: 'user_created',
        timestamp: new Date(),
        consent_verified: true,
        ip_address: consentData.ip_address,
        user_agent: consentData.user_agent
      }]
    });
    
    const savedUser = await user.save();
    
    // Log user creation
    console.log(`User created with consent: ${savedUser._id}`);
    
    return savedUser;
  }
  
} complete {
  audit_user_creation("database", consent_required=true)
}

ritual.user_retrieval_operation {
  intent: "Retrieve user records with consent verification",
  consent: user.permits("user_data_retrieval"),
  zone: 4,  // Sacred - accessing personal data records
  data_types: ["stored_user_data"],
  purpose: "user_data_access",
  language: javascript
} execute {
  
  async function getUsers(filters, requesterConsent) {
    // Verify requester has permission to access user data
    if (!verifyDataAccessConsent(requesterConsent)) {
      throw new ConsentViolationError('User data access requires valid consent');
    }
    
    // Only return users who have granted data access consent
    const consentFilter = {
      ...filters,
      'consent_granted.data_storage': true,
      'deletion_requested': { $ne: true }
    };
    
    const users = await User.find(consentFilter)
      .lean()
      .select('-audit_log'); // Don't expose audit logs
    
    // Log data access
    console.log(`Retrieved ${users.length} users with consent verification`);
    
    // Add access metadata
    return users.map(user => ({
      ...user,
      data_accessed_with_consent: true,
      access_logged: true
    }));
  }
  
} complete {
  audit_user_retrieval("database", consent_verified=true)
}

ritual.user_update_operation {
  intent: "Update user record with consent verification",
  consent: user.permits("user_data_modification"),
  zone: 4,  // Sacred - modifying personal data
  data_types: ["user_profile_updates"],
  reversible: true,
  language: javascript
} execute {
  
  async function updateUser(userId, updates, updateConsent) {
    // Verify update consent
    if (!verifyUpdateConsent(updateConsent, updates)) {
      throw new ConsentViolationError('User data updates require specific consent');
    }
    
    // Add audit trail to updates
    const auditEntry = {
      action: 'user_updated',
      timestamp: new Date(),
      consent_verified: true,
      fields_updated: Object.keys(updates),
      ip_address: updateConsent.ip_address
    };
    
    const updatedUser = await User.findByIdAndUpdate(
      userId,
      {
        ...updates,
        $push: { audit_log: auditEntry }
      },
      { 
        new: true,
        runValidators: true // Ensure consent validation runs
      }
    );
    
    if (!updatedUser) {
      throw new Error('User not found or consent expired');
    }
    
    console.log(`User ${userId} updated with consent verification`);
    
    return updatedUser;
  }
  
} complete {
  audit_user_modification("database", consent_verified=true)
}
```

---

## JavaScript Ecosystem Compatibility

### NPM Package Installation
```spirallogic
ritual.package_installation {
  intent: "Install JavaScript packages for application development",
  consent: user.permits("development_dependency_installation"),
  zone: 2,  // Casual - development tools
  packages: ["express", "react", "lodash", "axios"],
  language: javascript
} execute {
  
  // Standard NPM install - no changes needed
  // npm install express react lodash axios
  
  // All packages work exactly the same
  import express from 'express';  // ← Same Express
  import React from 'react';      // ← Same React
  import _ from 'lodash';          // ← Same Lodash
  import axios from 'axios';      // ← Same Axios
  
} complete {
  packages_installed_for_consent_native_development()
}
```

### Webpack/Build Tool Integration
```spirallogic
ritual.build_configuration {
  intent: "Configure build tools for SpiralLogic JavaScript application",
  consent: user.permits("build_system_configuration"),
  zone: 2,  // Casual - build tooling
  language: javascript
} execute {
  
  // webpack.config.js - works exactly the same
  module.exports = {
    entry: './src/index.js',
    output: {
      path: __dirname + '/dist',
      filename: 'bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          use: 'babel-loader'
        }
      ]
    }
    // SpiralLogic doesn't change build configuration at all
  };
  
} complete {
  build_system_configured()
}
```

### Framework Updates
```spirallogic
// React 18 → React 19 upgrade example
ritual.framework_upgrade {
  intent: "Upgrade React framework version while maintaining consent protocols",
  consent: user.permits("framework_version_upgrade"),
  zone: 2,  // Casual - development maintenance
  language: javascript
} execute {
  
  // Before upgrade: React 18 + SpiralLogic
  ritual.user_interface {
    consent: user.permits("react_ui_rendering"),
    zone: 2,
    language: javascript
  } execute {
    import React from 'react'; // v18
    const Component = () => <div>Hello</div>;
  }
  
  // After upgrade: React 19 + SpiralLogic
  ritual.user_interface {
    consent: user.permits("react_ui_rendering"),
    zone: 2,
    language: javascript
  } execute {
    import React from 'react'; // v19
    const Component = () => <div>Hello</div>; // Same code!
  }
  
  // SpiralLogic consent wrappers work with any React version
  
} complete {
  framework_upgraded_consent_protocols_maintained()
}
```

---

## Automated JavaScript Conversion Tools

### SpiralLogic JS Converter CLI

```javascript
// spiral-js-convert.js
const fs = require('fs');
const babel = require('@babel/core');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;

class JavaScriptSpiralLogicConverter {
  constructor() {
    this.consentOperations = {
      // Zone 1 - Utility
      'console.log': 1,
      'Math.': 1,
      'Date.now': 1,
      
      // Zone 2 - Casual  
      'localStorage.getItem': 2,
      'localStorage.setItem': 2,
      'fetch': 2,
      'axios.get': 2,
      
      // Zone 3 - Trusted
      'document.cookie': 3,
      'navigator.geolocation': 3,
      'FileReader': 3,
      
      // Zone 4 - Sacred
      'indexedDB': 4,
      'crypto.': 4,
      'eval': 4
    };
  }
  
  convertFile(inputPath, outputPath) {
    const code = fs.readFileSync(inputPath, 'utf8');
    const ast = parser.parse(code, {
      sourceType: 'module',
      plugins: ['jsx', 'typescript']
    });
    
    const operations = [];
    
    traverse(ast, {
      CallExpression: (path) => {
        const calleeName = this.getCallExpression(path.node);
        const zone = this.getOperationZone(calleeName);
        
        if (zone > 1) {
          operations.push({
            name: calleeName,
            zone: zone,
            line: path.node.loc.start.line
          });
        }
      }
    });
    
    const spiralLogicCode = this.generateSpiralLogicWrapper(code, operations);
    fs.writeFileSync(outputPath, spiralLogicCode);
    
    console.log(`Converted ${inputPath} → ${outputPath}`);
    console.log(`Found ${operations.length} operations requiring consent`);
  }
  
  generateSpiralLogicWrapper(originalCode, operations) {
    if (operations.length === 0) {
      return `ritual.utility_operation {
  intent: "Execute JavaScript utility functions",
  consent: automatic,
  zone: 1,
  language: javascript
} execute {

${this.indentCode(originalCode)}

} complete {
  javascript_utility_operation_complete()
}`;
    }
    
    const maxZone = Math.max(...operations.map(op => op.zone));
    const operationTypes = [...new Set(operations.map(op => this.classifyOperation(op.name)))];
    
    return `ritual.javascript_application {
  intent: "${this.generateIntent(operations)}",
  consent: user.permits(${JSON.stringify(operationTypes)}),
  zone: ${maxZone},
  data_types: ${JSON.stringify(this.inferDataTypes(operations))},
  language: javascript
} execute {

${this.indentCode(originalCode)}

} complete {
  audit_javascript_execution("${operationTypes.join('_')}", operations_completed=${operations.length})
}`;
  }
  
  classifyOperation(operationName) {
    const classifications = {
      'localStorage': 'local_storage_access',
      'fetch': 'http_requests',
      'axios': 'http_requests', 
      'document.cookie': 'cookie_management',
      'navigator.geolocation': 'location_access',
      'FileReader': 'file_access',
      'indexedDB': 'database_operations',
      'crypto': 'cryptographic_operations'
    };
    
    for (const [key, classification] of Object.entries(classifications)) {
      if (operationName.includes(key)) {
        return classification;
      }
    }
    
    return 'general_operations';
  }
  
  generateIntent(operations) {
    const types = operations.map(op => this.classifyOperation(op.name));
    const uniqueTypes = [...new Set(types)];
    
    if (uniqueTypes.length === 1) {
      return `Execute JavaScript application with ${uniqueTypes[0]}`;
    }
    
    return `Execute JavaScript application with multiple data operations`;
  }
  
  inferDataTypes(operations) {
    const dataTypes = [];
    
    operations.forEach(op => {
      if (op.name.includes('localStorage')) dataTypes.push('local_storage_data');
      if (op.name.includes('fetch') || op.name.includes('axios')) dataTypes.push('http_response_data');
      if (op.name.includes('cookie')) dataTypes.push('browser_cookies');
      if (op.name.includes('geolocation')) dataTypes.push('user_location');
    });
    
    return [...new Set(dataTypes)];
  }
  
  indentCode(code, spaces = 2) {
    return code.split('\n')
      .map(line => line.length > 0 ? ' '.repeat(spaces) + line : line)
      .join('\n');
  }
}

// CLI Usage
const converter = new JavaScriptSpiralLogicConverter();
const [,, inputFile, outputFile] = process.argv;

if (!inputFile || !outputFile) {
  console.log('Usage: node spiral-js-convert.js input.js output-spiral.js');
  process.exit(1);
}

converter.convertFile(inputFile, outputFile);
```

---

## Conclusion

**JavaScript + SpiralLogic = Same Functionality + User Sovereignty**

**Key Benefits:**
- **All JavaScript libraries work unchanged** - React, Vue, Express, Axios, Lodash, etc.
- **NPM ecosystem fully compatible** - install packages normally
- **Framework updates seamless** - React 18→19, Vue 2→3, no SpiralLogic changes needed
- **Build tools unchanged** - Webpack, Vite, Parcel all work the same
- **Node.js compatibility** - Server-side JavaScript works identically

**The Magic:** SpiralLogic wraps around standard JavaScript operations without modifying the language itself. Your `fetch()` calls are still `fetch()` calls - they just ask permission first.

**Scalability:**
- ✅ **New JS features?** Work immediately (async/await, modules, etc.)
- ✅ **New libraries?** Just add consent wrapper  
- ✅ **Framework updates?** No SpiralLogic changes needed
- ✅ **Browser updates?** API changes handled automatically

**The JavaScript ecosystem stays exactly the same - it just gains respect for human sovereignty.** 🌿🌀

Every JavaScript operation becomes consent-native without losing any functionality or compatibility.# JavaScript to SpiralLogic Conversion Guide
*How to Wrap JavaScript Code with Consent-Native Architecture*

---

## Overview

This guide shows how to convert regular JavaScript code into SpiralLogic-wrapped JavaScript that enforces consent protocols, zone-based security, and complete user sovereignty.

**Key Principle:** JavaScript functionality remains identical - Node.js, React, Vue, vanilla JS all work exactly the same. SpiralLogic just adds consent rituals around operations.

---

## Basic JavaScript Conversion Patterns

### API Calls and Fetch

**Before (Regular JavaScript):**
```javascript
// Fetch user data from API
const response = await fetch('/api/users');
const users = await response.json();

// Send analytics data
await fetch('/api/analytics', {
  method: 'POST',
  body: JSON.stringify({ event: 'page_view', page: '/dashboard' })
});
```

**After (SpiralLogic JavaScript):**
```spirallogic
ritual.api_data_retrieval {
  intent: "Fetch user data from internal API for dashboard display",
  consent: user.permits("internal_api_access"),
  zone: 3,  // Trusted - user data
  data_types: ["user_profiles", "dashboard_data"],
  language: javascript
} execute {
  
  const response = await fetch('/api/users');
  const users = await response.json();
  
  // Log data access for audit
  console.log(`Fetched ${users.length} user records`);
  
} complete {
  audit_api_access("/api/users", users_retrieved=users.length)
}

ritual.analytics_transmission {
  intent: "Send user behavior analytics to tracking service",
  consent: user.permits("analytics_data_sharing"),
  zone: 2,  // Casual - usage analytics
  data_types: ["page_view_events"],
  external_service: "internal_analytics",
  user_benefit: "improve_user_experience",
  language: javascript
} execute {
  
  await fetch('/api/analytics', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      event: 'page_view', 
      page: '/dashboard',
      consent_granted: true,
      timestamp: new Date().toISOString()
    })
  });
  
} complete {
  audit_analytics_transmission("page_view", consent_verified=true)
}
```

### Local Storage and Cookies

**Before (Regular JavaScript):**
```javascript
// Store user preferences
localStorage.setItem('theme', 'dark');
localStorage.setItem('language', 'en');

// Set tracking cookie
document.cookie = "user_id=12345; expires=Thu, 18 Dec 2024 12:00:00 UTC";

// Read stored data
const theme = localStorage.getItem('theme');
const userId = getCookie('user_id');
```

**After (SpiralLogic JavaScript):**
```spirallogic
ritual.local_data_storage {
  intent: "Store user interface preferences in browser local storage",
  consent: user.permits("local_preference_storage"),
  zone: 2,  // Casual - basic personalization
  data_types: ["ui_preferences"],
  storage_duration: "until_user_clears",
  deletion_method: "standard_browser_clear",
  language: javascript
} execute {
  
  // Store preferences with user consent
  localStorage.setItem('theme', 'dark');
  localStorage.setItem('language', 'en');
  
  // Add consent metadata
  localStorage.setItem('consent_granted', JSON.stringify({
    preferences: true,
    timestamp: new Date().toISOString(),
    expires: 'user_controlled'
  }));
  
} complete {
  audit_local_storage("user_preferences", items_stored=2)
}

ritual.tracking_cookie_creation {
  intent: "Set user identification cookie for session tracking",
  consent: user.permits("session_tracking_cookies"),
  zone: 3,  // Trusted - user identification
  data_types: ["user_session_id"],
  purpose: "maintain_user_session",
  expires: "24_hours",
  language: javascript
} execute {
  
  // Only set cookie with explicit consent
  if (user.hasGrantedConsent('session_tracking')) {
    document.cookie = "user_id=12345; expires=Thu, 18 Dec 2024 12:00:00 UTC; SameSite=Strict";
    
    // Log cookie creation
    console.log('Session tracking cookie set with user consent');
  } else {
    console.log('Cookie not set - user consent required');
  }
  
} complete {
  audit_cookie_creation("user_session", consent_verified=true)
}

ritual.stored_data_retrieval {
  intent: "Read previously stored user preferences and session data",
  consent: user.permits("stored_data_access"),
  zone: 2,  // Casual - reading own preferences
  language: javascript
} execute {
  
  const theme = localStorage.getItem('theme');
  const userId = getCookie('user_id');
  
  // Verify consent is still valid
  const consentData = JSON.parse(localStorage.getItem('consent_granted') || '{}');
  if (!consentData.preferences) {
    console.warn('Stored preferences accessed without current consent');
  }
  
} complete {
  audit_data_retrieval("local_storage", items_accessed=2)
}
```

### DOM Manipulation and User Interaction

**Before (Regular JavaScript):**
```javascript
// Track user clicks
document.addEventListener('click', (event) => {
  analytics.track('click', {
    element: event.target.tagName,
    position: { x: event.clientX, y: event.clientY }
  });
});

// Collect form data
document.getElementById('contact-form').addEventListener('submit', (event) => {
  const formData = new FormData(event.target);
  const email = formData.get('email');
  const message = formData.get('message');
  
  fetch('/api/contact', {
    method: 'POST',
    body: JSON.stringify({ email, message })
  });
});
```

**After (SpiralLogic JavaScript):**
```spirallogic
ritual.user_interaction_tracking {
  intent: "Track user click patterns for UX improvement analysis",
  consent: user.permits("interaction_analytics"),
  zone: 2,  // Casual - usage analytics
  data_types: ["click_coordinates", "ui_element_interactions"],
  purpose: "improve_user_interface",
  anonymized: true,
  language: javascript
} execute {
  
  document.addEventListener('click', (event) => {
    // Only track if user has consented
    if (user.hasGrantedConsent('interaction_analytics')) {
      analytics.track('click', {
        element: event.target.tagName,
        position: { x: event.clientX, y: event.clientY },
        timestamp: new Date().toISOString(),
        consent_verified: true
      });
    }
  });
  
} complete {
  audit_interaction_tracking("click_events", consent_required=true)
}

ritual.contact_form_processing {
  intent: "Process user contact form submission with personal information",
  consent: user.permits("contact_form_submission"),
  zone: 3,  // Trusted - personal contact information
  data_types: ["email_address", "personal_message"],
  purpose: "respond_to_user_inquiry",
  retention: "until_inquiry_resolved",
  language: javascript
} execute {
  
  document.getElementById('contact-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Request explicit consent for personal data processing
    const contactConsent = await requestUserConsent(
      'contact_data_processing',
      'We need to process your email and message to respond to your inquiry.'
    );
    
    if (!contactConsent) {
      showConsentRequiredMessage();
      return;
    }
    
    const formData = new FormData(event.target);
    const email = formData.get('email');
    const message = formData.get('message');
    
    // Validate and sanitize input
    if (!isValidEmail(email)) {
      showError('Please provide a valid email address');
      return;
    }
    
    await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        email, 
        message,
        consent_granted: true,
        submitted_at: new Date().toISOString()
      })
    });
    
    showSuccessMessage('Your message has been sent!');
  });
  
} complete {
  audit_form_processing("contact_form", personal_data=true, consent_verified=true)
}
```

---

## React Application Conversion

### Before (Regular React)
```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserDashboard() {
  const [users, setUsers] = useState([]);
  const [analytics, setAnalytics] = useState({});
  
  useEffect(() => {
    // Load user data
    axios.get('/api/users').then(response => {
      setUsers(response.data);
    });
    
    // Track page view
    axios.post('/api/analytics', {
      event: 'dashboard_view',
      user_id: getCurrentUserId()
    });
    
    // Load analytics data
    axios.get('/api/analytics/dashboard').then(response => {
      setAnalytics(response.data);
    });
  }, []);
  
  const handleUserDelete = async (userId) => {
    await axios.delete(`/api/users/${userId}`);
    setUsers(users.filter(u => u.id !== userId));
  };
  
  return (
    <div>
      <h1>User Dashboard</h1>
      <div>Total Users: {analytics.totalUsers}</div>
      {users.map(user => (
        <div key={user.id}>
          {user.name} - {user.email}
          <button onClick={() => handleUserDelete(user.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}
```

### After (SpiralLogic React)
```spirallogic
ritual.react_component_initialization {
  intent: "Initialize user dashboard React component with data loading",
  consent: user.permits("dashboard_component_access"),
  zone: 3,  // Trusted - user management dashboard
  data_types: ["user_records", "dashboard_analytics"],
  language: javascript
} execute {
  
  import React, { useState, useEffect } from 'react';
  import axios from 'axios';
  
  function UserDashboard() {
    const [users, setUsers] = useState([]);
    const [analytics, setAnalytics] = useState({});
    const [consentGranted, setConsentGranted] = useState(false);
    
} complete {
  react_component_structure_defined()
}

ritual.dashboard_data_loading {
  intent: "Load user data and analytics for dashboard display",
  consent: user.permits("user_data_dashboard_access"),
  zone: 3,  // Trusted - accessing user records
  data_types: ["all_user_records", "usage_analytics"],
  purpose: "administrative_dashboard",
  language: javascript
} execute {
  
    useEffect(() => {
      const loadDashboardData = async () => {
        // Request consent before loading any data
        const dashboardConsent = await requestConsentModal({
          title: 'Dashboard Data Access',
          message: 'This dashboard needs to access user records and analytics data. Continue?',
          dataTypes: ['user_records', 'dashboard_analytics']
        });
        
        if (!dashboardConsent) {
          setConsentGranted(false);
          return;
        }
        
        setConsentGranted(true);
        
        try {
          // Load user data with consent verification
          const usersResponse = await axios.get('/api/users', {
            headers: { 'X-Consent-Token': dashboardConsent.token }
          });
          setUsers(usersResponse.data);
          
          // Load analytics data
          const analyticsResponse = await axios.get('/api/analytics/dashboard', {
            headers: { 'X-Consent-Token': dashboardConsent.token }
          });
          setAnalytics(analyticsResponse.data);
          
          // Log dashboard access
          console.log(`Dashboard loaded: ${usersResponse.data.length} users`);
          
        } catch (error) {
          console.error('Dashboard loading failed:', error);
          if (error.response?.status === 403) {
            alert('Consent verification failed. Please refresh and try again.');
          }
        }
      };
      
      loadDashboardData();
    }, []);
    
} complete {
  audit_dashboard_loading("user_dashboard", consent_verified=true)
}

ritual.analytics_tracking {
  intent: "Track dashboard page view for usage analytics",
  consent: user.permits("admin_analytics_tracking"),
  zone: 2,  // Casual - internal usage tracking
  data_types: ["page_view_events"],
  purpose: "understand_admin_usage_patterns",
  language: javascript
} execute {
  
    useEffect(() => {
      const trackPageView = async () => {
        if (consentGranted) {
          await axios.post('/api/analytics', {
            event: 'dashboard_view',
            user_id: getCurrentUserId(),
            consent_verified: true,
            timestamp: new Date().toISOString()
          });
        }
      };
      
      trackPageView();
    }, [consentGranted]);
    
} complete {
  audit_analytics_tracking("dashboard_page_view")
}

ritual.user_deletion_operation {
  intent: "Delete user record from system with admin authorization",
  consent: user.permits("user_record_deletion"),
  zone: 4,  // Sacred - permanent data deletion
  data_types: ["user_personal_records"],
  irreversible: true,
  admin_action: true,
  language: javascript
} execute {
  
    const handleUserDelete = async (userId) => {
      // Double-check consent for destructive operation
      const deleteConsent = await requestConsentModal({
        title: 'Confirm User Deletion',
        message: `Are you sure you want to permanently delete user ${userId}? This cannot be undone.`,
        type: 'destructive',
        requireExplicitConfirmation: true
      });
      
      if (!deleteConsent) {
        return;
      }
      
      try {
        await axios.delete(`/api/users/${userId}`, {
          headers: { 
            'X-Consent-Token': deleteConsent.token,
            'X-Confirm-Destructive': 'true'
          }
        });
        
        // Remove from local state only after successful deletion
        setUsers(users.filter(u => u.id !== userId));
        
        // Log destructive action
        console.log(`User ${userId} deleted with admin consent`);
        
      } catch (error) {
        console.error('User deletion failed:', error);
        alert('Failed to delete user. Please try again.');
      }
    };
    
} complete {
  audit_user_deletion(user_id=userId, admin_consent_verified=true)
}

ritual.react_component_render {
  intent: "Render dashboard UI with consent-aware data display",
  consent: automatic,  // Rendering is consequence of earlier consents
  zone: 1,  // Utility - UI rendering
  language: javascript
} execute {
  
    return (
      <div>
        <h1>User Dashboard</h1>
        
        {!consentGranted ? (
          <div className="consent-required">
            <p>Dashboard data access requires your consent.</p>
            <button onClick={() => window.location.reload()}>
              Grant Dashboard Access
            </button>
          </div>
        ) : (
          <>
            <div className="analytics-summary">
              Total Users: {analytics.totalUsers || 'Loading...'}
              <small> (Data accessed with consent)</small>
            </div>
            
            <div className="user-list">
              {users.map(user => (
                <div key={user.id} className="user-card">
                  <span>{user.name} - {user.email}</span>
                  <button 
                    onClick={() => handleUserDelete(user.id)}
                    className="delete-button"
                  >
                    Delete User
                  </button>
                </div>
              ))}
            </div>
            
            <footer className="consent-info">
              <small>All data displayed with proper consent verification</small>
            </footer>
          </>
        )}
      </div>
    );
  }
  
} complete {
  react_component_render_complete("user_dashboard")
}
```

---

## Node.js Server Conversion

### Before (Express Server)
```javascript
const express = require('express');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');

const app = express();

// Database connection
mongoose.connect('mongodb://localhost:27017/myapp');

// User model
const User = mongoose.model('User', {
  email: String,
  password: String,
  profile: Object
});

// Login endpoint
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await User.findOne({ email });
  if (!user || !validatePassword(password, user.password)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = jwt.sign({ userId: user._id }, 'secret');
  res.json({ token, user: user.profile });
});

// Get users endpoint
app.get('/api/users', async (req, res) => {
  const users = await User.find({}).select('email profile');
  res.json(users);
});

app.listen(3000);
```

### After (SpiralLogic Express Server)
```spirallogic
ritual.server_initialization {
  intent: "Initialize Express server with database connection",
  consent: user.permits("server_deployment"),
  zone: 3,  // Trusted - server infrastructure
  external_services: ["mongodb"],
  data_access: ["user_database"],
  language: javascript
} execute {
  
  const express = require('express');
  const mongoose = require('mongoose');
  const jwt = require('jsonwebtoken');
  
  const app = express();
  app.use(express.json());
  
  // Add consent middleware
  app.use('/api', consentVerificationMiddleware);
  
} complete {
  server_infrastructure_initialized()
}

ritual.database_connection {
  intent: "Connect to MongoDB database containing user records",
  consent: user.permits("database_connection"),
  zone: 4,  // Sacred - database with personal data
  database: "mongodb://localhost:27017/myapp",
  data_types: ["user_credentials", "user_profiles"],
  language: javascript
} execute {
  
  mongoose.connect('mongodb://localhost:27017/myapp', {
    // Add connection metadata for audit
    appName: 'SpiralLogic_UserApp',
    maxPoolSize: 10
  });
  
  mongoose.connection.on('connected', () => {
    console.log('Database connected with consent protocols active');
  });
  
  // User model with consent metadata
  const User = mongoose.model('User', {
    email: { type: String, required: true },
    password: { type: String, required: true },
    profile: { type: Object, default: {} },
    consent_granted: { type: Object, default: {} },
    data_created: { type: Date, default: Date.now },
    audit_log: [{ action: String, timestamp: Date, consent_verified: Boolean }]
  });
  
} complete {
  audit_database_connection("mongodb", user_data_access=true)
}

ritual.user_authentication_endpoint {
  intent: "Authenticate user login with credential verification",
  consent: user.permits("authentication_processing"),
  zone: 4,  // Sacred - processing user credentials
  data_types: ["login_credentials"],
  purpose: "user_session_establishment",
  language: javascript
} execute {
  
  app.post('/api/login', async (req, res) => {
    try {
      const { email, password } = req.body;
      
      // Log authentication attempt (without sensitive data)
      console.log(`Authentication attempt for email: ${email.substring(0,3)}***`);
      
      const user = await User.findOne({ email });
      if (!user || !validatePassword(password, user.password)) {
        // Log failed attempt
        auditLog('login_failed', { email_hash: hashEmail(email) });
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      // Update user's audit log
      user.audit_log.push({
        action: 'successful_login',
        timestamp: new Date(),
        consent_verified: true
      });
      await user.save();
      
      const token = jwt.sign(
        { 
          userId: user._id,
          consentGranted: user.consent_granted,
          loginTime: new Date().toISOString()
        }, 
        process.env.JWT_SECRET || 'secret'
      );
      
      // Only return data user has consented to share
      const responseData = {
        token,
        user: user.profile,
        consent_status: user.consent_granted
      };
      
      auditLog('login_successful', { userId: user._id });
      res.json(responseData);
      
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({ error: 'Authentication service unavailable' });
    }
  });
  
} complete {
  audit_authentication_endpoint("user_login", security_protocols=true)
}

ritual.user_data_retrieval_endpoint {
  intent: "Retrieve user records for administrative dashboard",
  consent: user.permits("admin_user_data_access"),
  zone: 4,  // Sacred - exposing all user data
  data_types: ["all_user_profiles", "user_emails"],
  access_restriction: "admin_only",
  language: javascript
} execute {
  
  app.get('/api/users', async (req, res) => {
    try {
      // Verify admin consent token
      const consentToken = req.headers['x-consent-token'];
      if (!consentToken || !verifyAdminConsent(consentToken)) {
        return res.status(403).json({ 
          error: 'Admin consent required for user data access' 
        });
      }
      
      // Log admin data access
      auditLog('admin_user_data_access', { 
        admin_id: req.user?.id,
        consent_token: consentToken,
        timestamp: new Date().toISOString()
      });
      
      const users = await User.find({})
        .select('email profile consent_granted data_created')
        .lean();
      
      // Add consent metadata to response
      const usersWithMeta = users.map(user => ({
        ...user,
        data_accessed_with_consent: true,
        admin_access_logged: true
      }));
      
      res.json({
        users: usersWithMeta,
        total: users.length,
        consent_verified: true,
        access_logged: true
      });
      
    } catch (error) {
      console.error('User retrieval error:', error);
      res.status(500).json({ error: 'User data service unavailable' });
    }
  });
  
} complete {
  audit_user_data_endpoint("admin_user_access", consent_required=true)
}

ritual.server_deployment {
  intent: "Deploy server with consent-aware endpoints",
  consent: user.permits("production_server_deployment"),
  zone: 3,  // Trusted - production deployment
  external_access: true,
  audit_logging: true,
  language: javascript
} execute {
  
  // Consent verification middleware
  function consentVerificationMiddleware(req, res, next) {
    // Add consent checking logic for all API routes
    const path = req.path;
    const method = req.method;
    
    // Log all API access attempts
    console.log(`API Access: ${method} ${path} - Consent protocols active`);
    
    next();
  }
  
  // Global error handler with consent awareness
  app.use((error, req, res, next) => {
    console.error('Server error:', error);
    
    // Never expose user data in error messages
    res.status(500).json({
      error: 'Service temporarily unavailable',
      consent_protocols_maintained: true
    });
  });
  
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} with consent protocols enabled`);
  });
  
} complete {
  audit_server_deployment("consent_aware_server", port=PORT)
}
```

---

## Vue.js Application Conversion

### Before (Vue Component)
```vue
<template>
  <div>
    <h2>Product Catalog</h2>
    <div v-for="product in products" :key="product.id">
      {{ product.name }} - ${{ product.price }}
      <button @click="addToCart(product)">Add to Cart</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      products: []
    }
  },
  
  async created() {
    const response = await fetch('/api/products');
    this.products = await response.json();
    
    // Track page view
    gtag('event', 'page_view', {
      page_title: 'Product Catalog',
      page_location: window.location.href
    });
  },
  
  methods: {
    async addToCart(product) {
      await fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({ productId: product.id, quantity: 1 })
      });
      
      // Track add to cart
      gtag('event', 'add_to_cart', {
        currency: 'USD',
        value: product.price,
        items: [product]
      });
    }
  }
}
</script>
```

### After (SpiralLogic Vue Component)
```spirallogic
ritual.vue_component_definition {
  intent: "Define Vue.js product catalog component with consent-aware data loading",
  consent: user.permits("product_catalog_component"),
  zone: 2,  // Casual - public product information
  data_types: ["product_catalog", "shopping_interactions"],
  language: javascript
} execute {

<template>
  <div>
    <h2>Product Catalog</h2>
    
    <!-- Consent status indicator -->
    <div v-if="!consentGranted" class="consent-notice">
      <p>This catalog uses analytics to improve your experience.</p>
      <button @click="requestConsent">Enable Full Features</button>
    </div>
    
    <div v-for="product in products" :key="product.id" class="product-item">
      {{ product.name }} - ${{ product.price }}
      <button @click="addToCart(product)">Add to Cart</button>
    </div>
    
    <footer v-if="consentGranted" class="consent-info">
      Analytics active with your consent
    </footer>
  </div>
</template>

} complete {
  vue_template_structure_defined()
}

ritual.vue_component_logic {
  intent: "Implement Vue component logic with consent-aware data operations",
  consent: user.permits("vue_component_functionality"),
  zone: 2,  // Casual - product browsing functionality
  language: javascript
} execute {

<script>
export default {
  data() {
    return {
      products: [],
      consentGranted: false,
      consentToken: null
    }
  },
  
} complete {
  vue_component_data_structure_ready()
}

ritual.product_data_loading {
  intent: "Load product catalog data for display to user",
  consent: user.permits("product_catalog_access"),
  zone: 2,  // Casual - public product information
  data_types: ["product_listings"],
  purpose: "display_shopping_catalog",
  language: javascript
} execute {
  
  async created() {
    try {
      // Load products (public data, no consent needed)
      const response = await fetch('/api/products');
      this.products = await response.json();
      
      console.log(`Loaded ${this.products.length} products`);
      
    } catch (error) {
      console.error('Product loading failed:', error);
    }
  },
  
} complete {
  audit_product_loading("catalog_display", products_loaded=this.products.length)
}

ritual.analytics_tracking_setup {
  intent: "Set up user behavior tracking with consent verification",
  consent: user.permits("shopping_analytics"),
  zone: 2,  // Casual - shopping behavior analytics
  data_types: ["page_views", "product_interactions"],
  purpose: "improve_shopping_experience",
  language: javascript
} execute {
  
  methods: {
    async requestConsent() {
      const consent = await this.$consentModal({
        title: 'Shopping Analytics',
        message: 'Enable analytics to help us improve your shopping experience?',
        dataTypes: ['page_views', 'cart_interactions'],
        benefits: ['Personalized recommendations', 'Better user experience']
      });
      
      if (consent.granted) {
        this.consentGranted = true;
        this.consentToken = consent.token;
        
        // Now track the page view with consent
        await this.trackPageView();
      }
    },
    
    async trackPageView() {
      if (this.consentGranted) {
        gtag('event', 'page_view', {
          page_title: 'Product Catalog',
          page_location: window.location.href,
          consent_granted: true,
          consent_token: this.consentToken
        });
        
        console.log('Page view tracked with user consent');
      }
    },
    
} complete {
  analytics_tracking_consent_configured()
}

ritual.shopping_cart_interaction {
  intent: "Handle add to cart action with user behavior tracking",
  consent: user.permits("shopping_cart_operations"),
  zone: 3,  // Trusted - shopping cart with user data
  data_types: ["shopping_cart_contents", "purchase_intent"],
  purpose: "enable_shopping_functionality",
  language: javascript
} execute {
  
    async addToCart(product) {
      try {
        // Add to cart (functional operation)
        const cartResponse = await fetch('/api/cart', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-Consent-Token': this.consentToken || 'no-consent'
          },
          body: JSON.stringify({ 
            productId: product.id, 
            quantity: 1,
            consent_granted: this.consentGranted
          })
        });
        
        if (cartResponse.ok) {
          console.log(`Added ${product.name} to cart`);
          
          // Track add to cart only if consent granted
          if (this.consentGranted) {
            gtag('event', 'add_to_cart', {
              currency: 'USD',
              value: product.price,
              items: [product],
              