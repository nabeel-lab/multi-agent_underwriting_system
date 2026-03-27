'use client';

import { useState, useEffect } from 'react';
import { FormData } from '@/app/page';
import AgentCard from './agent-card';
import { motion } from 'framer-motion';

export type AgentState = 'pending' | 'processing' | 'complete';

interface Agent {
  id: string;
  name: string;
  description: string;
  icon: string;
}

const agents: Agent[] = [
  {
    id: 'income-verifier',
    name: 'Income Verifier',
    description: 'Analyzing income stability and employment history',
    icon: '💰',
  },
  {
    id: 'risk-assessor',
    name: 'Risk Assessor',
    description: 'Evaluating claim history and risk factors',
    icon: '📊',
  },
  {
    id: 'demographic-analyst',
    name: 'Demographic Analyst',
    description: 'Assessing geographic and demographic factors',
    icon: '🌍',
  },
  {
    id: 'compliance-checker',
    name: 'Compliance Checker',
    description: 'Verifying regulatory and policy compliance',
    icon: '✅',
  },
];

interface AgentPipelineProps {
  formData: FormData;
}

export default function AgentPipeline({ formData }: AgentPipelineProps) {
  const [agentStates, setAgentStates] = useState<Record<string, AgentState>>({});

  useEffect(() => {
    // Initialize all agents as pending
    const initialStates = agents.reduce(
      (acc, agent) => {
        acc[agent.id] = 'pending';
        return acc;
      },
      {} as Record<string, AgentState>
    );
    setAgentStates(initialStates);

    // Stagger agent processing
    agents.forEach((agent, index) => {
      const delay = index * 800;
      setTimeout(() => {
        setAgentStates((prev) => ({ ...prev, [agent.id]: 'processing' }));
      }, delay);

      const completeDelay = delay + 1200;
      setTimeout(() => {
        setAgentStates((prev) => ({ ...prev, [agent.id]: 'complete' }));
      }, completeDelay);
    });
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="mb-12 space-y-4"
    >
      <div className="mb-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900">Processing Application</h2>
        <p className="mt-2 text-gray-600">Our AI agents are analyzing your profile...</p>
      </div>

      <div className="space-y-4">
        {agents.map((agent, index) => (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
          >
            <AgentCard
              agent={agent}
              state={agentStates[agent.id] || 'pending'}
            />
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
