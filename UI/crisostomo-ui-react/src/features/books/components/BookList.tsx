import React, { useEffect, useState } from "react";
import { BookCard } from "./BookCard";
import { SkeletonCard } from "./SkeletonCard";

export const BookList: React.FC = () => {
    const [books, setBooks] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const res = await fetch("http://localhost:1708/book/?size=100&page=1");
                const data = await res.json();
                setBooks(data);
            } catch (err) {
                console.error("Error al cargar libros:", err);
            } finally {
                setLoading(false);
                
            }

        };
 
        fetchBooks();
    }, []);

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
