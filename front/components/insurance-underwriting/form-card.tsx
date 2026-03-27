'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { FormData } from '@/app/page';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { motion } from 'framer-motion';
import { Briefcase, Users, MapPin } from 'lucide-react';

const formSchema = z.object({
  fullName: z.string().min(2, 'Name must be at least 2 characters'),
  age: z.coerce.number().min(18, 'Must be at least 18').max(65, 'Must be at most 65'),
  occupation: z.string().min(1, 'Please select an occupation'),
  monthlyIncome: z.coerce.number().min(1000, 'Monthly income must be at least 1000'),
  city: z.string().min(2, 'City must be at least 2 characters'),
  yearsEmployed: z.coerce
    .number()
    .min(0.5, 'Must have at least 6 months employment')
    .max(40, 'Must be less than 40 years'),
  pastClaims: z.coerce.number().min(0, 'Must be 0 or more').max(10, 'Must be 10 or less'),
});

const occupations = [
  'Software Engineer',
  'Teacher',
  'Doctor',
  'Accountant',
  'Manager',
  'Sales Representative',
  'Nurse',
  'Architect',
  'Electrician',
  'Plumber',
];

const cities = [
  'New Delhi',
  'Mumbai',
  'Bangalore',
  'Chennai',
  'Hyderabad',
  'Pune',
  'Kolkata',
  'Chandigarh',
];

interface FormCardProps {
  onSubmit: (data: FormData) => void;
}

export default function FormCard({ onSubmit }: FormCardProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
    watch,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      fullName: 'Raj Kumar',
      age: 32,
      occupation: 'Software Engineer',
      monthlyIncome: 85000,
      city: 'Bangalore',
      yearsEmployed: 5,
      pastClaims: 1,
    },
  });

  const occupation = watch('occupation');
  const city = watch('city');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mb-12 rounded-2xl border border-blue-100 bg-white/80 p-8 shadow-lg backdrop-blur-sm sm:p-10"
    >
      <div className="mb-8">
        <h2 className="mb-2 text-2xl font-bold text-gray-900">Application Details</h2>
        <p className="text-sm text-gray-600">Please provide your information for underwriting</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid gap-6 sm:grid-cols-2">
          {/* Full Name */}
          <div>
            <label htmlFor="fullName" className="mb-2 block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <Input
              id="fullName"
              {...register('fullName')}
              placeholder="John Doe"
              className="border-gray-200"
            />
            {errors.fullName && (
              <p className="mt-1 text-xs text-red-600">{errors.fullName.message}</p>
            )}
          </div>

          {/* Age */}
          <div>
            <label htmlFor="age" className="mb-2 block text-sm font-medium text-gray-700">
              Age
            </label>
            <Input
              id="age"
              {...register('age')}
              type="number"
              placeholder="25"
              className="border-gray-200"
            />
            {errors.age && <p className="mt-1 text-xs text-red-600">{errors.age.message}</p>}
          </div>

          {/* Occupation */}
          <div>
            <label htmlFor="occupation" className="mb-2 block text-sm font-medium text-gray-700">
              <Briefcase className="mb-1 inline h-4 w-4 mr-1" />
              Occupation
            </label>
            <Select value={occupation} onValueChange={(val) => setValue('occupation', val)}>
              <SelectTrigger id="occupation" className="border-gray-200">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {occupations.map((occ) => (
                  <SelectItem key={occ} value={occ}>
                    {occ}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.occupation && (
              <p className="mt-1 text-xs text-red-600">{errors.occupation.message}</p>
            )}
          </div>

          {/* Monthly Income */}
          <div>
            <label htmlFor="monthlyIncome" className="mb-2 block text-sm font-medium text-gray-700">
              Monthly Income (INR)
            </label>
            <Input
              id="monthlyIncome"
              {...register('monthlyIncome')}
              type="number"
              placeholder="50000"
              className="border-gray-200"
            />
            {errors.monthlyIncome && (
              <p className="mt-1 text-xs text-red-600">{errors.monthlyIncome.message}</p>
            )}
          </div>

          {/* City */}
          <div>
            <label htmlFor="city" className="mb-2 block text-sm font-medium text-gray-700">
              <MapPin className="mb-1 inline h-4 w-4 mr-1" />
              City
            </label>
            <Select value={city} onValueChange={(val) => setValue('city', val)}>
              <SelectTrigger id="city" className="border-gray-200">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {cities.map((c) => (
                  <SelectItem key={c} value={c}>
                    {c}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.city && <p className="mt-1 text-xs text-red-600">{errors.city.message}</p>}
          </div>

          {/* Years Employed */}
          <div>
            <label htmlFor="yearsEmployed" className="mb-2 block text-sm font-medium text-gray-700">
              <Users className="mb-1 inline h-4 w-4 mr-1" />
              Years Employed
            </label>
            <Input
              id="yearsEmployed"
              {...register('yearsEmployed')}
              type="number"
              step="0.5"
              placeholder="5"
              className="border-gray-200"
            />
            {errors.yearsEmployed && (
              <p className="mt-1 text-xs text-red-600">{errors.yearsEmployed.message}</p>
            )}
          </div>

          {/* Past Claims */}
          <div>
            <label htmlFor="pastClaims" className="mb-2 block text-sm font-medium text-gray-700">
              Past Claims
            </label>
            <Input
              id="pastClaims"
              {...register('pastClaims')}
              type="number"
              placeholder="0"
              className="border-gray-200"
            />
            {errors.pastClaims && (
              <p className="mt-1 text-xs text-red-600">{errors.pastClaims.message}</p>
            )}
          </div>
        </div>

        <Button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 py-6 text-base font-semibold text-white transition-all hover:shadow-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Processing...' : 'Process Application'}
        </Button>
      </form>
    </motion.div>
  );
}
