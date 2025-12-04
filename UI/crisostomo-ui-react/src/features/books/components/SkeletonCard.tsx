import React from "react";

export const SkeletonCard: React.FC = () => {
    return (
        <div className="w-64 bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 animate-pulse">

            {/* Imagen fantasma */}
            <div className="w-full h-64 bg-gray-300"></div>

            {/* Contenido */}
            <div className="p-4 space-y-3">
                <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                <div className="h-3 bg-gray-300 rounded w-1/2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
            </div>
        </div>
    );
};
