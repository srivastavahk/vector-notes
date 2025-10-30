const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const token = sessionStorage.getItem("supabase_token");

    const config = {
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }
  }

  // Notes endpoints
  getNotes(page = 1, pageSize = 20) {
    return this.request(`/notes/?page=${page}&page_size=${pageSize}`);
  }

  createNote(data) {
    return this.request("/notes/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  updateNote(id, data) {
    return this.request(`/notes/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  deleteNote(id) {
    return this.request(`/notes/${id}`, { method: "DELETE" });
  }

  searchNotes(query) {
    return this.request(`/notes/search?q=${encodeURIComponent(query)}`);
  }
}

export const api = new ApiService();
