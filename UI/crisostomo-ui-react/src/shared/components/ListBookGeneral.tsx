import React from "react";
import { SkeletonCard } from "../../features/books/components/SkeletonCard";
import { BookCard } from "../../features/books/components/BookCard";

interface ListBookGeneralProps {
  books: any[]; // O tu interfaz Book[]
  loading?: boolean; // opcional si quieres mostrar skeleton desde fuera
}

export const ListBookGeneral: React.FC<ListBookGeneralProps> = ({ books, loading = false }) => {

  if (loading) {
      return (
          <div className="mt-20 px-10 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
              {Array.from({ length: 8 }).map((_, i) => (
                  <SkeletonCard key={i} />
              ))}
          </div>
      );
  }

  return (
      <div className="mt-5 px-10 gap-50 grid ml-2 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 ">
          {books.map((book) => (
              <BookCard
                  key={book.code}
                  code={book.code}
                  name={book.name}
                  author={book.author_name}
                  category={book.category_name}
              />
          ))}
      </div>
  );
};
