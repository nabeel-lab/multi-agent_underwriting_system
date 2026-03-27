import { Shield } from 'lucide-react';

export default function Header() {
  return (
    <div className="mb-12 text-center">
      <div className="mb-4 flex justify-center">
        <div className="rounded-full bg-gradient-to-br from-blue-600 to-purple-600 p-3">
          <Shield className="h-8 w-8 text-white" />
        </div>
      </div>
      <h1 className="mb-2 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
        Insurance Underwriting
      </h1>
      <p className="text-lg text-gray-600">
        Fast, fair, and intelligent risk assessment powered by AI
      </p>
    </div>
  );
}
