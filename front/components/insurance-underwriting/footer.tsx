import { Github, ExternalLink } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-gray-200 py-8 text-center">
      <div className="space-y-3">
        <p className="text-sm text-gray-600">
          Advanced AI-powered insurance underwriting with fairness and compliance auditing
        </p>
        <div className="flex items-center justify-center gap-4">
          <a
            href="#"
            className="inline-flex items-center gap-2 rounded-lg bg-gray-100 px-3 py-2 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-200"
          >
            <Github className="h-4 w-4" />
            GitHub
          </a>
          <a
            href="#"
            className="inline-flex items-center gap-2 rounded-lg bg-blue-100 px-3 py-2 text-xs font-medium text-blue-700 transition-colors hover:bg-blue-200"
          >
            <ExternalLink className="h-4 w-4" />
            Documentation
          </a>
        </div>
        <p className="text-xs text-gray-500">
          © 2024 Insurance Underwriting AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
