import React, { useState, useEffect } from "react";
import { api } from "@/services/api";
import { useToast } from "@/contexts/ToastContext";
import { useApi } from "@/hooks/useApi";
import Header from "@/components/layout/Header";
import NoteList from "@/components/notes/NoteList";
import NoteForm from "@/components/forms/NoteForm";
import Modal from "@/components/ui/Modal";
import ConfirmDialog from "@/components/ui/ConfirmDialog";

const Dashboard = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [showNoteForm, setShowNoteForm] = useState(false);
  const [editingNote, setEditingNote] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  const { addToast } = useToast();
  const { loading: apiLoading, execute } = useApi();

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    await execute(() => api.getNotes(), {
      onSuccess: (data) => {
        setNotes(data);
        setLoading(false);
      },
      onError: () => setLoading(false),
      errorMessage: "Failed to load notes",
    });
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      loadNotes();
      return;
    }

    setIsSearching(true);
    await execute(() => api.searchNotes(searchQuery), {
      onSuccess: setNotes,
      onError: () => setIsSearching(false),
      errorMessage: "Search failed",
    });
    setIsSearching(false);
  };

  const clearSearch = () => {
    setSearchQuery("");
    loadNotes();
  };

  const handleCreateNote = async (noteData) => {
    await execute(() => api.createNote(noteData), {
      onSuccess: (newNote) => {
        setNotes([newNote, ...notes]);
        setShowNoteForm(false);
      },
      successMessage: "Note created successfully",
      errorMessage: "Failed to create note",
    });
  };

  const handleUpdateNote = async (noteData) => {
    await execute(() => api.updateNote(editingNote.id, noteData), {
      onSuccess: () => {
        setNotes(
          notes.map((note) =>
            note.id === editingNote.id
              ? {
                  ...editingNote,
                  ...noteData,
                  updated_at: new Date().toISOString(),
                }
              : note,
          ),
        );
        setEditingNote(null);
      },
      successMessage: "Note updated successfully",
      errorMessage: "Failed to update note",
    });
  };

  const handleDeleteNote = async (noteId) => {
    await execute(() => api.deleteNote(noteId), {
      onSuccess: () => {
        setNotes(notes.filter((note) => note.id !== noteId));
        setDeleteConfirm(null);
      },
      successMessage: "Note deleted successfully",
      errorMessage: "Failed to delete note",
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        searchQuery={searchQuery}
        onSearchChange={(e) => setSearchQuery(e.target.value)}
        onSearchSubmit={handleSearch}
        onSearchClear={clearSearch}
        onCreateNote={() => setShowNoteForm(true)}
        isSearching={isSearching}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">
            {searchQuery ? `Search Results for "${searchQuery}"` : "Your Notes"}
          </h2>
          <p className="text-gray-600 mt-1">
            {notes.length} {notes.length === 1 ? "note" : "notes"} found
          </p>
        </div>

        <NoteList
          notes={notes}
          loading={loading}
          onEdit={setEditingNote}
          onDelete={(id) => setDeleteConfirm(id)}
          onCreateNew={() => setShowNoteForm(true)}
          searchQuery={searchQuery}
        />
      </main>

      {/* Note Form Modal */}
      <Modal
        isOpen={showNoteForm || !!editingNote}
        onClose={() => {
          setShowNoteForm(false);
          setEditingNote(null);
        }}
        title={editingNote ? "Edit Note" : "Create New Note"}
      >
        <NoteForm
          note={editingNote}
          onSave={editingNote ? handleUpdateNote : handleCreateNote}
          onCancel={() => {
            setShowNoteForm(false);
            setEditingNote(null);
          }}
          loading={apiLoading}
        />
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={!!deleteConfirm}
        onConfirm={() => handleDeleteNote(deleteConfirm)}
        onCancel={() => setDeleteConfirm(null)}
        title="Delete Note"
        message="Are you sure you want to delete this note? This action cannot be undone."
        confirmText="Delete"
      />
    </div>
  );
};

export default Dashboard;
