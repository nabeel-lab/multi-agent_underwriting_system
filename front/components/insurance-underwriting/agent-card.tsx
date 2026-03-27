'use client';

import { AgentState } from './agent-pipeline';
import { Check, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface AgentCardProps {
  agent: {
    id: string;
    name: string;
    description: string;
    icon: string;
  };
  state: AgentState;
}

export default function AgentCard({ agent, state }: AgentCardProps) {
  const getBgColor = () => {
    if (state === 'complete') return 'bg-green-50 border-green-200';
    if (state === 'processing') return 'bg-blue-50 border-blue-200';
    return 'bg-gray-50 border-gray-200';
  };

  const getStatusColor = () => {
    if (state === 'complete') return 'bg-green-500';
    if (state === 'processing') return 'bg-blue-500';
    return 'bg-gray-300';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`rounded-lg border-2 p-4 transition-all ${getBgColor()}`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="text-3xl">{agent.icon}</div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900">{agent.name}</h3>
            <p className="text-sm text-gray-600">{agent.description}</p>
          </div>
        </div>

        <motion.div
          className="flex flex-col items-center gap-2"
          animate={state === 'processing' ? { rotate: 360 } : {}}
          transition={state === 'processing' ? { repeat: Infinity, duration: 2 } : {}}
        >
          {state === 'pending' && (
            <div className={`h-10 w-10 rounded-full border-2 ${getStatusColor()} border-opacity-30`} />
          )}
          {state === 'processing' && (
            <div className={`flex h-10 w-10 items-center justify-center rounded-full ${getStatusColor()}`}>
              <Loader2 className="h-5 w-5 text-white animate-spin" />
            </div>
          )}
          {state === 'complete' && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className="flex h-10 w-10 items-center justify-center rounded-full bg-green-500"
            >
              <Check className="h-5 w-5 text-white" />
            </motion.div>
          )}
          <span className="text-xs font-medium text-gray-600 capitalize">{state}</span>
        </motion.div>
      </div>
    </motion.div>
  );
}
