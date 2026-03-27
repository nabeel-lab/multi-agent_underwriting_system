'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

interface RiskGaugeProps {
  score: number; // 0-100
}

export default function RiskGauge({ score }: RiskGaugeProps) {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    let animationFrame: number;
    let currentScore = 0;
    const increment = score / 50;

    const animate = () => {
      if (currentScore < score) {
        currentScore = Math.min(currentScore + increment, score);
        setDisplayScore(Math.round(currentScore));
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [score]);

  const getColor = () => {
    if (score <= 40) return '#10B981'; // Green
    if (score <= 70) return '#F59E0B'; // Orange
    return '#EF4444'; // Red
  };

  const getTextColor = () => {
    if (score <= 40) return 'text-green-600';
    if (score <= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  const getRiskLabel = () => {
    if (score <= 40) return 'Low Risk';
    if (score <= 70) return 'Medium Risk';
    return 'High Risk';
  };

  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (displayScore / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative h-48 w-48">
        {/* Background circle */}
        <svg className="h-full w-full" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke="#E5E7EB"
            strokeWidth="8"
          />
          {/* Animated progress circle */}
          <motion.circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke={getColor()}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: 'easeOut' }}
            style={{ transform: 'rotate(-90deg)', transformOrigin: '60px 60px' }}
          />
        </svg>

        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="text-center"
          >
            <div className={`text-4xl font-bold ${getTextColor()}`}>{displayScore}</div>
            <div className="text-xs font-medium text-gray-500">Score</div>
          </motion.div>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.4 }}
        className={`mt-4 rounded-lg px-4 py-2 font-semibold ${
          score <= 40
            ? 'bg-green-100 text-green-700'
            : score <= 70
              ? 'bg-orange-100 text-orange-700'
              : 'bg-red-100 text-red-700'
        }`}
      >
        {getRiskLabel()}
      </motion.div>
    </div>
  );
}
