import React from "react";
import { Search, Plus, LogOut, FileText, X } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import Button from "@/components/ui/Button";

const Header = ({
  searchQuery,
  onSearchChange,
  onSearchSubmit,
  onSearchClear,
  onCreateNote,
  isSearching,
}) => {
  const { signOut } = useAuth();

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <FileText className="w-8 h-8 text-blue-600" />
            <h1 className="ml-3 text-xl font-bold text-gray-900">
              AudioScribeAI
            </h1>
          </div>

          <div className="flex items-center gap-4">
            <form onSubmit={onSearchSubmit} className="flex items-center">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={onSearchChange}
                  placeholder="Search notes..."
                  className="w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Search className="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
                {searchQuery && (
                  <button
                    type="button"
                    onClick={onSearchClear}
                    className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>
              <Button type="submit" className="ml-2" loading={isSearching}>
                Search
              </Button>
            </form>

            <Button onClick={onCreateNote}>
              <Plus className="w-4 h-4 mr-2" />
              New Note
            </Button>

            <Button onClick={signOut} variant="ghost">
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
