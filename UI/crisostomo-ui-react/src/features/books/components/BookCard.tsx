import React from "react";
import type { BookCardProps } from "../types/BookCard.type";
import { useNavigate } from "react-router-dom";

export const BookCard: React.FC<BookCardProps> = ({ code, name, author, category }) => {
    const navigate = useNavigate();
      // Función para descargar el PDF
      const handleDownload = async () => {
        try {
            const response = await fetch(`http://localhost:1708/book/pdf/${code}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al descargar el PDF');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            // Extraer nombre de archivo desde Content-Disposition
            const disposition = response.headers.get('Content-Disposition');
            let filename = code + '.pdf';
            if (disposition && disposition.includes('filename=')) {
                filename = disposition.split('filename=')[1].replace(/"/g, '');
            }

            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error(error);
            alert('No se pudo descargar el archivo');
        }
    };


    return (
        <div className="bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-xl transition-all cursor-pointer w-64 flex flex-col">
            
            {/* Imagen */}
            <img 
                src={`http://localhost:1708/book/img/${code}/300/300`}
                alt={name}
                className="w-full h-64 object-cover"
            />

            {/* Contenido y botones */}
            <div className="p-4 flex flex-col grow justify-between">
                <div>
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

                {/* Botones al final, siempre dentro de la card */}
                <div className="mt-4 flex gap-2">
                    <button
                        onClick={() => navigate(`/read/${code}/${name}`)}
                        className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition-colors"
                    >
                        Leer
                    </button>
                    <button
                        onClick={handleDownload}
                        className="flex-1 bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded transition-colors"
                    >
                        Descargar
                    </button>
                </div>
            </div>
        </div>
    );
};
