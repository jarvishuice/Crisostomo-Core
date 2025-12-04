import React from "react";
import { useNavigate } from "react-router-dom";
import type { AuthorCardProps } from "../types/AuthorCardProps.type";



export const AuthorCard: React.FC<AuthorCardProps> = ({
    cod,
    name,
    description,
    created_at
}) => {

    const navigate = useNavigate();

    return (
        <div className="bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-xl transition-all w-64 flex flex-col">

            {/* Imagen placeholder (puedes cambiarla luego si tienes fotos de autores) */}
            <img
                src={"http://localhost:1708/author/"+cod+"/300/300"}
                
                className="w-full h-64 object-cover"
            />
        

            {/* Contenido y botones */}
            <div className="p-4 flex flex-col grow justify-between">
                <div>
                    <h3 className="text-lg font-semibold text-gray-800 truncate">
                        {name}
                    </h3>

                    <p className="text-sm text-gray-500 mt-1 line-clamp-3">
                        {description}
                    </p>

                    <p className="text-xs text-gray-400 italic mt-2">
                        Creado el: {new Date(created_at).toLocaleDateString()}
                    </p>
                </div>

                {/* Botones inferiores, siempre dentro del card */}
                <div className="mt-4 flex gap-2">
                    <button
                        onClick={() => navigate(`/author/view/${cod}`)}
                        className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition-colors"
                    >
                        Ver
                    </button>

                    <button
                        onClick={() => navigate(`/author/edit/${cod}`)}
                        className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-4 rounded transition-colors"
                    >
                        Editar
                    </button>
                </div>
            </div>
        </div>
    );
};
