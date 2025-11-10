import React, { useState, useEffect } from 'react';
import { AlertCircle, Lock, Shield, Zap, Settings } from 'lucide-react';

const SpiralLogicDemo = () => {
  const [currentZone, setCurrentZone] = useState(1);
  const [userConsent, setUserConsent] = useState({});
  const [operations, setOperations] = useState([]);
  const [userData, setUserData] = useState({
    name: '',
    email: '',
    preferences: {},
    sensitiveData: ''
  });

  // SpiralLogic Consent System
  const requestConsent = async (operation, zone, description) => {
    return new Promise((resolve) => {
      const consent = window.confirm(
        `Zone ${zone} Operation Request:\n\n${description}\n\nDo you give consent for this operation?`
      );
      
      const timestamp = new Date().toISOString();
      setOperations(prev => [...prev, {
        timestamp,
        operation,
        zone,
        description,
        consent,
        id: Date.now()
      }]);

      resolve(consent);
    });
  };

  // Zone 1: Utility Operations (No consent needed)
  const utilityOperation = (action) => {
    setOperations(prev => [...prev, {
      timestamp: new Date().toISOString(),
      operation: action,
      zone: 1,
      description: `Utility: ${action}`,
      consent: 'automatic',
      id: Date.now()
    }]);
  };

  // Zone 2: Casual Operations (Light consent)
  const casualOperation = async (action, description) => {
    if (currentZone >= 2) {
      const consent = await requestConsent(action, 2, description);
      if (consent) {
        // Perform operation
        return true;
      }
    } else {
      alert('Must enter Zone 2 or higher for this operation');
    }
    return false;
  };

  // Zone 3: Trusted Operations (Full consent)
  const trustedOperation = async (action, description) => {
    if (currentZone >= 3) {
      const consent = await requestConsent(action, 3, description);
      if (consent) {
        // Perform operation
        return true;
      }
    } else {
      alert('Must enter Zone 3 or higher for this operation');
    }
    return false;
  };

  // Zone 4: Sacred Operations (Maximum consent)
  const sacredOperation = async (action, description) => {
    if (currentZone >= 4) {
      const consent = await requestConsent(action, 4, description);
      if (consent) {
        // Perform operation
        return true;
      }
    } else {
      alert('Must enter Zone 4 for this operation');
    }
    return false;
  };

  const zoneConfig = {
    1: { name: 'Utility', icon: Zap, color: 'bg-gray-500', desc: 'Basic tools, no memory' },
    2: { name: 'Casual', icon: Settings, color: 'bg-blue-500', desc: 'Light personalization' },
    3: { name: 'Trusted', icon: Shield, color: 'bg-green-500', desc: 'Memory with consent' },
    4: { name: 'Sacred', icon: Lock, color: 'bg-purple-500', desc: 'Maximum containment' }
  };

  const enterZone = (zone) => {
    if (zone > currentZone) {
      const confirm = window.confirm(`Enter Zone ${zone} (${zoneConfig[zone].name})?\n\n${zoneConfig[zone].desc}\n\nHigher zones enable more operations but require explicit consent.`);
      if (confirm) {
        setCurrentZone(zone);
        utilityOperation(`Entered Zone ${zone}`);
      }
    } else {
      setCurrentZone(zone);
      utilityOperation(`Returned to Zone ${zone}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">SpiralLogic Consent Zones</h1>
          <p className="text-gray-600">Live demonstration of consent-native computing</p>
        </div>

        {/* Zone Selector */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Current Zone: {zoneConfig[currentZone].name}</h2>
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(zone => {
              const config = zoneConfig[zone];
              const Icon = config.icon;
              const isActive = zone === currentZone;
              const isAvailable = zone <= currentZone + 1;
              
              return (
                <button
                  key={zone}
                  onClick={() => enterZone(zone)}
                  disabled={!isAvailable && zone > currentZone}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    isActive 
                      ? `${config.color} text-white border-transparent` 
                      : isAvailable
                        ? 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'
                        : 'bg-gray-50 text-gray-400 border-gray-200 cursor-not-allowed'
                  }`}
                >
                  <Icon className="w-6 h-6 mx-auto mb-2" />
                  <div className="text-sm font-semibold">Zone {zone}</div>
                  <div className="text-xs">{config.name}</div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          
          {/* Operations Panel */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Test Operations</h2>
            
            <div className="space-y-3">
              {/* Zone 1 Operations */}
              <div className="border rounded p-3 bg-gray-50">
                <div className="text-sm font-medium text-gray-600 mb-2">Zone 1 - Utility</div>
                <button 
                  onClick={() => utilityOperation('Calculator: 2+2=4')}
                  className="bg-gray-500 text-white px-3 py-1 rounded text-sm mr-2"
                >
                  Calculator
                </button>
                <button 
                  onClick={() => utilityOperation('Weather: 72°F, Sunny')}
                  className="bg-gray-500 text-white px-3 py-1 rounded text-sm"
                >
                  Weather
                </button>
              </div>

              {/* Zone 2 Operations */}
              <div className="border rounded p-3 bg-blue-50">
                <div className="text-sm font-medium text-blue-600 mb-2">Zone 2 - Casual</div>
                <button 
                  onClick={async () => {
                    const success = await casualOperation('save_theme', 'Save your theme preference (dark/light mode)');
                    if (success) {
                      setUserData(prev => ({...prev, preferences: {...prev.preferences, theme: 'dark'}}));
                    }
                  }}
                  className="bg-blue-500 text-white px-3 py-1 rounded text-sm mr-2"
                  disabled={currentZone < 2}
                >
                  Save Theme
                </button>
                <button 
                  onClick={async () => {
                    await casualOperation('basic_personalization', 'Remember basic preferences for better user experience');
                  }}
                  className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
                  disabled={currentZone < 2}
                >
                  Personalize
                </button>
              </div>

              {/* Zone 3 Operations */}
              <div className="border rounded p-3 bg-green-50">
                <div className="text-sm font-medium text-green-600 mb-2">Zone 3 - Trusted</div>
                <button 
                  onClick={async () => {
                    const success = await trustedOperation('save_email', 'Store your email address for notifications and updates');
                    if (success) {
                      const email = prompt('Enter your email:');
                      if (email) {
                        setUserData(prev => ({...prev, email}));
                      }
                    }
                  }}
                  className="bg-green-500 text-white px-3 py-1 rounded text-sm mr-2"
                  disabled={currentZone < 3}
                >
                  Save Email
                </button>
                <button 
                  onClick={async () => {
                    await trustedOperation('access_documents', 'Access and process your personal documents');
                  }}
                  className="bg-green-500 text-white px-3 py-1 rounded text-sm"
                  disabled={currentZone < 3}
                >
                  Access Docs
                </button>
              </div>

              {/* Zone 4 Operations */}
              <div className="border rounded p-3 bg-purple-50">
                <div className="text-sm font-medium text-purple-600 mb-2">Zone 4 - Sacred</div>
                <button 
                  onClick={async () => {
                    const success = await sacredOperation('financial_data', 'Access sensitive financial information for analysis');
                    if (success) {
                      alert('Sacred operation completed - highest security protocols active');
                    }
                  }}
                  className="bg-purple-500 text-white px-3 py-1 rounded text-sm mr-2"
                  disabled={currentZone < 4}
                >
                  Financial Data
                </button>
                <button 
                  onClick={async () => {
                    await sacredOperation('system_admin', 'Perform system administration with full privileges');
                  }}
                  className="bg-purple-500 text-white px-3 py-1 rounded text-sm"
                  disabled={currentZone < 4}
                >
                  Admin Access
                </button>
              </div>
            </div>
          </div>

          {/* Audit Log */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Consent Audit Log</h2>
            <div className="max-h-96 overflow-y-auto space-y-2">
              {operations.slice(-10).reverse().map(op => (
                <div key={op.id} className={`p-3 rounded border-l-4 ${
                  op.consent === 'automatic' ? 'border-gray-400 bg-gray-50' :
                  op.consent ? 'border-green-400 bg-green-50' : 'border-red-400 bg-red-50'
                }`}>
                  <div className="flex justify-between items-start">
                    <div className="text-sm">
                      <div className="font-medium">Zone {op.zone}: {op.operation}</div>
                      <div className="text-gray-600 text-xs mt-1">{op.description}</div>
                    </div>
                    <div className={`text-xs px-2 py-1 rounded ${
                      op.consent === 'automatic' ? 'bg-gray-200 text-gray-700' :
                      op.consent ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
                    }`}>
                      {op.consent === 'automatic' ? 'Auto' : op.consent ? 'Granted' : 'Denied'}
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    {new Date(op.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Current Data State */}
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Data Sovereignty Status</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm font-medium text-gray-600">Stored Data</div>
              <div className="text-xs text-gray-500 mt-2">
                Email: {userData.email || 'None'}
                <br />
                Theme: {userData.preferences?.theme || 'Default'}
                <br />
                Total Operations: {operations.length}
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm font-medium text-gray-600">Consent Status</div>
              <div className="text-xs text-gray-500 mt-2">
                Granted: {operations.filter(op => op.consent === true || op.consent === 'automatic').length}
                <br />
                Denied: {operations.filter(op => op.consent === false).length}
                <br />
                Active Zone: {currentZone}
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm font-medium text-gray-600">User Control</div>
              <div className="text-xs text-gray-500 mt-2">
                <button 
                  onClick={() => {
                    setUserData({name: '', email: '', preferences: {}, sensitiveData: ''});
                    setOperations([]);
                    utilityOperation('User deleted all data');
                  }}
                  className="bg-red-500 text-white px-2 py-1 rounded text-xs"
                >
                  Delete All Data
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Explanation */}
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">How This Demonstrates SpiralLogic</h2>
          <div className="text-sm text-gray-600 space-y-2">
            <p>• <strong>Zone-based consent:</strong> Different operations require different permission levels</p>
            <p>• <strong>Explicit invocation:</strong> You must consciously enter higher zones</p>
            <p>• <strong>Audit trail:</strong> Every operation is logged with consent status</p>
            <p>• <strong>User sovereignty:</strong> You can delete all data instantly</p>
            <p>• <strong>No accidental violations:</strong> Operations fail if consent isn't granted</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpiralLogicDemo;