
import React from "react";

import { AuthorCard } from "./AuthorCard";
import type { AuthorCardProps } from "../types/AuthorCardProps.type";

interface AuthorListProps {
    authors: AuthorCardProps[];
}

export const AuthorList: React.FC<AuthorListProps> = ({ authors }) => {
    return (
        <div className="w-full">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">
                Lista de Autores
            </h2>

            {/* Grid responsivo */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {authors.length === 0 ? (
                    <p className="text-gray-500 text-center col-span-full">
                        No hay autores registrados.
                    </p>
                ) : (
                    authors.map((author) => (
                        <AuthorCard
                            key={author.cod}
                            cod={author.cod}
                            name={author.name}
                            description={author.description}
                            created_at={author.created_at}
                            updated_at={author.updated_at}
                        />
                    ))
                )}
            </div>
        </div>
    );
};
