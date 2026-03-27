'use client';

import { useState } from 'react';
import Header from '@/components/insurance-underwriting/header';
import FormCard from '@/components/insurance-underwriting/form-card';
import AgentPipeline from '@/components/insurance-underwriting/agent-pipeline';
import DecisionCard from '@/components/insurance-underwriting/decision-card';
import Footer from '@/components/insurance-underwriting/footer';
import { toast } from 'sonner';

export interface FormData {
  fullName: string;
  age: number;
  occupation: string;
  monthlyIncome: number;
  city: string;
  yearsEmployed: number;
  pastClaims: number;
}

export interface DecisionResponse {
  approved: boolean;
  final_risk_score: number;
  monthly_premium_inr: number;
  plain_english_explanation: string;
  bias_audit_summary: string;
  confidence_level: 'High' | 'Medium' | 'Low';
}

type ProcessingState = 'idle' | 'processing' | 'complete';

export default function Home() {
  const [processingState, setProcessingState] = useState<ProcessingState>('idle');
  const [formData, setFormData] = useState<FormData | null>(null);
  const [decisionResponse, setDecisionResponse] = useState<DecisionResponse | null>(null);

  const handleSubmit = async (data: FormData) => {
    setFormData(data);
    setProcessingState('processing');

    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to process application');
      }

      const result = await response.json();
      setDecisionResponse(result);
      setProcessingState('complete');
    } catch (error) {
      console.error('Error processing application:', error);
      toast.error('Failed to process application. Please try again.');
      setProcessingState('idle');
    }
  };

  const handleReset = () => {
    setProcessingState('idle');
    setFormData(null);
    setDecisionResponse(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 via-purple-50 to-blue-50">
      <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        <Header />

        {processingState === 'idle' && (
          <FormCard onSubmit={handleSubmit} />
        )}

        {processingState === 'processing' && formData && (
          <AgentPipeline formData={formData} />
        )}

        {processingState === 'complete' && decisionResponse && (
          <div className="space-y-6">
            <DecisionCard response={decisionResponse} />
            <div className="text-center">
              <button
                onClick={handleReset}
                className="rounded-lg bg-blue-600 px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
              >
                Process Another Application
              </button>
            </div>
          </div>
        )}

        <Footer />
      </div>
    </main>
  );
}
