import React, { useState, useEffect } from 'react';
import { Plus, Zap, Mail, MessageSquare, Database, Calendar, FileText, Globe, Settings, Play, Pause, Trash2, Eye, Shield } from 'lucide-react';

const IntegrationHub = () => {
  const [currentZone, setCurrentZone] = useState(1);
  const [integrations, setIntegrations] = useState([]);
  const [auditLog, setAuditLog] = useState([]);
  const [connectedApps, setConnectedApps] = useState({});
  
  // Available apps to connect
  const availableApps = {
    email: { name: 'Email', icon: Mail, color: 'bg-blue-500', zone: 3 },
    slack: { name: 'Slack', icon: MessageSquare, color: 'bg-purple-500', zone: 2 },
    database: { name: 'Database', icon: Database, color: 'bg-green-500', zone: 4 },
    calendar: { name: 'Calendar', icon: Calendar, color: 'bg-red-500', zone: 3 },
    docs: { name: 'Documents', icon: FileText, color: 'bg-yellow-500', zone: 3 },
    webhook: { name: 'Webhook', icon: Globe, color: 'bg-gray-500', zone: 2 }
  };

  // SpiralLogic consent system
  const requestConsent = async (operation, zone, description, dataTypes = []) => {
    return new Promise((resolve) => {
      const dataWarning = dataTypes.length > 0 ? `\n\nData types involved: ${dataTypes.join(', ')}` : '';
      const consent = window.confirm(
        `Zone ${zone} Integration Request:\n\n${description}${dataWarning}\n\nThis will create a permanent connection between your apps.\n\nDo you give consent?`
      );
      
      logOperation(operation, zone, description, consent, dataTypes);
      resolve(consent);
    });
  };

  const logOperation = (operation, zone, description, consent, dataTypes = []) => {
    const logEntry = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      operation,
      zone,
      description,
      consent,
      dataTypes,
      user: 'current_user'
    };
    setAuditLog(prev => [logEntry, ...prev]);
  };

  const enterZone = async (zone) => {
    if (zone > currentZone) {
      const zoneNames = { 1: 'Utility', 2: 'Casual', 3: 'Trusted', 4: 'Sacred' };
      const consent = await requestConsent(
        `enter_zone_${zone}`,
        zone,
        `Enter Zone ${zone} (${zoneNames[zone]}) to access higher-level integrations`
      );
      if (consent) {
        setCurrentZone(zone);
      }
    } else {
      setCurrentZone(zone);
      logOperation(`zone_change`, zone, `Moved to Zone ${zone}`, 'automatic');
    }
  };

  const connectApp = async (appKey) => {
    const app = availableApps[appKey];
    if (currentZone < app.zone) {
      alert(`Need Zone ${app.zone} access for ${app.name}. Current zone: ${currentZone}`);
      return;
    }

    const dataTypes = getDataTypes(appKey);
    const consent = await requestConsent(
      `connect_${appKey}`,
      app.zone,
      `Connect to ${app.name} - this will allow reading and writing data`,
      dataTypes
    );

    if (consent) {
      setConnectedApps(prev => ({
        ...prev,
        [appKey]: {
          connected: true,
          connectedAt: new Date().toISOString(),
          permissions: dataTypes
        }
      }));
    }
  };

  const createIntegration = async (sourceApp, targetApp, triggerType) => {
    const maxZone = Math.max(availableApps[sourceApp].zone, availableApps[targetApp].zone);
    if (currentZone < maxZone) {
      alert(`Need Zone ${maxZone} access for this integration`);
      return;
    }

    const dataFlow = getDataFlow(sourceApp, targetApp, triggerType);
    const consent = await requestConsent(
      `create_integration`,
      maxZone,
      `Create integration: ${availableApps[sourceApp].name} → ${availableApps[targetApp].name}`,
      dataFlow.dataTypes
    );

    if (consent) {
      const integration = {
        id: Date.now(),
        source: sourceApp,
        target: targetApp,
        trigger: triggerType,
        dataFlow,
        active: true,
        createdAt: new Date().toISOString(),
        executions: 0
      };
      setIntegrations(prev => [...prev, integration]);
    }
  };

  const getDataTypes = (appKey) => {
    const dataMap = {
      email: ['email addresses', 'message content', 'attachments'],
      slack: ['messages', 'user names', 'channel data'],
      database: ['user records', 'application data', 'query results'],
      calendar: ['events', 'attendees', 'scheduling data'],
      docs: ['document content', 'file metadata', 'edit history'],
      webhook: ['HTTP requests', 'payload data', 'response data']
    };
    return dataMap[appKey] || [];
  };

  const getDataFlow = (source, target, trigger) => {
    return {
      trigger,
      dataTypes: [...getDataTypes(source), ...getDataTypes(target)],
      flow: `When ${trigger} in ${availableApps[source].name}, then update ${availableApps[target].name}`
    };
  };

  const toggleIntegration = async (integrationId, active) => {
    const integration = integrations.find(i => i.id === integrationId);
    const action = active ? 'activate' : 'pause';
    const consent = await requestConsent(
      `${action}_integration`,
      3,
      `${active ? 'Activate' : 'Pause'} integration: ${availableApps[integration.source].name} → ${availableApps[integration.target].name}`
    );

    if (consent) {
      setIntegrations(prev => prev.map(i => 
        i.id === integrationId ? { ...i, active } : i
      ));
    }
  };

  const deleteIntegration = async (integrationId) => {
    const integration = integrations.find(i => i.id === integrationId);
    const consent = await requestConsent(
      'delete_integration',
      4,
      `Permanently delete integration: ${availableApps[integration.source].name} → ${availableApps[integration.target].name}\n\nThis cannot be undone.`
    );

    if (consent) {
      setIntegrations(prev => prev.filter(i => i.id !== integrationId));
    }
  };

  const simulateExecution = async (integrationId) => {
    const integration = integrations.find(i => i.id === integrationId);
    if (!integration.active) {
      alert('Integration is paused');
      return;
    }

    const consent = await requestConsent(
      'execute_integration',
      Math.max(availableApps[integration.source].zone, availableApps[integration.target].zone),
      `Execute integration: ${integration.dataFlow.flow}`,
      integration.dataFlow.dataTypes
    );

    if (consent) {
      setIntegrations(prev => prev.map(i => 
        i.id === integrationId ? { ...i, executions: i.executions + 1 } : i
      ));
      alert(`Integration executed successfully!\n${integration.dataFlow.flow}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">App Integration Hub</h1>
              <p className="text-gray-600">Connect your apps with consent-native security</p>
            </div>
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-green-500" />
              <span className="text-sm text-gray-600">Zone {currentZone} Active</span>
            </div>
          </div>
        </div>

        {/* Zone Selector */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">Access Zones</h2>
          <div className="grid grid-cols-4 gap-4">
            {[
              { zone: 1, name: 'Utility', desc: 'Basic operations', color: 'bg-gray-500' },
              { zone: 2, name: 'Casual', desc: 'Light integrations', color: 'bg-blue-500' },
              { zone: 3, name: 'Trusted', desc: 'Personal data', color: 'bg-green-500' },
              { zone: 4, name: 'Sacred', desc: 'Sensitive systems', color: 'bg-purple-500' }
            ].map(({ zone, name, desc, color }) => (
              <button
                key={zone}
                onClick={() => enterZone(zone)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  zone === currentZone 
                    ? `${color} text-white border-transparent` 
                    : zone <= currentZone + 1
                      ? 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'
                      : 'bg-gray-50 text-gray-400 border-gray-200 cursor-not-allowed'
                }`}
              >
                <div className="text-sm font-semibold">Zone {zone}</div>
                <div className="text-xs">{name}</div>
                <div className="text-xs opacity-75">{desc}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          
          {/* Available Apps */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">Connect Apps</h2>
            <div className="space-y-3">
              {Object.entries(availableApps).map(([key, app]) => {
                const Icon = app.icon;
                const isConnected = connectedApps[key]?.connected;
                const canConnect = currentZone >= app.zone;
                
                return (
                  <div key={key} className={`p-3 border rounded-lg ${isConnected ? 'border-green-300 bg-green-50' : 'border-gray-200'}`}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded ${app.color} text-white`}>
                          <Icon className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="font-medium">{app.name}</div>
                          <div className="text-xs text-gray-500">Zone {app.zone} required</div>
                        </div>
                      </div>
                      {isConnected ? (
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">Connected</span>
                      ) : (
                        <button
                          onClick={() => connectApp(key)}
                          disabled={!canConnect}
                          className={`text-xs px-3 py-1 rounded ${
                            canConnect 
                              ? 'bg-blue-500 text-white hover:bg-blue-600' 
                              : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                          }`}
                        >
                          Connect
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Create Integration */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">Create Integration</h2>
            
            {Object.keys(connectedApps).length < 2 ? (
              <div className="text-center text-gray-500 py-8">
                <Plus className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Connect at least 2 apps to create integrations</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="space-y-3">
                  {[
                    { source: 'email', target: 'slack', trigger: 'new email received', desc: 'Forward important emails to Slack' },
                    { source: 'calendar', target: 'email', trigger: 'meeting starts', desc: 'Send meeting reminders via email' },
                    { source: 'webhook', target: 'database', trigger: 'data received', desc: 'Store webhook data in database' },
                    { source: 'docs', target: 'slack', trigger: 'document updated', desc: 'Notify team of document changes' }
                  ].map((template, idx) => (
                    <div key={idx} className="border rounded p-3 hover:bg-gray-50">
                      <div className="text-sm font-medium mb-1">{template.desc}</div>
                      <div className="text-xs text-gray-500 mb-2">
                        {availableApps[template.source]?.name} → {availableApps[template.target]?.name}
                      </div>
                      <button
                        onClick={() => createIntegration(template.source, template.target, template.trigger)}
                        disabled={!connectedApps[template.source] || !connectedApps[template.target]}
                        className="text-xs bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 disabled:bg-gray-300"
                      >
                        Create Integration
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Audit Log */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">Consent Audit Log</h2>
            <div className="max-h-96 overflow-y-auto space-y-2">
              {auditLog.slice(0, 10).map(entry => (
                <div key={entry.id} className={`p-3 rounded border-l-4 text-xs ${
                  entry.consent === 'automatic' ? 'border-gray-400 bg-gray-50' :
                  entry.consent ? 'border-green-400 bg-green-50' : 'border-red-400 bg-red-50'
                }`}>
                  <div className="font-medium">{entry.operation}</div>
                  <div className="text-gray-600 mt-1">{entry.description}</div>
                  {entry.dataTypes.length > 0 && (
                    <div className="text-gray-500 mt-1">Data: {entry.dataTypes.join(', ')}</div>
                  )}
                  <div className="flex justify-between items-center mt-2">
                    <span className={`px-2 py-1 rounded ${
                      entry.consent === 'automatic' ? 'bg-gray-200 text-gray-700' :
                      entry.consent ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
                    }`}>
                      {entry.consent === 'automatic' ? 'Auto' : entry.consent ? 'Granted' : 'Denied'}
                    </span>
                    <span className="text-gray-400">Zone {entry.zone}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Active Integrations */}
        {integrations.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mt-6">
            <h2 className="text-lg font-semibold mb-4">Active Integrations</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {integrations.map(integration => {
                const SourceIcon = availableApps[integration.source].icon;
                const TargetIcon = availableApps[integration.target].icon;
                
                return (
                  <div key={integration.id} className={`border rounded-lg p-4 ${integration.active ? 'border-green-300' : 'border-gray-300'}`}>
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <SourceIcon className="w-4 h-4" />
                        <Zap className="w-3 h-3 text-gray-400" />
                        <TargetIcon className="w-4 h-4" />
                      </div>
                      <span className={`text-xs px-2 py-1 rounded ${
                        integration.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                      }`}>
                        {integration.active ? 'Active' : 'Paused'}
                      </span>
                    </div>
                    
                    <div className="text-sm font-medium mb-1">
                      {availableApps[integration.source].name} → {availableApps[integration.target].name}
                    </div>
                    <div className="text-xs text-gray-600 mb-3">{integration.dataFlow.flow}</div>
                    <div className="text-xs text-gray-500 mb-3">Executions: {integration.executions}</div>
                    
                    <div className="flex space-x-2">
                      <button
                        onClick={() => simulateExecution(integration.id)}
                        className="text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
                        disabled={!integration.active}
                      >
                        <Play className="w-3 h-3 inline mr-1" />
                        Test
                      </button>
                      <button
                        onClick={() => toggleIntegration(integration.id, !integration.active)}
                        className={`text-xs px-2 py-1 rounded ${
                          integration.active 
                            ? 'bg-yellow-500 text-white hover:bg-yellow-600' 
                            : 'bg-green-500 text-white hover:bg-green-600'
                        }`}
                      >
                        {integration.active ? <Pause className="w-3 h-3 inline mr-1" /> : <Play className="w-3 h-3 inline mr-1" />}
                        {integration.active ? 'Pause' : 'Resume'}
                      </button>
                      <button
                        onClick={() => deleteIntegration(integration.id)}
                        className="text-xs bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                      >
                        <Trash2 className="w-3 h-3 inline mr-1" />
                        Delete
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Info Panel */}
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-lg font-semibold mb-4">How This Works</h2>
          <div className="grid md:grid-cols-2 gap-6 text-sm text-gray-600">
            <div>
              <h3 className="font-medium text-gray-800 mb-2">Consent-Native Integrations</h3>
              <ul className="space-y-1">
                <li>• Every connection requires explicit permission</li>
                <li>• Data flow is transparent and logged</li>
                <li>• Different apps require different security zones</li>
                <li>• You can pause or delete integrations anytime</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-800 mb-2">Zone-Based Security</h3>
              <ul className="space-y-1">
                <li>• Zone 1: Basic utility operations</li>
                <li>• Zone 2: Light data sharing (Slack, webhooks)</li>
                <li>• Zone 3: Personal data (email, calendar, docs)</li>
                <li>• Zone 4: Sensitive systems (databases, admin)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntegrationHub;