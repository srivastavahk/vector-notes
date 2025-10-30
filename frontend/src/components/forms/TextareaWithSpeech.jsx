import React from "react";
import { Mic, MicOff } from "lucide-react";
import { useSpeechToText } from "@/hooks/useSpeechToText";
import { useToast } from "@/contexts/ToastContext";

const TextareaWithSpeech = ({
  label,
  value,
  onChange,
  placeholder,
  ...props
}) => {
  const { isListening, startListening, stopListening, isSupported } =
    useSpeechToText();
  const { addToast } = useToast();

  const handleSpeechResult = (transcript) => {
    const newValue = value ? `${value} ${transcript}` : transcript;
    onChange({ target: { value: newValue } });
    addToast("Speech converted to text", "success");
  };

  const toggleSpeech = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening(handleSpeechResult);
    }
  };

  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <div className="relative">
        <textarea
          className="w-full px-3 py-2 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          rows={4}
          {...props}
        />
        {isSupported && (
          <button
            type="button"
            onClick={toggleSpeech}
            className={`absolute top-2 right-2 p-2 rounded-lg transition-colors
              ${
                isListening
                  ? "text-red-600 bg-red-50 hover:bg-red-100"
                  : "text-gray-400 hover:text-gray-600 hover:bg-gray-50"
              }`}
          >
            {isListening ? (
              <MicOff className="w-5 h-5" />
            ) : (
              <Mic className="w-5 h-5" />
            )}
          </button>
        )}
      </div>
      {isListening && (
        <p className="text-sm text-blue-600 flex items-center gap-1">
          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
          Listening... Speak now
        </p>
      )}
    </div>
  );
};

export default TextareaWithSpeech;
