import React from "react";
import { Check, AlertCircle, X } from "lucide-react";

const Toast = ({ id, message, type, onClose }) => {
  const typeStyles = {
    success: "bg-green-50 border-green-200 text-green-800",
    error: "bg-red-50 border-red-200 text-red-800",
    info: "bg-blue-50 border-blue-200 text-blue-800",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
  };

  const icons = {
    success: Check,
    error: AlertCircle,
    info: AlertCircle,
    warning: AlertCircle,
  };

  const Icon = icons[type];

  return (
    <div
      className={`flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg max-w-sm border ${typeStyles[type]}`}
    >
      <Icon className="w-5 h-5 flex-shrink-0" />
      <span className="text-sm font-medium">{message}</span>
      <button
        onClick={onClose}
        className="ml-auto text-gray-400 hover:text-gray-600"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};

export default Toast;
