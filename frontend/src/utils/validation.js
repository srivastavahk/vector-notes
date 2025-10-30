export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validatePassword = (password) => {
  return {
    isValid: password.length >= 6,
    errors:
      password.length < 6 ? ["Password must be at least 6 characters"] : [],
  };
};

export const validateNote = (content, tags = []) => {
  const errors = [];

  if (!content || content.trim().length === 0) {
    errors.push("Note content is required");
  }

  if (content && content.length > 10000) {
    errors.push("Note content is too long (max 10,000 characters)");
  }

  if (tags.length > 10) {
    errors.push("Maximum 10 tags allowed");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};
