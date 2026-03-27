'use client';

import { DecisionResponse } from '@/app/page';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, Copy } from 'lucide-react';
import { useState, useEffect } from 'react';
import { toast } from 'sonner';
import RiskGauge from './risk-gauge';
import confetti from 'canvas-confetti';

interface DecisionCardProps {
  response: DecisionResponse;
}

export default function DecisionCard({ response }: DecisionCardProps) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // Trigger confetti on approval
    if (response.approved) {
      setTimeout(() => {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#3B82F6', '#8B5CF6', '#10B981'],
        });
      }, 300);
    }
  }, [response.approved]);

  const handleCopy = () => {
    const text = `Risk Score: ${response.final_risk_score}\nMonthly Premium: ₹${response.monthly_premium_inr}\nStatus: ${response.approved ? 'APPROVED' : 'DECLINED'}\nConfidence: ${response.confidence_level}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    toast.success('Decision copied to clipboard');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="mb-8 rounded-2xl border border-blue-100 bg-white/90 shadow-xl backdrop-blur-sm"
    >
      {/* Header with Decision Status */}
      <div
        className={`border-b px-8 py-6 ${
          response.approved ? 'bg-gradient-to-r from-green-50 to-emerald-50' : 'bg-gradient-to-r from-red-50 to-rose-50'
        }`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {response.approved ? (
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
              >
                <CheckCircle className="h-12 w-12 text-green-600" />
              </motion.div>
            ) : (
              <AlertCircle className="h-12 w-12 text-red-600" />
            )}
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {response.approved ? 'Application Approved' : 'Application Declined'}
              </h2>
              <p className="text-sm text-gray-600">
                {response.confidence_level} confidence in this decision
              </p>
            </div>
          </div>
          <button
            onClick={handleCopy}
            className="rounded-lg bg-white p-2 text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-900"
            title="Copy decision"
          >
            <Copy className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid gap-8 px-8 py-8 sm:grid-cols-2">
        {/* Left: Risk Gauge */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="flex items-center justify-center sm:border-r sm:border-gray-200"
        >
          <RiskGauge score={response.final_risk_score} />
        </motion.div>

        {/* Right: Decision Details */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="space-y-6"
        >
          {/* Premium */}
          <div className="rounded-lg bg-blue-50 p-4">
            <p className="text-sm font-medium text-gray-600">Monthly Premium</p>
            <p className="mt-1 text-3xl font-bold text-blue-600">
              ₹{response.monthly_premium_inr.toLocaleString()}
            </p>
          </div>

          {/* Confidence Level */}
          <div className="rounded-lg bg-purple-50 p-4">
            <p className="text-sm font-medium text-gray-600">Confidence Level</p>
            <div className="mt-2 flex items-center gap-2">
              <div
                className={`h-2 flex-1 rounded-full ${
                  response.confidence_level === 'High'
                    ? 'bg-green-500'
                    : response.confidence_level === 'Medium'
                      ? 'bg-orange-500'
                      : 'bg-red-500'
                }`}
              />
              <span className="font-semibold text-gray-900">{response.confidence_level}</span>
            </div>
          </div>

          {/* Explanation */}
          <div className="rounded-lg bg-gray-50 p-4">
            <p className="text-sm font-medium text-gray-600">Decision Summary</p>
            <p className="mt-2 text-sm leading-relaxed text-gray-700">
              {response.plain_english_explanation}
            </p>
          </div>
        </motion.div>
      </div>

      {/* Bias Audit Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="border-t border-gray-200 bg-gradient-to-r from-indigo-50 to-blue-50 px-8 py-6"
      >
        <h3 className="mb-3 font-semibold text-gray-900">Fairness & Compliance Audit</h3>
        <p className="text-sm leading-relaxed text-gray-700">{response.bias_audit_summary}</p>
      </motion.div>
    </motion.div>
  );
}
