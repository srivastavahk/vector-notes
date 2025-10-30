import React from "react";
import { Plus, FileText } from "lucide-react";
import NoteCard from "./NoteCard";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

const NoteList = ({
  notes,
  loading,
  onEdit,
  onDelete,
  onCreateNew,
  searchQuery = "",
  emptyMessage = "No notes found",
}) => {
  if (loading) {
    return <LoadingSpinner className="min-h-[200px]" />;
  }

  if (notes.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {searchQuery ? "No notes found" : "No notes yet"}
        </h3>
        <p className="text-gray-600 mb-6">
          {searchQuery
            ? "Try adjusting your search terms"
            : "Create your first note to get started"}
        </p>
        {!searchQuery && (
          <Button onClick={onCreateNew}>
            <Plus className="w-4 h-4 mr-2" />
            Create Your First Note
          </Button>
        )}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {notes.map((note) => (
        <NoteCard
          key={note.id}
          note={note}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default NoteList;
