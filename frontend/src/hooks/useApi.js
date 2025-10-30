import { useState, useCallback } from "react";
import { api } from "@/services/api";
import { useToast } from "@/contexts/ToastContext";

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const { addToast } = useToast();

  const execute = useCallback(
    async (apiCall, options = {}) => {
      const {
        onSuccess,
        onError,
        successMessage,
        errorMessage = "Something went wrong",
      } = options;

      try {
        setLoading(true);
        const result = await apiCall();

        if (successMessage) {
          addToast(successMessage, "success");
        }

        if (onSuccess) {
          onSuccess(result);
        }

        return result;
      } catch (error) {
        const message = error.message || errorMessage;
        addToast(message, "error");

        if (onError) {
          onError(error);
        }

        throw error;
      } finally {
        setLoading(false);
      }
    },
    [addToast],
  );

  return { loading, execute };
};
