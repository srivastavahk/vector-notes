import React, { useState } from "react";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import TextareaWithSpeech from "./TextareaWithSpeech";
import { validateNote } from "@/utils/validation";

const NoteForm = ({ note, onSave, onCancel, loading }) => {
  const [content, setContent] = useState(note?.content || "");
  const [tags, setTags] = useState(note?.tags?.join(", ") || "");
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();

    const tagArray = tags
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);
    const validation = validateNote(content, tagArray);

    if (!validation.isValid) {
      setErrors({ content: validation.errors[0] });
      return;
    }

    setErrors({});
    onSave({
      content: content.trim(),
      tags: tagArray,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <TextareaWithSpeech
        label="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What's on your mind?"
        error={errors.content}
        required
      />

      <Input
        label="Tags (comma separated)"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        placeholder="work, personal, ideas"
        error={errors.tags}
      />

      <div className="flex gap-3 justify-end">
        <Button variant="secondary" onClick={onCancel} disabled={loading}>
          Cancel
        </Button>
        <Button type="submit" loading={loading} disabled={!content.trim()}>
          {note ? "Update Note" : "Create Note"}
        </Button>
      </div>
    </form>
  );
};

export default NoteForm;
