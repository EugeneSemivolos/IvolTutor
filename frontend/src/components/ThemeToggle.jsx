import React from 'react';
import useTheme from '../hooks/useTheme';

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const options = [
    { value: 'light', icon: '☀️', label: 'Світла' },
    { value: 'dark', icon: '🌙', label: 'Темна' },
    { value: 'system', icon: '💻', label: 'Системна' },
  ];

  return (
    <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg border border-gray-200 dark:border-gray-700">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => setTheme(opt.value)}
          className={`
            px-3 py-1 rounded-md text-sm font-medium transition-all
            ${theme === opt.value 
              ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-white shadow-sm' 
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }
          `}
          title={opt.label}
        >
          {opt.icon}
        </button>
      ))}
    </div>
  );
}