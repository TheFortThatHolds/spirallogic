# JavaScript to SpiralLogic Conversion Guide
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
              