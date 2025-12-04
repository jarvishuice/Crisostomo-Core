import React from "react";
import type { BookCardProps } from "../types/BookCard.type";



export const BookCard: React.FC<BookCardProps> = ({ code, name, author, category }) => {
    return (
        <div className="bg-white rounded-lg  shadow-md overflow-hidden border border-gray-200 hover:shadow-xl transition-all cursor-pointer w-64">
            
            {/* Imagen estilo Instagram */}
            <img 
                src={`http://localhost:1708/book/img/${code}/300/300`}
                alt={name}
                className="w-full h-64 object-cover"
            />

            {/* Contenido */}
            <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-800 truncate">
                    {name}
                </h3>

                <p className="text-sm text-gray-500 mt-1">
                    Autor: <span className="font-medium text-gray-700">{author}</span>
                </p>

                <p className="text-xs text-gray-400 italic">
                    {category}
                </p>
            </div>
        </div>
    );
};
