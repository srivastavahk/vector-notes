import React from "react";
import { Edit3, Trash2, Tag } from "lucide-react";
import { formatDate } from "@/utils/helpers";

const NoteCard = ({ note, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-gray-900 line-clamp-2">
          {note.title}
        </h3>
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onEdit(note)}
            className="text-gray-400 hover:text-blue-600 focus:outline-none p-1 rounded"
            title="Edit note"
          >
            <Edit3 className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(note.id)}
            className="text-gray-400 hover:text-red-600 focus:outline-none p-1 rounded"
            title="Delete note"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      <p className="text-gray-600 text-sm line-clamp-3 mb-4">{note.content}</p>

      {note.tags && note.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {note.tags.map((tag, index) => (
            <span
              key={index}
              className="inline-flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs"
            >
              <Tag className="w-3 h-3" />
              {tag}
            </span>
          ))}
        </div>
      )}

      <p className="text-xs text-gray-400">{formatDate(note.updated_at)}</p>
    </div>
  );
};

export default NoteCard;
