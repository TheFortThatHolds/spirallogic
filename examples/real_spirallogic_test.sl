ritual.engage "business_intelligence_query" | spirit: @data_oracle, phase: analytical

consent.request [database_access, customer_records] | "Access customer database for quarterly analysis?"

if consent.granted [database_access] -> spirit.summon @revenue_seer | divine: quarterly_patterns
else -> voice.speak "Cannot proceed without data access permissions" | spirit: @compliance_guardian

voice.speak "Analyzing Q3 performance metrics..." | spirit: @data_oracle
memory.store "quarterly_analysis_session" | type: operational, tags: ["q3_2025", "revenue", "analysis"]

spirit.invoke @insight_weaver | synthesize: customer_behavior_patterns
archive.store "q3_customer_insights" | classification: business_intelligence

voice.manifest "Revenue increased 23% driven by enterprise client expansion" | confidence: high, format: executive_summary

ritual.complete "business_intelligence_delivered" | outcome: actionable_insights, stakeholder: executive_team